#!/usr/bin/env python3

import argparse
import jargparse
import json
import requests

############
### MAIN ###
############
parser = jargparse.ArgParser(
    'Test query to list creation using an anonymous session token',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''QUERY EXAMPLE:
<query view="Gene.primaryIdentifier Gene.symbol" sortOrder="Gene.primaryIdentifier asc">
  <constraint path="Gene.organism.name" code="A" editable="true" op="=" value="Escherichia coli str. K-12 substr. MG1655"/>
</query>''')

parser.add_argument('query', help='query XML')
parser.add_argument('service', help='InterMine service URL.  e.g. http://synbiomine.org/synbiomine')
args = parser.parse_args()

with open(args.query) as f:
  xml = f.readlines()

r = requests.get('%s/session' % args.service)
rjson = json.loads(r.text)
print(rjson['token'])

rdata = { 'query' : xml, 'name' : 'jc1' }
r = requests.post('%s/query/tolist' % args.service, headers = { 'Authorization':'Token %s' % rjson['token'] }, params = rdata)
print(r)
