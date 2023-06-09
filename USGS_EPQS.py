import requests
from aiohttp import ClientSession

from support.LogChannels import log
from support.GTimer import gtimer

log.addChannel("epqs", "epqs")
log.setChannel("epqs", False)

#  --------------------------------------------------------------------------------------------------------
# methods to query United States Geological Survey Elevation Point Query Service 
#  --------------------------------------------------------------------------------------------------------
class USGS_EPQS:
	def __init__(self):
		pass

	#  -----------------------------------------------------------------
	@staticmethod
	def query_url(lat_long_arr):
		return f"https://epqs.nationalmap.gov/v1/json?x={lat_long_arr[1]}&y={lat_long_arr[0]}&wkid=4326&units=Feet&includeDate=false"

	#  -----------------------------------------------------------------
	# gets height of point in lat,long from USGS point query service
	# for some reason the api uses x,y insead of long,lat
	# expects length 2 array: lat_long_arr = [lat,long]
	@staticmethod
	def getHeight(lat_long_arr:list):
		gtimer.startTimer("epqsSerial")
		api_url = USGS_EPQS.query_url(lat_long_arr)
		api_response = requests.get(api_url)
		response_json = api_response.json()
		gtimer.markTimer("epqsSerial", "EPQSgetHeightSerial")
		return response_json["value"]

	# --------------------------------------------------------------------
	# get height function that speaks acyncio
	@staticmethod
	async def getHeightAsync(lat_long_arr:list, session:ClientSession):
		timer_name = f"epqs_{lat_long_arr}"
		gtimer.startTimer(timer_name)

		epqs_url = USGS_EPQS.query_url(lat_long_arr)
		resp = await session.request(method="GET", url=epqs_url)
		resp.raise_for_status()
		json_resp = await resp.json()

		log.epqs(f"for {lat_long_arr} returning {json_resp['value']}")

		gtimer.markTimer(timer_name, "eqpsgetHeightAsync")
		return json_resp["value"]

