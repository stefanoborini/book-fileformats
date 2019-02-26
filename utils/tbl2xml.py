#!/usr/bin/python

import sys
import xml.dom.minidom

meta = {}
fp = file(sys.argv[1])
while True:
	line = fp.readline().strip()
	if not line: break
	k, v = [ x.strip() for x in line.split(':') ]
	meta[k] = v

header = [ x.strip() for x in fp.readline().split('|') ]

doc = xml.dom.minidom.Document()
table = doc.createElement('table')
table.attributes['id'] = meta['Table-ID']
doc.appendChild(table)

title = doc.createElement('title')
title.appendChild(doc.createTextNode(meta['Title']))
table.appendChild(title)

tgroup = doc.createElement('tgroup')
tgroup.attributes['cols'] = str(len(header))
table.appendChild(tgroup)

thead = doc.createElement('thead')
tgroup.appendChild(thead)

hrow = doc.createElement('row')
thead.appendChild(hrow)

for hname in header:
	entry = doc.createElement('entry')
	entry.appendChild(doc.createTextNode(hname))
	hrow.appendChild(entry)

tbody = doc.createElement('tbody')
tgroup.appendChild(tbody)

while True:
	line = fp.readline().strip()
	if not line: break
	row = doc.createElement('row')
	tbody.appendChild(row)
	for name in [ x.strip() for x in line.split('|') ]:
		entry = doc.createElement('entry')
		entry.appendChild(doc.createTextNode(name))
		row.appendChild(entry)

print doc.toxml()
#for line in fp:
	
