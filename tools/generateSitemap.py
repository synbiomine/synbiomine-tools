#!/usr/bin/env python3

import datetime
import jargparse
from intermine.webservice import Service
from lxml import etree

# MAIN
parser = jargparse.ArgParser('Generate a sitemap for an InterMine installation.')
parser.add_argument(
    'mineUrl', help="InterMine URL.  For example, http://www.synbiomine.org/synbiomine")
args = parser.parse_args()

service = Service(args.mineUrl + '/service')

# Get a new query on the class (table) you will be querying:
query = service.new_query("Gene")

# The view specifies the output columns
query.add_view("primaryIdentifier")

# Uncomment and edit the line below (the default) to select a custom sort order:
# query.add_sort_order("Pathway.primaryIdentifier", "ASC")

# You can edit the constraint values below
# query.add_constraint("primaryIdentifier", "IS NOT NULL", code = "A")
query.add_constraint("primaryIdentifier", "IS NOT NULL", code="A")
# query.add_constraint("organism.shortName", "=", "H. sapiens", code = "B")

# Uncomment and edit the code below to specify your own custom logic:
# query.set_logic("A")

sitemapCount = 0

prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
prefix += "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"\n"
prefix += "  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
prefix += "  xsi:schemaLocation=\"http://www.sitemaps.org/schemas/sitemap/0.9" \
    + " http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n"

postfix = "</urlset>"

rowCount = 0

f = open('sitemap' + str(sitemapCount) + '.xml', 'w')

f.write(prefix)

for row in query.rows():
    f.write(
        '<url><loc>'
        + args.mineUrl + '/portal.do?class=Gene&amp;externalids=' + row["primaryIdentifier"]
        + "</loc></url>\n")

    rowCount = rowCount + 1

    if rowCount >= 50000:
        f.write(postfix)
        f.close()
        sitemapCount = sitemapCount + 1
        f = open('sitemap' + str(sitemapCount) + '.xml', 'w')
        f.write(prefix)
        rowCount = 1

f.write(postfix)
f.close() 

dateString = datetime.datetime.now().strftime('%Y-%m-%d')

# Write main sitemap file
nsMap = {None: 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xsi': 'http://www.w3.org/1999/xlink'}
rootElem = etree.Element('urlset', nsmap=nsMap)
rootElem.attrib['{http://www.w3.org/1999/xlink}schemaLocation'] \
    = 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'

for i in range(0, sitemapCount + 1):
    sitemapElem = etree.SubElement(rootElem, 'sitemap')
    locElem = etree.SubElement(sitemapElem, 'loc')
    locElem.text = '%s/sitemap%d.xml' % (args.mineUrl, i)
    lastmodElem = etree.SubElement(sitemapElem, 'lastmod')
    lastmodElem.text = dateString

print(etree.tostring(rootElem, pretty_print=True))

etree.ElementTree(rootElem).write('sitemap.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
