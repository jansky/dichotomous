#!/usr/bin/python3

"""
The MIT License (MIT)

Copyright (c) 2015 Ian Duncan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys

def DCParseKeyFile(keyfilename):

	keyfile = ""
	linenum = 1
	
	rules = []
	
	with open(keyfilename, encoding='utf-8') as f:
	
		keyfile = f.read()
	
	rules_raw = keyfile.split("%%")
	
	for rule_raw in rules_raw:
	
		conditions_raw = rule_raw.splitlines()
		
		rule = []
		
		for condition_raw in conditions_raw:
	
			if condition_raw.strip() == "" or condition_raw.startswith(';'):
				# Comment or empty line
				pass
			else:
			
				condition_array = condition_raw.split(':')
				
				if len(condition_array) < 3:
					print("Error: " + keyfilename + ":" + str(linenum) + " A condition statement requires three parts.")
					sys.exit(1)
				else:
					condition = {}
					
					if condition_array[0].startswith('!'):
						condition["negative"] = True
						condition_array[0] = condition_array[0][1:]
					else:
						condition["negative"] = False
					
					condition["condition"] = condition_array[0]
					
					if condition_array[1] == "goto":
					
						condition["action"] = "goto"
						
						try:
							condition["data"] = int(condition_array[2])
						except ValueError:
							print("Error: " + keyfilename + ":" + str(linenum) + " Goto action requires integer argument.")
							sys.exit(1)
					elif condition_array[1] == "result":
					
						condition["action"] = "result"
						condition["data"] = condition_array[2]
					else:
						print(keyfilename + ":" + str(linenum) + " Action not recognized.")
						sys.exit(1)
				
					rule.append(condition)
			linenum += 1
					
		rules.append(rule)
		
	return rules

def DCParseObjectFile(objectfilename):

	objectfile = ""
	linenum = 1
	
	objects = []
	
	with open(objectfilename,encoding='utf-8') as f:
	
		objectfile = f.read()
	
	objects_raw = objectfile.split("%%")
	
	for object_raw in objects_raw:
	
		conditions_raw = object_raw.splitlines()
		
		obj = {}
		nameFound = False
		conditions = []
		
		for condition_raw in conditions_raw:
		
			if condition_raw.strip() == "" or condition_raw.startswith(';'):
				#Comment
				pass
			else:
				if nameFound == False:
					obj["name"] = condition_raw
					nameFound = True
				else:
					if condition_raw.startswith('!'):
						#Negative
						pass
					else:
						conditions.append(condition_raw)
			linenum += 1
		
		if nameFound == False:
			print("Error: " + objectfilename + ":" + str(linenum) + " A name is required for an object.")
			sys.exit(1)
		
		obj["conditions"] = conditions
		
		objects.append(obj)
	
	return objects

def DCCheckRule(rules, obj, rulenum):

	rule = rules[rulenum - 1]
	
	for condition in rule:
	
		if condition["condition"] == "*" and condition["negative"] == False:
			return {'data':condition['data'], 'action':condition['action']}
	
		elif condition["negative"] == True and condition["condition"] not in obj["conditions"]:
			return {'data':condition['data'], 'action':condition['action']}
		
		elif condition["negative"] == False and condition["condition"] in obj["conditions"]:
			return {'data':condition['data'], 'action':condition['action']}
	
	#No result found, so indeterminate
	
	return {'data':'indet','action':'result'}

def DCIterateObjectsRules(rules, objects):

	results = []
	
	for obj in objects:
	
		rulenum = 1
		resultFound = False
		
		while resultFound == False:
		
			result = DCCheckRule(rules, obj, rulenum)
			
			if result['action'] == "result":
			
				resultFound = True
				results.append({'object':obj['name'],'classification':result['data']})
			
			elif result['action'] == "goto":
			
				if result['data'] > len(rules):
					print("Error: " + "Cannot goto rule '" + str(result['data']) + "', as it does not exist.")
					sys.exit(1)
				else:
					if result['data'] == rulenum:
						#Infinite loop detected
						print("Error: Infinite loop detected. Goto rule '" + str(result['data']) + "' from rule '" + str(rulenum) + "'.")
						sys.exit(1)
					else:
						rulenum = result['data']
			else:
				print("Action '" + result['action'] + "' does not exist.")
				sys.exit(2)
	
	return results

def DCPrintResults(results):

	counter = 1
	
	for result in results:
	
		if result['classification'] == "indet":
			print(str(counter) + ". " + result['object'] + ": Indeterminate")
		else:
			print(str(counter) + ". " + result['object'] + ": " + result['classification'])
		counter += 1
		
def DCPrintHelpMessage():

	print("Dichotomous Interpreter")
	print()
	print("By Ian Duncan")
	print("Version 1")
	print("Licensed under the MIT License")
	print()
	print("Usage: " + sys.argv[0] + " dichotomous_key_file.dck dichotomous_object_file.dco - Runs the interpreter")
	print("Usage: " + sys.argv[0] + " -h - Displays this help message")
	print()
	print("THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")


if(len(sys.argv) < 3):
	DCPrintHelpMessage()
else:
	
	DCPrintResults(DCIterateObjectsRules(DCParseKeyFile(sys.argv[1]),DCParseObjectFile(sys.argv[2])))


		
	
	
	
					
						
					
		
			
	
		
						
						
					
		
			
			
