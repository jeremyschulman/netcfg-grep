# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import List
import re

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from ciscoconfparse import CiscoConfParse

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ['grep']

# -----------------------------------------------------------------------------
#
#                              CODE BEGINS
#
# -----------------------------------------------------------------------------


def grep_include(parsed: CiscoConfParse, expr: str):
    pass


def grep_include_exact_lines(parsed: CiscoConfParse, expr: List[str]) -> str:
    res = list()

    for each_expr in expr:
        found = parsed.find_lines(re.escape(each_expr))
        if (n_found := len(found)) > 1:
            raise RuntimeError(
                f'Found more than one ({n_found}) matching expr: {each_expr}'
            )

        res.append(found[0])

    return '\n'.join(res)


def grep_include_block(parsed: CiscoConfParse, expr: str) -> str:
    pass


def grep_include_exact_block(parsed: CiscoConfParse, expr: str) -> str:
    pass


def grep_include_block_lines(parsed: CiscoConfParse, expr: str) -> str:
    pass


FILTER_OPTIONS = {
    'include': grep_include,
    'include-exact-lines': grep_include_exact_lines,
    'include-block': grep_include_block,
    'include-exact-block': grep_include_exact_block,
    'include-block-lines': grep_include_block_lines
}


def grep(ncg_config: dict, netcfg_filepath) -> List[str]:
    """
    This function uses the provided grep config ncg_config to filter the
    configuration sections from the network configuration file
    `netcfg_filepath`.  The return value is a list containing the results for
    each of the filter statements defined in ncg_config.

    Parameters
    ----------
    ncg_config: dict
        The grep configuration that includes the `filters` to apply to the
        device configuration content.

    netcfg_filepath
        The filepath to the network configuration file.  This file must be
        consumable by the `ciscoparseconf` package.

    Raises
    ------
    RuntimeError:
        When there was an issue processing either the ncg_config definition
        or parsing the contents of the network configuraiton file.

    Returns
    -------
    The list of string representing the results of each of the filter
    expressions defined in `ncg_config`.
    """
    parsed = CiscoConfParse(config=netcfg_filepath, syntax=ncg_config['os_name'])
    filters = ncg_config['filters']

    grep_results = list()

    for filter_idx, filter_rec in enumerate(filters):

        # Going to write this to locate first any of the known FILTER_OPTIONS
        # since future filter_rec content could be more than just the filter
        # option.

        filter_opt = next((opt for opt, value in filter_rec.items()
                           if opt in FILTER_OPTIONS), None)

        if not filter_opt:
            raise RuntimeError(
                f'No valid filter option found in filter item {filter_idx}'
            )

        filter_func = FILTER_OPTIONS[filter_opt]
        res = filter_func(parsed, expr=filter_rec[filter_opt])
        grep_results.append(res)

    breakpoint()
    return grep_results

