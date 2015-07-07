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
		# on commence par demander un socket, de famille AF_INET et de type SOCK_STREAM

		self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# premier parametre : definit le protocole

		self.host = HOST
		self.port = PORT

	def launch(self):
		self.listen_socket.bind((self.host,self.port))
		# on associe le socket à une adresse

		self.listen_socket.listen(1)
		print "Serving HTTP on port %s ..." % self.port

		while True:
			self.client_connection, self.client_address = self.listen_socket.accept()
			request = self.client_connection.recv(1024)
			self.interpretRequest(request)

			self.client_connection.close()

	def interpretRequest(self,request):
		print "=======Requête :======="

		print request

		print "=====FIN REQUETE===="

		http_response = self.generateResponse(request)

		print "========Réponse :======"

		print http_response

		print "=======FIN REPONSE===="
		self.client_connection.sendall(http_response)

	def checkType(self,requesttype):
		if requesttype != "POST" and requesttype != "GET":
			raise HttpErrorException("Requête pas de type GET ou POST")

	def generateResponse(self,request):
		try:
			requestInLines = request.split('\n')
			while requestInLines[0] == '':
				del a[0]
			requestType, requestContent, requestHttp = requestInLines[0].split(' ')
			self.checkType(requestType)
			return """HTTP/1.1 200 OK

Hello, World!"""
		except HttpErrorException as erreur:
			return """HTTP/1.1 500 OK
<html><body><h1>500 Service Unavailable</h1>
<p>"""+erreur.getContent()+"</p></body></html>"
		except (IndexError, ValueError):
			return """HTTP/1.1 500 OK
<html><body><h1>500 Service Unavailable</h1>
<p>Incorrect type of request</p></body></html>"""
		

serveur = Server('',8000)
serveur.launch()