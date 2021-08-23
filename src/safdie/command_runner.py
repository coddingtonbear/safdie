import argparse
import sys
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type

from . import finder
from .command import BaseCommand


class SafdieRunner:
    _entrypoint_name: str
    _cmd_class: Type[BaseCommand]
    _parser: argparse.ArgumentParser
    _commands: Dict[str, Type[BaseCommand]]

    def __init__(
        self,
        entrypoint_name: str,
        cmd_class: Type[BaseCommand] = BaseCommand,
        parser_class=argparse.ArgumentParser,
    ):
        self._entrypoint_name = entrypoint_name
        self._cmd_class = cmd_class
        self._commands = finder.get_entrypoints(self._entrypoint_name, self._cmd_class)
        self._parser = parser_class()

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        pass

    def _add_subparser(self, parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(dest="command")
        subparsers.required = True

        for cmd_name, cmd_class in self._commands.items():
            parser_kwargs = {}

            cmd_help = cmd_class.get_help()
            if cmd_help:
                parser_kwargs["help"] = cmd_help

            subparser = subparsers.add_parser(cmd_name, **parser_kwargs)
            cmd_class.add_arguments(subparser)

    def parse_args(
        self,
        argv: List[str] = None,
    ) -> argparse.Namespace:
        if argv is None:
            argv = sys.argv[1:]

        self.add_arguments(self._parser)
        self._add_subparser(self._parser)

        return self._parser.parse_args(argv)

    def handle(
        self,
        args: argparse.Namespace,
        init_args: Iterable[Any],
        init_kwargs: Dict[str, Any],
        handle_args: Iterable[Any],
        handle_kwargs: Dict[str, Any],
    ) -> Any:
        """Perform work you need to do before launching the command"""
        cls = self._commands[args.command]
        return cls(*init_args, **init_kwargs).handle(*handle_args, **handle_kwargs)

    def _run_command_for_parsed_args(
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

        if "options" in init_kwargs:
            raise ValueError(
                "Keyword-argument 'options' is provided by "
                "Safdie and cannot be provided by the caller."
            )
        init_kwargs["options"] = args

        return self.handle(args, init_args, init_kwargs, handle_args, handle_kwargs)

    def run(
        self,
        argv: Optional[List[str]] = None,
        init_args: Optional[Iterable[Any]] = None,
        init_kwargs: Optional[Dict[str, Any]] = None,
        handle_args: Optional[Iterable[Any]] = None,
        handle_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        args = self.parse_args(argv)
        self._run_command_for_parsed_args(
            args, init_args, init_kwargs, handle_args, handle_kwargs
        )
