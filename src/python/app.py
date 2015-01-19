import time
import os

import docker
from mako.lookup import TemplateLookup

import yaml

lookup = TemplateLookup(
	directories=[
		'src/templates/'
	],
	output_encoding='utf-8',
	input_encoding='utf-8',
	module_directory='/tmp'
)

c = docker.Client(base_url="unix://docker.sock")

try:
	os.mkdir("/config/nginx")
except:
	pass

def gen_configs(config, container):
	if 'nginx' in config:
		for port in container['Ports']:
			if port['PrivatePort'] == config['nginx']['port']:
				gen_nginx(config, port['PublicPort'])

				break

def gen_nginx(config, host_port):
	print '  Generating: Nginx'

	f = open('/config/nginx/%s.conf' % config['nginx']['host'], 'w')

	templ = lookup.get_template('nginx.mako')

	f.write(templ.render(host=config['nginx']['host'], port=host_port))

	f.close()

def remove_nginx(config):
	print '  Removing: Nginx'

	try:
		os.unlink('/config/nginx/%s.conf' % config['nginx']['host'])
	except OSError:
		pass

def remove_configs(config):
	if 'nginx' in config:
		remove_nginx(config)

last_running = {}

print "Looping..."
while True:
	with open('/config.yml') as f:
		conf = yaml.safe_load(f)

	imgs = {}

	for v in conf.itervalues():
		imgs[v['image']] = v

	running = {}

	for container in c.containers():
		if container['Image'] in imgs:
			if container['Image'] not in last_running or container['Id'] != last_running[container['Image']]:
				print 'Image discovered:', container['Image']

				gen_configs(imgs[container['Image']], container)

			running[container['Image']] = container['Id']

	for img in last_running.iterkeys():
		if img not in running or last_running[img] != running[img]:
			print 'Image went away:', img

			remove_configs(imgs[img])

	last_running = running


	time.sleep(15)