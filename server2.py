# -*- coding: UTF-8 -*-

import socket

class HttpErrorException:
	def __init__(self,content):
		self.content = content

	def getContent(self):
		return self.content

	def __str__(self):
		return self.content

class Server:

	def __init__(self,HOST,PORT):
		self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.host = HOST
		self.port = PORT

	def launch(self):
		self.listen_socket.bind((self.host,self.port))
		self.listen_socket.listen(1)
		print "Serving HTTP on port %s ..." % self.port

		while True:
			self.client_connection, self.client_address = self.listen_socket.accept()
			request = self.client_connection.recv(1024)
			self.interpretRequest(request)
			self.client_connection.close()

	def interpretRequest(self,request):
		http_response = self.generateResponse(request)
		self.client_connection.sendall(http_response)

	def checkType(self,requesttype):
		if requesttype != "POST" and requesttype != "GET":
			raise HttpErrorException("Requete pas de type GET ou POST")

	def treatAdresseString(self, string):
		finalString = ""
		for i in range(1,len(string)):
			finalString = finalString + string[i]
		return finalString

	def getFileContent(self, contentOriginal):
		content = self.treatAdresseString(contentOriginal)
		print "====>ADRESSE DU FICHIER====>",content
		fileObject = open(content)
		string = fileObject.read(1024)
		fileObject.close()
		return string

	def generateResponse(self,request):
		try:
			requestInLines = request.split('\n')
			while requestInLines[0] == '':
				del requestInLines[0]
			requestType, requestContent, requestHttp = requestInLines[0].split(' ')
			self.checkType(requestType)
			content = """HTTP/1.1 200 OK

"""+self.getFileContent(requestContent)
			return content
		except HttpErrorException as erreur:
			return """HTTP/1.1 406 Not Acceptable
Content-type: text/html

<html><body><h1>400 Bad Request</h1>
<p>"""+erreur.getContent()+"</p></body></html>"
		except (IndexError, ValueError):
			return """HTTP/1.1 406 Not Acceptable
Content-type: text/html

<html><body><h1>400 Bad Request</h1>
<p>Incorrect type of request</p></body></html>"""
		except IOError:
			return """HTTP/1.1 404 Not Found
Content-type: text/html

<html><body><h1>404 Unavailable file</h1>
<p>File cannot be found</p></body></html>"""
		

serveur = Server('',8000)
serveur.launch()
