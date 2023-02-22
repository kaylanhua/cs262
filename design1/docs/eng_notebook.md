# Engineering Notebook

**Instructions:** Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

## Set Up Decisions
There were a few key decisions we made when setting up the code base. Mainly, we decided to modularize all the work within a conda environment, particularly because the gRPC unit would require so many outside packages and version control might present a general issue. 

## Wire Protocol Design Decisions
A few key decisions
- Operation codes were instituted early on with 0 for create account, 1 for log in, 2 for send message, 3 for log out, 4 for delete account, and 5 for list all currently logged in users
- We used percentage signs and piping to separate parts of messages out from one another when sending messages back and forth to the server. 
    - Messages sent to the server from the client is of the form '{opcode}%{username}%{target}%{message}'.
    - This means that users cannot input a username or message which contains any of our separators (mainly spaces, percentages, and pipes) and we check for that when querying the user for an input. 
    - Piping is used to separate when multiple messages are sent separately from the same client to the server but received together. The pipe then separates these messages, in this edge case, into separate packets. 
- We made sure to lock all threads inside of the server so that no thread could alter the shared data structures when others were trying to access it. 

## GRPC Engineering Decisions
More key decisions
- Why we used polling in gRPC: instead of running a thread inside of gRPC to constantly be listening for a message from the server, we have the client constantly polling with opcode '6' every half second. This means that the client in the gRPC situation will receive their messages with at max an 0.5 second delay. Servers using gRPC usually only send messages to clients after the client has queried the server, so we thought this would be the most intuitive way for client and server to communicate. When a client queries the server with opcode 6 (which happens in the background automatically with no input from the user), if the client has a message waiting (either they just signed in or someone just sent a message) on the server queue, the server will send it. 
- Functions shared between these two protocols (socket and grpc) were copied instead of exported because they were slightly different in how they communicate back and forth with the client. This meant that any larger changes from one side would have to be manually reflected on the other side. However, this was a trade off we were willing to make because of the difficulty of refactoring the socket code to be compatible with the ever so slightly different gRPC code. 
    - In any future work, we would want to abstract these functions. 


## User Experience 
- We chose to colorize the new messages that were coming in on the client side from other clients so that they are easier to differentiate from the menu text.
- All user messages come in with [ sender_name ] in brackets (like shown) before the message so that there is no extra bulk in the message.


## Testing Decisions
- In order to keep our code robust to changes, we wanted to make sure that we had a robust testing suite. To do this, we wrote a monolithic test suite that tested all of the functionality of the server. This meant that we could test all of the functionality of the server and client with a single command, to ensure that any changes to either the server or client would not break the functionality of the other.
- Our test uses mutliple threads to spawn a server and two clients. The clients then interact via the server, and the test checks that the server and clients are behaving as expected. The response values given by the server are checked in a non-fragile manner to ensure correct behavior, while being flexible to changes in the actual text returned by the server.


## Edge Cases
- Stripped spaces from inputs (i.e. when someone says '2 ' instead of '2')
- Not allowing percentage signs or pipes.
- When someone logs into the same account that someone else is already logged into, the first person who logged into the account gets automatically logged out. 
- When someone deletes an account that still has outstanding messages, the messages are deleted with the account, without the user ever having been aware that there are still outstanding messages. This really only applies in the gRPC case in which the message is deleted in the 0.5 seconds before the outstanding message is sent to the client, which is a very rare case. In all other cases, there will be no outstanding messages, because a user has to be logged in to try to delete their account (and, thus, will immediately receive messages that are sent to them).
- We manually tested what happens what someone sends a string of messages to someone who is logged out and the user logs in. Upon log in, while the messages are being printed in the new terminal, and another user starts to try to send the user new messages, we made sure that the new messages arrive after the queued messages finish printing. This is accomplished with locking. 