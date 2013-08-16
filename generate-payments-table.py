# -*- coding: utf-8 -*
"""Payments Table Generator

Usage: 
  generate-payments-table.py <from> <to> --token=<token>

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

    transactions = client.period(arguments['<from>'], arguments['<to>'])

    for transaction in transactions:
        try:
            transactions['recipient_message']
        except KeyError:
            transaction['recipient_message'] = ''
        try:
            transaction['variable_symbol']
        except KeyError:
            transaction['variable_symbol'] = ''

        print "||%s\t||%s\t||%s\t||%s\t||%s\t||" % (transaction['date'], transaction['user_identifiaction'], transaction['recipient_message'], transaction['variable_symbol'], transaction['amount'])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Payments Table Generator 0.1')
    main(arguments)
