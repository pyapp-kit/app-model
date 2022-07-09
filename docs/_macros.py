from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocs_macros.plugin import MacrosPlugin


def define_env(env):
    "Hook function"
    from app_model.types import Action, CommandRule, MenuRule, KeyBindingRule
    env.variables["Action"] = Action

    @env.macro
    def mymacro():
        return "some_string"
