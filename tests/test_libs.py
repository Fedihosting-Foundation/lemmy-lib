import os

from lemmylib.lib import LemmyLib

import dotenv

dotenv.load_dotenv()


def test_main():
    lib = LemmyLib(url=os.getenv('SITE_URL'), )
    lib.login(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))

    print(lib.get_post(46).community_view)
