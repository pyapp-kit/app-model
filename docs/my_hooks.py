def on_page_markdown(md: str, page, config, files):
    T = "::: app_model.types"
    T2 = T + "\n\toptions:\n\t\tdocstring_section_style: table"
    md = md.replace(T, T2)
    return md
