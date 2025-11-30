import bcrypt
import uuid
import time

from sqlalchemy import select, create_engine, Table, Column, Integer, String, Engine, MetaData, LargeBinary, ForeignKey, UnicodeText, text
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from dto import *


class DBClient:
    uri: str
    engine: Engine

    def __init__(self, endpoint: str, db_name: str):
        self.uri = endpoint
        self.engine = create_engine(endpoint, isolation_level='AUTOCOMMIT')

        with self.engine.connect() as connection:
            try:
                connection.execute(text(f'CREATE DATABASE {db_name}'))
            except Exception as e:
                print(e)

        metadata = MetaData()

        users = Table(
            'Users', metadata,
            Column('id', UUID, primary_key=True),
            Column('username', String(32), nullable=False, unique=True),
            Column('passhash', String(256), nullable=False),
        )

        active_tokens = Table(
            'ActiveTokens', metadata,
            Column('token', String(32), primray_key=True),
            Column('user', UUID, ForeignKey('users.id'))
        )

        open_games = Table(
            'OpenGames', metadata,
            Column('id', UUID, primary_key=True),
            Column('user1id', UUID, ForeignKey('users.id')),
            Column('user2id', UUID, ForeignKey('users.id'), nullable=True),
            Column('starttime', Integer, nullable=False)
        )

        closed_games = Table(
            'ClosedGames', metadata,
            Column('id', UUID, primary_key=True),
            Column('user1id', UUID, ForeignKey('users.id')),
            Column('user2id', UUID, ForeignKey('users.id')),
            Column('starttime', Integer, nullable=False),
            Column('endtime', Integer, nullable=False),
            Column('winner', UUID, ForeignKey('users.id'))
        )
        
        friends = Table(
            'Friends', metadata,
            Column('id1', UUID, ForeignKey('users.id')),
            Column('id2', UUID, ForeignKey('users.id'))
        )

        messages = Table(
            'Messages', metadata,
            Column('sender', UUID, ForeignKey('users.id')),
            Column('receiver', UUID, ForeignKey('users.id')),
            Column('message', UnicodeText)
        )

        metadata.create_all(self.engine)


    # General purpose read / write functions. Handles sql injection problems and transaction management
    def run_query(query, params=None):
        with engine.connect() as conn:
            return conn.execute(text(query), params or {}).fetchall()


    def run_exec(query, params=None):
        with engine.begin() as conn:
            return conn.execute(text(query), params or {})

    # Specific data functions, these are what will be called in app.py
    def login_user(self, user: str, passw: str) -> bool:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """
        result = run_query("SELECT passhash FROM Users WHERE username = :username", {"username": user})

        if not result:
            return False

        return bcrypt.checkpw(passw.encode("utf-8"), result[0].passhash.encode("utf-8"))


    def register_user(self, user: str, passw: str) -> Optional[uuid.UUID]:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(passw, salt).decode("utf-8")

        try:
            identity = uuid.uuid4()
            run_query("INSERT INTO Users (id, username, passhash) VALUES (:id, :uname, :passhash)", {"id": identity, "uname": user, "passhash": hashed})
            return identity

        except Exception as e:
            print(e)
            return None

    
    def get_public_user_details(self, identity) -> Optional[UserDetails]:
        result = run_query("SELECT username FROM Users WHERE id = :identity", {"identity": identity})

        if not result:
            return False

        user_details = {
            "identity": result[0].id,
            "username": result[0].username,
        }

        return user_details


    def create_token(self, identity: str, token: str) -> bool:
        result = run_exec("INSERT INTO ActiveTokens (token, user) VALUES (:token, :user)", {"token": token, "user": identity})
        return result


    def check_token_validity(self, identity: uuid.UUID, token: str) -> bool:
        token_exists = run_query("SELECT * FROM ActiveTokens WHERE identity = :id AND token = :tok", {"id": identity, "tok": token})

        if token_exists is None:
            return False
        return True


    def create_open_game(self, user1id: str) -> bool:
        result = run_exect("INSERT INTO ActiveTokens (id, user1id, starttime) VALUES (:id, :user1, :user2, :start)", 
            {"id": uuid.uuid4(), "user1": user1id, "starttime": time.now()})

        if not result:
            return False
        return True


    def get_open_games(self) -> Optional[list[OpenGame]]:
        result = run_query("SELECT * FROM ActiveGames")

        if not result:
            return None

        return [
            {
                "identity": current.id,
                "user1id": current.user1id,
                "user2id": current.user2id,
                "starttime": current.starttime
            } 
            for current in result ]


    def create_closed_game(self, game_id: uuid.UUID, winner_id: uuid.UUID) -> bool:
        query_result = run_query("SELECT * FROM ActiveGames where id = :id", {"id", game_id})

        if query_result is None:
            return False

        game_data: OpenGame = {
            "identity": query_result[0].id,
            "user1id": query_result[0].user1id,
            "user2id": query_result[0].user2id,
            "starttime": query_result[0].starttime,
        }

        insert_result = run_exec(
            "INSERT INTO ClosedGames (id, user1id, user2id, starttime, endtime, winner) VALUES (:id, :user1id, :user2id, :starttime, :endtime, :winner)",
            {"id": game_data.identitty, "user1id": game_data.user1id, "user2id": game_data.user2id, "starttime": game_data.starttime, "endtime": time.now(), "winner": winner_id}
            )

        if insert_result is None:
            return False
        return True


    def get_closed_games(self, identity: str) -> Optional[list[ClosedGame]]:
        result = run_query("SELECT * FROM ClosedGames")

        if result is None:
            return None

        return [{
            "identity": instance.identity,
            "user1id": instance.user1id,
            "user2id": instance.user2id,
            "starttime": instance.starttime,
            "endtime": instance.endtime,
            "winner": instance.winner,
        } for instance in result]


    def add_friend(self, user1id: str, user2id: str) -> bool:
        pass


    def get_friends(self, identity: str) -> list[Friend]:
        pass


    def send_message(self, sender: str, recipient: str, message: str) -> bool:
        pass


    def get_messages(self, identity: str) -> list[Message]:
        pass
