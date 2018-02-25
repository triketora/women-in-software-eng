#!/usr/bin/python

"""Much thanks to this blog post:
http://www.mattcutts.com/blog/write-google-spreadsheet-from-python/
"""

import argparse
import datetime
import re

from gdata import gauth
from gdata.spreadsheet import service as ss_service
from gdata.service import RequestError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

CLIENT_SECRETS_FILENAME = 'client_secrets.json'
SS_KEY = '0AlZH8QBl60oodEJTdFA5TlZOcDJCMU02RkZoSHF5SHc'
WORKSHEET_ID = 'od6'

ss_client = None

def init_ss_client(client_secrets_filename, flags):
    global ss_client
    if not ss_client:
        storage = Storage('creds.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(
                flow_from_clientsecrets(
                    client_secrets_filename,
                    scope=['https://spreadsheets.google.com/feeds']),
                storage,
                flags)

        ss_client = ss_service.SpreadsheetsService(
            additional_headers={'Authorization': 'Bearer %s' % credentials.access_token})
        ss_client.auth_token = gauth.OAuth2TokenFromCredentials(credentials)
        ss_client.source = 'Update Script'
        ss_client.ProgrammaticLogin()


def _print_line_skip_warning(line):
    print 'Warning... skipping line:\n\t%s\n' % line


row_key_pattern = '\[(?P<row_key>\w+)\]'
row_key_prog = re.compile(row_key_pattern)


def _extract_row_key_from_data_line(line):
    row_key = None
    m = row_key_prog.match(line)
    if m and m.group('row_key'):
        row_key = m.group('row_key')
    return row_key


col_keys = ('company', 'team', 'num_female_eng', 'num_eng', 'last_updated')


def _extract_col_key_value_from_data_line(line):
    col_key, col_value = None, None

    split_line = line.split(':')
    if len(split_line) == 2:
        if split_line[0] in col_keys:
            col_key, col_value = split_line
            col_key = col_key.strip()
            col_value = col_value.strip()

    return col_key, col_value


required_col_keys = ('company', 'num_female_eng', 'num_eng')


def _clean_row_data(row_data):
    for required_col_key in required_col_keys:
        if required_col_key not in row_data.keys():
            return None

    try:
        num_female_eng = int(row_data['num_female_eng'])
        row_data['num_female_eng'] = num_female_eng
        num_eng = int(row_data['num_eng'])
        row_data['num_eng'] = num_eng
    except ValueError:
        return None

    row_data['percent_female_eng'] = '%.2f' % (
        100. * num_female_eng / num_eng)

    col_keys = row_data.keys()
    if 'team' not in col_keys:
        row_data['team'] = 'N/A'
    if 'last_updated' not in col_keys:
        row_data['last_updated'] = 'Not provided'

    return row_data

def parse_ss_rows_data_from_file(filename):
    rows_data = {}
    row_key = None
    row_data = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('#'):
                continue
            next_row_key = _extract_row_key_from_data_line(line)

            if row_key and next_row_key:
                # Save last row's data.
                clean_row_data = _clean_row_data(row_data)
                if clean_row_data:
                    clean_row_data['key'] = row_key
                    rows_data[row_key] = clean_row_data
                row_data = {}
            if next_row_key:
                # Move onto constructing data for the next row.
                row_key = next_row_key
                continue

            if not row_key:
                # No row_key!
                _print_line_skip_warning(line)
            else:
                col_key, col_value = _extract_col_key_value_from_data_line(line)
                if col_key is not None and col_value is not None:
                    row_data[col_key] = col_value
                else:
                    # Invalid col data.
                    _print_line_skip_warning(line)
        clean_row_data = _clean_row_data(row_data)
        if clean_row_data:
            clean_row_data['key'] = row_key
            rows_data[row_key] = clean_row_data

    return rows_data


def _summarize_rows_data(rows_data):
    num_female_eng = 0
    num_eng = 0
    for row_data in rows_data:
        num_female_eng += row_data['num_female_eng']
        num_eng += row_data['num_eng']

    today = datetime.date.today()
    summary_row_data = {
        'key': 'all',
        'company': 'ALL',
        'num_female_eng': num_female_eng,
        'num_eng': num_eng,
        'last_updated': today.strftime('%m/%d/%y')
    }
    return _clean_row_data(summary_row_data)


def clear_ss_data(ss_key, worksheet_id):
    list_feed = ss_client.GetListFeed(ss_key, worksheet_id)
    if list_feed:
        for row in list_feed.entry:
            ss_client.DeleteRow(row)


def update_ss_from_file(ss_key, worksheet_id, data_filename):
    if not ss_client:
        print 'Oops! SpreadsheetsService client not initialized.'
        return

    clear_ss_data(ss_key, worksheet_id)

    rows_data = parse_ss_rows_data_from_file(data_filename).values()
    summary_row_data = _summarize_rows_data(rows_data)
    rows_data.append(summary_row_data)

    # Sort in descending order by number of total engineers.
    rows_data.sort(key=lambda r: r['num_eng'], reverse=True)

    for row_data in rows_data:
        row_data = dict((key.replace('_', ''), str(value))
                        for key, value in row_data.items())
        inserted = False
        while not inserted:
            try:
                ss_client.InsertRow(row_data, ss_key, worksheet_id)
                inserted = True
            except RequestError as e:
                print "Request error: {0}".format(e)
            except:
                raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Update spreadsheet.', parents=[tools.argparser])
    parser.add_argument('-c', '--client-secrets-filename')
    parser.add_argument('-d', '--data-filename')
    parser.add_argument('-s', '--spreadsheet-key')

    flags = parser.parse_args()
    client_secrets_filename = flags.client_secrets_filename or CLIENT_SECRETS_FILENAME
    data_filename = flags.data_filename
    ss_key = flags.spreadsheet_key

    init_ss_client(client_secrets_filename, flags)
    update_ss_from_file(ss_key, WORKSHEET_ID, data_filename)
