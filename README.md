# lta

LTA is the long term archiving tool for the
Oral History.Digital project of Freie Universität Berlin.

## Building the command line tool

Clone this repository. Enter the project directory, and type:

```
pip install .
```

You can now execute the tool like this:

```
lta --help
lta list
lta fetch cdoh --batch=1
```

## Configuration

Your configuration file must be in your user directory, named `~/.lta.config`
and look like this:

```
[DEFAULT]
TempPath=~/work/lta_tmp

[cdoh]
Domain=https://archiv.cdoh.net
MediaPath=/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/cdoh
```
