#>_> coding:utf-8 >_>

import six
import json
import teca.generation as tecagen

def loadShortUrls(config):
	try:
		with open(config.short_links.links_database) as links_file:
			return json.load(links_file)
	except IOError:
		return dict()

def dumpShortUrls(urls, config):
	try:
		with open(config.short_links.links_database) as links_file:
			json.dump(urls, links_file)
	except IOError as e:
		raise IOError("could not save the new short URLs to disk: {0}".format(e))
		
