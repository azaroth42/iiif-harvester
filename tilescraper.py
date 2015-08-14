from PIL import Image
import json, StringIO, requests
import time

service = "http://dlss-dev-azaroth.stanford.edu/services/iiif/f1rc/"
resp = requests.get(service + "info.json")
js = json.loads(resp.text)
h = js['height']
w = js['width']
img = Image.new("RGB", (w,h), "white")
tilesize = 400

for x in range(w/tilesize+1):
	for y in range(h/tilesize+1):
		region = "%s,%s,%s,%s" % (x*tilesize, y*tilesize, tilesize, tilesize)
		tileresp = requests.get(service + ("/%s/full/0/default.jpg" % region))
		tile = Image.open(StringIO.StringIO(tileresp.content))
		img.paste(tile, (x*tilesize,y*tilesize))
img.save("full.jpg")

