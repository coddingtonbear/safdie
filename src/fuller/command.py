import argparse


class BaseCommand:
    _options: argparse.Namespace

    def __init__(self, options: argparse.Namespace, *args, **kwargs):
        self._options: argparse.Namespace = options
        super().__init__()

    @property
    def options(self) -> argparse.Namespace:
        """Provides options provided at the command-line."""
        return self._options

    @classmethod
    def get_help(cls) -> str:
        """Retuurns help text for this function."""
        return ""

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        """Allows adding additional command-line arguments."""
        pass

    def handle(self, *args, **kwargs) -> None:
        """This is where the work of your function starts."""
        raise NotImplementedError()
