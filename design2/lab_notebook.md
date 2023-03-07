# Logical Clocks Lab Notebook
Students: Kayla Huang and Tom Cobley

While working on this, keep a lab notebook in which you note the design decisions you have made. Then, run the scale model at least 5 times for at least one minute each time. Examine the logs, and discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. Observations and reflections about the model and the results of running the model are more than welcome.

Once you have run this on three virtual machines that can vary their internal times by an order of magnitude, try running it with a smaller variation in the clock cycles and a smaller probability of the event being internal. What differences do those variations make? Add these observations to your lab notebook. Play around, and see if you can find something interesting.

You may use whatever packages or support code for the construction of the model machines and for the communication between the processes. 

You will turn in both the code (or a pointer to your repo containing the code) and the lab notebook. You will also demo this, presenting your code and choices, during demo day 2.

---

# Model Machine Decisions
In regards to the self.cycle() function, the ModelMachine waits for global_time_ms() - self.last_tick_time > 1000 / self.ticks_ps to be true as opposed to waiting for a modulo to be matched. This is because the exact instance at which the ms matches the tick benchmark might be missed. 