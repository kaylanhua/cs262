# engineering notebook
kayla lanting huang and thomas mitchell cobley

---
**Instructions:** Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

## to do from pset specs
- [x] Create an account. You must supply a unique user name.
- [x] List accounts (or a subset of the accounts, by text wildcard) like 10 or something
- [x] Send a message to a recipient. 
- [x] If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand. 
- [x] If the message is sent to someone who isn't a user, return an error message
- [x] Deliver undelivered messages to a particular user
- [x] Delete an account. 
- [ ] You will need to specify the semantics of what happens if you attempt to delete an account that contains undelivered message.
- [ ] make tests

## part two of the assignment
- [ ] implement grpc

### edge cases
- [x] when someone says '2 ' instead of '2' (stripped spaces)
- [ ] making logged in / delivery thread safe
- [x] talking on multiple machines
- [ ] fix the threading issues (joining the threads)
- [x] not allowing percentage signs
- [x] splitting messages sent at once to client (preventing it from being interpreted as one long message)

operations
1. create account
2. log in to account
3. send message
4. log out of account
5. receive message
6. delete account

---

### references
- [python sockets guide](https://realpython.com/python-sockets/#echo-client-and-server)
- [socket programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [protoc installation](https://grpc.io/docs/protoc-installation/)
- [protobuf compiling](https://grpc.io/docs/protoc-installation/)

---

## useful commands
- netstat -an, which will show the current state of all sockets
- ipconfig getifaddr en0 to get ip addr
- [run from the experimentation folder to generate proto files] python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto


## tech debt
- [ ] get rid of the extra functions in proto file
- [ ] testing two clients at once (i.e. that the server is multithreading correctly)
- [ ] comment all the code well

## engineering decisions to expand on
- [ ] created a conda environment to install all requisite packages in 
- [ ] why we used polling in grpc
- [ ] the operation codes
- [ ] using percentage signs and piping
- [ ] how we wrote the test code
- [ ] user experience tweaks
- [ ] functions shared between implementations (tradeoff between ease of code changes and the abstraction needed for functions to be used in multiple settings)