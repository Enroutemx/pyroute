import click

import os

from pyroute.run import Run as Pyroute

DEFAULT_CONFIG_JSON = '{}/config/config.json'.format(os.getcwd())


@click.group()
def runnable():
    """
    """
    pass


@runnable.command()
def init():
    """
    Initializes a testing project, allows the user to select different options.
    """
    pass


@runnable.command()
def create():
    """
    Creates the page objects, custom modules, test data, etc.
    """
    pass


@runnable.command()
@click.option('--config', default=DEFAULT_CONFIG_JSON,
              help='Location of config file')
def run(config):
    """Allows you to run tests.
    """
    msg = 'Using config.json location: {}'.format(config)

    click.secho(msg, fg="cyan")
    Pyroute(config).execute_tests()


@runnable.command()
def shell():
    """Use an interactive shell to test your modules with Pyroute env.
    """
    pass
