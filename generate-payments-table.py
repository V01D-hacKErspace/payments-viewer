# -*- coding: utf-8 -*
"""Payments Table Generator

Usage: 
  generate-payments-table.py <month> --token=<token>
  generate-payments-table.py <from> <to> --token=<token>

Options:
  -h --help         Show this screen.
  --version         Show version.
  --token=<token>   Fio Bank token.

"""
from docopt import docopt

import sys
from fiobank import FioBank

import calendar
from timelib import strtodatetime
import datetime

def table_header():
    header = """||border="2" style="border-collapse:collapse;margin-left:0px;" cellpadding="5" width=100%
||! Datum ||! Odosielatel ||! Sprava ||! Variabilny symbol ||! Suma ||"""

    return header

def main(arguments):
    client = FioBank(token=arguments['--token'])

    if '<month>' in arguments:
        month = strtodatetime(arguments['<month>'])
        month_range = calendar.monthrange(month.year, month.month)
        
        month_start = datetime.date(month.year, month.month, month_range[0])
        month_end = datetime.date(month.year, month.month, month_range[1])

        transactions = client.period(month_start, month_end)
    else:
        transactions = client.period(arguments['<from>'], arguments['<to>'])
    
    print table_header()

    for transaction in transactions:
        try:
            transaction['recipient_message']
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
