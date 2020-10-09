import sys
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
@click.option(
    "--fail-error",
    help="Fail and stop when filter expression not found as expected",
    is_flag=True,
)
@click.option(
    "--debug",
    is_flag=True,
    help="Add debug comment lines to output for missing filtered values",
)
def cli(grep_config, device_config, fail_error, debug):
    ncg_config = yaml.safe_load(grep_config)
    try:
        results_list = grep(
            ncg_config=ncg_config,
            netcfg_filepath=device_config.name,
            raise_onerror=fail_error,
            debug=debug,
        )

    except RuntimeError as exc:
        sys.exit(f"ABORT {device_config.name}: {exc.args[0]}")
    else:
        print("\n\n".join(results_list))
