import bcrypt
import uuid
import time

from sqlalchemy import select, create_engine, Table, Column, Integer, String, Engine, MetaData, LargeBinary, ForeignKey, UnicodeText, text, Boolean
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
            Column('ID', UUID, primary_key=True),
            Column('Username', String(32), nullable=False, unique=True),
            Column('PassHash', String(256), nullable=False),
            Column('Online', Boolean())
        )

        active_tokens = Table(
            'ActiveTokens', metadata,
            Column('UserID', UUID, ForeignKey('Users.ID'), primary_key=True),
            Column('Token', String(32))
        )

        open_games = Table(
            'OpenGames', metadata,
            Column('ID', UUID, primary_key=True),
            Column('User1ID', UUID, ForeignKey('Users.ID')),
            Column('User2ID', UUID, ForeignKey('Users.ID'), nullable=True),
            Column('StartTime', Integer, nullable=False)
        )

        closed_games = Table(
            'ClosedGames', metadata,
            Column('ID', UUID, primary_key=True),
            Column('User1ID', UUID, ForeignKey('users.id')),
            Column('User2ID', UUID, ForeignKey('users.id')),
            Column('StartTime', Integer, nullable=False),
            Column('EndTime', Integer, nullable=False),
            Column('Winner', UUID, ForeignKey('users.id'))
        )
        
        friends = Table(
            'Friends', metadata,
            Column('ID1', UUID, ForeignKey('users.id'), nullable=False),
            Column('ID2', UUID, ForeignKey('users.id'), nullable=False),
            Column('Accepted', Boolean, nullable=False)
        )

        messages = Table(
            'Messages', metadata,
            Column('ID', UUID, primary_key=True),
            Column('TimeStamp', Integer, nullable=False),
            Column('SenderID', UUID, ForeignKey('users.id')),
            Column('RecipientID', UUID, ForeignKey('users.id')),
            Column('Message', UnicodeText)
        )

        metadata.create_all(self.engine)


    # General purpose read / write functions. Handles sql injection problems and transaction management
    def __run_query(self, query, params=None):
        with self.engine.connect() as conn:
            return conn.execute(text(query), params or {}).fetchall()


    def __run_exec(self, query, params=None):
        with self.engine.begin() as conn:
            return conn.execute(text(query), params or {})

    # Specific data functions, these are what will be called in app.py
    def validate_user(self, user: str, passw: str) -> Optional[uuid.UUID]:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """
        result = self.__run_query("SELECT PassHash FROM Users WHERE Username = :username", {"username": user})

        if not result:
            return False

        return bcrypt.checkpw(passw.encode("utf-8"), result[0].passhash.encode("utf-8"))


    def post_user(self, user: str, passw: str) -> Optional[uuid.UUID]:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(passw, salt).decode("utf-8")

        try:
            identity = uuid.uuid4()
            self.__run_exec("INSERT INTO Users (ID, Username, PassHash, Online) VALUES (:id, :uname, :passhash, :online)",
                {"id": identity, "uname": user, "passhash": hashed, "online": True})
            return identity

        except Exception as e:
            print(e)
            return None


    def get_public_user(self, identity) -> Optional[PublicUserDetails]:
        result = self.__run_query("SELECT Username FROM Users WHERE ID = :identity", {"identity": identity})

        if not result:
            return False

        user_details = {
            "identity": result[0].id,
            "username": result[0].username,
        }

        return user_details


    def get_private_user(self, identity: UUID) -> Optional[PrivateUserDetails]:
        result = self.__run_exec("SELECT * FROM User WHERE ID = :id", {"id": identity})

        if not result:
            return None

        return result[0]


    def post_token(self, identity: str, token: str) -> bool:
        result = self.__run_exec("INSERT INTO ActiveTokens (Token, UserID) VALUES (:token, :user)", {"token": token, "user": identity})
        return result


    def get_token(self, identity: uuid.UUID, token: str) -> bool:
        token_exists = self.__run_query("SELECT * FROM ActiveTokens WHERE UserID = :id AND Token = :tok", {"id": identity, "tok": token})

        if token_exists is None:
            return False
        return True


    def post_open_game(self, user1id: str) -> bool:
        result = self.__run_exec("INSERT INTO ActiveTokens (ID, User1ID, StartTime) VALUES (:id, :user1, :start)", 
            {"id": uuid.uuid4(), "user1": user1id, "start_time": time.now()})

        if result.rowcount <= 0:
            return False
        return True


    def get_open_games(self) -> Optional[list[OpenGame]]:
        result = self.__run_query("SELECT * FROM ActiveGames")

        if not result:
            return None

        return [
            {
                "identity": current.id,
                "user1id": current.user1id,
                "user2id": current.user2id,
                "starttime": current.starttime
            } 
            for current in result]


    def post_closed_game(self, game_id: uuid.UUID, winner_id: uuid.UUID) -> bool:
        query_result = self.__run_query("SELECT * FROM OpenGames where ID = :id", {"id": game_id})

        if query_result is None:
            return False

        game_data: OpenGame = {
            "identity": query_result[0].id,
            "user1id": query_result[0].user1id,
            "user2id": query_result[0].user2id,
            "starttime": query_result[0].starttime,
        }

        insert_result = run_exec(
            "INSERT INTO ClosedGames (ID, User1ID, User2ID, StartTime, EndTime, Winner) VALUES (:id, :user1id, :user2id, :starttime, :endtime, :winner)",
            {"id": game_data.identitty, "user1id": game_data.user1id, "user2id": game_data.user2id, "starttime": game_data.starttime, "endtime": time.now(), "winner": winner_id}
            )

        if insert_result is None:
            return False
        return True


    def get_closed_games(self, identity: str) -> Optional[list[ClosedGame]]:
        result = self.__run_query("SELECT * FROM ClosedGames")

        if result is None:
            return None

        return [
            {
                "identity": instance.identity,
                "user1id": instance.user1id,
                "user2id": instance.user2id,
                "starttime": instance.starttime,
                "endtime": instance.endtime,
                "winner": instance.winner,
            } 
        for instance in result]


    def post_friend(self, user1id: uuid.UUID, user2id: uuid.UUID) -> bool:
        result = sef.__run_exec("INSERT INTO Friends (ID1, ID2) VALUES (:id1, :id2)", {"id1": user1id, "id2": user2id})

        if result is None:
            return None

        return result


    def get_friends(self, identity: uuid.UUID) -> list[Friend]:
        result = self.__run_query("SELECT * FROM Friends WHERE ID1 = :id OR ID2 = :id", {"id": identity})

        if result is None:
            return None

        return result


    def post_message(self, sender: uuid.UUID, recipient: uuid.UUID, message: str) -> bool:
        result = self.__run_exec("INSERT INTO Messages (ID, TimeStamp, SenderID, RecipientID, Message) VALUES (:id, :ts, :si, :ri, m)", 
            {"id": uuid.uuid4(), "ts": time.now(), "si": sender, "ri": recipient, "m": message}
        )

        if result.rows_affected <= 0:
            return False
        return True


    def get_messages(self, inbox_owner: uuid.UUID, external_contact: uuid.UUID) -> list[Message]:
        result = self.__run_query("SELECT (ID, Message, TimeStamp) FROM Messages WHERE SenderID = :io AND RecipientID = :ec", 
            {"io": inbox_owner, "ec": external_contact}
        )

        if result is None:
            return None

        return result
