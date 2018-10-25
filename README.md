# Wikibox

WikiBox project software.

Chooses a random Wikipedia entry from a category and prints it in a thermal printer.

## License

The project is under MIT License.

## Installation

The project is intender to run in Python 3 and a Raspberry Pi.

The Wikipedia API must be installed for running this program:

`python3 -m pip install wikipedia-api`

## Running at boot

For starting the python program at boot a line in `/etc/rc.local` must be insterted:

`/path_to_program/wikibox.py &`
