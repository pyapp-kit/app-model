from enum import StrEnum


class CommandId(StrEnum):
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


class MenuId(StrEnum):
    FILE = "myapp/file"
    EDIT = "myapp/edit"

    def __str__(self) -> str:
        return self.value
