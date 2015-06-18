# -*- coding: utf-8 -*-

#TO DO
# Create hash of Hebrew parshiot to English parshiot


import pdb
import urllib
import urllib2
from urllib2 import URLError, HTTPError
import json
from sefaria.model.schema import AddressTalmud	


def post_text(ref, text):
    textJSON = json.dumps(text)
    ref = ref.replace(" ", "_")
    url = 'http://localhost:8000/api/texts/New_Zohar'
    values = {'json': textJSON, 'apikey': 'YourApiKey'}#'F4J2j3RF6fHWHLtmAtOTeZHE3MOIcsgvcgtYSwMzHtM'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(req)
        print response.read()
    except HTTPError, e:
        print 'Error code: ', e.code
        print e.read()


genesis_parshiot = ["Introduction", "Bereishit", "Noach", "Lech_lecha", "Vayera", "Chayei_Sarah", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi"]
exodus_parshiot = ["Exodus", "Vaera", "Bo", "Beshalach", "Haman", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki_Tisa", "Vayakhel", "Pekudei"]
leviticus_parshiot = ["Vayikra", "Tzav", "Shemini", "Tazria", "Metzora", "Acharei_Mot", "Kedoshim", "Emor", "Behar", "Bechukotai"]
numbers_parshiot = ["Bamidbar", "Naso", "Behalotcha", "Shelach", "Korach", "Chukat", "Balak", "Pinchas", "Matot"]
deut_parshiot = ["Devarim", "Vaetchanan", "Eikev", "Shoftim", "Ki_Teitzei", "Vayelech", "Haazinu", "Haadre_Zuta_Kadisha"]
english_parshiot = genesis_parshiot+exodus_parshiot+leviticus_parshiot+numbers_parshiot+deut_parshiot

curr_parsha = 0
curr_parsha_file = ""
prev_vol = 0
prev_daf = 0
prev_para = 0
zohar_struct = range(3)
for vol_num in range(3):
	para_count = 1	
	if vol_num == 0:
		daf_count = 1
		vol_file = 'intro'
		zohar_struct[vol_num] = []
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
	elif vol_num == 1:
		daf_count = 3
		vol_file = 'shemot'
		zohar_struct[vol_num] = []
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
	elif vol_num == 2:
		daf_count = 3
		vol_file = 'lnd'
		zohar_struct[vol_num] = []
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
		zohar_struct[vol_num].append([])
	first_line = True
	vol = open(vol_file, 'r')
	for line in vol:
		stray_tag = False
		blank_line = False
		if line == '\n' or (len(line)<4 and line.find('\n')>=0):
			blank_line = True
		if len(line.split(' '))==1 and (line.find('<b>')>=0 or line.find('</b>')>=0):
			stray_tag = True			
		if first_line == True:
			first_line = False
			if curr_parsha_file != "":
				curr_parsha_file.write('\n'+str(prev_vol+1)+":"+AddressTalmud.toStr("en", prev_daf)+":"+str(prev_para))
				curr_parsha_file.close()					
			curr_parsha_file = open(english_parshiot[curr_parsha], 'a')
			curr_parsha_file.write(str(vol_num+1)+":"+AddressTalmud.toStr("en", daf_count)+":1")  
			curr_parsha += 1
		elif blank_line==False and stray_tag==False:
			new_daf = line.find('דף')
			new_parsha = line.find('h1') #all parsha titles are surrounded by <h1> tags
			if new_daf >= 0 and len(line.split(' ')) < 6:  
				daf_count += 1
				zohar_struct[vol_num].append([])
				para_count = 1		
			elif new_parsha >= 0 and len(line.split(' ')) < 6:
				curr_parsha_file.write('\n'+str(vol_num+1)+":"+AddressTalmud.toStr("en", daf_count)+":"+str(para_count-1))
				curr_parsha_file.close()
				curr_parsha_file = open(english_parshiot[curr_parsha], 'a')
				curr_parsha_file.write(str(vol_num+1)+":"+AddressTalmud.toStr("en", daf_count)+":"+str(para_count))
				curr_parsha += 1					
			else:
				zohar_struct[vol_num][daf_count].append(line)
				para_count += 1		
	prev_para = para_count-1
	prev_vol = vol_num
	prev_daf = daf_count
	if vol_file=='lnd':
		curr_parsha_file.write('\n'+str(vol_num+1)+":"+AddressTalmud.toStr("en", daf_count)+":"+str(para_count))
		curr_parsha_file.close()

text = {
"versionTitle": "New Zohar",
"versionSource": "http://www.toratemetfreeware.com/online/d_root__106_kblh.html",
"language": "he",
"text": zohar_struct,
}
post_text("New Zohar", text)

		
'''
def inc_daf_count(curr_daf):
	amud = curr_daf[-1] #always 'a' or 'b'
	if amud=='b':
		return str(int(curr_daf[0:-1])+1)+'a'
	elif amud=='a':
		return curr_daf[0:-1]+'b'
'''

