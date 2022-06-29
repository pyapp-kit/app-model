import os
import platform
import sys


def test_plat():
    print(f"{os.name=}")
    print(f"{sys.platform=}")
    print(f"{platform.system()=}")
    print(f"{platform.release()=}")
