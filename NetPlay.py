#!/usr/bin/python

import winsound
import os.path
import glob

import os

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

songList = glob.glob(MUSIC_DIR+"/**/*.*",recursive=True)[:]
currentSong = ""

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	global playerThread
	global currentSong
	
	# GET
	def do_GET(self):
		global currentSong
		# Send response status code
		self.send_response(200)

		# Send headers
		self.send_header('Content-type','text/html')
		self.end_headers()
		
		
		Webpage_Filename = os.path.join(os.path.dirname(__file__), 'Webpage/Main.html')
		with open(Webpage_Filename, 'r') as MainPage:
			data=MainPage.read().replace('\n', '')
		self.write(data)
	
		if (self.requestline.split(" ")[1].split("/")[1] == "play") :
			print ("Play requested!")
			print (self.requestline)
			# GET /play/EVERYTHINGGOESHERE
			self.findSong("/".join(self.requestline.split(" ")[1].replace("%20"," ").split("/")[2:]))
			
		if (self.requestline.split(" ")[1].split("/")[1] == "spec") :
			print ("Play requested")
			print (self.requestline)
			# GET /play/EVERYTHINGGOESHERE
			self.openSong("/".join(self.requestline.split(" ")[1].replace("%20"," ").split("/")[2:]))
		
		
		self.write("<h1>Playing: " + currentSong + "</h1>")
		
		self.write("<p>")
		for file in songList :
			self.write("<br> - <a href=\"/spec/"+file+"\">"+ file + "</a>\n")
			
		self.write("</p>")
		
		self.write("</body>")
		self.write("</html>")
		return
	
	def write(self, text) :
		self.wfile.write(bytes(text,"UTF-8"))
	
	def openSong (self, songPath) :
		global playerThread
		global currentSong
		
		print("Attempting to play: " + songPath)
		
		if (glob.glob(songPath)) :
			print(" Found song!")
			if (playerThread.is_alive()) :
				self.write("<h1>Song already playing</h1>")
				print ("Cannot comply, song already playing")
			else :
				playerThread = threading.Thread(target=playSong, args=([songPath]), kwargs={})
				playerThread.start()
				currentSong = songPath
				print ("Playing")
		else :
			print(" Could not find song!")
	
	def findSong(self, songName) :
		global playerThread
		global currentSong
		
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
				currentSong = files[0]
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

