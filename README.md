# lta

LTA is the long term archiving tool for the
[Oral History.Digital](https://www.oral-history.digital/)
project of Freie Universität Berlin.

The lta tool prepares
[CMDI metadata files](https://www.clarin.eu/content/component-metadata)
for the
[BAS CLARIN Repository](https://clarin.phonetik.uni-muenchen.de/BASRepository/)
of the
[Bavarian Archive for Speech Signals](https://www.bas.uni-muenchen.de/Bas/BasHomeeng.html).

## Building the command line tool

Clone this repository. Enter the project directory, and type:

```bash
pip install .
```

You can now execute the tool like this:

```bash
lta --help
lta list
lta fetch cdoh --batch=1
```

## Configuration

Your configuration file must be in your user directory, named `~/.lta.config`
and look like this:

```ini
[DEFAULT]
TempPath=~/work/lta_tmp

[cdoh]
Domain=https://archiv.cdoh.net
MediaPath=/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/cdoh
```
