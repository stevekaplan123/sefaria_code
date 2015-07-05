# -*- coding: utf8 -*-

import re
import sys
import os
from fuzzywuzzy import fuzz
from sefaria.model import *
#import helperFunctions as Helper
#import hebrew
import json
import urllib
import urllib2
import pdb

found_dict = {}
confirmed_dict = {}
gematria = {}
gematria['א'] = 1
gematria['ב'] = 2
gematria['ג'] = 3
gematria['ד'] = 4
gematria['ה'] = 5
gematria['ו'] = 6
gematria['ז'] = 7
gematria['ח'] = 8
gematria['ט'] = 9
gematria['י'] = 10
gematria['כ'] = 20
gematria['ל'] = 30
gematria['מ'] = 40
gematria['נ'] = 50
gematria['ס'] = 60
gematria['ע'] = 70
gematria['פ'] = 80
gematria['צ'] = 90
gematria['ק'] = 100
gematria['ר'] = 200
gematria['ש'] = 300
gematria['ת'] = 400

acronyms = {}
f = open('spellings.txt', 'r')
count = 0
RT = ""
for line in f:
	count+=1
	line = line.replace("\n", "")
	if count == 1:
		if not line in acronyms.keys():
			acronyms[line] = []
		RT = line
	elif count == 2:
		acronyms[RT].append(line)
	elif count == 3:
		count=0
f.close()

count = 0
too_match = 0
matched = 0
non_match = 0
total=0
step = 5
min_ratio = 82
list_of_many_finds={}
links_list = []
found_list =[]
too_many_file = open('too_many', 'w')
no_match_file = open('no_match', 'w')

	

def gematriaFromSiman(line):
	txt = line.split(" ")[1]
	index=0
	sum=0
	while index <= len(txt)-1:
		if txt[index:index+2] in gematria:
			sum += gematria[txt[index:index+2]]
		index+=1
	return sum


def get_text(ref):
    ref = ref.replace(" ", "_")
    url = 'http://www.sefaria.org/api/texts/'+ref
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        data = json.load(response)
        return data['he']
    except:
        print 'Error'
        
def splitInHalf(txt):
	halfway = len(txt)/2
	return txt[0:halfway], txt[halfway:]
	
def replaceAcronyms(dh):
	dh_list = []
	duplicates = False
	for acronym in acronyms:
		if acronym.decode('utf-8') in dh:
			for expansion in acronyms[acronym]:
				new_dh = dh.replace(acronym.decode('utf-8'), expansion.decode('utf-8'))
				if new_dh.find('"')>=0 or new_dh.find("'")>=0:
					temp_dh_list = replaceAcronyms(new_dh)
					for i in range(len(temp_dh_list)):
						dh_list.append(temp_dh_list[i])
					return dh_list
				else:
					dh_list.append(new_dh)
	return dh_list
'''
	temp_list = dh_list
	dh_list = []
	if duplicates==True:
		for i in range(len(temp_list)):
			if i==0:
				dh_list.append(temp_list[i])
			else:
				for j in range(len(dh_list)):
					if j != i and dh_list[j] == temp_list[i]:
'''								

def match(orig_dh,sa_siman,siman_num,dh_position,ratio=87):
	global total
	global too_match
	global non_match
	global matched
	global found_dict
	partial_ratios = []	
	found_dict[siman_num][dh_position] = {}
	found_dict[siman_num][dh_position][orig_dh] = []
	dh = orig_dh.decode('utf-8')
	etc = " כו'"
	etc = etc.decode('utf-8')
	etc_plus_and = " וכו'"
	etc_plus_and = etc_plus_and.decode('utf-8')
	etc_short = "כו "
	etc_short = etc_short.decode('utf-8')
	if dh.find(etc_plus_and) >= 0:
		dh = dh.replace(etc_plus_and, "")
	elif dh.find(etc) >= 0:
		dh = dh.replace(etc, "")
	elif dh.find(etc_short) >= 0:
		dh = dh.replace(etc_short, "")
	found = 0
	dh_list = []
	if dh.find('"') >= 0 or dh.find("'")>=0:
		dh_list = replaceAcronyms(dh)
	#if orig_dh.find("הראשונ'")>=0:
	#	pdb.set_trace()
	for line_n, para in enumerate(sa_siman):
	  lines = para.split(".")
	  for line in lines:
		partial_ratios.append(fuzz.partial_ratio(dh, line))
		if dh in line or fuzz.partial_ratio(dh, line) >= ratio or fuzz.partial_ratio(line, dh) >= ratio:
			found += 1
			found_dict[siman_num][dh_position][orig_dh].append(line_n)
		for found_dh in dh_list:  #only happens if there is an acronym, found_dh refers to expanded acronym
			if found_dh in line or fuzz.partial_ratio(found_dh, line)>=ratio or fuzz.partial_ratio(line, found_dh) >= ratio:
				found += 1
				found_dict[siman_num][dh_position][orig_dh].append(line_n)
		if dh.find("'") >= 0 and len(dh) > 3: #just remove the apostrophe and re-check, unless it's a single character
			dh_without = dh.replace("'", "")
			if dh_without in line or fuzz.partial_ratio(dh_without, line) >= ratio:
				found+=1
				found_dict[siman_num][dh_position][orig_dh].append(line_n)
	if found > 1:
		too_match+=1
		total += 1
	if found == 0:
		if ratio > min_ratio:
			match(orig_dh, sa_siman, siman_num, dh_position, ratio-step)
		else: 
			non_match += 1
			total += 1
			#if dh.find('"') >= 0:
			no_match_file.write(str(siman_num))
			no_match_file.write(", ")		
			no_match_file.write(orig_dh)
			no_match_file.write(", ")
			for pr in partial_ratios:
				no_match_file.write(str(pr))
				no_match_file.write(", ")
			no_match_file.write("\n")
	if found == 1:
		matched += 1
		total += 1

def removeExtras(siman_num):
	global found_dict
	global confirmed_dict
	global dh_dict
	confirmed_dict[siman_num] = {}
	for dh_pos in found_dict[siman_num]:
		dh = dh_dict[siman_num][dh_pos]
		confirmed_dict[siman_num][dh_pos] = {}
		dh_found_list = found_dict[siman_num][dh_pos][dh] 
		if len(dh_found_list) == 1:
			confirmed_dict[siman_num][dh_pos][dh] = dh_found_list[0]
		elif len(dh_found_list) > 1:
			dh_list = dh_dict[siman_num]
			temp = dh_pos-1
			min = 0
			while temp >= 0:
				if len(found_dict[siman_num][temp][dh_list[temp]]) >= 1:
					#try:
					  min = confirmed_dict[siman_num][temp][dh_list[temp]]
					  break
					#except:
					#  pdb.set_trace() 
				temp -= 1
			temp = dh_pos+1
			max = len(dh_list)-1
			while temp <= max:
				temp_list = found_dict[siman_num][temp][dh_list[temp]]
				if len(temp_list) == 1:
					max = temp_list[0]
					break
				temp+=1
			list_actual_lines = []
			for line_n in dh_found_list:
				if line_n >= min and line_n <= max:
					list_actual_lines.append(line_n)
			if len(list_actual_lines) == 0:
				if dh_pos > 0 :
				 	confirmed_dict[siman_num][dh_pos][dh] = confirmed_dict[siman_num][dh_pos-1][dh_list[dh_pos-1]]	
				else:
					confirmed_dict[siman_num][dh_pos][dh] = 0
			elif len(list_actual_lines) == 1:
				global picking_well
				picking_well +=1
				confirmed_dict[siman_num][dh_pos][dh] = list_actual_lines[0]
			elif len(list_actual_lines) > 1: #currently picking the first one, but we don't know which is the right one
				global picking_random
				guesses = open("guesses", "a")
				guesses.write(str(siman_num))
				guesses.write(" : ")
				guesses.write(dh)
				already_guessed = []
				for poss_line in list_actual_lines:
					guesses.write(", ")
					if not poss_line in already_guessed:
						guesses.write(str(poss_line))
						already_guessed.append(poss_line)
				guesses.write("\n")
				guesses.close()
				picking_random+=1
				confirmed_dict[siman_num][dh_pos][dh] = list_actual_lines[0]


picking_random=0
picking_well = 0
dh_dict = {} #key is siman number, value is list of dh's for that siman
dh_file = open('magen_dh', 'r')
curr_siman = 0
for line in dh_file:
	no_spaces = line.replace(" ", "")
	no_return = no_spaces.replace("\n", "") #empty if blank line
	if line.find('סימן') >= 0:
		curr_siman = gematriaFromSiman(line)
		dh_dict[curr_siman] = []
	elif len(no_return) > 0:
		line = line.replace("\n", "")
		dh_dict[curr_siman].append(line)
dh_file.close()
magen_avraham = {}
shulchan_aruch = {}
for j in range(150):
	i = 400 + j
	found_dict[i+1] = {}
	magen_avraham[str(i+1)] = get_text("Magen Avraham "+str(i+1))
	shulchan_aruch[str(i+1)] = get_text("Shulchan Arukh, Orach Chayyim "+str(i+1))
	try:
 	  if len(magen_avraham[str(i+1)]) > 0: #Magen doesn't skip this siman
		dh_list = dh_dict[i+1]
		for j in range(len(dh_list)):
			match(dh_list[j], shulchan_aruch[str(i+1)], (i+1), j)
	except:
	  pdb.set_trace()
	  
for j in range(150):
	i = 400 + j
	removeExtras(i+1)

print str(total) + " = Total"
print str(non_match) + " = Non-matches"
print str(too_match) + " = More than one"
print str(matched) + " = Matches"

too_many_file.close()
no_match_file.close()
print picking_well
print picking_random

#match first goes through each line comparing it with dh
#adding each match by line number to list_of_found_links 
#for each line that matches dh, increment 'found' counter
#add condition to match ifs:
#check if this is an acronym with a ", 
#if it is, for loop through acronyms checking if acronym is inside 'dh', 
#new_dh = dh.replace(acronym, expansion)
#if it is, check if new_dh in line, and check if fuzz.partial_ratio(line, new_dh)
#after loop, check if found > 1, ==1, ==0
#if found > 1: set more_than_one to true and all lines to dict
#if found == 1: set more_than_one to false, consider it a match
#if found == 0:
#try again with lower ratio
#error_log=open('error_log', 'w')
	
'''double dict function:
dh_dict is dictionary where keys are siman numbers and value is an in order list of dh's in that siman
therefore:
match should create data structure, found_dict, where each siman number maps to dictionary where
keys are tuples of dh_position (position in dh_dict[siman_num] array)
and matched (found>=1) dh's and where the value is a list of line numbers

confirmed_dict  = {}
for each tuple of (dh_pos, dh) in found_dict whose list's length == 1
	simply set confirmed_dict[siman_num][(dh_pos, dh)] = line_num
for each tuple of (dh_pos, dh) in found_dict whose list's length is > 1 where siman_num is current siman number:
	find maximum and minimum line numbers for this dh 
		do this by setting i to dh_pos
		starting at i-1, counting down to 1, we look for the first dh = dh_dict[siman_num][i]
		such that confirmed_dict[siman_num][(i, dh)]'s length is 1 or we just use line 1
		we then set confirmed_dict[siman_num][(i, dh)] to line_n
		 (???? what if previous dh is 0?  ignore it)
		starting at i+1, counting until highest line, we look for the first dh_dict[siman_num][i]
		such that it's found == 1, or we just use highest line
	
	once we find max and min, we go through each dh, only adding them to our final_list
	if the line they occur on is <=max and >=min
	
	if there are still multiples left over, pick the first or middle one
		
'''