#!/usr/bin/python3

""" This module checks whether it is possible to successfully connect to
the EPP server (domains registry). The connection to the EPP server
is performed over HTTP using SSL encryption(i.e., in https mode). The module
uses the built-in libraries: argparse, errno, sys, xml.etree.ElementTree,
as well as loadable requests, urllib3.
"""

import argparse
import errno
import sys
import xml.etree.ElementTree as ET

import requests
import urllib3

# disabling the connection warning without using CA_certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# request form
xmlReq = """<?xml version="1.0" encoding="UTF-8" ?>
<epp xmlns="http://www.ripn.net/epp/ripn-epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ripn.net/epp/ripn-epp-1.0 ripn-epp-1.0.xsd">
  <hello/>
</epp>
"""


# creating a command-line parser
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='this argument is required')
    parser.add_argument('--clicert', metavar='Client_certificate',
                        help='this argument is required')
    parser.add_argument('--clikey', metavar='Client_key',
                        help='this argument is required')
    parser.add_argument('--cacert', default=False, metavar='CA_certificate')
    return parser


# parsing and command line checking
parser = createParser()
namespace = parser.parse_args()
args = list()
if not (namespace.url and namespace.clicert and namespace.clikey):
    if not namespace.url:
        args.append("--url")
    if not namespace.clicert:
        args.append("--clicert")
    if not namespace.clikey:
        args.append("--clikey")
    print("ERROR: the following arguments are required:", args)
    parser.print_help()
    sys.exit(3)

# request, error handling and parsing xml-response
try:
    wrong_file = namespace.clicert
    file = open(str(namespace.clicert))
    file.close()
    wrong_file = namespace.clikey
    file = open(str(namespace.clikey))
    file.close()
    if namespace.cacert:
        wrong_file = namespace.cacert
        file = open(str(namespace.cacert))
        file.close()
    r = requests.post(namespace.url, data=xmlReq, json="",
                      cert=(namespace.clicert, namespace.clikey),
                      verify=namespace.cacert, timeout=3)
    root = ET.fromstring(r.text)
except OSError as e:
    if e.errno == errno.ENOENT:
        print("ERROR: No such file or directory:", wrong_file)
        sys.exit(3)
    else:
        pos1 = str(e).find(":")
        pos2 = str(e).find("Failed to")
        pos3 = str(e).find("Connection to")
        if pos2 != -1:
            print("CRITICAL:", str(e)[:pos1 + 1],
                  str(e)[pos2:len(str(e)) - 4])
        elif pos3 != -1:
            print("CRITICAL:", str(e)[:pos1 + 1],
                  str(e)[pos3:len(str(e)) - 3])
        else:
            print("CRITICAL:", e)
        sys.exit(2)
except requests.exceptions.SSLError as e:
    print("CRITICAL:", e)
    sys.exit(2)
except ET.ParseError as e:
    print("WARNING: can`t parse xml-response:", e)
    sys.exit(1)
else:
    f = False
    for child in root:
        if str(child.tag).endswith('greeting'):
            f = True
    if f and str(root.tag).endswith('epp'):
        print("OK: possible to successfully connect to the EPP server")
        sys.exit(0)
    else:
        if f:
            print("WARNING: response has not epp tag")
        else:
            print("WARNING: response has not greeting tag")
        sys.exit(1)
