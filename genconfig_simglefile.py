#!/usr/bin/env python
#coding=utf-8

import json
import sys
import re
import os
config = {}
General = {}
Proxy = {}
Rule = {}
DOMAINKEYWORD = {}
DOMAINSUFFIX = {}
IPCIDR = {}
Hosts = {}
Agent = {}
GEOIP = {}
def convert(file):
	dict = {}
	i = 0 
	for line in file:
		i = i+ 1
		print ++i
		if re.match('#', line):
			print "# and pass"
			continue
		if re.match('//', line):
			print "// and pass"
			continue
		if len(line) <=2:
			print "no need" + line
			continue
		
		if re.match('\[General\]', line):
			print "Found General"
			dict = General
			continue
		elif re.match('\[Hosts\]', line):
			print "Found Hosts"
			dict = Hosts
			continue
		elif re.match('\[Proxy\]', line):
			print "Found Proxy"
			dict = Proxy
			continue
		elif re.match('\[Rule\]', line):
			dict = Rule
			print "Found Proxy"
			continue
		else :
			 #print "Not found block this is rule" + 
			 pass
		#print line
		list  = line.split('=')
		if len(list) >1:
			print list
			x = list[1].split(',')
			if  len(x)> 1:
				if dict ==  Proxy:
					hostconfig = {}
					hostconfig['protocol'] =  x[0].strip()
					hostconfig['host'] =  x[1].strip()
					hostconfig['port'] =  x[2].strip()
					hostconfig['method'] =  x[3].strip()
					hostconfig['passwd'] =  x[4].strip()
					#hostconfig['xx'] =  x[5]
					dict[list[0].strip()] = hostconfig
				else:
					print line
					dict[list[0].strip()] =  [str(j).strip() for j in x]
			else:
				dict[list[0].strip()] = str(list[1]).strip()
			
		else:
			if re.match('DOMAIN-KEYWORD',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()
				if len(k) > 3:
					rule["force-remote-dns"] = k[3].strip()
				# try:
				# 	rule["force-remote-dns"] = k[3].strip()
				# except Exception, e:
				# 	print e
				
				DOMAINKEYWORD[k[1].strip()] = rule 
			elif re.match('DOMAIN-SUFFIX',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()
				if len(k) > 3:
					rule["force-remote-dns"] = k[3].strip()
				# try:
				# 	rule["force-remote-dns"] = k[3].strip()
				# except Exception, e:
				# 	print e
				
				DOMAINSUFFIX[k[1].strip()] = rule
			elif re.match('DOMAIN',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()
				if len(k) > 3:
					rule["force-remote-dns"] = k[3].strip()
				# try:
				# 	rule["force-remote-dns"] = k[3].strip()
				# except Exception, e:
				# 	print e
				
				DOMAINSUFFIX[k[1].strip()] = rule
			elif re.match('IP-CIDR',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()
				if len(k) > 3:
					rule["no-resolve"] = k[3].strip()
				# try:
				# 	rule["no-resolve"] = k[3].strip()
				# except Exception, e:
				# 	print e
				
				IPCIDR[k[1].strip()] = rule
			elif re.match('USER-AGENT',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()				
				Agent[k[1].strip()] = rule
			elif re.match('GEOIP',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				rule = {}
				rule["Proxy"] = k[2].strip()				
				GEOIP[k[1]] = rule
			elif re.match('FINAL',line):
				k  = line.split(',')
				#k.remove(k[0])
				#r = ', '.join([str(x) for x in k]) 
				#rule = {}
				#rule["Proxy"] = k[2].strip()				
				#GEOIP[k[1]] = rule
				Rule["FINAL"] = k[1].strip()
			else:
				#this section shoud Hosts
				k  = line.split(' ')
				if len(k) > 1:
					ip = k[0]
					for index in range(1,len(k)):
						host = k[index]
						Hosts[host] = ip.strip()
				else:
					print "host format error"	
	#print dict
	print "[General]"
	print General
	General["author"] = "surfing"
	General["commnet"] = "this is comment"
	print "[Proxy]"
	print Proxy
	print "[Rule]"
	Rule["DOMAIN-KEYWORD"] = DOMAINKEYWORD
	Rule["DOMAIN-SUFFIX"] = DOMAINSUFFIX
	Rule["IP-CIDR"] = IPCIDR
	Rule["USER-AGENT"] = Agent
	Rule["GEOIP"] = GEOIP
	#print Rule
	print "cool"

	config["Hosts"] = Hosts
	config["Rule"] = Rule
	config["Proxy"] = Proxy
	config["General"] = General
	
	
	
	#saveRuslt()
	# print "[DOMAINKEYWORD]"
	# print DOMAINKEYWORD
	# print "[DOMAINSUFFIX]"
	# print DOMAINSUFFIX
	# print "[IPCIDR]"
	# print IPCIDR
def saveRuslt(name):
	#print config
	s = json.dumps(config)
	f = open(name,"w")
	f.write(s)
	f.close()
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "add surge config file path"
		exit()
	surgeconfig = sys.argv[1]
	print surgeconfig
	#paths = os.path.split(surgeconfig)
	fname = os.path.basename(surgeconfig)
	name = fname.split('.')[0]
	dest = os.path.dirname(surgeconfig) + name + '.json'
	file = open(surgeconfig)
	convert(file)
	saveRuslt(dest)
	file.close() 
