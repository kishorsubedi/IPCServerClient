"""A proxy server that forwards requests from one port to another server.

To run this using Python 2.7:

% python proxy.py

It listens on a port (`LISTENING_PORT`, below) and forwards commands to the
server. The server is at `SERVER_ADDRESS`:`SERVER_PORT` below.
"""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import library
import socket 

# Where to find the server. This assumes it's running on the smae machine
# as the proxy, but on a different port.
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 7777

# The port that the proxy server is going to occupy. This could be the same
# as SERVER_PORT, but then you couldn't run the proxy and the server on the
# same machine.
LISTENING_PORT = 8888

# Cache values retrieved from the server for this long.
MAX_CACHE_AGE_SEC = 60.0  # 1 minute


def ForwardCommandToServer(command, server_addr, server_port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_addr, server_port))
    s.sendall(command.encode())
    data = s.recv(1024)
    return data
  """Opens a TCP socket to the server, sends a command, and returns response.

  Args:
    command: A single line string command with no newlines in it.
    server_addr: A string with the name of the server to forward requests to.
    server_port: An int from 0 to 2^16 with the port the server is listening on.
  Returns:
    A single line string response with no newlines.
  """

  ###################################################
  #TODO: Implement Function: WiP
  ###################################################



def CheckCachedResponse(command_line, cache):
  cmd, name, text = library.ParseCommand(command_line)

  # Update the cache for PUT commands but also pass the traffic to the server.
  ##########################
  #TODO: Implement section
  ##########################

  # GET commands can be cached.

  ############################
  #TODO: Implement section
  ############################
  
def SendText(sock, text):
  """Sends the result over the socket along with a newline."""
  sock.send(text.encode() + b"\n")

def ServerFound(data):
  if(data == "Key Not Found\n"):
    return False
  return True 

def ProxyClientCommand(sock, server_addr, server_port, cache):

    command_line = library.ReadCommand(sock)
    command, name, text = library.ParseCommand(command_line)
    returning_str = ""

    if(command == "GET"):#if GET, name might be in cache or not
      if(name in cache.keyvalue):
        timeElapsed = time.time() - (cache.keyvalue[name])[1]
        if(timeElapsed < MAX_CACHE_AGE_SEC ):#No problem with cached information if last cached time is less than 60 seconds.
          returning_text = (cache.keyvalue[name])[0].decode() + "     ( Returned from proxy)    "
          SendText(sock, returning_text ) 
        else: 
          data = ForwardCommandToServer(command_line, server_addr, server_port)#If last cached time is more than 60 seconds, pull the info from main server
          cache.keyvalue[name] = [data, time.time() ]
          sock.send(data + b"\n")
      else:#if not found in cache, forward to the server. Server will handle KEY NOT FOUND error 
        data = ForwardCommandToServer(command_line, server_addr, server_port)
        if(ServerFound(data)== True):
          cache.keyvalue[name] = [data, time.time() ] #cache the data only if server found the key
        sock.send(data + b"\n")

    elif(command == "PUT"): 
      if(name == None or text == None):
        returning_str = "Key And Value both needed for PUT operation\n"
        SendText(sock,returning_str)
      else:
        returning_str = name + " = " + text
        ForwardCommandToServer(command_line, server_addr, server_port)
        SendText(sock,returning_str)

    elif (command == "DUMP"): #command = "DUMP"
      data = ForwardCommandToServer(command_line, server_addr, server_port)
      sock.send(data + b"\n")
    else:
      SendText(sock, 'Unknown command %s' % command)
    return
    #if get, check in cache return if exists otherwise forward it to main server
    #if post, update cache forward it to main server
    #if dump, forward it to main server

"""Receives a command from a client and forwards it to a server:port.

A single command is read from `sock`. That command is passed to the specified
`server`:`port`. The response from the server is then passed back through
`sock`.

Args:
  sock: A TCP socket that connects to the client.
  server_addr: A string with the name of the server to forward requests to.
  server_port: An int from 0 to 2^16 with the port the server is listening on.
  cache: A KeyValueStore object that maintains a temorary cache.
  max_age_in_sec: float. Cached values older than this are re-retrieved from
    the server.
"""

  ###########################################
  #TODO: Implement ProxyClientCommand
  ###########################################




def main():
  # Listen on a specified port...
  server_sock = library.CreateServerSocket(LISTENING_PORT)
  cache = library.KeyValueStore()
  # Accept incoming commands indefinitely.
  while True:
    # Wait until a client connects and then get a socket that connects to the
    # client.
    client_sock, (address, port) = library.ConnectClientToServer(server_sock)
    print('Received connection from %s:%d' % (address, port))
    ProxyClientCommand(client_sock, SERVER_ADDRESS, SERVER_PORT,
                       cache)
    client_sock.close()
  #################################
  #TODO: Close socket's connection
  #################################


main()
