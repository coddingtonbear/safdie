# Safdie

Easily make your app extensible by you or others via use of setuptools entrypoints.

* Free software: MIT license

I've written roughly the same module system for ten or so command-line apps over the last few years, and by now I've landed on a pattern that I've found pretty flexible and useful.  Here, I've packed it into a module so both you and I can avoid re-inventing it every time we have a new project.

## Installation

```
pip install safdie
```

You can also install the in-development version with:

```

pip install https://github.com/coddingtonbear/safdie/archive/master.zip

```

## Quickstart

The below example isn't particularly useful, but does demonstrate a fully-working use of this.

1. Create your commands as subclasses of `safdie.BaseCommand` and write whatever command classes you need:

```python
# Module Path: my_app.commands
from safdie import BaseCommand

class MyCommand(BaseCommand):
    def handle(self):
        print("Do whatever you need to do here")

```

2. Create your program's main command-line function:

```python
# Module Path: my_app.cli
from safdie import SafdieRunner, BaseCommand

def main():
    # This will look up the command and run it's `handle` function.
    SafdieRunner("myapp.commands").run()

```

3. In setuptools entrypoints, declare your entrypoints for both your command-line entrypoint and each of your commands:

```python
   setup(
       ...
       entrypoints={
           "console_scripts": [
               "my_command_line_app = my_app.cli:main",
           ],
           "myapp.commands": {
               "somecommand = my_app.commands:MyCommand",
           }
       }
   )
```

4. Install your app with `python setup.py install`

Now you can run `my_command_line_app somecommand` to execute your function.

## Tips

### Adding arguments

Maybe you want to add a command-line flag to your app; you can add those by subclassing `SafdieRunner` and defining an override for `add_arguments` as shown below:

```python
from argparse import ArgumentParser
from safdie import SafdieRunner


class MyRunner(SafdieRunner):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--something", action="store_true")


def main():
    MyRunner("myapp.commands").run()
```

### Customizing your argument parser

By default, Safdie will generate a new argument parser for you, but maybe you want to use `Gooey` or some other Argparse-compatible parser?  You can provide the class to use for generating the argument parser by specifying the `parser_class` command-line argument:

```python
from gooey import GooeyParser, Gooey
from safdie import SafdieRunner


@Gooey
def main():
    SafdieRunner("myapp.commands", parser_class=GooeyParser).run()
```

### Doing something before executing a command

Maybe you want to be able to optionally start a debugger between parsing args and executing the command?

```python
import argparse
from safdie import SafdieRunner
from typing import Any, Dict, Iterable


class MyRunner(SafdieRunner):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--debugger", action="store_true')

    def handle(
        self,
        args: argparse.Namespace,
        init_args: Iterable[Any],
        init_kwargs: Dict[str, Any],
        handle_args: Iterable[Any],
        handle_kwargs: Dict[str, Any],
    ) -> Any:
        if args.debugger:
            import debugpy

            debugpy.listen(("0.0.0.0", 5678))
            debugpy.wait_for_client()

        super().handle(
            args,
            init_args,
            init_kwargs,
            handle_args,
            handle_kwargs
        )


def main():
    MyRunner("myapp.commands").run()
```

### Using your own command subclass

In the below example, you have your own command subclass that requires an additional parameter at init-time.  Although the example below only uses an extra parameter for `__init__`, you can also pass extra parameters to `handle`.  See the source for more details.

```python
# Module Path: my_app.commands
from safdie import BaseCommand


class MyAppCommandBase(BaseCommand):
    def __init__(self, some_additional_init_param, *args, **kwargs):
        # Do something with `some_additional_init_param
        super().__init__(*args, **kwargs)


class MyCommand(MyAppBaseCommand):
    def handle(self):
        print("Do whatever you need to do here")
```

```python
from typing import Any, Dict, Iterable

from safdie import SafdieRunner

from .commands import MyAppCommandBase


class MyRunner(SafdieRunner):
    def handle(
        self,
        args: argparse.Namespace,
        init_args: Iterable[Any],
        init_kwargs: Dict[str, Any],
        handle_args: Iterable[Any],
        handle_kwargs: Dict[str, Any],
    ) -> Any:
        some_value_i_want_to_pass = "Arbitrary"

        init_kwargs['some_additional_init_param'] = (
            some_value_i_want_to_pass
        )

        super().handle(
            args,
            init_args,
            init_kwargs,
            handle_args,
            handle_kwargs
        )

def main():
    MyRunner("myapp.commands", cmd_class=MyAppCommandBase).run()
```

## Why is this named 'Safdie'?

You've probably seen at least a few photos of the famous building named [Habitat 67](https://en.wikipedia.org/wiki/Habitat_67). [Moshe Safdie](https://en.wikipedia.org/wiki/Moshe_Safdie) is the man who designed it.
