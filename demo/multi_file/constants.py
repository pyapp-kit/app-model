from enum import Enum


class CommandId(str, Enum):
    OPEN = "myapp.open"
    CLOSE = "myapp.close"
    SAVE = "myapp.save"
    QUIT = "myapp.quit"

    UNDO = "myapp.undo"
    REDO = "myapp.redo"
    COPY = "myapp.copy"
    PASTE = "myapp.paste"
    CUT = "myapp.cut"

    def __str__(self) -> str:
        return self.value


class MenuId(str, Enum):
    FILE = "myapp/file"
    EDIT = "myapp/edit"

    def __str__(self) -> str:
        return self.value
