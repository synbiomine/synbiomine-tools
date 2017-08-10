#!/usr/bin/env python3

import jargparse
import json
import requests

############
### MAIN ###
############
parser = jargparse.ArgParser('Test creating a new user')

parser.add_argument('newUserName')
parser.add_argument('service', help='InterMine service URL.  e.g. http://synbiomine.org/synbiomine')
args = parser.parse_args()

print('Creating new user account [%s]' % (args.newUserName))
rdata = { 'name' : args.newUserName, 'password' : 'passw0rd' }
r = requests.post('%s/users' % args.service, params = rdata)
print(json.loads(r.text))