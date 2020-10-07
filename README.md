# Network Device Config Grep Tool

This package contains a tool called `netcfg-grep` that allows a User to extract (grep)
specific sections of a network configuration file.  The motivating use-case:

    As a member of the network team I need to perform configuration audits.  I need
    a tool that will allow me to selectively extract sections of the config that I need
    to examine as I might not want to compare the entire configuration file.  For example,
    I might want to only check the "IP access Lists" or the "VLAN interfaces" for audit
    compliance.
    
    As such, I would use the `netcfg-grep` tool to extract only those sections I
    want to examine from the actual configuration file.  I will also have an
    *expected** configuration file.  I would use the same netcfg-grep control
    file to extract the same sections from the expected configuration file so
    that I could diff the results of the acutal config against the results of
    the expected config.

    I want to be able to obtain the actual network configuration file independently
    of the `netcfg-grep` tool.  I may have another system that keeps these files,
    or I may want to retrieve them on demand.
    
    I want to be able to perform the diff of the actual configuration and the
    expected configuration independently of the `netcfg-grep` tool. I could use
    icdiff on my laptop, or I might want to use Github compare feature.
    

# Installation

This package is not yet available in PyPi.  To install in your local environment:

```shell
pip install netcfg-grep@git+https://github.com/jeremyschulman/netcfg-grep.git
```

# Usage

You will need to create a YAML configuration file that defines the sections of
the configuraiton to filter.  Once created, you can then use `netcfg-grep` to
extract the results from the network configuration file:

```shell
netcfg-grep -g <grep-config-file.yaml> -d <device-config-file>
```

The output of this command will be the filtered content, which you can redirect
to an output file.

The structure of the `netcfg-grep` configuration file is current a WIP, and will
be documented [here](docs/config.md)


