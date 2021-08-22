from __future__ import annotations

import logging
from typing import Dict
from typing import Type
from typing import TypeVar

import pkg_resources

logger = logging.getLogger(__name__)


def get_module_dotpath(o):
    klass = o.__class__
    module = klass.__module__
    return module + "." + klass.__qualname__


T = TypeVar("T")


def get_entrypoints(entrypoint_name: str, cls: Type[T]) -> Dict[str, Type[T]]:
    possible_commands: Dict[str, Type[T]] = {}
    for entry_point in pkg_resources.iter_entry_points(group=entrypoint_name):
        try:
            loaded_class = entry_point.load()
        except ImportError:
            logger.warning(
                "Attempted to load entrypoint %s, but an ImportError occurred.",
                entry_point,
            )
            continue
        if not issubclass(loaded_class, cls):
            logger.warning(
                "Loaded entrypoint %s, but loaded class is "
                "not a subclass of `%s.%s`.",
                entry_point,
                cls.__module__,
                cls.__qualname__,
            )
            continue
        possible_commands[entry_point.name] = loaded_class

    return possible_commands
