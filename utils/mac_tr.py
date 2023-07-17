#!/usr/bin/python3

import sys
import re
import logging
import argparse
from logging import info, debug
import pdb


logging.basicConfig(
    format='[%(asctime)s %(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
)


def check_multicast_ip_format(ip):
    patt = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    try:
        multicast_ip = patt.search(ip).group()
    except:
        print(f'Not valid format IP address. check your input "{ip}"')
        return False, ''

    valid = True
    for i, elem in enumerate(multicast_ip.split('.')):
        elem = int(elem)
        if i == 0:
            if not (224 <= elem <= 239):
                valid = False
        else:
            if not (0 <= elem <= 255):
                valid = False

    if not(valid):
        print(f'Not valid IP address scope. check your input "{ip}"')
        return False, ''
    
    return True, multicast_ip


def translate_to_mac(multicast_ip):
    # hex format
    mac_addr = ['01', '00', '5E']

    for i, elem in enumerate(multicast_ip.split('.')[1:]):
        elem = int(elem)
        if i == 0:
            elem = elem & 0b01111111
        hex_value = hex(elem)[2:]
        if len(hex_value) == 1:
            hex_value = '0' + hex_value
        mac_addr.append(hex_value.upper())
    mac_addr = ':'.join(mac_addr)

    return mac_addr


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('multicast_ip')
    args = parser.parse_args()
    arg1 = args.multicast_ip

    result, multicast_ip = check_multicast_ip_format(arg1)
    if not(result):
        exit(-1)

    debug(f'multicast ip: {multicast_ip}')

    mac_addr = translate_to_mac(multicast_ip)
    info(f'{mac_addr}')


if __name__ == "__main__":
    main(sys.argv[1:])
