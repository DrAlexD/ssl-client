# SSL-Client for connecting to the EPP server
This module checks whether it is possible to successfully connect to
the EPP server (domains registry). The connection to the EPP server
is performed over HTTP using SSL encryption(i.e., in https mode). The module
uses the built-in libraries: argparse, errno, sys, xml.etree.ElementTree,
as well as loadable requests, urllib3.

usage: Client.py [-h] [--url URL] [--clicert Client_certificate] [--clikey Client_key] [--cacert CA_certificate]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             this argument is required
  --clicert Client_certificate
                        this argument is required
  --clikey Client_key   this argument is required
  --cacert CA_certificate
