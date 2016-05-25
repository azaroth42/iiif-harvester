from PIL import Image
import json, StringIO, requests
import time
import robotparser
import re

host = "http://dlss-dev-azaroth.stanford.edu/"

service = host + "services/iiif/f1rc/"
resp = requests.get(service + "info.json")
js = json.loads(resp.text)
h = js['height']
w = js['width']
img = Image.new("RGB", (w,h), "white")

## Respect tile dimensions of server
tilesize = 1024
if js.has_key('tiles'):
	tilesize = js['tiles']['width']

## Introduce baseline crawl delay
delay = 1

## Parse robots.txt
resp = requests.get(host + "/robots.txt")
if resp.status == 200:
	parser = robotparser.RobotFileParser()
	parser.parse(resp.text)
	okay = parser.can_fetch("*", service)
	if not okay:
		print "Blocked by robots.txt"
		sys.exit()
	# No support for Crawl-delay extension ... just search
	cd = re.compile("Crawl-delay: ([0-9]+)")
	m = cd.search(resp.text)
	if m:
		delay = int(m.groups()[0])

for x in range(w/tilesize+1):
	for y in range(h/tilesize+1):
		region = "%s,%s,%s,%s" % (x*tilesize, y*tilesize, tilesize, tilesize)
		tileresp = requests.get(service + ("/%s/full/0/default.jpg" % region))
		tile = Image.open(StringIO.StringIO(tileresp.content))
		img.paste(tile, (x*tilesize,y*tilesize))
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(delay)

img.save("full.jpg")

