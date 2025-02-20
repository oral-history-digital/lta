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
lta archive cdoh --batch=1
```

As an alternative, you can execute the tool with [uv](https://docs.astral.sh/uv/) if you do not want to install it:

```bash
uv run lta
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

[ev]
Domain=https://archiv.eiserner-vorhang.de
MediaPath=/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/ev
```

General settings belong in the `DEFAULT` section:
* `TempPath` Path to a temporary directory that is used for downloading metadata files from the server.

For each archive there should be a specific section, named after the archive
shortname (e.g. cdoh, ev, ...). Within these sections, section specific settings
can be made:
* `Domain` Domain of the archive for downloading metadata files.
* `MediaPath` Directory on the file server where the media files for a specific
archiving process are stored.


## Usage

### General usage

Before using the LTA tool, make sure that an archiving batch is set up on the server.
An archiving batch consists of a number (e.g. 001) and the interviews that should be
archived. At the moment, the archiving batch has to be created with the Rails console
on the server.

Also make sure that the archive is in the configuration file. To see, which archives
are configured, you can use the `list` command:

```console
$ lta list
adg cdoh ev
```

You can also list the batches for an archive that are currently set up on the
server with the `batches` command:

```console
$ lta batches ev
Batch 1 (ohd_ev_001) was created on 2023/02/20 and has 16 interviews:
ev001, ev002, ev003, ev004, ev005, ev006, ev007, ev008, ev009, ev010, ev011, ev012, ev013, ev014, ev015, ev016
```

The archiving process basically consists of two steps: 1) downloading metadata files
from the server and 2) enriching those files with information about the archived
media files and transcript files. Those steps are combined into one step within
the LTA tools `archive` command:

```console
$ lta archive cdoh --batch=2
```

The above command would try to download metadata files of the cdoh archive that
belong to batch number 2 as it is set up on the server. Then it would look at the
media files in the `MediaPath` directory and add information about those
to the metadata files. At the same time, the media files are checked for obvious
missing files. In the end, the enriched metadata files are saved within the
`MediaPath` directory.

### Options

Because the whole process can be error-prone, the `archive` command has a lot
of options to alter its behaviour. You can use type `lta archive --help` to see
them:

```console
$ lta archive --help
Usage: lta archive [OPTIONS] ARCHIVE

  fetch and process archive metadata

Options:
  -b, --batch INTEGER           batch number  [default: 1]
  -f, --fetch-only              just fetch metadata files to temp dir
  -s, --skip-fetch              do not fetch metadata, use temp dir instead
  -o, --output-dir DIRECTORY    use output directory other than media
                                directory
  -d, --dry-run                 do not create any files
  -c, --checksums               create checksums
  -t, --type [MD5|SHA1|SHA256]  hash type for checksum generation  [default:
                                SHA256]
  -h, --help                    Show this message and exit.
```

#### --fetch-only

This option just executes the first step of the two-step process. It downloads
the metadata files to the temp directory `TempPath`.

#### --skip-fetch

This option skips the first step and only executes the second step of the process.
If you encountered an error during the enrichment of the metadata files, you
can use this option to not download the metadata files again. Instead, the files
in `TempPath` are used.

#### --output-dir

Normally, `lta archive` attempts to directly save the enriched metadata files
within the `MediaPath` directory, side by side with the media files. Sometimes
you may not want this, e.g. if you need to further adjust the media files before
copying them or if you just want to inspect the enriched files.
In this case, use `--output-dir` to specifiy the directory the enrichted metadata
files should be saved to.

#### --dry-run

With this option, no files or directories are created. You can use it to make a
test run. During the run, the lta tool outputs which files or directories would
normally be created.

#### --checksums

not available yet

#### --type

not available yet

### Possible workflows

With the above options, you could use one of several workflows that work best
for you, e.g.

```console
$ lta archive cdoh --batch=2 --fetch-only
```

to fetch the metadata. Then do a dry run:

```console
$ lta archive cdoh --batch=2 --dry-run
```

and if everything seems okay do the real run:

```console
$ lta archive cdoh --batch=2 --skip-fetch
```

Instead of doing a dry-run, you could also write to a different output directory
with the `--output-dir` option and later remove that option to write directly
to the `MediaPath` directory.
