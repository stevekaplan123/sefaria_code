# -*- coding: utf-8 -*-

'''
introduction 1
introduction 2
introduction 3
chapter 1
chapter 2
chapter 3
...
chapter 72
Summary of the laws of pesach
Laws of yayin nesach
'''


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
		
IndexSet({"title": "New Zohar"}).delete()



root = SchemaNode()
root.add_title("Gevurot Hashem", "en", primary=True)
root.add_title(u"גבורות השם", "he", primary=True)
root.key = "gevurot"

part1 = JaggedArrayNode()
part1.add_title(u"הקדמה א", "he", primary=True)
part1.add_title("Introduction to Gevurot Hashem", "en", primary=True)
part1.depth = 1
part1.sectionNames = ["Paragraph"]
part1.addressTypes = ["Integer"]
part1.key = "intro 1"

part2 = JaggedArrayNode()
part2.add_title(u"הקדמה ב", "he", primary=True)
part2.add_title("Second Introduction to Gevurot Hashem", "en", primary=True)
part2.depth = 1
part2.sectionNames = ["Paragraph"]
part2.addressTypes = ["Integer"]
part2.key = "intro 2"

part3 = JaggedArrayNode()
part3.add_title(u"הקדמה ב", "he", primary=True)
part3.add_title("Third Introduction to Gevurot Hashem", "en", primary=True)
part3.depth = 1
part3.sectionNames = ["Paragraph"]
part3.addressTypes = ["Integer"]
part3.key = "intro 3"

part4 = JaggedArrayNode()
part4.depth = 2
part4.lengths = [72]
part4.sectionNames = ["Chapter", "Paragraph"]
part4.addressTypes = ["Integer", "Integer"]
part4.key = "default"
part4.default = True

part5 = JaggedArrayNode()
part5.add_title(u"הלכות פסח בקצרה", "he", primary=True)
part5.add_title("Summary of the Laws of Pesach", "en", primary=True)
part5.depth = 1
part5.sectionNames = ["Paragraph"]
part5.addressTypes = ["Integer"]
part5.key = "laws pesach"

part6 = JaggedArrayNode()
part6.add_title(u"הלכות יין נסך", "he", primary=True)
part6.add_title("Laws of Yayin Nesach", "en", primary=True)
part6.depth = 1
part6.sectionNames = ["Paragraph"]
part6.addressTypes = ["Integer"]
part6.key =  "laws yayin nesach"

root.append(part1)
root.append(part2)
root.append(part3)
root.append(part4)
root.append(part5)
root.append(part6)


root.validate()

index = {
    "title": "Gevurot Hashem",
    "categories": ["Philosophy", "Maharal"],
    "schema": root.serialize()
}

Index(index).save()
post_index(index)

