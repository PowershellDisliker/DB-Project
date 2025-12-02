import bcrypt
import uuid

from sqlalchemy import select, create_engine, Table, Column, Integer, String, Engine, MetaData, LargeBinary, ForeignKey, UnicodeText, text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from typing import Optional
from dto import DB_ClosedGame, DB_Friend, DB_Message, DB_OpenGame, DB_Token, DB_User


class DBClient:
    uri: str
    engine: Engine

    users: Table
    active_tokens: Table
    open_games: Table
    closed_games: Table
    friends: Table
    messages: Table

    def __init__(self, endpoint: str, db_name: str) -> None:
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
            Column('ID', UUID(as_uuid=True), primary_key=True),
            Column('Username', String(32), nullable=False, unique=True),
            Column('PassHash', String(256), nullable=False),
            Column('Online', Boolean())
        )

        active_tokens = Table(
            'ActiveTokens', metadata,
            Column('UserID', UUID(as_uuid=True), ForeignKey('Users.ID'), primary_key=True),
            Column('Token', UUID(as_uuid=True), unique=True)
        )

        open_games = Table(
            'OpenGames', metadata,
            Column('ID', UUID(as_uuid=True), primary_key=True),
            Column('User1ID', UUID(as_uuid=True), ForeignKey('Users.ID')),
            Column('User2ID', UUID(as_uuid=True), ForeignKey('Users.ID'), nullable=True),
            Column('StartTime', DateTime(timezone=True), server_default=func.now())
        )

        closed_games = Table(
            'ClosedGames', metadata,
            Column('ID', UUID(as_uuid=True), primary_key=True),
            Column('User1ID', UUID(as_uuid=True), ForeignKey('Users.ID')),
            Column('User2ID', UUID(as_uuid=True), ForeignKey('Users.ID')),
            Column('StartTime', DateTime(timezone=True), server_default=func.now()),
            Column('EndTime', DateTime(timezone=True), server_default=func.now()),
            Column('Winner', UUID(as_uuid=True), ForeignKey('Users.ID'))
        )
        
        friends = Table(
            'Friends', metadata,
            Column('ID1', UUID(as_uuid=True), ForeignKey('Users.ID'), primary_key=True),
            Column('ID2', UUID(as_uuid=True), ForeignKey('Users.ID'), primary_key=True),
            Column('Accepted', Boolean, nullable=False)
        )

        messages = Table(
            'Messages', metadata,
            Column('ID', UUID(as_uuid=True), primary_key=True),
            Column('TimeStamp', DateTime(timezone=True), server_default=func.now()),
            Column('SenderID', UUID(as_uuid=True), ForeignKey('Users.ID')),
            Column('RecipientID', UUID(as_uuid=True), ForeignKey('Users.ID')),
            Column('Message', UnicodeText)
        )

        self.users = users
        self.active_tokens = active_tokens
        self.open_games = open_games
        self.closed_games = closed_games
        self.friends = friends
        self.messages = messages

        metadata.create_all(self.engine)


    # General purpose read / write functions. Handles sql injection problems and transaction management
    def __run_query(self, query, params=None):
        with self.engine.connect() as conn:
            return conn.execute(text(query), params or {}).fetchall()


    def __run_exec(self, query, params=None):
        with self.engine.begin() as conn:
            return conn.execute(text(query), params or {})

    # Specific data functions, these are what will be called in app.py
    def validate_user(self, user: str, passw: str) -> DB_User | None:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """
        result = self.__run_query("SELECT PassHash FROM Users WHERE Username = :username", {"username": user})

        if not result:
            return None

        if not bcrypt.checkpw(passw.encode("utf-8"), result[0].PassHash.encode("utf-8")):
            return None

        return DB_User(
            user_id=result[0].ID,
            username=result[0].Username,
        )


    def post_user(self, user: str, passw: str) -> DB_User | None:
        """
        HANDLES THE ENCRYPTION OF PASSWORD
        """

        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(passw.encode(), salt).decode()

        try:
            identity = uuid.uuid4()

            result = self.__run_exec("INSERT INTO Users (ID, Username, PassHash, Online) VALUES (:id, :uname, :passhash, :online)",
                {"id": identity, "uname": user, "passhash": hashed, "online": True})

            if result.rowcount <= 0:
                return None

            return DB_User(
                user_id=identity,
                username=user,
                online=True
            )

        except Exception as e:
            print(e)
            return None


    def get_public_user(self, identity: uuid.UUID) -> DB_User | None:
        result = self.__run_query("SELECT Username, Online FROM Users WHERE ID = :identity", {"identity": identity})

        if not result:
            return None

        return DB_User(
            user_id=identity,
            username=result[0].Username,
            online=result[0].Online
        )


    def get_private_user(self, identity: uuid.UUID) -> DB_User | None:
        result = self.__run_query("SELECT Username, PassHash, Online FROM Users WHERE ID = :identity", {"identity": identity})

        if not result:
            return None

        return DB_User(
            user_id=identity,
            username=result[0].Username,
            pass_hash=result[0].PassHash,
            online=result[0].Online
        )


    def post_token(self, identity: str, token: str) -> bool:
        result = self.__run_exec("INSERT INTO ActiveTokens (Token, UserID) VALUES (:token, :user)", {"token": token, "user": identity})

        if result.rowcount <= 0:
            return False
        return True


    def get_token(self, identity: uuid.UUID, token: str) -> bool:
        result = self.__run_query("SELECT * FROM ActiveTokens WHERE UserID = :id AND Token = :tok", {"id": identity, "tok": token})

        if not result:
            return False
        return True


    def post_open_game(self, user1id: str) -> bool:
        result = self.__run_exec("INSERT INTO OpenGames (ID, User1ID) VALUES (:id, :user1)", 
            {"id": uuid.uuid4(), "user1": user1id})

        if result.rowcount <= 0:
            return False
        return True


    def get_open_games(self) -> list[DB_OpenGame] | None:
        result = self.__run_query("SELECT * FROM OpenGames")

        if not result:
            return None

        return [
            DB_OpenGame(
                game_id=row.ID,
                user_1_id=row.User1ID,
                user_2_id=row.User2ID,
                start_time=row.StartTime
            )
            for row in result
        ]


    def post_closed_game(self, game_id: uuid.UUID, winner_id: uuid.UUID) -> DB_ClosedGame | None:
        result = self.__run_query("SELECT * FROM OpenGames where ID = :id", {"id": game_id})

        if not result:
            return None

        insert_result = self.__run_exec("INSERT INTO ClosedGames (ID, User1ID, User2ID, StartTime, Winner) VALUES (:id, :user1id, :user2id, :starttime, :winner)",
            {"id": result[0].ID, "user1id": result[0].User1ID, "user2id": result[0].User2ID, "starttime": result[0].StartTime, "winner": winner_id}
        )

        if insert_result.rowcount <= 0:
            return False

        delete_result = self.__run_exec("DELETE FROM OpenGames WHERE ID = :id", {"id": game_id})

        if delete_result.rowcount <= 0:
            return False
        return True


    def get_closed_games(self, identity: str) -> list[DB_ClosedGame] | None:
        result = self.__run_query("SELECT * FROM ClosedGames WHERE User1ID = :id OR User2ID = :id", {"id": identity})

        if not result:
            return None

        return [
            DB_ClosedGame(
                game_id=row.ID,
                user_1_id=row.User1ID,
                user_2_id=row.User2ID,
                start_time=row.StartTime,
                end_time=row.EndTime,
                winner=row.Winner,
            )
        for row in result]


    def post_friend(self, user1id: uuid.UUID, user2id: uuid.UUID) -> bool:
        result = self.__run_exec("INSERT INTO Friends (ID1, ID2, Accepted) VALUES (:id1, :id2, FALSE)", {"id1": user1id, "id2": user2id})

        if result.rowcount <= 0:
            return False
        return True


    def get_friends(self, identity: uuid.UUID) -> list[DB_Friend] | None:
        result = self.__run_query("SELECT * FROM Friends WHERE ID1 = :id OR ID2 = :id", {"id": identity})

        if not result:
            return None

        return [
            DB_Friend(
                friend_id=row.ID2 if row.ID2 != identity else row.ID1,
                accepted=row.Accepted
        )
        for row in result]


    def post_message(self, sender: uuid.UUID, recipient: uuid.UUID, message: str) -> bool:
        result = self.__run_exec("INSERT INTO Messages (ID, SenderID, RecipientID, Message) VALUES (:id, :si, :ri, :m)", 
            {"id": uuid.uuid4(), "si": sender, "ri": recipient, "m": message}
        )

        if result.rowcount <= 0:
            return False
        return True


    def get_messages(self, inbox_owner: uuid.UUID, external_contact: uuid.UUID) -> list[DB_Message] | None:
        result = self.__run_query("SELECT ID, Message, TimeStamp FROM Messages WHERE SenderID = :io AND RecipientID = :ec", 
            {"io": inbox_owner, "ec": external_contact}
        )

        if not result:
            return None

        return [
            DB_Message(
                message_id=row.ID,
                time_stamp=row.TimeStamp,
                sender_id=external_contact,
                recipient_id=inbox_owner,
                message=row.Message
            )
        for row in result]