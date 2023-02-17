# engineering notebook
Keep a notebook for what decisions you made, and why you made them the way you did, and any interesting observations that come up along the way.

## to do from pset specs
- [x] Create an account. You must supply a unique user name.
- [x] List accounts (or a subset of the accounts, by text wildcard) like 10 or something
- [x] Send a message to a recipient. 
- [ ] If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand. 
- [ ] If the message is sent to someone who isn't a user, return an error message
- [ ] Deliver undelivered messages to a particular user
- [x] Delete an account. 
- [ ] You will need to specify the semantics of what happens if you attempt to delete an account that contains undelivered message.

operations
1. create account
2. log in to account
3. send message
4. log out of account
5. receive message
6. delete account

---

## references
- [python sockets guide](https://realpython.com/python-sockets/#echo-client-and-server)
- [socket programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [protoc installation](https://grpc.io/docs/protoc-installation/)
- [protobuf compiling](https://grpc.io/docs/protoc-installation/)

---

## useful commands
- netstat -an, which will show the current state of all sockets

## tech debt