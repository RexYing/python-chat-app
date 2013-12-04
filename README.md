python-chat-app
===============

Author: Rex

===============

Prerequisite:
Python3.3. The standard package of python 3.3 will include the default GUI module tkinter. If not,
download pythontk from apt-get or other distribution sites.

The serverinfo file SHOULD BE CONFIGURED BEFORE STARTING SERVER. Just enter server IP on the first line,
and port on the second line following the simple format already written there.

Start server by clicking main_server.py, or by running python main_server.py in command line.

Then copy the code to the client machines. (no need if server and client are run in the same machine)

Start client by clicking main_client.py. If only wants GUI interface without command line (the command
line is used to display information such as RTT and ACK), change the extension from .py to .pyc.


===============
Functionality:

Upon start, the client will automatically connect to server and display other client in the list box
on the right. The list will get AUTOMATICALLY UPDATED when a client goes on-line or off-line, though
do expect a little bit of delay.

Select one of them and click start chat button

To chat with another peer, type characters in the bottom text box and press Ctrl-Enter to send the text.

Before the first peer sends the message to the second peer, the second peer needs to select the first peer,
and click start chat button. Then both can type messages which will be received by each other.

To close the chat, just press the "close this chat" button. The other peer that is chatting with this peer
receives the notification that the peer gets disconnected. The other peer would not be able to send messages
to the other peer after that. The peer can choose to reconnect just by selecting that user and click "start 
chat" again.

ACK and RTT calculation:
RTT calculation results see the separate text file RTTResult
In addition, after receiving acknowledgement from a user each time, the ACK info and average RTT value so far
are both displayed in command line. If the client is started from command line (.py), these information can be
viewed there. Of course, if the client is started using .pyc extension, only GUI is displayed and these ACK
and RTT information are hidden from the user.

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