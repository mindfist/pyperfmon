"""
gh_api : module to generate and send DAPI request payload for 
	* gameStorage.getUserBlob
	* gameStorage.setUserBlob

"""

import sys
import os
import string
import random
import time
import StringIO
import pycurl
import traceback
import select
from time import time as now
from config import Config
from constants import Constants
from multiprocessing import Pool
from genjson import *
import simplejson as json

Config = Config()
DAPI_URL = Config.dapi_server

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return False
	return ret

def dapi_data(payload):
	return Constants.DAPI_VERSION + json.dumps(payload, separators=(',',':'))

def curl_web_req(params, url=DAPI_URL):
	try :
		st = time.time()
		result = StringIO.StringIO()
		c = pycurl.Curl()
		c.setopt(pycurl.WRITEFUNCTION, result.write)
		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.CONNECTTIMEOUT, 180)
		c.setopt(pycurl.TIMEOUT, 180)
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, params)
		c.perform()
	
		ret = result.getvalue()
		ret = decode_post(ret)
		result.close()
		c.close()
		return ret,time.time()-st

	except:
		return 0,0
	
def gameStorage_userBlobSet(zuid,response_time_list):
	token = {}
        token[Constants.DAPI_APPID] = zuid[1]
        token[Constants.DAPI_REQUEST_TYPE] = 18
        token[Constants.DAPI_APP_SECRET] = zuid[2]

        param = {}
        param[Constants.GS_CAS] = ""
        param[Constants.GS_USER_BLOB] = jsonBlob(Config.user_blob_size)
        param[Constants.GS_BLOBTYPE] = Constants.GS_BLOB
        param[Constants.GS_ZID] = "{0}" .format(zuid[0])

        command = {}
        command[Constants.DAPI_MODULE] = Constants.GS_SETUSERBLOB
        command[Constants.DAPI_MODULE_ARG] = param
        command[Constants.DAPI_REQUEST_TYPE] = 7

        comm_list = []
        comm_list.append(command)

        payload = {}
        payload[Constants.DAPI_NETWORK_ID] = comm_list
        payload[Constants.DAPI_TOKEN] = token

        ret = curl_web_req(dapi_data(payload))
        response_time_list.append(ret[1])
        return ret[0]

def gameStorage_userBlobGet(zuid,response_time_list):
	token = {}
	token[Constants.DAPI_APPID] = zuid[1]
	token[Constants.DAPI_REQUEST_TYPE] = 18
	token[Constants.DAPI_APP_SECRET] = zuid[2]
	
	param = {}
	param[Constants.GS_BLOBTYPES] = Constants.GS_BLOB
	param[Constants.GS_ZID] = "{0}" .format(zuid[0])
	
	command = {}
	command[Constants.DAPI_MODULE] = Constants.GS_GETUSERBLOB
	command[Constants.DAPI_MODULE_ARG] = param
	command[Constants.DAPI_REQUEST_TYPE] = 7

	comm_list = []
	comm_list.append(command)

	payload = {}
	payload[Constants.DAPI_COMMAND] = comm_list
	payload[Constants.DAPI_TOKEN] = token

	ret = curl_web_req(dapi_data(payload))
	response_time_list.append(ret[1])
	return ret[0]
