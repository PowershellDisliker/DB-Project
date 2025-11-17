from sqlalchemy import select, create_engine, Column, Integer, String, Engine, MetaData, LargeBinary, ForeignKey, UnicodeText

class DBClient:
    uri: str
    engine: Engine

    def __init__(self, endpoint: str):
        self.uri = endpoint
        self.engine = create_engine(endpoint)

        metadata = MetaData()

        users = Table(
            'users', metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(32), nullable=False, unique=True),
            Column('password', String(256), nullable=False),
            Column('pfp', LargeBinary),
        )

        open_games = Table(
            'OpenGames', metadata,
            Column('id', Integer, primary_key=True),
            Column('user1id', Integer, ForeignKey('users.id')),
            Column('user2id', Integer, ForeignKey('users.id'), nullable=True),
            Column('starttime', Integer, nullable=False)
        )

        closed_games = Table(
            'ClosedGames', metdata,
            Column('id', Integer, primary_key=True),
            Column('user1id', Integer, ForeignKey('users.id')),
            Column('user2id', Integer, ForeignKey('users.id')),
            Column('starttime', Integer, nullable=False),
            Column('endtime', Integer, nullable=False),
            Column('winner', Integer, ForeignKey('users.id'))
        )
        
        friends = Table(
            'friends', metadata,
            Column('id1', Integer, ForeignKey('users.id')),
            Column('id2', Integer, ForeignKey('users.id'))
        )

        messages = Table(
            'messages', metadata,
            Column('sender', Integer, ForeignKey('users.id')),
            Column('receiver', Integer, ForeignKey('users.id')),
            Column('message', UnicodeText)
        )

        metadata.create_all(self.engine)

    def get_user_details(self):
        query = select()