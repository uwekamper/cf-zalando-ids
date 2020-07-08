import os
import csv
import logging
import random

log = logging.getLogger(__name__)

SHORT_CODE_LENGTH = 8
SHORT_CODE_ALPHABET = [
    # Numbers
    # excluded: '0',
    '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # upper-case chars
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    # excluded: 'I',
    'J','K', 'L', 'M', 'N',
    # excluded: 'O',
    'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    # lower-case chars
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    # excluded: 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]


def make_short_code(blocked: set, length: int=SHORT_CODE_LENGTH, alphabet: list=SHORT_CODE_ALPHABET):
    done = False
    new_code = None
    while done is False:
        new_code = ''.join( random.choices(alphabet, k=length) )
        if not new_code in blocked:
            blocked.add(new_code)
            done = True
        else:
            print("MEEEEEP")
                
    return new_code


def read_blocked_ids(filename=None) -> set:
    blocked_codes = set()
    if not filename:
        filename = os.path.join(os.path.dirname(__file__), 'Code-2020-07-08.csv')
        
    log.info("Reading block codes from '%s' ..." % filename)
    with open(filename, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            code = row['short_code'].strip()
            if len(code) < 1:
                # print("WARNING empty short code ingnored.")
                continue
                
            if code in blocked_codes:
                print("WARNING %s appears multiple times" % code)
            blocked_codes.add(code)
    num_code = len(blocked_codes)
    log.info("%d blocked codes found." % num_code)
    return blocked_codes


def bulk_create(blocked: set, skus: tuple) -> list:
    total_codes = []
    all_codes = {}
    serial_no = 1
    for sku, number_needed in skus:
        sku_serial_no = 1
        sku_codes = []
        for i in range(number_needed):
            label = make_short_code(blocked)
            qr = make_short_code(blocked)
            row = [serial_no, sku_serial_no, sku, 'circularity.id/%s' % label, 'https://circularity.id/%s' % qr]
            sku_codes.append(row)
            total_codes.append(row)
            sku_serial_no += 1
            serial_no += 1
        all_codes[sku] = sku_codes
    all_codes['total'] = total_codes
    return all_codes


def bulk_save(code_lists, export_dir):
    headers = ['serial_no', 'sku_serial_no', 'sku', 'label', 'qr_code']
    for sku, codes in code_lists.items():
        with open(os.path.join(export_dir, '%s.csv' % sku), mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(headers)
            for row in codes:
                writer.writerow(row)
        