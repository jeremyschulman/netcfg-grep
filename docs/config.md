# Netcfg-Grep Configuration File

This document describes the structure of the `netcfg-grep` YAML file that is used
to filter (grep) the content from a network device configuration file.

The `netcfg-grep` tool uses [ciscoparseconf](http://www.pennington.net/py/ciscoconfparse/) to
find the configuration statements to filter.   The `netcfg-grep` tool is essentially a nice
wrapper-tool around this library.

## Primary Settings

You will need to identify the network OS sytax for parsing purposes.  You set this
value in the config file using the `os_name` keyword.  You can provide any value
that is valid for the `ciscoparseconf` library.  

```yaml
os_name: nxos
```

The next section identifies the filtering statements used to grep (include)
content from the device configuration file.  The `filters` key is a list of
filter expressions (explained later). These filters are executed in list order.
This behavior results in a nice benefit so that you do not need to ensure your
filtering statements match the order of the content in the device configuration
file.

```yaml
filters:
    - <first-filter>
    - <second-filter>
    - <third-filter>
```

## Filtering Expressions

This section documents each of the filtering expression options.

**Regex Match a Line**<br/>
Use the `include-line` expression to match a _single line_.  The start of line anchor (^)
is automatically applied.  The end of line anchor ($) is **not** automatically applied.

Example: Find the hostname configuration line.

```yaml
filters:
  - include-line: hostname
```

**Regex Match a Block**<br/>
Use the `include-block` expression to match a specific block of configuration. 
The start of line anchor is automatically applied.  The end of line anchor ($)
is automatically applied.  The block results will contain all children
sub-blocks (if any).

Example: Find the loopback0 ineterface.

```yaml
filters:
  - include-block: interface loopback0
```

Note that end of line anchor will ensure that you do not accidentally pick up
wrong blocks.  For example, this block will find _only_ Ethernet1, and not
Etherent11, Ethernet12, etc.

```yaml
filters:
    - include-block: interface Ethernet1
```

Note that if your block contains regex special characters, the plus (+) for exmple, you 
will need to explicitly escape it using the backslash as shown:

```yaml
filters:
  - include-block: aaa group server tacacs\+ MY_GROUP 
```

**Regex Match Multi-Line Block**<br/>

In some cases the "block" is many command lines, each of which start with the
same prefix, but may include additional content.  A good example of this is a
route-map statement, where we want to include the "MCAST" route map.

```text
route-map MCAST permit 10
  match ip multicast group 239.200.101.0/24
route-map MCAST permit 20
  match ip multicast group 239.200.141.0/24
```

Use the `include-block-lines` expression to match these types of configuration blocks.

```yaml
filters:
  - include-block-lines: route-map MCAST
```

**Exact Line Matches**<br/>
Use the `include-exact-lines` expression when you want to filter exact line
statements, meaning that the filter expression should be treated "as-is" and not
interpreted as a regular expression.  This would commonly apply to username
configurations given the text may include regular expression control characters
such as the $.  For example:

```text
username admin password 5 $1$GFT6wdTBABEFACEDEADBEEFODEdPPN  role network-admin
```

Given the perpensity for multiple line use-cases, the `include-exact-lines` can 
be used for more than one configuration file providing you use the folding pipe (|) 
as shown:

```yaml
filters:
  - include-exact-lines: |
      spanning-tree port type edge bpduguard default
      spanning-tree loopguard default
      spanning-tree vlan 1-12,14-3500 priority 4096
      spanning-tree vlan 13 priority 0
```
