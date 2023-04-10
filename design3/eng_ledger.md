# design ex 3 engineering ledger
students: kayla huang and tom cobley

# to do 

- [ ] connect servers to one another
- [ ] list of ports in client
- [ ] some sort of paxos / election with two machines
- [ ] detect when primary replica is down
- [ ] mechanism for client to switch the port they are communicating with (i.e. if no response, try next port)


justify decisions
0. framework: primary replica and secondary replicas
1. using the grpc server implementation
2. commit log and pending log 



server receives message
- if primary, deals w it
- if not primary, sends message back with primary port
    - put a delay in checking primary in case this is the old primary which is dead

server behavior
- any message it receives goes straight to the pending log
- server does a heartbeat to see if primary is alive
    - if not, leadership election


how to do consensus
three machines
- PR sends messages to both SRs, waits for both acks, then tells both to commit and all three commit

if an sr dies
- 

all replicas have to keep a record of all other ports and who is alive
- list and then remove if they die (one missed ack)
- assuming perfect network


database: write everything to a csv (all messages sent and received)

questions
- grpc + sockets?
- what is sufficient to say that the system is fault tolerant?