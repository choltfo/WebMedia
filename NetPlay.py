#!/usr/bin/python

import winsound
import os.path
import glob

import threading

PORT_NUMBER = 8080
MUSIC_DIR = "Z:/MP3 Music"

from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import call


def playSong (path) :
	call(["ffplay",path,"-autoexit"])

playerThread = threading.Thread(target=playSong, args=(""), kwargs={})

# Plan!
# Host a webpage that contains JS and a form that sends data by POST.
# Implement a do_POST that receives the name in the form.
# When received, queue it up!
#

# Once a queue is formed, update page model with information on new songs. Track up/down votes.

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	global playerThread
	
	# GET
	def do_GET(self):
		# Send response status code
		self.send_response(200)

		# Send headers
		self.send_header('Content-type','text/html')
		self.end_headers()
		
		self.write("<html>")
		self.write("<head>")
		self.write("<title>Song loader</title>")
		self.write("</head>")
		self.write("<body>")
		
		if (self.requestline.split(" ")[1].split("/")[1] == "play") :
			print ("Play requested!")
			print (self.requestline)
			# GET /play/EVERYTHINGGOESHERE
			self.requestSong("/".join(self.requestline.split(" ")[1].replace("%20"," ").split("/")[2:]))
		
		self.write("<p>Hello World!")
		
		self.write("</body>")
		self.write("</html>")
		return
	
	def write(self, text) :
		self.wfile.write(bytes(text,"UTF-8"))
	
	def requestSong(self, songName) :
		global playerThread
		gsearch = MUSIC_DIR+'/**/*'+songName+'*.*'
		
		print ("Finding song for "+gsearch)
		
		files = glob.glob(gsearch,recursive=True)
		
		if (len(files) > 0) :
			self.write("<h1>Loadin' 'em sweet tunes.</h1>")
			if (playerThread.is_alive()) :
				self.write("<h1>Song already playing.</h1>")
			else :
				playerThread = threading.Thread(target=playSong, args=([files[0]]), kwargs={}) 
				print (files[0])
				playerThread.start()
			
		else :
			self.write("<h1>Could not find anything for \"" + songName+ "\"\n</h1>")
 
def run():
	print('starting server...')
	
	# Server settings
	#server_address = ('127.0.0.1', PORT_NUMBER)
	#server_address = ('192.168.0.66', PORT_NUMBER)
	server_address = ('', PORT_NUMBER)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()


run()

