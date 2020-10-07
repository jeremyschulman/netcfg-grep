from importlib import metadata

import click
import yaml

from netcfg_grep.grep import grep


VERSION = metadata.version("netcfg-grep")


@click.command()
@click.version_option(version=VERSION)
@click.option(
    "-g", "--grep-config", help="netcfg-grep configuration YAML file", type=click.File()
)
@click.option(
    "-d",
    "--device-config",
    help="network device configuration TEXT file",
    type=click.File(),
)
def cli(grep_config, device_config):
    ncg_config = yaml.safe_load(grep_config)
    results_list = grep(ncg_config=ncg_config, netcfg_filepath=device_config.name)
    print("\n\n".join(results_list))
