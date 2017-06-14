#!/usr/bin/python
import argparse, os, pipes, urllib3
from modules import general,firewall

urllib3.disable_warnings()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='Assimilator Tools',description='Assimilator tools for Assimilator API.\nhttps://github.com/videlanicolas/assimilator')
	parser.add_argument('-v','--version', action='version', version='%(prog)s - Version: 1.0.0')
	generalNamed = parser.add_argument_group('General commands')
	generalNamed.add_argument('-f','--firewall', required=True, help='firewall name as configured in Assimilator')
	generalNamed.add_argument('-p','--port', required=False, default='443', type=str, help='Assimilator\'s listening port')
	generalNamed.add_argument('-c','--config', required=False, action='store_true', default=False , help='get firewall\'s configuration')
	ruleNamed = parser.add_argument_group('Rules commands')
	ruleNamed.add_argument('-r','--rules', required=False, action='store_true', default=False, help='get firewall\'s rules')
	ruleNamed.add_argument('--source-zone', required=False, action='store_true', default=False, help='filter by source zone, requires --rules')
	ruleNamed.add_argument('--destination-zone', required=False, action='store_true', default=False, help='filter by destination zone, requires --rules')
	objectnamed = parser.add_argument_group('Objects commands')
	objectnamed.add_argument('-o','--objects', required=False, action='store_true', default=False , help='get firewall\'s objects')
	objectnamed.add_argument('--address', required=False, action='store_true', default=False, help='get only object addresses, requires --objects')
	objectnamed.add_argument('--address-group', required=False, action='store_true', default=False, help='get only object address-groups, requires --objects')
	objectnamed.add_argument('--service-group', required=False, action='store_true', default=False, help='get only object service-groups, requires --objects')
	objectnamed.add_argument('--service', required=False, action='store_true', default=False, help='get only object services, requires --objects')
	routenamed = parser.add_argument_group('Route commands')
	routenamed.add_argument('-t','--routes', required=False, action='store_true', default=False , help='get firewall\'s routes')
	routenamed.add_argument('--ip', required=False, default=None , help='get this IP through the route table, requires --routes')
	args = parser.parse_args()
	#Check Environment variables
	if 'ASSIMILATOR_HOSTNAME' not in os.environ or 'ASSIMILATOR_APIKEY' not in os.environ:
		print "You must specify Assimilator's hostname and apikey, this information will be stored in environment variables named ASSIMILATOR_HOSTNAME and ASSIMILATOR_APIKEY."
		os.environ['ASSIMILATOR_HOSTNAME'] = raw_input("ASSIMILATOR_HOSTNAME: ")
		os.environ['ASSIMILATOR_APIKEY'] = raw_input("ASSIMILATOR_APIKEY: ")

	print "Loading firewall ..."
	fw = firewall.Firewall(os.environ['ASSIMILATOR_APIKEY'],os.environ['ASSIMILATOR_HOSTNAME'],args.port)
	###############GENERAL SECTION#####################
	if args.config:
		try:
			print "Retrieving {0} configuraiton ...".format(args.firewall)
			r = fw.config(args.firewall)
		except Exception as e:
			print str(e)
			quit(1)
		else:
			print "Firewall {0} configuration:"
			print r['config']
	elif args.rules:
		try:
			print "Retrieving {0} rules ...".format(args.firewall)
			r = fw.rules(args.firewall)
		except Exception as e:
			print str(e)
			quit(1)
		else:
			print "Firewall {0} rules:"
			print r
	elif args.objects:
		try:
			if args.address:
				print "Retrieving {0} address objects ...".format(args.firewall)
				r = fw.objects(args.firewall,'address')
			elif args.address_group:
				print "Retrieving {0} address-group objects ...".format(args.firewall)
				r = fw.objects(args.firewall,'address-group')
			elif args.service:
				print "Retrieving {0} service objects ...".format(args.firewall)
				r = fw.objects(args.firewall,'service')
			elif args.service_group:
				print "Retrieving {0} service-group objects ...".format(args.firewall)
				r = fw.objects(args.firewall,'service-group')
			else:
				print "You need to specify the type of object to retrieve:\n--address\n--address-group\n--service\n--service-group"
				quit(0)
		except Exception as e:
			print str(e)
			quit(1)
		else:
			print "Firewall {0} objects:".format(args.firewall)
			print r
	elif args.routes:
		try:
			print "Retrieving {0} routes ...".format(args.firewall)
			r = fw.routes(args.firewall)
		except Exception as e:
			print str(e)
			quit(1)
		else:
			print "Firewall {0} routes:".format(args.firewall)
			print r
	############### SECTION#####################
