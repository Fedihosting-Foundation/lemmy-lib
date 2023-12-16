import logging

import dotenv

dotenv.load_dotenv()

import app_name_here.__main__ as app_main


class TestMain:
    @classmethod
    def test_hi(cls):
        app_main.print_hi()
