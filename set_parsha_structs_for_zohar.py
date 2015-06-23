# -*- coding: utf-8 -*-

from sefaria.model import *
import json
import pprint
import pdb
import urllib
import urllib2
from urllib2 import URLError, HTTPError


def post_index(index):
	url = 'http://localhost:8000/api/v2/raw/index/New_Zohar'
	indexJSON = json.dumps(index)
	values = {
		'json': indexJSON, 
		'apikey': 'F4J2j3RF6fHWHLtmAtOTeZHE3MOIcsgvcgtYSwMzHtM'
	}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	try:
		response = urllib2.urlopen(req)
		print response.read()
	except HTTPError, e:
		print 'Error code: ', e.code

#intro has he_title


title = "New Zohar"
genesis_parshiot = ["Bereshit", "Noach", "Lech Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi"]
exodus_parshiot = ["Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei"]
leviticus_parshiot = ["Vayikra", "Tzav", "Shmini", "Tazria", "Metzora", "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai"]
numbers_parshiot = ["Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach", "Chukat", "Balak", "Pinchas", "Matot"]
deut_parshiot = ["Devarim", "Vaetchanan", "Eikev", "Shoftim", "Ki Teitzei", "Vayeilech", "Ha'Azinu"]
english_parshiot = genesis_parshiot+exodus_parshiot+leviticus_parshiot+numbers_parshiot+deut_parshiot

structs = {}
structs = { "nodes" : [] }

intro_file = open("Introduction", 'r')
intro_start = Ref("New Zohar "+intro_file.readline())
intro_end = Ref("New Zohar "+intro_file.readline())
intro_ref = intro_start.to(intro_end).normal()
intro_file.close()
structs["nodes"].append({
	"title":  [{
				"lang": "en",
				"text": "Introduction to the Zohar"
				},
				{
				"lang": "he",
				"text": "הקדמת ספר הזוהר"
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": intro_ref
})


haman_file = open("Haman", 'r')
haman_start = Ref("New Zohar "+haman_file.readline())
haman_end = Ref("New Zohar "+haman_file.readline())
haman_ref = haman_start.to(haman_end).normal()
haman_file.close()
structs["nodes"].append({
	"title":  [{
				"lang": "en",
				"text": "Haman"
				},
				{
				"lang": "he",
				"text": "המן"
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": haman_ref
})


conc_file = open("Ha_Idra", 'r')
conc_start = Ref("New Zohar "+conc_file.readline())
conc_end = Ref("New Zohar "+conc_file.readline())
conc_ref = conc_start.to(conc_end).normal()
conc_file.close()
structs["nodes"].append({
	"title":  [{
				"lang": "en",
				"text": "Ha-Idra Zuta Kadisha"
				},
				{
				"lang": "he",
				"text": "האדרא זוטא קדישא"
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": conc_ref
})


for parsha in english_parshiot:
	f = open(parsha, 'r')
	start = Ref("New Zohar "+f.readline())
	end = Ref("New Zohar "+f.readline())
	whole_ref = start.to(end).normal()
		
	structs["nodes"].append({
		"sharedTitle": parsha,
		"nodeType": "ArrayMapNode",
		"refs": [],
		"depth": 0,
		"addressTypes": [],
		"sectionNames": [],
		"wholeRef": whole_ref
	})
	f.close()

'''
structsJSON = json.dumps(structs)
zohar_i = get_index("New Zohar")
zohar_i.set_alt_structure("Parasha", structsJSON)
zohar_JSON = json.dumps(zohar_i.schema)
post_index(zohar_JSON)
'''

zohar_i = get_index("New Zohar")
obj = deserialize_tree(structs, index=zohar_i, struct_class=TitledTreeNode)
obj.title_group = zohar_i.nodes.title_group
obj.validate()
zohar_i.set_alt_structure("Parasha", obj)
zohar_i.save()
