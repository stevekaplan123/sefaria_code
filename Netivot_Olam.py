# -*- coding: utf-8 -*-

from sefaria.model import *
from sefaria.tracker import add
import urllib
import urllib2
from urllib2 import URLError, HTTPError
import json



def post_index(index):
	url = 'http://www.sefaria.org/api/index/' + index["title"].replace(" ", "_")
	indexJSON = json.dumps(index)
	print indexJSON
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
		
root = SchemaNode()
root.add_title("Netivot Olam", "en", primary=True)
root.add_title(u"נתיבות עולם", "he", primary=True)
root.key = "netivot"

part1 = JaggedArrayNode()
part1.add_title(u"הקדמה", "he", primary=True)
part1.add_title("Introduction to Netivot Olam", "en", primary=True)
part1.depth = 1
part1.sectionNames = ["Paragraph"]
part1.addressTypes = ["Integer"]
part1.key = "intro"

root.append(part1)

subsections = [
	["Netiv Hatorah", 18, u"נתיב התורה"],
	["Netiv Ha'Avodah", 19, u"נתיב העבודה"],
	["Netiv Gmilut Chasadim", 5, u"נתיב גמילות חסדים"],
	["Netiv Hatzdaka", 6, u"נתיב הצדקה"],
	["Netiv Hadin", 2, u"נתיב הדין"],
	["Netiv Haemet", 3, u"נתיב האמת"],
	["Netiv Haemuna", 2, u"נתיב האמונה"],
	["Netiv Hashalom", 3, u"נתיב השלום"],
	["Netiv Ahavat Reia", 3, u"נתיב אהבת ריע"],
	["Netiv Haanava", 8, u"נתיב הענוה"],
	["Netiv Yirat Hashem", 6, u"נתיב יראת השם"],
	["Netiv Halashon", 11, u"נתיב הלשון"],
	["Netiv Ahavat Hashem", 2, u"נתיב אהבת השם"],
	["Netiv Hashtika", 1, u"נתיב השתיקה"],
	["Netiv Haprishut", 3, u"נתיב הפּרישות"],
	["Netiv Hatzniut", 4, u"נתיב הצניעות"],
	["Netiv Koach Hayeitzer", 4, u"נתיב כח היצר"],
	["Netiv Hatzedek", 3, u"נתיב הצדק"],
	["Netiv Hatshuva", 8, u"נתיב התשובה"],
	["Netiv Hayisurin", 3, u"נתיב היסורין"],
	["Netiv Hazrizut", 2, u"נתיב הזריזות"],
	["Netiv Hatochacha", 3, u"נתיב התוכחה"],
	["Netiv Habusha", 2, u"נתיב הבושה"],
	["Netiv Hatmimut", 2, u"נתיב התמימות"],
	["Netiv Lev Tov", 1, u"נתיב לב טוב"],
	["Netiv Ayin Tov", 1, u"נתיב עין טוב"],
	["Netiv Haleitzanut", 2, u"נתיב הליצנות"],
	["Netiv Haosher", 2, u"נתיב העושר"],
	["Netiv Habitachon", 1, u"נתיב הבטחון"],
	["Netiv Hakaas", 2, u"נתיב הכעס"],
	["Netiv Hanedivut", 1, u"נתיב הנדיבות"],
	["Netiv Sheim Tov", 1, u"נתיב שם טוב"],
	["Netiv Derech Eretz", 1, u"נתיב דרך ארץ"],
	]
	
	
for sub in subsections:
    n = JaggedArrayNode()
    n.key = sub[0]
    n.add_title(sub[0], "en", primary=True)
    n.add_title(sub[2], "he", primary=True)
    n.depth = 2
    n.lengths = [sub[1]]
    n.sectionNames = ["Chapter", "Paragraph"]
    n.addressTypes = ["Integer", "Integer"]
    root.append(n)


root.validate()

index = {
    "title": "Netivot Olam",
    "categories": ["Philosophy", "Maharal"],
    "schema": root.serialize()
}

post_index(index)
Index(index).save()
