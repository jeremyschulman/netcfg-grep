from importlib import metadata
import click

VERSION = metadata.version("netcfg-grep")


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass

