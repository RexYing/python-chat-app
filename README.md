python-chat-app
===============

Author: Rex

===============
Functionality:

Upon start, the client will automatically connect to server and display other client in the list box
on the right. The list will get automatically updated when a client goes on-line or off-line, though
do expect a 0.5 seconds delay.

Select one of them and click start chat button

To chat with another peer, type characters in the bottom text box and press Ctrl-Enter to send the text.

When a first peer sends the message to the second peer, the second peer needs to select the first peer,
and click start chat button. Then both can type messages which will be received by each other

===============
Note:

The file 'serverinfo' contains the ip and port of the server.

===============
Implementation:

The program is written in standard Python 3.3, using the default built-in GUI tool tkinter. On windows
tkinter is automatically installed with Python3.3; on some Linux one will need to install manually
(eg. sudo apt-get install python-tk). All network code is written using standard socket package.

The main thread is the GUI thread. A background thread communicates with the server at a fixed time interval
to obtain a list of peer clients information. Another thread is running a TCP service that allows other 
peers to connect with it.