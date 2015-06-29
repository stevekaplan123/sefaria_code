# -*- coding: utf-8 -*-

from sefaria.model import *
import json
import pprint
import pdb
import urllib
import urllib2
from urllib2 import URLError, HTTPError

def processDaf(daf):
	daf_array = daf.split(':')
	letter = daf_array[1][-1]
	value = 1
	if letter == 'b':
		value = 2
	num = int(daf_array[1][0:-1])
	num = ((num-1)*2)+value
	return daf_array[0]+":"+str(num)+daf_array[2]

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
	"titles":  [{
				"lang": "en",
				"text": "Introduction to the Zohar",
				"primary": True
				},
				{
				"lang": "he",
				"text": "הקדמת ספר הזוהר",
				"primary": True
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": intro_ref
})


for parsha in english_parshiot:
	if parsha == "Yitro":
		break
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




haman_file = open("Haman", 'r')
haman_start = Ref("New Zohar "+haman_file.readline())
haman_end = Ref("New Zohar "+haman_file.readline())
haman_ref = haman_start.to(haman_end).normal()
haman_file.close()
structs["nodes"].append({
	"titles":  [{
				"lang": "en",
				"text": "Haman",
				"primary": True
				},
				{
				"lang": "he",
				"text": "המן",
				"primary": True
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": haman_ref
})

dont_go = True
for parsha in english_parshiot:
	if parsha == "Yitro":
		dont_go = False
	if dont_go == True:
		continue
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





conc_file = open("Ha_Idra", 'r')
conc_start = Ref("New Zohar "+conc_file.readline())
conc_end = Ref("New Zohar "+conc_file.readline())
conc_ref = conc_start.to(conc_end).normal()
conc_file.close()
structs["nodes"].append({
	"titles":  [{
				"lang": "en",
				"text": "HaIdra Zuta Kadisha",
				"primary": True
				},
				{
				"lang": "he",
				"text": "האדרא זוטא קדישא",
				"primary": True
				}],
	"nodeType": "ArrayMapNode",
	"refs": [],
	"depth": 0,
	"addressTypes": [],
	"sectionNames": [],
	"wholeRef": conc_ref
})



root = JaggedArrayNode()
root.add_title("New Zohar", "en", primary=True)
root.add_title(u"זהר הבא", "he", primary=True)
#	root.add_title("Sefer Zohar", "en", primary=False)
#	root.add_title("Sefer haZohar", "en", primary=False)
#	root.add_title(u"ספר זוהר", "he", primary=False)
#	root.add_title(u"ספר הזוהר", "he", primary=False)

root.key = "new_zohar"
root.depth = 3
#root.lengths = [3]
root.sectionNames = ["Volume", "Daf", "Paragraph"]
root.addressTypes = ["Integer", "Talmud", "Integer"]

root.validate()

index = {
	"title": "New Zohar",
	"titleVariants": [""],#["Sefer Zohar", "Sefer haZohar"],
	"sectionNames": ["Volume", "Daf", "Paragraph"],
	"categories": ["Kabbalah"],
	"addressTypes": ["Integer", "Talmud", "Integer"],
	"alt_structs": {"Parasha": structs},
	"schema": root.serialize()
}


#Index(index).save()
post_index(index)


'''
structsJSON = json.dumps(structs)
zohar_i = get_index("New Zohar")
zohar_i.set_alt_structure("Parasha", structsJSON)
zohar_JSON = json.dumps(zohar_i.schema)
post_index(zohar_JSON)



zohar_i = get_index("New Zohar")
#zohar_i = get_index_zohar()
#pdb.set_trace()
obj = deserialize_tree(structs, index=zohar_i, struct_class=TitledTreeNode)
obj.title_group = zohar_i.nodes.title_group
obj.validate()
zohar_i.set_alt_structure("Parasha", obj)
zohar_i.save()
'''
