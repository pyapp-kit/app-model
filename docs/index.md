# App Model Documentation

## Action

| Field | Type | Description  |
| ----  | ---- | -----------  |
{% for field in Action.__fields__.values() -%}
| {{field.name}} | `{{ field.outer_type_ }}` | {{ field.field_info.description }}  |
{% endfor %}

::: app_model.types.Action
    options:
      members:
        - title
        - dict
      show_root_heading: false
      show_source: false
