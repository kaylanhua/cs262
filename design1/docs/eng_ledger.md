# engineering ledger
kayla lanting huang and thomas mitchell cobley

## to do from pset specs
- [x] Create an account. You must supply a unique user name.
- [x] List accounts (or a subset of the accounts, by text wildcard) like 10 or something
- [x] Send a message to a recipient. 
- [x] If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand. 
- [x] If the message is sent to someone who isn't a user, return an error message
- [x] Deliver undelivered messages to a particular user
- [x] Delete an account. 
- [x] You will need to specify the semantics of what happens if you attempt to delete an account that contains undelivered message.
- [ ] Make tests
- [x] Write configuration/set up instructions
- [x] Write documentation
- [ ] Improve UI?

## part two of the assignment
- [x] Implement grpc

### edge cases
- [x] when someone says '2 ' instead of '2' (stripped spaces)
- [x] making logged in / delivery thread safe
- [x] talking on multiple machines
- [x] fix the threading issues (joining the threads)
- [x] not allowing percentage signs
- [x] splitting messages sent at once to client (preventing it from being interpreted as one long message)
- [x] when user logs in, the message queue sends everything in the queue, not just the first one
- [x] double logging in

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
- information on [bidirectional streams in grpc](https://levelup.gitconnected.com/grpc-how-to-make-bi-directional-streaming-calls-70b4a0569b5b), though we didn't end up using it

---

## useful commands
- netstat -an, which will show the current state of all sockets
- ipconfig getifaddr en0 to get ip addr
- command to run from the experimentation folder to generate proto files 
    - python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto


## tech debt
- [x] get rid of the extra functions in proto file
- [x] testing two clients at once (i.e. that the server is multithreading correctly)
- [ ] comment all the code well
- [ ] rename all files
- [ ] deleting the extra files


## engineering decisions to expand on
- [x] created a conda environment to install all requisite packages in 
- [x] why we used polling in grpc
- [x] the operation codes
- [x] using percentage signs and piping
- [x] how we wrote the test code
- [x] user experience tweaks
- [x] functions shared between implementations (tradeoff between ease of code changes and the abstraction needed for functions to be used in multiple settings)


## future work
### general case
- when someone logs out, bring them back to the "landing page"

### grpc section
- could, instead of polling, wait for batches instead (i.e. longer wait time between polling)
- wait for users to be done typing (or wait for the next menu reprisal) to show new messages, as opposed to consistent polling
- modularize a lot of the shared functions and abstract out the components which are agnostic to the protocol
