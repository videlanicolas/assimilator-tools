import requests, logging, urllib3

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

class Rule():
	def __init__(self,firewall_type,**kvargs):
		if firewall_type not in ['paloalto','juniper']:
			self.firewall_type = firewall_type
		else:
			raise Exception("Unknown Firewall type.")
		self.rule = kvargs

class Firewall():
	def __init__(self,apikey,hostname='localhost',port=443,verify=False):
		self.hostname = hostname
		self.verify = verify
		self.port = port
		self.headers = {'Content-Type' : 'application/json', 'User-Agent' : 'Assimilator Tools', 'key' : apikey}
	def __get(self,firewall,resource):
		r = requests.get('https://{0}:{1}/api/{2}/{3}'.format(self.hostname,self.port,firewall,resource),headers=self.headers,verify=self.verify)
		if r.status_code == 200:
			return r.json()
		else:
			raise Exception("Error retrieving configuration: HTTP {0}\n{1}".format(str(r.status_code),r.text))
	def config(self,firewall):
		return self.__get(firewall,'config')
	def rules(self,firewall):
		return self.__get(firewall,'rules')
	def objects(self,firewall,object_type):
		return self.__get(firewall,'objects/' + object_type)
	def routes(self,firewall):
		return self.__get(firewall,'route')