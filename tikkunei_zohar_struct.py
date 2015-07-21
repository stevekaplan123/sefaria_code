# -*- coding: utf-8 -*-
import os
import sys
import pdb
import json
import urllib
import urllib2
from urllib2 import URLError, HTTPError

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, p)
os.environ['DJANGO_SETTINGS_MODULE'] = "sefaria.settings"

from local_settings import *
sys.path.insert(0, SEFARIA_PROJECT_PATH)

from sefaria.model.schema import AddressTalmud	

def post_text(ref, text):
    textJSON = json.dumps(text)
    ref = ref.replace(" ", "_")
    url = SEFARIA_SERVER + '/api/texts/'+ref
    values = {'json': textJSON, 'apikey': API_KEY}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(req)
        print response.read()
    except HTTPError, e:
        print 'Error code: ', e.code
        print e.read()


genesis_parshiot = ["Introduction", "Bereshit", "Noach", "Lech Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi"]
exodus_parshiot = ["Shemot", "Vaera", "Bo", "Beshalach", "Haman", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei"]
leviticus_parshiot = ["Vayikra", "Tzav", "Shmini", "Tazria", "Metzora", "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai"]
numbers_parshiot = ["Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach", "Chukat", "Balak", "Pinchas", "Matot"]
deut_parshiot = ["Devarim", "Vaetchanan", "Eikev", "Shoftim", "Ki Teitzei", "Vayeilech", "Ha'Azinu", "Ha_Idra"]
english_parshiot = genesis_parshiot+exodus_parshiot+leviticus_parshiot+numbers_parshiot+deut_parshiot

curr_parsha = 0
ranges = ""
prev_vol = 0
prev_daf = -1
prev_para = 0
current_line = "not header"
prev_line = "not header"
prev_prev_line = "not header"
para_count = 1	
daf_count = -1
zohar_struct = []
first_line = True
vol = open("tikkunei_zohar", 'r')
for line in vol:
	stray_tag = False
	blank_line = False
	no_spaces = line.replace(" ", "")
	no_return = no_spaces.replace("\n", "")
	if len(no_return)==0:
		blank_line = True
	if len(line.split(' '))==1 and (line.find('<b>')>=0 or line.find('</b>')>=0):
		stray_tag = True			
	if first_line == True:
		first_line = False	
		if os.path.exists("ranges") == True:
			os.remove("ranges")		
		ranges = open("ranges", 'a')
		ranges.write(AddressTalmud.toStr("en", daf_count+2)+":1")  
		curr_parsha += 1
	elif blank_line==False and stray_tag==False:
		prev_prev_line = prev_line
		prev_line = current_line
		new_daf = line.find('דף')
		new_parsha = line.find('h1') #all parsha titles are surrounded by <h1> tags
		if new_daf >= 0 and len(line.split(' ')) < 6:  
			current_line = "daf"
			daf_count += 1
			zohar_struct.append([])
			prev_para = para_count
			para_count = 1
		elif new_parsha >= 0 and len(line.split(' ')) < 6:
			current_line = "parsha"
			if para_count==1:
				ranges.write('\n'+AddressTalmud.toStr("en", daf_count)+":"+str(prev_para-1))
			else:
				ranges.write('\n'+AddressTalmud.toStr("en", daf_count+1)+":"+str(para_count-1))	
			curr_parsha += 1					
		else:
			current_line = "neither"
			zohar_struct[daf_count].append(line)
			para_count += 1
		if current_line == "daf" and prev_line == "parsha": #typical case: parsha, daf
			ranges.write('\n'+AddressTalmud.toStr("en", daf_count+1)+":1")
		elif current_line=="parsha" and prev_line == "daf": #Chayei Sara case: daf, parsha
			ranges.write('\n'+AddressTalmud.toStr("en", daf_count+1)+":1")
		elif current_line == "neither" and prev_line == "parsha" and prev_prev_line == "neither": #Lech Lecha case: new parsha in middle of page
			ranges.write('\n'+AddressTalmud.toStr("en", daf_count+1)+":"+str(para_count-1))

				
	prev_para = para_count-1
	prev_daf = daf_count
	
ranges.write('\n'+AddressTalmud.toStr("en", daf_count+1)+":"+str(para_count-1))
ranges.close()



text = {
"versionTitle": "Zohar",
"versionSource": "http://www.toratemetfreeware.com/online/d_root__106_kblh.html",
"language": "he",
"text": zohar_struct,
}
post_text("Tikkunei Zohar", text)
