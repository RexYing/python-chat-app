python-chat-app
===============

Author: Rex (Zhitao) Ying

email: zy26@duke.edu
(email me if the program didn't work as specified by this Readme)

===============

Prerequisite:
Python3.3. The standard package of python 3.3 will include the default GUI module tkinter. If not,
download pythontk from apt-get or other distribution sites.

The program has been tested on both Linux (Ubuntu 13.04 and 13.10) and Windows 7/8. On Mac, however, sometimes
the tkinter.ttk is not installed, and may cause class not found problem.

The serverinfo file SHOULD BE CONFIGURED BEFORE STARTING SERVER. Just enter server IP on the first line,
and port on the second line following the simple format already written there.

Start server by clicking main_server.py, or by running python main_server.py in command line.

Then copy the code to the client machines. (no need if server and client are running on the same machine)

Start client by clicking main_client.py. If only wants GUI interface without command line (the command
line is used to display information such as RTT and ACK), change the extension from .py to .pyc.


===============
Functionality:

Upon start, the client will need to enter its unique id number and click ok to enter the main GUI window.
the client will automatically connect to server and display other client in the list box
on the right. The list will get AUTOMATICALLY UPDATED when a client goes on-line or off-line, though
do expect a little bit of delay.

Select one of them and click start chat button to start chatting with that peer.

To chat with another peer, type characters in the bottom text box and press Ctrl-Enter to send the text.

Before the first peer sends the message to the second peer, the second peer needs to select the first peer,
and click start chat button. Then both can type messages which will be received by each other. If one peer 
clicks "start chat" button, but the other does not, then a message "peer XXX wants to chat with you!" message
will appear on the welcome tab of the other peer.

Although both peers have to click "start chat" in order to chat with each other, actually only 1 TCP 
connection (duplex) is created. The button click for the second peer simply opens up the GUI chat window.

To close the chat, just press the "close this chat" button. The other peer that is chatting with this peer
receives the notification that the peer gets disconnected. The other peer would not be able to send messages
to the other peer after that. The peer can choose to reconnect just by selecting that user and click "start 
chat" again. Or the other peer too, can click "close this chat" to close the chat tab.
Each TCP connection to peers, as well as connection to server are safely closed by closing the corresponding
sockets, provided that the user does not force-close the program by Ctrl-alt-del, kill, Ctrl-C commands. If
in Windows, close GUI instead of close command line to close the program.

ACK and RTT calculation:
RTT calculation results see the separate text file RTTResult
In addition, after receiving acknowledgement from a user each time, the ACK info and average RTT value so far
are both displayed in command line. If the client is started from command line (.py), these information can be
viewed there. Of course, if the client is started using .pyc extension, only GUI is displayed and these ACK
and RTT information are hidden from the user.

===============

Bonus:

1. RTT calculation, shown in the file RTTResult. Also the RTT information is displayed in command line of each
client. Client connects to server periodically using UDP protocol. Each request will generate a new line of 
RTT information. client chats with another peer using TCP protocol. Each time the user types in a message, and
press Ctrl-Enter, the message is sent to the peer using TCP, and RTT of TCP is calculated.

2. Multiple Chat Window Support. A client is able to connect to multiple other clients, and chat with them at 
the same time. Each time a different peer is selected and "start chat" clicked, a new tab will pop up, and the 
user is able to talk to that guy. It can also talk to the previous guy it was chatting with by switching the tab.

===============
Note:

The file 'serverinfo' contains the ip and port of the server.

===============
Implementation:

The program is written in standard Python 3.3, using the default built-in GUI tool tkinter. 
All network code is written using standard socket package.

The main thread is the GUI thread. A background thread communicates with the server at a fixed time interval
to obtain a list of peer clients information. Another thread is running a TCP service that allows other 
peers to connect with it.


===============