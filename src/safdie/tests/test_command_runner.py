import argparse
from unittest import TestCase
from unittest.mock import patch

from .. import command_runner


class TestRunner(TestCase):
    def setUp(self):
        self.arbitrary_entrypoint_name = "myapp.test"

        self.arbitrary_entrypoints = {}
        super().setUp()

    def _get_runner(self, **kwargs) -> command_runner.SafdieRunner:
        with patch("safdie.finder.get_entrypoints") as get_entrypoints:
            get_entrypoints.return_value = self.arbitrary_entrypoints

            cmd = command_runner.SafdieRunner(self.arbitrary_entrypoint_name, **kwargs)

        return cmd

    def test_init_uses_argparse_if_undefined(self):
        cmd = self._get_runner()

        assert isinstance(cmd._parser, argparse.ArgumentParser)

    def test_fetches_entrypoints_on_init(self):
        self.arbitrary_entrypoints["arbitrary"] = True

        cmd = self._get_runner()

        assert "arbitrary" in cmd._commands
