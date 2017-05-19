'''
	create a cpptools vsix dependency server
'''
import SimpleHTTPServer
import SocketServer
import os
from os.path import expanduser
import json

def write_backup(components):
	'''
	backup urls for checking next time
	'''
	if not components:
		return
	backup = open('url.backup', 'w')
	for key, value in components.items():
		if '127.0.0.1' in value:
			print 'already backuped'
			return
		backup.write('{}->{}\n'.format(key,value))
	backup.close()
	
def check_backup(component, url):
	'''
	checking if component's url is changed since last update
	'''
	backup = None
	try:
		backup = open('url.backup','r')
		while True:
			line = backup.readline()
			if not line:
				print 'component {} not found'.format(component)
				return
			content = line.split('->')
			if content[0].strip() != component:
				continue
			old = content[1].strip()
			if old == url:
				# not changed
				return False
			else:
				# changed
				print 'component [{}] changed, manually download package use below url'.format(component),
				print 'then put it in current directory, press enter to continue'
				print '[{}]'.format(url)
				return True
	except IOError:
		return False
	finally:
		if backup:
			backup.close()
			
COMPONENTS = {
	r'C/C++ language components':			r'http://127.0.0.1/Bin_Windows.zip',
	r'ClangFormat':							r'http://127.0.0.1/LLVM_Windows.zip',
	r'Visual Studio Windows Debugger':		r'http://127.0.0.1/Microsoft.VisualStudio.VsDbg.zip'
}

def modify_dependency(path):
	'''
	modify package.json
	'''
	origin = open(path + '/package.json', 'r+')
	total = json.loads(origin.read())
	print 'modifing dependency urls...'
	backups = {}
	for i in total['runtimeDependencies']:
		if 'Windows' in i['description']:
			desc = i['description']
			for key, value in COMPONENTS.items():
				if key in desc:
					if '127.0.0.1' in i['url']:
						print '[{}] url already patched to {}'.format(key, i['url'])
						break
					if check_backup(key, i['url']):
						raw_input()
					backups[key] = i['url']
					print '{} -> {}'.format(i['url'], value)
					i['url'] = value
	write_backup(backups)
	origin.seek(0)
	origin.write(json.dumps(total, indent=4, separators=(',',':')))
	origin.close()
	
def get_path():
	'''
	found cpptools install path
	'''
	try:
		user = expanduser('~/.vscode/extensions/')
		found = []
		for i in os.listdir(user):
			if 'cpptools' in i:
				result = (user + i).replace('\\', '/')
				found.append(result)
		if not found:
			print 'can not found cpptools extension path, install it first.'
			return ''
			
		if len(found) > 1:
			for i, cpptool in enumerate(found):
				print '{} - {}'.format(i, cpptool)
			choice = raw_input('found {} cpptools, choose one to use: '.format(len(found)))
			return found[int(choice)]
		
		return found[0]
	except IndexError:
		print 'choice out of range'
		return ''
	except ValueError:
		print 'invalid input'
		return ''
		
def start_server():
	'''
	startup a local-server
	'''
	port = 80
	httpd = SocketServer.TCPServer(("", port), SimpleHTTPServer.SimpleHTTPRequestHandler)
	print 'serving at port {}, now restart vscode...'.format(port)
	try:
		http.serve_forever()
	except KeyboardInterrupt:
		print 'exit...'
		
def modify_js(path):
	'''
	modify out/src/Debugger/packageManager.js : require('https') -> require('http')
	'''
	print 'replace require('https') -> require('http')'
	js_path = path + '/out/src/packageManager.js'
	js_file = open(js_path, 'r+')
	content = js_file.read().replace('require("https")', 'require("http")')
	content = content.replace("require('https')", "require('http')")
	js_file.seek(0)
	js_file.write(content)
	js_file.close()
	
if __name__ == '__main__':
	PATH = get_path()
	if not PATH:
		exit(-1)
	print 'get cpptools path: {}'.format(PATH)
	modify_dependency(PATH)
	modify_js(PATH)
	start_server()
