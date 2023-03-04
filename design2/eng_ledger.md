# to do

## each virtual machine must have
- [x] clock rate: random number between 1 and 6
- [x] network queue which holds incoming messages
- [ ] listen on one or more sockets for messages
- [ ] connect to each of the other machines upon initialization
- [x] open a file as a log
- [ ] logical clock

## after initialization
- [ ] check if there is a message for that machine in the message queue
- [ ] take one message off the queue, update the local logical clock, and write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time
- [ ] no message, generate random number 1-10

