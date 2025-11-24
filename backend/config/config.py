import os
from dotenv import load_dotenv

class Config:
    SECRET_KEY: str

    def __init__(self) -> None:
        # Load the file
        load_dotenv()

        # Extract Variables
        self.SECRET_KEY = os.getenv("SECRET_KEY")

        # Check for presence of required variables
        self.__check_required()


    def __check_required(self) -> None:
        required = [
            self.SECRET_KEY,
        ]

        for value in required:
            if value == None:
                raise ValueError("Missing required environment variables")

