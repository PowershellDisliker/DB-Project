import bcrypt
import uuid

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
            'users', metadata,
            Column('id', UUID, primary_key=True),
            Column('username', String(32), nullable=False, unique=True),
            Column('passhash', String(256), nullable=False),
        )

        active_tokens = Table(
            'active_tokens', metadata,
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
            'friends', metadata,
            Column('id1', UUID, ForeignKey('users.id')),
            Column('id2', UUID, ForeignKey('users.id'))
        )

        messages = Table(
            'messages', metadata,
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
        result = run_query("SELECT passhash FROM users WHERE username = :username", {"username": user})

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
            run_query("INSERT INTO users (id, username, passhash) VALUES (:id, :uname, :passhash)", {"id": identity, "uname": user, "passhash": hashed})
            return identity

        except Exception as e:
            print(e)
            return None

    
    def get_public_user_details(self, identity) -> Optional[str]:
        result = run_query("SELECT username FROM users WHERE id = :identity", {"identity": identity})

        if not result:
            return False

        user_details = result[0].username

        return user_details


    def create_token(self, identity: str, token: str) -> bool:
        result = run_exec("INSERT INTO active_tokens (token, user) VALUES (:token, :user)", {"token": token, "user": identity})
        return result


    def check_token_validity(self, identity: uuid.UUID, token: str) -> bool:
        token_exists = run_query("SELECT * FROM active_tokens WHERE ")


    def create_open_game(self, user1id: str) -> bool:
        pass


    def get_open_games(self) -> list[OpenGame]:
        pass


    def create_closed_game(self, identity: str) -> bool:
        pass


    def get_closed_games(self, identity: str) -> list[ClosedGame]:
        pass


    def add_friend(self, user1id: str, user2id: str) -> bool:
        pass


    def get_friends(self, identity: str) -> list[Friend]:
        pass


    def send_message(self, sender: str, recipient: str, message: str) -> bool:
        pass


    def get_messages(self, identity: str) -> list[Message]:
        pass
