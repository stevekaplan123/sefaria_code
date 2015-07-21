# -*- coding: utf-8 -*-

import urllib
import re
from bs4 import BeautifulSoup
import pdb
import os
import sys

if os.path.exists("tikkunei_zohar") == True:
	os.remove("tikkunei_zohar")	


parshiot = ["הקדמת תקוני הזהר", "הקדמה אחרת לתקוני הזהר", "תקונא קדמאה", "[ודא תקונא תניינא]",
"[תקונא תליתאה] תקונא תניינא", "ודא תקונא תליתאה כגוונא דא", "תקונא רביעאה", "תקונא חמישאה", 
"תקונא שתיתאה", "תקונא שביעאה", "תקונא תמינאה", "תקונא תשיעאה", "תקונא עשיראה", "תקונא חד סר",
"תקונא תריסר", "תקונא תליסר", "תקונא ארביסר", "תקונא חמיסר", "תקונא שיתסר", "תקונא שיבסר", "תקונא תמני סרי", 
"תקונא תשסרי", "תקונא עשרין, וחד ועשרין", "תקונא עשרין ותרין", "תקונא עשרין ותלת", "תקונא עשרין וארבע", 
"תקונא עשרין וחמשא", "תקונא עשרין ושית", "תקונא עשרין ותמניא", "תקונא עשרין ותשע", "תקונא תלתין",
"תקונא תלתין וחד", "תקונא תלתין ותרין", "תקונא תלתין ותלת", "תקונא תלתין וארבע", "תקונא תלתין וחמשא",
"תקונא תלתין ושתא", "תקונא שבע ותלתין", "תקונא תמניא ותלתין", "תקונא תשע ותלתין", "תקונא ארבעין",
"תקונא חד וארבעין", "תקונא ארבעין ותרין", "תקונא ארבעין ותלת", "תקונא ארבעין וארבע", "תקונא ארבעין וחמשא",
"תקונא שית וארבעין", "תקונא שבע וארבעין", "תקונא תמניא וארבעין", "תקונא תשע וארבעין", "תקונא חמשין", 
"תקונא חד וחמשין", "תקונא תרין וחמשין", "תקונא חמשין ותלת", "תקונא חמשין וארבע", "תקונא חמשין וחמש", "תקונא חמשין ושתא",
"תקונא שבע וחמשין", "תקונא תמניא וחמשין", "תקונא תשעה וחמשין", "תקונא שתין","תקונא חד ושתין", "תקונא שתין ותרין",
"תקונא שתין ותלת", "תקונא שתין וארבע", "תקונא שתין וחמש", "תקונא שתין ושתא", "תקונא שתין ושבע", "תקונא תמניא ושתין",
"תקונא שתין ותשעה", "תקונא שבעין", "= תקונא תניינא", "= תקונא תליתאה", "= תקונא רביעאה", "= תקונא חמישאה",
"= תקונא שתיתאה", "= תקונא שביעאה", "= תקונא תמינאה", "= תקונא תשיעאה", "= תקונא עשיראה", "= תקונא אחת עשרה"]
bereishit = 'http://www.toratemetfreeware.com/online/f_01153_part_'
for i in range(81):
	f=urllib.urlopen(bereishit+str(i+1)+'.html')
	soup_str = str(BeautifulSoup(f.read()))

	#remove stray </b> tag at the beginning
	curr_parsha = parshiot[i]
	soup_arr = soup_str.rsplit(curr_parsha)
	text_to_parse = '<h1>'+curr_parsha+'</h1><BR>'+soup_arr[4]
	text_to_parse = text_to_parse.replace('</b>', '', 1)
	
	#Delete bold underlined daf headers because they are inaccurate.
	bad_daf_title = "<u>"+"דף"
	bad_daf_title += ".*?</u>"
	all_bad_titles = re.findall(bad_daf_title, text_to_parse)
	for i in range(len(all_bad_titles)):
		text_to_parse = text_to_parse.replace(all_bad_titles[i], '')


	#Instead, we will use the daf titles that are in between parentheses
	good_daf_title = "\(" + "דף"
	good_daf_title += ".*?" + "ע"
	good_daf_title += ".*?" + "\)"
	all_good_titles = re.findall(good_daf_title, text_to_parse)
	for i in range(len(all_good_titles)):
		if len(all_good_titles[i]) <= 22:  #this is how long a daf title inside parentheses can be
			new_daf_header = "<p></p><p></p><b>"+all_good_titles[i]+"</b><p></p><p></p>"
			text_to_parse = text_to_parse.replace(all_good_titles[i], new_daf_header)

	#Delete strings and HTML elements we don't want in the final parsed text
	text_to_parse = text_to_parse.replace('<!--$~-->', '')
	text_to_parse = text_to_parse.replace('<!--$@-->', '')
	text_to_parse = text_to_parse.replace('<BR></U>', '')
	text_to_parse = text_to_parse.replace('<div>', '')
	text_to_parse = text_to_parse.replace('</div>', '')
	text_to_parse = text_to_parse.replace('<u>', '')
	text_to_parse = text_to_parse.replace('</u>', '')
	text_to_parse = text_to_parse.replace('</a>', '')
	text_to_parse = text_to_parse.replace('</span>', '')
	text_to_parse = text_to_parse.replace('<small>', '')
	text_to_parse = text_to_parse.replace('</small>', '')
	text_to_parse = text_to_parse.replace('<big>', '')
	text_to_parse = text_to_parse.replace('</big>', '')


	#remove <a ...> and <span ...> tags
	a_start = re.compile('<a.*?>')
	span_start = re.compile('<span.*?>')
	match = re.search(a_start, text_to_parse)
	while match:
		text_to_replace = match.group(0)
		text_to_parse = text_to_parse.replace(text_to_replace, '')
		match = re.search(a_start, text_to_parse)
	match = re.search(span_start, text_to_parse)
	while match:
		text_to_replace = match.group(0)
		text_to_parse = text_to_parse.replace(text_to_replace, '')
		match = re.search(span_start, text_to_parse)

	#separate paragraphs from each other and headers
	text_to_parse = text_to_parse.replace('<BR><BR><p></p>', '\n')
	text_to_parse = text_to_parse.replace('<BR><p></p>', '\n')
	text_to_parse = text_to_parse.replace('<p></p>', '\n')
	text_to_parse = text_to_parse.replace('<BR>', '\n')
	text_to_parse = text_to_parse.replace('<br/>', '')

	text_to_parse = text_to_parse.replace('</b>', '</b>\n\n')  #</BIG> tag is at the end of alternate headers 
											#such as ספר הבהיר or רַעֲיָא מְהֵימְנָא 
	text_to_parse = text_to_parse.replace('<b></b>', '')

	text_to_parse = text_to_parse.replace('<!--BODY_END-->', '')
	text_to_parse = text_to_parse.replace('<!--_LEND--> ', '')
	text_to_parse = text_to_parse.replace('</body></html>', '')

		
	f = open('tikkunei_zohar', 'a')
	f.write(text_to_parse)
	f.close()




