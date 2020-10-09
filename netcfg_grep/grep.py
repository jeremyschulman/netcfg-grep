# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import List, Optional
import re

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from ciscoconfparse import CiscoConfParse

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["grep"]

# -----------------------------------------------------------------------------
#
#                              CODE BEGINS
#
# -----------------------------------------------------------------------------

# regex start of line anchor
_LINE_START_ = r"^"

# allow line endings to include optional whitespace; cuz it happens :(
_LINE_END_ = r"\s*$"


class FilterMatchError(RuntimeError):
    def __init__(self, expr: str , count: Optional[int] = 0):
        super().__init__()
        self.expr = expr
        self.count = count


def grep_include_line(parsed: CiscoConfParse, expr: str) -> str:
    found = parsed.find_lines(_LINE_START_ + expr)

    if (n_found := len(found)) != 1:
        raise FilterMatchError(expr=expr, count=n_found)

    return found[0].rstrip()


def grep_include_exact_lines(parsed: CiscoConfParse, expr: str) -> str:
    res = list()

    for each_expr in expr.splitlines(keepends=False):
        found = parsed.find_lines(
            _LINE_START_ + re.escape(each_expr.strip()) + _LINE_END_
        )

        if (n_found := len(found)) != 1:
            raise FilterMatchError(expr=each_expr, count=n_found)

        res.append(found[0].rstrip())

    return "\n".join(res)


def grep_include_block(parsed: CiscoConfParse, expr: str) -> str:
    return "\n".join(map(str.rstrip, parsed.find_all_children(_LINE_START_ + expr + _LINE_END_)))


def grep_include_block_lines(parsed: CiscoConfParse, expr: str) -> str:
    return "\n".join(map(str.rstrip, parsed.find_all_children(_LINE_START_ + expr)))


FILTER_OPTIONS = {
    "include-line": grep_include_line,
    "include-exact-lines": grep_include_exact_lines,
    "include-block": grep_include_block,
    "include-block-lines": grep_include_block_lines,
}


def grep(
    ncg_config: dict, netcfg_filepath, raise_onerror: Optional[bool] = False,
    debug: Optional[bool] = False
) -> List[str]:
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

    raise_onerror: bool
        When False (default) any filter expression that results in not found is simply
        ignored, which is a similiar behavior of grep.  Set `ignore_notfound` to True
        and any missing values will raise a FilterMatchError.

    debug: bool
        When True, and when raise_onerr is False, then add a debug line to
        indicate the error in the output.  When False (default) and
        raise_onerror is False, then the missing filtered value is returned as
        empty-string.


    Returns
    -------
    The list of string representing the results of each of the filter
    expressions defined in `ncg_config`.
    """
    parsed = CiscoConfParse(config=netcfg_filepath, syntax=ncg_config["os_name"])
    filters = ncg_config["filters"]

    grep_results = list()

    for filter_idx, filter_rec in enumerate(filters):

        # Going to write this to locate first any of the known FILTER_OPTIONS
        # since future filter_rec content could be more than just the filter
        # option.

        filter_opt = next(
            (opt for opt, value in filter_rec.items() if opt in FILTER_OPTIONS), None
        )

        if not filter_opt:
            raise RuntimeError(
                f"No valid filter option found in filter item {filter_idx}"
            )

        filter_func = FILTER_OPTIONS[filter_opt]
        filter_expr = filter_rec[filter_opt]

        try:
            res = filter_func(parsed, filter_expr)

        except FilterMatchError as exc:
            if raise_onerror:
                raise RuntimeError(
                    f"filter match error[ {filter_opt}: {exc.expr} ] ({exc.count})"
                )

            if debug is True:
                if exc.count == 0:
                    res = f"! DEBUG-MISSING: {exc.expr}"
                else:
                    res = f"! DEBUG-EXTRA: {exc.expr}"
            else:
                res = ''

        grep_results.append(res)

    return grep_results
