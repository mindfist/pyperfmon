"""
Config : module to parser config file
	 refer multi-proc.cfg for more detail 
"""

import re
import sys
import ConfigParser
from constants import Constants

class Config(object):
	def __init__(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(Constants.CONFIG_FILE)
			self.dapi_server = config.get(Constants.DAPI_CONFIG, Constants.DAPI_SERVER)
			self.user_nos = config.get(Constants.DAPI_CONFIG, Constants.USER_NOS)
			self.concurrency = config.get(Constants.DAPI_CONFIG, Constants.USER_CONSS)
			self.zlive_apps = config.get(Constants.DAPI_CONFIG, Constants.ZLIVE_APPS)
			self.enable_api = config.get(Constants.DAPI_CONFIG, Constants.ENABLE_API)
			self.mix_ratio = map(int,re.split(':',config.get(Constants.DAPI_CONFIG, Constants.MIX_RATIO)))
			self.user_blob_size = int(config.get(Constants.DAPI_CONFIG, Constants.USER_BLOB_SIZE))
		
			self.zlive = config.items(Constants.DAPI_AUTH_CONFIG)
			self.zlive_auth = []		
			if int(self.zlive_apps) < len(self.zlive):  
				for key, value in self.zlive[:int(self.zlive_apps)]:
					self.zlive_auth.append(re.split(', ',value))
			else:
				print 'Enable app(s) are more than define, check config'
		
		except Exception, e:
			print 'Error while reading config {0} - {1}'.format(Constants.CONFIG_FILE, e)

