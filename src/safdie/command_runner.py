import argparse
import sys
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type

from typing_extensions import Protocol

from . import finder
from .command import BaseCommand


class ArgparseProtocol(Protocol):
    def add_argument(self, *args, **kwargs):
        ...

    def add_subparsers(self, *, dest: str) -> Any:
        ...

    def parse_args(self, args: List[str]):
        ...


class SafdieRunner:
    _entrypoint_name: str
    _cmd_class: Type[BaseCommand]
    _parser: ArgparseProtocol
    _commands: Dict[str, Type[BaseCommand]]

    def __init__(
        self,
        entrypoint_name: str,
        cmd_class: Type[BaseCommand] = BaseCommand,
        parser: Optional[ArgparseProtocol] = None,
    ):
        self._entrypoint_name = entrypoint_name
        self._cmd_class = cmd_class
        self._commands = finder.get_entrypoints(self._entrypoint_name, self._cmd_class)

        if parser:
            self._parser = parser
        else:
            self._parser = argparse.ArgumentParser()

    def parse_args(
        self,
        argv: List[str] = None,
    ) -> argparse.Namespace:
        if argv is None:
            argv = sys.argv[1:]

        subparsers = self._parser.add_subparsers(dest="command")
        subparsers.required = True

        for cmd_name, cmd_class in self._commands.items():
            parser_kwargs = {}

            cmd_help = cmd_class.get_help()
            if cmd_help:
                parser_kwargs["help"] = cmd_help

            subparser = subparsers.add_parser(cmd_name, **parser_kwargs)
            cmd_class.add_arguments(subparser)

        return self._parser.parse_args(argv)

    def get_command_class_for_parsed_args(
        self, args: argparse.Namespace
    ) -> Type[BaseCommand]:
        return self._commands[args.command]

    def get_command_class(self, argv: List[str] = sys.argv) -> Type[BaseCommand]:
        args = self.parse_args(argv)
        return self.get_command_class_for_parsed_args(args)

    def run_command_for_parsed_args(
        self,
        args: argparse.Namespace,
        init_args: Optional[Iterable[Any]] = None,
        init_kwargs: Optional[Dict[str, Any]] = None,
        handle_args: Optional[Iterable[Any]] = None,
        handle_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        if init_args is None:
            init_args = []
        if init_kwargs is None:
            init_kwargs = {}
        if handle_args is None:
            handle_args = []
        if handle_kwargs is None:
            handle_kwargs = {}

        cls = self.get_command_class_for_parsed_args(args)
        return cls(args, *init_args, **init_kwargs).handle(
            *handle_args, **handle_kwargs
        )

    def run(
        self,
        argv: List[str] = sys.argv,
        init_args: Optional[Iterable[Any]] = None,
        init_kwargs: Optional[Dict[str, Any]] = None,
        handle_args: Optional[Iterable[Any]] = None,
        handle_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        args = self.parse_args(argv)
        self.run_command_for_parsed_args(
            args, init_args, init_kwargs, handle_args, handle_kwargs
        )
