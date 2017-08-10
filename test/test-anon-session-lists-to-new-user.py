#!/usr/bin/env python3

import argparse
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

parser.add_argument('service', help='InterMine service URL.  e.g. http://synbiomine.org/synbiomine')
args = parser.parse_args()

with open(args.query) as f:
  xml = f.readlines()

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
    if listJson['authorized'] == True:
        print('Got private list [%s], id [%d]' % (listJson['name'], listJson['id']))

print('Creating new user account [%s] feeding in anon session [%s]' % (args.newUserName, anonSessionToken))
rdata = { 'name' : args.newUserName, 'password' : 'passw0rd', 'existing-anon-session-token' : anonSessionToken }
r = requests.post('%s/users' % args.service, params = rdata)
rjson = json.loads(r.text)
createdUserSessionToken = rjson['user']['temporaryToken']

r = requests.get('%s/lists' % args.service, headers = { 'Authorization':'Token %s' % createdUserSessionToken})
rListsJson = json.loads(r.text)

print('Got %d lists' % len(rListsJson['lists']))
for listJson in rListsJson['lists']:
    if listJson['authorized'] == True:
        print('Got private list [%s], id [%d]' % (listJson['name'], listJson['id']))

# Todo: check if now permanent list has the same id as the temporary one