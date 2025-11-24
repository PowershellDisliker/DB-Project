from sqlalchemy import select, create_engine, Column, Integer, String, Engine, MetaData, LargeBinary, ForeignKey, UnicodeText
from dto import *


class DBClient:
    uri: str
    engine: Engine

    # def __init__(self, endpoint: str):
        # self.uri = endpoint
        # self.engine = create_engine(endpoint)

        # metadata = MetaData()

        # users = Table(
        #     'users', metadata,
        #     Column('id', Integer, primary_key=True),
        #     Column('username', String(32), nullable=False, unique=True),
        #     Column('passhash', String(256), nullable=False),
        # )

        # active_tokens = Table(
        #     'active_tokens', metadata,
        #     Column('token', String(32), nullable=False, unique=True)
        # )

        # open_games = Table(
        #     'OpenGames', metadata,
        #     Column('id', Integer, primary_key=True),
        #     Column('user1id', Integer, ForeignKey('users.id')),
        #     Column('user2id', Integer, ForeignKey('users.id'), nullable=True),
        #     Column('starttime', Integer, nullable=False)
        # )

        # closed_games = Table(
        #     'ClosedGames', metdata,
        #     Column('id', Integer, primary_key=True),
        #     Column('user1id', Integer, ForeignKey('users.id')),
        #     Column('user2id', Integer, ForeignKey('users.id')),
        #     Column('starttime', Integer, nullable=False),
        #     Column('endtime', Integer, nullable=False),
        #     Column('winner', Integer, ForeignKey('users.id'))
        # )
        
        # friends = Table(
        #     'friends', metadata,
        #     Column('id1', Integer, ForeignKey('users.id')),
        #     Column('id2', Integer, ForeignKey('users.id'))
        # )

        # messages = Table(
        #     'messages', metadata,
        #     Column('sender', Integer, ForeignKey('users.id')),
        #     Column('receiver', Integer, ForeignKey('users.id')),
        #     Column('message', UnicodeText)
        # )

        # metadata.create_all(self.engine)

    def login_user(self, user: str, passw: str):
        pass

    def register_user(self, user: str, passhash: str) -> bool:
        pass

    def get_user_details(self, identity: str) -> UserDetails | None:
        pass

    def create_token(self, identity: str, token: str) -> bool:
        pass

    def check_token_validity(self, identity: str, token: str) -> bool:
        pass

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