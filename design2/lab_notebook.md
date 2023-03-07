# Logical Clocks Lab Notebook
Students: Kayla Huang and Tom Cobley

While working on this, keep a lab notebook in which you note the design decisions you have made. Then, run the scale model at least 5 times for at least one minute each time. Examine the logs, and discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. Observations and reflections about the model and the results of running the model are more than welcome.

Once you have run this on three virtual machines that can vary their internal times by an order of magnitude, try running it with a smaller variation in the clock cycles and a smaller probability of the event being internal. What differences do those variations make? Add these observations to your lab notebook. Play around, and see if you can find something interesting.

You may use whatever packages or support code for the construction of the model machines and for the communication between the processes. 


---

## Model Machine Decisions
Our model relies primarily on two classes ModelMachine in model_machine.py, which calls the rudimentary LogicalClock class in logical_clock.py. The logical clock contains only two functions—one to update to a new logical clock time given by the callee and one to simply increment the current internal self.time attribute of the logical clock.

Meanwhile, in creating ModelMachine, we decided to implement peer to peer connections as opposed to connecting to a central server. This is in an effort to

In regards to the self.cycle() function, the ModelMachine waits for global_time_ms() - self.last_tick_time > 1000 / self.ticks_ps to be true as opposed to waiting for a modulo to be matched. This is because the exact instance at which the ms matches the tick benchmark might be missed, so we want to check duration as opposed to checking the raw global time. 


## Testing Decisions
In terms of testing, we 


---

# Analysis

## Base case
For the base case of P(internal event) = 0.7, we ran five different tests using three different machines each. We fed in tick rates for the following five experiments and let the system run for one minute each:

| Experiment # | A tick rate | B tick rate | C tick rate |
| --- | --- | --- | --- |
| i | 1 | 1 | 1 |
| ii | 1 | 2 | 3 |
| iii | 1 | 3 | 6 |
| iv | 3 | 4 | 5 |
| v | 4 | 5 | 6 |

The results for the logical clock divergence in these five cases, when plotted against the global time, can be seen in the plots.ipynb file. There, we also observe the differences in message queue length when varying the tick rate parameters. 


add in observations about
- [ ] gaps in the logical clock values 
- [ ] length of the message queue
