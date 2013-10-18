"""
genJson : module to generate sample user blob based on 'user_blob_size' 
	specified in config

"""
import simplejson as json
import random 


MAXSIZE = 128
KEY = 5

def generate(size):
	string = ""
	for i in range(size):
		string += chr(random.randrange(65,90,1))
	return string 

def jsonBlob(size):
	count = (size*1024)/MAXSIZE
	diction = {}

	for i in range(count):
		diction[generate(KEY)] = generate(MAXSIZE-8-KEY)
	
	return json.dumps(diction)

