#!/usr/bin/env python3

"""A server to store and retrieve key/value pairs using a socket interface.

Once it's running on your machine, you can test it by connecting to it
with a socket. "telent" is a unix program that allows unencrypted socket
communication from the command line. Localhost is the name of the IPv4 address
127.0.0.1. The second telnet command is the port.

% telnet localhost 7777
Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
PUT Fred Office Hours are 12:30 on Tuesday.
Fred = Office Hours are 12:30 on Tuesday.
Connection closed by foreign host.

That command stores a string under the name "Fred". It can be retrieved in
a similar way:

% telnet localhost 7777
Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
GET Fred
Office Hours are 12:30 on Tuesday.
Connection closed by foreign host.
"""


# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# A few commands are used by both the server and the proxy server. Those
# functions are in library.py.
import library


# The port that we accept connections on. (A.k.a. "listen" on.)
LISTENING_PORT = 7777


def PutCommand(name, text, database):
  database.keyvalue[name] = text
  return name + "=" + text

  """Handle the PUT command for a server.

  PUT's first argument is the name of the key to store the value under.
  All remaining arguments are stitched together and used as the value.

  Args:
    name: The name of the value to store.
    text: The value to store.
    database: A KeyValueStore containing key/value pairs.
  Returns:
    A human readable string describing the result. If there is an error,
    then the string describes the error.
  """
  # Store the value in the database.
  ##########################################
  #TODO: Implement PUT function
  ##########################################


def GetCommand(name, database):
  if(name not in database.keyvalue):
    return "Key Not Found" 
  return database.keyvalue[name]
  """Handle the GET command for a server.

  GET takes a single argument: the name of the key to look up.

  Args:
    name: The name of the value to retrieve.
    database: A KeyValueStore containing key/value pairs.
  Returns:
    A human readable string describing the result. If there is an error,
    then the string describes the error.
  """
  ##########################################
  #TODO: Implement GET function
  ##########################################


def DumpCommand(database):
  allkeyvalues = ""
  for key in database.keyvalue:
    allkeyvalues = allkeyvalues + key + " " + database.keyvalue[key] + "\n"
  return allkeyvalues
  """Creates a function to handle the DUMP command for a server.

  DUMP takes no arguments. It always returns a CSV containing all keys.

  Args:
    database: A KeyValueStore containing key/value pairs.
  Returns:
    A human readable string describing the result. If there is an error,
    then the string describes the error.
  """

  ##########################################
  #TODO: Implement DUMP function
  ##########################################
  
 

def SendText(sock, text):
  """Sends the result over the socket along with a newline."""
  sock.send(text.encode() + b"\n")


def main():
  # Store all key/value pairs in here.
  database = library.KeyValueStore()
  # The server socket that will listen on the specified port. If you don't
  # have permission to listen on the port, try a higher numbered port.
  server_sock = library.CreateServerSocket(LISTENING_PORT)

  # Handle commands indefinitely. Use ^C to exit the program.
  while True:
    # Wait until a client connects and then get a socket that connects to the
    # client.
    client_sock, (address, port) = library.ConnectClientToServer(server_sock)
    print('Received connection from %s:%d' % (address, port))

    # Read a command.
    command_line = library.ReadCommand(client_sock)
    command, name, text = library.ParseCommand(command_line)

    # Execute the command based on the first word in the command line.
    
    if command == 'PUT':
      result = PutCommand(name, text, database)
    elif command == 'GET':
      result = GetCommand(name, database)
    elif command == 'DUMP':
      result = DumpCommand(database)
    else:
      SendText(client_sock, 'Unknown command %s' % command)
    
    SendText(client_sock, result)

    # We're done with the client, so clean up the socket.

    #################################
    #TODO: Close socket's connection
    #################################
    client_sock.close()



main()
