import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB_NAME: str
    JWT_ALGO: str

    def __init__(self) -> None:
        # Load the file
        # load_dotenv()

        # Extract Variables
        self.SECRET_KEY = os.getenv("SECRET_KEY", "")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
        self.POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "")
        self.POSTGRES_PASS = os.getenv("POSTGRES_PASS", "")
        self.JWT_ALGO = os.getenv("JWT_ALGO", "HS256")

        # Check for presence of required variables
        self.__check_required()


    def __check_required(self) -> None:
        required = [
            self.SECRET_KEY,
            self.POSTGRES_HOST,
            self.POSTGRES_DB_NAME,
            self.POSTGRES_USER,
            self.POSTGRES_PASS,
            self.JWT_ALGO
        ]

        for i ,value in enumerate(required):
            if value == "":
                raise ValueError(f"Missing required environment variable {i}")

