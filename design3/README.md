# design exercise three
fault tolerant chat server
students: kayla huang and tom cobley

## specs
Take one of the two implementations you created for the first design exercise (the chat application) and re-design it so that the system is both persistent (it can be stopped and re-started without losing messages that were sent during the time it was running) and 2-fault tolerant in the face of crash/failstop failures. In other words, replicate the back end of the implementation, and make the message store persistent.

The replication can be done in multiple processes on the same machine, but you need to show that the replication also works over multiple machines (at least two). That should be part of the demo.

As usual, you will demo the system on Demo Day III (April 10). Part of the assignment is figuring out how you will demo both the new features. As in the past, keep an engineering notebook that details the design and implementation decisions that you make while implementing the system. 

## running gRPC code
To run the gRPC code, navigate to the grpc folder in the repository. Then, inside of that folder, run the command
``` $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./messages.proto ```

This will generate the _pb2_grpc.py and _pb2.py from the messages.proto file. 

Then, from the grpc_server.py, set the host and port to the same thing as in grpc_client.py (if running on one machine) and run the two files using the instructions above replacing socket_server.py with grpc_server.py and same for the client file. If you are running in two machines, follow the instructions above. 

---

## general design choices

### grpc choice
We chose to use our grpc implementation of the first design exercise because it was cleaner in terms of code and communication. Mainly, every server would acknowledge the client every time any client said anything to the server. This meant that detecting server death would be much easier. 

### design architecture
We first implemented the PR/SR model as specified in section with grpc communication between client and server and socket communication between one primary replica and two secondary replicas. Though this was a valid framework and used a good combination of the first two design projects, we felt that this did not handle Byzantine faults in a way that was satisfactory (that is to say, at all). Thus, we switched to a model with five replicas (recall that two fault tolerance when taking Byzantine failure into account) requires 2f+1 = 5 machines. 

### persistence 
Client perspective:
As long as the servers are up (i.e. three or more), all messages are "persistent" from the perspective of the client, as in the first design project.

Server perspective: 
We wanted to make sure that, even if the entire program went down, no pending messages would be lost. In order to achieve this level of persistence, we chose to log all the pending messages (stored in self.messages in the grpc_server.py file/the Server class) in a csv for each replica. We chose to overwrite this csv, named ID.csv where ID was the letter associated with the replica, every time that there was a change to the pending log because it was less time consuming than picking through the existing csv and trying to eliminate all messages that had been sent or added. There is a trade off here in that as the system gets larger, this does not scale. A proper, persistent database would be needed under those conditions.

Note that we make sure our pending messages and existing user records both persist. This is so that the full state of the application, which really only relies on these two aspects, is preserved when the entire system dies. The trouble comes when this persistence does not agree, as outlined in the below edge case section. 

We make sure that there is a script/way for an admin to delete all the databases (i.e. the csvs) when the servers all come back online but we want to reset the entire applicatioin (for demo purposes, mainly). Though this would never be the case in real life, we noted that this is important because of a particularly nasty (and very rare edge case).

#### the nasty edge case
Under our system design, there is a case in which, if three servers experience Byzantine failure (or even crash failure) in a particular order/with a particularly unlucky timing, there might be a case in which three of the servers record a state which does not agree with each other. For example, replicas A, B, and C all fail at different times and have different snapshots of the state stored in their persistent CSVs. When all five machines come on at once, the five machines will get stuck in an infinite instant death loop. This is because there will be no 3 replica consensus for the clients to trust and the clients will automatically shut down, under our design, after realizing this. 

On one hand, this is not necessarily something we need to deal with because this case demonstrates three faults and we only need to make sure the system is two fault tolerant, but we also want to be able to bring the entire system back online after three faults (i.e. restart the system).

To combat this, we wrote a script called reset.sh which erase everything from all the CSVs (sessions as well as messages). This is called whenever we need to recover after three faults occur. 


### testing
Testing was done manually and through asserts. We wrote a script to automatically start up the five server replicas in different terminals and n clients, each in their own terminal  We tested several cases:

- Incorrect IDs being fed in for the five replicas (we accept only A, B, C, D, E as replica names)
- Two fault tolerance: clients stop receiving messages after three machines have died/the processes are killed and are told that the servers are down
- Two Byzantine fault tolerance: when two replicas are not down but start sending incorrect messages to the clients, the clients will nt
- Clients receiving messages that are 

