from typing import Any


def on_page_markdown(md: str, **kwargs: Any) -> str:
    T = "::: app_model.types"
    T2 = T + "\n\toptions:\n\t\tdocstring_section_style: table"
    return md.replace(T, T2)
