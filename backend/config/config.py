import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY: str
    POSTGRES_URL: str
    POSTGRES_DB_NAME: str
    JWT_ALGO: str

    def __init__(self) -> None:
        # Load the file
        load_dotenv()

        # Extract Variables
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.POSTGRES_URL = os.getenv("POSTGRES_URL")
        self.POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
        self.JWT_ALGO = os.getenv("JWT_ALGO")

        # Check for presence of required variables
        self.__check_required()


    def __check_required(self) -> None:
        required = [
            self.SECRET_KEY,
            self.POSTGRES_URL,
            self.POSTGRES_DB_NAME,
            self.JWT_ALGO
        ]

        for value in required:
            if value == None:
                raise ValueError("Missing required environment variables")

