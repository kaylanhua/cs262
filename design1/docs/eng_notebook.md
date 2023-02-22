# Engineering Notebook
kayla lanting huang and tom mitchell cobley

**Instructions:** Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

## Set Up Decisions
There were a few key decisions we made when setting up the code base. Mainly, we decided to modularize all the work within a conda environment, particularly because the gRPC unit would require so many outside packages and version control might present a general issue. The dependencies downloaded into the conda environment are preserved in the environment.yml file. 

We also used a Github repository and VSCode Live Share to maintain versions throughout the creation of the code base.

## Wire Protocol Design Decisions
A few key decisions
- Operation codes were instituted early on with 0 for create account, 1 for log in, 2 for send message, 3 for log out, 4 for delete account, and 5 for list all currently logged in users
- We used percentage signs and piping to separate parts of messages out from one another when sending messages back and forth to the server. 
    - Messages sent to the server from the client is of the form '{opcode}%{username}%{target}%{message}'.
    - This means that users cannot input a username or message which contains any of our separators (mainly spaces, percentages, and pipes) and we check for that when querying the user for an input. 
    - Piping is used to separate when multiple messages are sent separately from the same client to the server but received together. The pipe then separates these messages, in this edge case, into separate packets. 
- We included who sent the message in every packet (string) we sent to the server. This makes it easier for the server to be about certain who the client claims to be. Though this is technically redundant information, it was also very helpful for testing as we could print easily on the server side and it provided every packet with complete information. 
- Instead of asking the client to remember the operation codes, we used the terminal to send out a menu querying the user for numerical input.
- Used a thread to listen on the client side for any information transmitted from the server side. 
- One thread per client was used on the server side. This was relatively intuitive since each of the clients have to maintain their own indpendent line of communication with the server. However, we could have considered batching, but this would have to be a future consideration as we haven't scaled to the point of needing functionality of that caliber. 
- If the user already exists when someone tries to create an account, we just automatically log that person into the account. We thought this would provide a better user experience, though it would not work great at scale (i.e. many people have the same name and might try to claim the same username).
- When someone queries for all users who are logged in, we list all the users who are logged in, not just some sample of them. We thought this to be more constructive, since the idea of listing the accounts which are active is to figure out who you can possibly talk to at a given moment. 
- We made sure to lock all threads inside of the server so that no thread could alter the shared data structures when others were trying to access it. 
- Messsages are at most 800 characters. If a user attempts to submit any more than that, they are asked to cut their message down. This is because we want to have enough space in the max 1024 char message to put in the sender and receiver's usernames, as well as any other op codes or separators we might have. We could have done more than 800 chars (op codes and usernames wouldn't take up more than 100 chars), but 800 is playing it safe. 

## GRPC Engineering Decisions
More key decisions
- Why we used polling in gRPC: instead of running a thread inside of gRPC to constantly be listening for a message from the server, we have the client constantly polling with opcode '6' every half second. This means that the client in the gRPC situation will receive their messages with at max an 0.5 second delay. Servers using gRPC usually only send messages to clients after the client has queried the server, so we thought this would be the most intuitive way for client and server to communicate. When a client queries the server with opcode 6 (which happens in the background automatically with no input from the user), if the client has a message waiting (either they just signed in or someone just sent a message) on the server queue, the server will send it. 
- Functions shared between these two protocols (socket and grpc) were copied instead of exported because they were slightly different in how they communicate back and forth with the client. This meant that any larger changes from one side would have to be manually reflected on the other side. However, this was a trade off we were willing to make because of the difficulty of refactoring the socket code to be compatible with the ever so slightly different gRPC code. 
    - In any future work, we would want to abstract these functions. 


## User Experience 
- We chose to colorize the new messages that were coming in on the client side from other clients so that they are easier to differentiate from the menu text.
- All user messages come in with [ sender_name ] in brackets (like shown) before the message so that there is no extra bulk in the message.
- Messages show up in the recipient's terminal immediately even if they are in the middle of responding to the customer service like menu. This does not affect their response in the menu or the packet that they end up sending to the server, but it does allow them to immediately see what someone has said to them, which we thought to be important. 


## Testing Decisions
- In order to keep our code robust to changes, we wanted to make sure that we had a robust testing suite. To do this, we wrote a monolithic test suite that tested all of the functionality of the server. This meant that we could test all of the functionality of the server and client with a single command, to ensure that any changes to either the server or client would not break the functionality of the other.
- Our test uses mutliple threads to spawn a server and two clients. The clients then interact via the server, and the test checks that the server and clients are behaving as expected. The response values given by the server are checked in a non-fragile manner to ensure correct behavior, while being flexible to changes in the actual text returned by the server.


## Edge Cases
- Stripped spaces from inputs (i.e. when someone says '2 ' instead of '2')
- Not allowing percentage signs or pipes.
- When someone logs into the same account that someone else is already logged into, the first person who logged into the account gets automatically logged out. 
- When someone deletes an account that still has outstanding messages, the messages are deleted with the account, without the user ever having been aware that there are still outstanding messages. This really only applies in the gRPC case in which the message is deleted in the 0.5 seconds before the outstanding message is sent to the client, which is a very rare case. In all other cases, there will be no outstanding messages, because a user has to be logged in to try to delete their account (and, thus, will immediately receive messages that are sent to them).
- We manually tested what happens what someone sends a string of messages to someone who is logged out and the user logs in. Upon log in, while the messages are being printed in the new terminal, and another user starts to try to send the user new messages, we made sure that the new messages arrive after the queued messages finish printing. This is accomplished with locking. 


## Comparing gRPC
In terms of code complexity, the gRPC implementation required less design specifications (i.e. how what information is transmitted and parsed) and fewer lines of code in general. We were also able to reuse a few functions from the socket implementation and transfer knowledge, so the coding process was smoother and more concise. In terms of performance, the gRPC implementation is a bit slower in terms of communication between client and server. Any call and response (i.e. message sending) in the gRPC implementation takes anywhere from around 0.002-0.006 seconds. However, messages take only about 6e-05 seconds to complete when using the socket implementation. This is a significant difference in time (around 100x faster to use the socket method), but is imperceptible to the human user. Not to mention, the user gets the messages instantly in the socket implementation, but might have to wait up to 0.5 seconds to receive live messages in the polling gRPC implementation. 

In terms of size, the size of the buffer being sent back and forth for the socket implementation is at most 1024 bytes, but it depends on the messages size. However, for gRPC, the buffer size is always 96 bytes because we are always sending a server log object back and forth. This means that, technically, the gRPC buffer is smaller because the message object is being pointed to as opposed to being passed back and forth between the client and server. 
