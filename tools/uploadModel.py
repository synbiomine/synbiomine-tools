#!/usr/bin/env python3

import jargparse
import psycopg2

############
### MAIN ###
############
parser = jargparse.ArgParser('Upload an InterMine model to an existing database.')
parser.add_argument('dbName', help='name of the database.')
parser.add_argument('modelPath', help='path to the InterMine model xml')
parser.add_argument('--dbUser', help='db user if this is different from the current')
parser.add_argument('--dbHost', help='db host if this is not localhost')
parser.add_argument('--dbPort', help='db port if this is not localhost')
parser.add_argument('--dbPass', help='db password if this is required')
args = parser.parse_args()

modelPath = args.modelPath
dbName = args.dbName
connString = "dbname=%s" % dbName

if args.dbUser:
    connString += " user=%s" % args.dbUser

dbHost = 'localhost'
if args.dbHost:
    dbHost = args.dbHost
    connString += " host=%s" % dbHost

if args.dbPort:
    connString + " port=%s" % args.dbPort

if args.dbPass:
    connString += " password=%s" % args.dbPass

with open(modelPath) as f:
    modelXml = f.read()

with psycopg2.connect(connString) as conn:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM intermine_metadata WHERE key='model';")
        cur.execute("INSERT INTO intermine_metadata (key, value) VALUES ('model',%s);", (modelXml,))

    conn.commit()