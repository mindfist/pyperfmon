#!/usr/bin/python2.6

"""
pyperfmon : main module used to load DAPI server with
	* multiple users across multiple game/app
	* single or multiple api(s) having different mix ratio
	* different user concurrency
	* different user blob size

Response time and Request per sec (RPS) are also been calculated 

"""


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/libs")
import itertools
import time
import random
import numpy
import multiprocessing
import simplejson as json
from gh_api import *
from config import Config
from constants import Constants

Config = Config()
USER_NOS = int(Config.user_nos)


def dapi_auth(zid):
	""" return user zid, zlive app id  and zlive app secret """

        if (len(Config.zlive_auth) == 1):
		zlive_id = Config.zlive_auth[0]
        else:
		zlive_auth = tuple(Config.zlive_auth)
		zlive_id = (random.choice(zlive_auth))
        return zid, zlive_id[0], zlive_id[1]


def get_user_blob(ZidStatusList):
	""" load dapi with user blob get API """

	return gameStorage_userBlobGet(dapi_auth(ZidStatusList[0]),ZidStatusList[1])	


def set_user_blob(ZidStatusList):
	""" load dapi with user blob set API """

	return gameStorage_userBlobSet(dapi_auth(ZidStatusList[0]),ZidStatusList[1])


def mix_ratio(func_list,ratio_list):
	""" generate mix of get and set request based on define mix ratio """

        final_list = []
        unit = float(USER_NOS)/float(sum(ratio_list))
        last = USER_NOS - int((sum(ratio_list) - ratio_list[len(ratio_list)-1])*unit)

        for i in range(len(ratio_list)-1):                              
                final_list.extend([func_list[i]]*int(unit*ratio_list[i]))
        final_list.extend([func_list[len(ratio_list)-1]]*last)
        index_list = [i for i in range(USER_NOS)]                        
        random.shuffle(index_list)

        return [final_list[i] for i in index_list]


def mix_load(api_list):
	""" load dapi with mix load (Get aad Set) based on mix ratio """

	if api_list[0][1] == Constants.GH_USER_BLOB_GET:
		return gameStorage_userBlobGet(dapi_auth(api_list[0][0]), api_list[1])
	elif api_list[0][1] == Constants.GH_USER_BLOB_SET:
		return gameStorage_userBlobSet(dapi_auth(api_list[0][0]), api_list[1])
	else:
		print 'Undefined GH API'


def sum_of_avg(list,processes):
	""" calculate average response time per user concurrency per run """

        sum = 0
	leng = len(list)
        
	if (leng%processes != 0):
                sub_list = [[list[j] 
			for j in range(i*processes,min( (i+1)*processes,len(list) ) )] \
				for i in range(int(leng/processes) + 1)]
        else:
                sub_list = [[list[j] 
			for j in range(i*processes,min( (i+1)*processes,len(list) ) )] \
				for i in range(int(leng/processes))]

        for i in range(len(sub_list)):
                sum += numpy.mean(numpy.array(sub_list[i]))

        return sum,len(sub_list)


def multi_ops(func,list):
	"""
	multi_ops : spawning multiple processes based on user concurrency
	
	@params FunctionType  func : API function used to send request
	@params List	list: Userid list to used 

	return :average response time and average RPS
	"""
        
	response_time_list = multiprocessing.Manager().list() 
        proc_pool = multiprocessing.Pool(processes=int(Config.concurrency))
        
	print '\n Loading DAPI server ...'
        for i, _ in enumerate(proc_pool.imap_unordered(
			func,itertools.izip(list,itertools.repeat(response_time_list))),1):
                sys.stdout.write('\r {0}/{1} \t['.format(i, USER_NOS))
                sys.stdout.write('#'* int(100 * (float(i)/float(USER_NOS))))
                sys.stdout.write('] {0}%'.format(int(100 * (float(i)/float(USER_NOS)))))
                sys.stdout.flush
        sys.stdout.write('\n')
        sys.stdout.flush
        proc_pool.close()

        responseTime,stages = sum_of_avg(response_time_list,int(Config.concurrency))
        print '\n Average Response Time         : {0} Sec'.format(float(responseTime)/float(stages))
        print ' Average Request/Sec (RPS)       : {0} Nos\n'.format(float(USER_NOS)/float(responseTime))


def main():
	"""
	main : main function load dapi server by calling mulit_ops func 
		based on enable api type in config

	"""

	uid = range(Constants.DEFAULT_START_UID, (Constants.DEFAULT_START_UID + USER_NOS))
	
	if Config.enable_api == Constants.ENABLE_BLOB_GET:
		multi_ops(get_user_blob, uid)
	elif Config.enable_api == Constants.ENABLE_BLOB_SET:
		multi_ops(set_user_blob, uid)
	elif Config.enable_api == Constants.ENABLE_MIX_LOAD:
		api = mix_ratio([Constants.GH_USER_BLOB_GET,Constants.GH_USER_BLOB_SET],Config.mix_ratio)
		mix_list = []
		for key in uid:
			mix_list += [[uid[uid.index(key)], api[uid.index(key)]]]
		multi_ops(mix_load, mix_list)
	else:
		print 'API not define in multi-proc.conf'
	

if __name__ == '__main__':
	main()
