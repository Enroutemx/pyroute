import click

import os

from pyroute.run import Run as Pyroute

DEFAULT_CONFIG_JSON = '{}/config/config.json'.format(os.getcwd())


@click.group()
def runnable():
    pass


@runnable.command()
def init():
    pass


@runnable.command()
def create():
    pass


@runnable.command()
@click.option('--config', default=DEFAULT_CONFIG_JSON,
              help='Location of config file')
def run(config):
    msg = 'Using default config.json location: {}'.format(config)

    click.secho(msg, fg="cyan")
    Pyroute(config).execute_tests()


@runnable.command()
def shell():
    pass
