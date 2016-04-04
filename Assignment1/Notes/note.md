equally divide the work among the cores

#Performance of different processor number

##Speedup
In practice, we’re unlikely to get linear speedup because the use of multiple processes/threads almost invariably introduces some overhead.

>Because:
shared- memory programs will almost always have critical sections.
Distributed-memory programs will almost always need to transmit data across the network. Serial programs, on the other hand, won’t have these overheads

##Efficiency
Furthermore, it’s likely that the overheads will increase as we increase the number of processes. More processes will probably mean more data needs to be transmitted across the network.
S/p will probably get smaller and smaller as p increases.

##Amdahl's Law
Amdahl’s law. It says, roughly, that unless virtually all of a serial program is parallelized, the possible speedup is going to be very limited—regardless of the number of cores available.



===
#Performance of different problem size

it doesn’t take into con- sideration the problem size. a more mathemat- ical version of this statement is known as **Gustafson’s law**.

We also need to keep in mind that T-parallel, S, E, and T-serial all depend on the problem size.

We see that in this example, when we increase the problem size, the speedups and the efficiencies increase, while they decrease when we decrease the problem size.

>Many parallel programs are developed by dividing the work of the serial program among the processes/threads and adding in the necessary “parallel overhead” such as mutual exclusion or communication.
Therefore, if T-overhead denotes this parallel overhead, it’s often the case that:
`T-parallel = T-serial/p + T-overhead.`
Furthermore, as the problem size is increased, T-overhead often grows more slowly than T-serial

Reason:  there’s more work for the processes/threads to do, so the relative amount of time spent coordinating the work of the processes/threads should be less.



###How to choose T-serial?
A final issue to consider is what values of T-serial should be used when report- ing speedups and efficiencies.
In practice, most authors use a serial program on which the parallel program was based and run it on a single processor of the parallel system.
