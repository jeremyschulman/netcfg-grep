from importlib import metadata

import click
import yaml

from netcfg_grep.grep import grep


VERSION = metadata.version("netcfg-grep")


@click.command()
@click.version_option(version=VERSION)
@click.option(
    '-c', '--config',
    help='netcfg-grep configuration YAML file',
    type=click.File()
)
@click.option(
    '-f', '--device-config-file',
    help='network device configuration TEXT file',
    type=click.File()
)
def cli(config, device_config_file):
    ncg_config = yaml.safe_load(config)
    results_list = grep(ncg_config=ncg_config, netcfg_filepath=device_config_file.name)
    print('\n\n'.join(results_list))

