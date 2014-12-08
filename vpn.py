"""Usage:
  cli.py connect
  cli.py disconnect
"""

from docopt import docopt

from lib import connect

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')
    if arguments['connect']:
        connect.main()
    if arguments['disconnect']:
        connect.disconnect()