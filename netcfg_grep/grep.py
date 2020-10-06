from typing import List
from ciscoconfparse import CiscoConfParse


def grep(ncg_config: dict, netcfg_filepath) -> List[str]:
    parsed = CiscoConfParse(config=netcfg_filepath, syntax=ncg_config['os_name'])
    breakpoint()
    return []

