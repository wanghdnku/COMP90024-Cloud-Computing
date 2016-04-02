#Concepts and Notes
------------------------------------------------
##Difference between Nodes and CPUs when running software on a cluster?
###[Stack Overflow Question](http://scicomp.stackexchange.com/questions/7530/difference-between-nodes-and-cpus-when-running-software-on-a-cluster)

This issue has become much more nuanced as the changes in architectures has shifted the HPC landscape. As Wolfgang Bangerth mentions one current longstanding view, I'll split my answer into basic definitiions and further details.

###Basic Definition
* **A node** refers to the physical box, i.e. cpu sockets with north/south switches connecting memory systems and extension cards, e.g. disks, nics, and accelerators

* **A cpu socket** is the connector to these systems and the cpu cores, you plug in chips with multiple cpu cores. This creates a split in the cache memory space, hence the need for NUMA aware code.

* **A cpu core** is an independent computing with its own computing pipeline, logical units, and memory controller. Each cpu core will be able to service a number of cpu threads, each having an independent instruction stream but sharing the cores memory controller and other logical units.

This notion of node and cpu core gets you through most HPC queuing systems, but note many HPC centers will charge you "Service Units" which is a variable rate dependent on aspects of the node.

###Going further
If you are interested in actually giving some performance details of a distributed code, this story is a bit more troublesome. Let me put it in terms of questions this model doesn't answer:

* How many cores is a GPU accelerator?

The GPU has very small processors with few logical units, so comparing them to an x86 cpu is not fair. Nonetheless marketers will tell you that GPUs have 1000s of cpus.

* Cloud architectures are putting many traditional nodes on a single physical server with integrated networking between them.

Companies like Calxeda are going around many of the inefficiencies in the current node configurations and your traditional node configuration is sharing many more systems. This idea of node is becoming vague.

**[Wolfgang Bangerth’s Video Lecture](http://www.math.tamu.edu/~bangerth/videos.676.39.html)**

---


###CPU
>CPU stands for Central Processing Unit, and is the part of a computer which executes software programs. The term is not specific to a particular method of execution: units based on transistors, relays, or vacuum tubes might be considered CPU's. However, for clarity, we will use the term to refer to individual silicon chips, such as Intel's Pentium or AMD's Athlon. Thus, a CPU contains one or more cores, however, an HPC system may contain many CPU's. For example, Kraken contains several thousand AMD Opteron CPU's.

###Core
>A core is an individual processor: the part of a computer which actually executes programs. CPUs used to have a single core, and the terms were interchangeable. In recent years, several cores, or processors, have been manufactured on a single CPU chip, which may be referred to as a multiprocessor. It is important to note, however, that the relationship between the cores may vary radically: AMD's Opteron, Intel's Itanium, and IBM's Cell have very distinct setups.

###Node
>In traditional computing, a node is an object on a network. For example, on a home network, your computer, router, and printer might all be nodes. Supercomputers like Kraken are essentially networks, with nodes that communicate with each other to solve a larger problem than any singular computer could in a reasonable amount of time. Kraken contains several types of nodes; compute nodes are the work-horses of the system, and are much like a stripped-down computer. An I/O node is the interface between the compute nodes and other computers, that is, it deals with input and output for the system.

---


**http://en.community.dell.com/techcenter/high-performance-computing/w/wiki/2329**


To properly compute the theoretical performance of a system, we need to agree upon some common terms, or a taxonomy, if you will, of HPC compute components. Then, we simply do a dimensional analysis as we did in high school.

In the past, a chassis contained a single node. This chassis was a desktop computer or a tower version or a deskside unit or a rack-mounted pizza box server, etc. Within that thing you bought was a single node. A single node contained a single processor. A processor contained a single (CPU) core and fit into a single socket. But times change...

With recent "systems,” we can have a single chassis containing multiple nodes. And those nodes contain multiple sockets. And the processors in those sockets contain multiple (CPU) cores.

Therefore, let’s define a few terms.
>1. A “**chassis**” houses one or more nodes.
>2. A **node** contains one or more sockets.
>3. A **socket** holds one processor.
>4. A **processor** contains one or more (CPU) cores.
>5. The **cores** perform FLOPS.

**The "chassis" is that thing that houses one or more compute nodes.** Note that the chassis may be a rack-mounted pizza box, or a blade enclosure or entire rack computer, which accepts plug-in compute nodes. One must buy one or more of these in order to have a computer system. Nonetheless, I call the piece of hardware that is a unit that houses compute nodes a chassis.

**Nodes, usually a printed circuit board(s) of some type, are manufactured with (empty) sockets.** There is not, in general, a node board for each available processor. The node boards are built to accommodate a family of processors. Depending upon your needs, your desires, or your budget, you select a specific processor to go into that socket. Today, within the same processor family, you can select between differing core counts, a wide range of frequencies and vastly differing memory cache structures.

Also note that the "thing" that Intel and AMD and other microprocessor companies sell is a processor. One cannot buy anything smaller than a processor. And they call it a processor with preceding adjectives, e.g., the ABC dual-core processor, or the XYZ quad-core processor.

Finally, **the cores within the processor perform the actual mathematical computations.** One sequence of these mathematical operations involves the exclusive use of floating point numbers and is called a **FLOP or Floating-point Operation**. The plural of FLOP is FLOPs, with a small “s,” like many things when made plural.

In general, a core can do a certain number of FLOPs or Floating-point Operations every time its internal clock ticks. These clock ticks are called cycles and measured in Hertz (Hz). Most microprocessors today can do four (4) FLOPs per clock cycle, that is, 4 FLOPs per Hz. Thus, depending upon the Hz frequency of the processor’s internal clock, the floating point operations per second or FLOPS can be calculated. Note the large “S” in FLOPS.

The internal clock speed of the core is known. It’s that GHz rating typical of today’s processor. For example, a 2.5-GHz processor ticks 2.5 billion times per second (Giga ~ billion). Therefore, a 2.5-GHz processor ticking 2.5 billion times per second and capable of performing 4 FLOPs each tick is rated with a theoretical performance of 10 billion FLOPs per second or 10 GFLOPS.

That’s probably more than anyone needs to know about the details of counting mathematical operations done by microprocessors. Fortunately, the final formula for computing theoretical performance of a system is quite simple and straightforward.

Here is a full and complete sample formula using dimensional analysis:

`GFLOPS = #chassis * #nodes/chassis * #sockets/node * #cores/socket * GHz/core * FLOPs/cycle`

Note that the use of a GHz processor yields GFLOPS of theoretical performance. Divide GFLOPS by 1000 to get TeraFLOPS or TFLOPS.

Likewise, MHz clocks used in the formula will yield MFLOPS, if you need that number. Similarly divide MFLOPS by 1000 to get GFLOPS. When might you need MHz these days, you ask? Think GPU speeds.

Note that for multi-rack systems, the formula may be improved by adding the number of chassis per rack as the first term.
