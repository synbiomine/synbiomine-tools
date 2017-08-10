#!/usr/bin/env python3

import argparse
import base64
import jargparse
import json
import requests

############
### MAIN ###
############
parser = jargparse.ArgParser(
    'Test anon session lists to new user',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''QUERY EXAMPLE:
<query view="Gene.primaryIdentifier Gene.symbol" sortOrder="Gene.primaryIdentifier asc">
  <constraint path="Gene.organism.name" code="A" editable="true" op="=" value="Escherichia coli str. K-12 substr. MG1655"/>
</query>''')

parser.add_argument('newUserName')
parser.add_argument('query', help='query XML')
parser.add_argument('listname')
password = 'passw0rd'

parser.add_argument('service', help='InterMine service URL.  e.g. http://synbiomine.org/synbiomine')
args = parser.parse_args()

with open(args.query) as f:
  xml = f.readlines()

print('Creating new user account [%s]' % (args.newUserName))
rdata = { 'name' : args.newUserName, 'password' : password }
r = requests.post('%s/users' % args.service, params = rdata)

print('Requesting anonymous session')
r = requests.get('%s/session' % args.service)
rjson = json.loads(r.text)
anonSessionToken = rjson['token']
print('Got session token [%s]' % anonSessionToken)

print('Creating temporary list [%s]' % args.listname)
rdata = { 'query' : xml, 'name' : args.listname }
r = requests.post('%s/query/tolist' % args.service, headers = { 'Authorization':'Token %s' % anonSessionToken }, params = rdata)
# print(json.loads(r.text))

r = requests.get('%s/lists' % args.service, headers = { 'Authorization':'Token %s' % anonSessionToken})
rListsJson = json.loads(r.text)

print('Got %d lists' % len(rListsJson['lists']))
for listJson in rListsJson['lists']:
    if listJson['authorized']:
        print('Got private list [%s], id [%d]' % (listJson['name'], listJson['id']))

print('Getting API token for existing user account [%s] feeding in anon session [%s]' % (args.newUserName, anonSessionToken))
rdata = { 'type' : 'api', 'existing-anon-session-token' : anonSessionToken }
authString = '%s:%s' % (args.newUserName, password)
print('authString [%s]' % authString)
authStringBytes = bytes(authString, 'utf-8')
authStringB64 = bytes.decode(base64.b64encode(authStringBytes), 'utf-8')
# authStringB64 = base64.b64encode(authString)
r = requests.post(
    '%s/user/tokens' % args.service,
    headers = { 'Authorization':'Basic %s' % authStringB64 },
    params = rdata)
print('[%s]' % r.text)
rjson = json.loads(r.text)
createdUserSessionToken = rjson['token']

r = requests.get('%s/lists' % args.service, headers = { 'Authorization':'Token %s' % createdUserSessionToken})
rListsJson = json.loads(r.text)

print('Got %d lists' % len(rListsJson['lists']))
for listJson in rListsJson['lists']:
    if listJson['authorized']:
        print('Got private list [%s], id [%d]' % (listJson['name'], listJson['id']))