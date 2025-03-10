import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv() #Load environment variables from .env


class RequestsBaseApi:
    BASE_URL = os.getenv("BASE_URL")

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        if self.BASE_URL is None:
            raise ValueError("BASE_URL environment variable not set")




