import ast
import contextlib
import inspect

import fieldz
from fieldz._repr import display_as_type
from griffe import Extension, Object, ObjectNode, dynamic_import, get_logger
from griffe.dataclasses import Docstring
from griffe.docstrings.dataclasses import DocstringParameter, DocstringSectionParameters
from griffe.docstrings.utils import parse_annotation
from pydantic import BaseModel

logger = get_logger(__name__)


class DynamicDocstrings(Extension):
    def __init__(self, object_paths: list[str] | None = None) -> None:
        self.object_paths = object_paths

    def on_instance(self, node: ast.AST | ObjectNode, obj: Object) -> None:
        if isinstance(node, ObjectNode):
            return  # skip runtime objects, their docstrings are already right

        if self.object_paths and obj.path not in self.object_paths:
            return  # skip objects that were not selected

        # import object to get its evaluated docstring
        try:
            runtime_obj = dynamic_import(obj.path)
            docstring = runtime_obj.__doc__
        except ImportError:
            logger.debug(f"Could not get dynamic docstring for {obj.path}")
            return
        except AttributeError:
            logger.debug(f"Object {obj.path} does not have a __doc__ attribute")
            return

        with contextlib.suppress(TypeError):
            fieldz.get_adapter(runtime_obj)
            docstring = inspect.cleandoc(docstring)
            self._inject_fields(docstring, obj, runtime_obj)

    def _inject_fields(
        self, docstring: str, obj: Object, runtime_obj: type[BaseModel]
    ) -> None:
        # update the object instance with the evaluated docstring
        if obj.docstring:
            obj.docstring.value = docstring
        else:
            obj.docstring = Docstring(docstring, parent=obj)

        params = [
            DocstringParameter(
                name=field.name,
                annotation=(
                    parse_annotation(
                        display_as_type(field.type, modern_union=True), obj.docstring
                    )
                    if field.type
                    else None
                ),
                description=field.description or "",
                value=repr(field.default)
                if field.default is not field.MISSING
                else None,
            )
            for field in fieldz.fields(runtime_obj)
            if field.name in runtime_obj.__annotations__
        ]
        param_section = DocstringSectionParameters(params)
        # TODO: merge rather than overwrite
        parsed = [
            x
            for x in obj.docstring.parsed
            if not isinstance(x, DocstringSectionParameters)
        ]
        parsed.append(param_section)
        obj.docstring.parsed = parsed
