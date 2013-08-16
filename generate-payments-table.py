# -*- coding: utf-8 -*
"""Payments Table Generator

Usage: generate-payments-table.py <from> <to> --token=<token>

Options:
  -h --help         Show this screen.
  --version         Show version.
  --token=<token>   Fio Bank token.

"""
from docopt import docopt

import sys
from fiobank import FioBank

def main(arguments):
    client = FioBank(token=arguments['--token'])

    gen = client.period(arguments['<from>'], arguments['<to>'])

    for g in gen:
        try:
            g['recipient_message']
        except KeyError:
            g['recipient_message'] = ''
        try:
            g['variable_symbol']
        except KeyError:
            g['variable_symbol'] = ''

        print "||%s\t||%s\t||%s\t||%s\t||%s\t||" % (g['date'], g['user_identifiaction'], g['recipient_message'], g['variable_symbol'], g['amount'])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Payments Table Generator 0.1')
    main(arguments)
