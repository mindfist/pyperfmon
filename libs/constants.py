
class Constants(object):
	"""
	Constants multi-proc.cfg. Don't change CONFIG_FILE constant
	"""

	CONFIG_FILE		= "./config/multi-proc.cfg"
	DAPI_AUTH_CONFIG	= "dapi-auth"
	DAPI_CONFIG		= "dapi-config"
	DAPI_SERVER		= "dapi_server"
	USER_NOS		= "user_nos"
	USER_CONSS		= "concurrency"
	ZLIVE_APPS		= "zlive_apps"
	ENABLE_API		= "enable_api"
	ENABLE_BLOB_GET		= "userblobget"
	ENABLE_BLOB_SET		= "userblobset"
	ENABLE_MIX_LOAD		= "mixload"
	MIX_RATIO		= "mix_ratio"
	USER_BLOB_SIZE		= "user_blob_size"


	"""
	GH API Define
	"""
	GH_USER_BLOB_GET	= 0x01
	GH_USER_BLOB_SET	= 0x02
	

	"""
	DAPI API's Params
	"""
	DAPI_VERSION		= "v=1.2&p="
	DAPI_COMMAND		= "c"
	DAPI_MODULE		= "m"
	DAPI_MODULE_ARG		= "al"
	DAPI_REQUEST_TYPE	= "n"
	DAPI_TOKEN		= "t"
	DAPI_APPID		= "a"
	DAPI_NETWORK_ID		= "c"
	DAPI_APP_SECRET		= "as"
	
	GS_ZID			= "zid"
	GS_BLOBTYPE		= "blobType"
	GS_BLOBTYPES		= "blobTypes"
	GS_BLOB			= "game-world"
	GS_GETUSERBLOB		= "gameStorage.getUserBlobs"
	GS_SETUSERBLOB		= "gameStorage.setUserBlob"
	GS_CAS			= "checkAndSet"
	GS_USER_BLOB		= "blob"		
	
	"""
	Misc constants
	"""	
	DEFAULT_START_UID       = 10000
	
	
