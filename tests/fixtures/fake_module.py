from unittest.mock import Mock

GLOBAL_MOCK = Mock(name="GLOBAL")


def run_me() -> bool:
    GLOBAL_MOCK()
    return True


attr = "not a callble"
