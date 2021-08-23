import argparse
from unittest import TestCase
from unittest.mock import Mock

from pytest import raises

from ..command import BaseCommand


class TestBaseCommand(TestCase):
    def test_normal(self):
        options = Mock(spec=argparse.Namespace)

        cmd = BaseCommand(options=options)

        assert cmd.options == options

    def test_positional_args_not_options(self):
        options = Mock(spec=argparse.Namespace)

        with raises(TypeError):
            BaseCommand(options)
