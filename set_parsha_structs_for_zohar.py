# -*- coding: utf-8 -*-

from sefaria.model import *
import json
import pprint
import pdb
import urllib
import urllib2
from urllib2 import URLError, HTTPError


def post_index(index):
	url = 'http://dev.sefaria.org/api/v2/raw/index/New_Zohar'
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



title = "New_Zohar"
genesis_parshiot = ["Introduction", "Bereishit", "Noach", "Lech_lecha", "Vayera", "Chayei_Sarah", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi"]
exodus_parshiot = ["Exodus", "Vaera", "Bo", "Beshalach", "Haman", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki_Tisa", "Vayakhel", "Pekudei"]
leviticus_parshiot = ["Vayikra", "Tzav", "Shemini", "Tazria", "Metzora", "Acharei_Mot", "Kedoshim", "Emor", "Behar", "Bechukotai"]
numbers_parshiot = ["Bamidbar", "Naso", "Behalotcha", "Shelach", "Korach", "Chukat", "Balak", "Pinchas", "Matot"]
deut_parshiot = ["Devarim", "Vaetchanan", "Eikev", "Shoftim", "Ki_Teitzei", "Vayelech", "Haazinu", "Ha_Idra_Zuta_Kadisha"]
english_parshiot = genesis_parshiot+exodus_parshiot+leviticus_parshiot+numbers_parshiot+deut_parshiot

structs = {}
structs[title] = { "nodes": [] }
for parsha in english_parshiot:
	f = open(parsha, 'r')
	start = Ref("New Zohar  "+f.readline())
	end = Ref("New Zohar "+f.readline())
	whole_ref = start.to(end).normal()
		
	structs[title]["nodes"].append({
		"sharedTitle": title,
		"nodeType": "ArrayMapNode",
		"depth": 0,
		"addressTypes": [],
		"sectionNames": [],
		"wholeRef": whole_ref
	})
	f.close()

zohar_i = get_index("New_Zohar")
zohar_i.set_alt_structure("Parasha", structs)
#post_index(structs)
'''
for struct in structs[title]['nodes']:
	obj = deserialize_tree(struct, index=zohar_index, struct_class=TitledTreeNode)
	obj.title_group = i.nodes.title_group
	obj.validate()
	zohar_index.set_alt_structure("Parasha", obj)
	zohar_index.save()
'''

