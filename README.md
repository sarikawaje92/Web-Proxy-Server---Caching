# Web-Proxy-Server---Caching

What to implement:

Implement a multi-threaded web proxy server that is capable of processing multiple simultaneous service requests in parallel. 
A proxy server is a server that acts as an intermediary for requests from clients seeking resources from other servers. 
Web proxies forward HTTP requests.
A full HTTP-1.0 compliant Web serversupports HEAD, POST, and GET methods.
Your proxy server only needs to support GET method and it should handle errors whenever a client requests an object that is not available. Your proxy server should also implement caching. HTTP proxy caching enables you to store copies of
frequently-accessed web objects and then serve this information to users on demand.
It improves performance and frees up Internet bandwidth for other tasks. 
You do not need to implement any replacement or validation policies.

I)	Code Language and Version
--------------------------------------
Python 3.5.2

II)	Development Environment
---------------------------------------
Eclipse Neon - PyDev

III)	Code File name
-----------------------
server.py

IV)	Packages required to run the code
-----------------------------------------------
1)	socket
2)	sys
3)	threading
4)	io
5)	time

V)	Requirements before running the code
----------------------------------------------------
Web browser (Client)
Change the following in the Web Browser
1)	Go to ‘Options’
2)	Go to ‘Advanced Setting’
3)	Select Network/Connection Settings
4)	Check ‘Manual proxy configuration:’
5)	Set ‘HTTP Proxy:’ to ‘localhost’ and ‘Port:’ to ‘8080’
6)	Check ‘Use this proxy server for all the protocols’
7)	Click ‘OK’
 
8)	Clear the browser cache by Ctrl+Shift+Delete and then selecting ‘Clear Now’.

VI)	Instruction to run the code
--------------------------------------
1)	Run the code in Eclipse
2)	Type the request Eg. ‘www.google.com’ in the web browser and click Enter.
3)	The code displays the client, request, response details in code output.
4)	While running, the response from server is cached in a txt file which gets generated in Eclipse workspace directory. Eg. If request made is ‘www.google.com‘ then filename is ‘wwwgooglecom’
5)	While running, the client, request, socket, response, RTT details are logged in a text file ‘log.txt’
6)	For entering a new request, wait until ‘Make new request’ is displayed in code output.
7)	Stop the code in Eclipse.

NOTE: While the code is running and a request is made to the server, the browser self generates new requests. Details regarding these requests are also cached and logged in the file. 
