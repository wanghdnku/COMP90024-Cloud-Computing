#SLURM ‘srun’ command
----
[Simple Linux Utility for Resource Management](https://computing.llnl.gov/linux/slurm/srun.html)

##DESCRIPTION
**Run a parallel job on cluster managed by SLURM. If necessary, srun will first create a resource allocation in which to run the parallel job.**
The following document describes the the influence of various options on the allocation of cpus to jobs and tasks. 
https://computing.llnl.gov/linux/slurm/cpu_management.html


##OPTIONS
###**`--begin=<time>`**
>Defer initiation of this job until the specified time. It accepts times of the form HH:MM:SS to run a job at a specific time of day (seconds are optional). (If that time is already past, the next day is assumed.) You may also specify midnight, noon, or teatime (4pm) and you can have a time-of-day suffixed with AM or PM for running in the morning or the evening. You can also say what day the job will be run, by specifying a date of the form MMDDYY or MM/DD/YY YYYY-MM-DD. Combine date and time using the following format YYYY-MM-DD[THH:MM[:SS]]. You can also give times like now + count time-units, where the time-units can be seconds (default), minutes, hours, days, or weeks and you can tell SLURM to run the job today with the keyword today and to run the job tomorrow with the keyword tomorrow. The value may be changed after job submission using the scontrol command. For example:

```shell script
   --begin=16:00
   --begin=now+1hour
   --begin=now+60           (seconds by default)
   --begin=2010-01-20T12:34:00
```
>Notes on date/time specifications: 
 - Although the 'seconds' field of the HH:MM:SS time specification is allowed by the code, note that the poll time of the SLURM scheduler is not precise enough to guarantee dispatch of the job on the exact second. The job will be eligible to start on the next poll following the specified time. The exact poll interval depends on the SLURM scheduler (e.g., 60 seconds with the default sched/builtin). 
 - If no time (HH:MM:SS) is specified, the default is (00:00:00). 
 - If a date is specified without a year (e.g., MM/DD) then the current year is assumed, unless the combination of MM/DD and HH:MM:SS has already passed for that year, in which case the next year is used.


###**`-c, --cpus-per-task=<ncpus>`**
>Request that ncpus be allocated per process. This may be useful if the job is multithreaded and requires more than one CPU per task for optimal performance. The default is one CPU per process. If -c is specified without -n, as many tasks will be allocated per node as possible while satisfying the -c restriction. For instance on a cluster with 8 CPUs per node, a job request for 4 nodes and 3 CPUs per task may be allocated 3 or 6 CPUs per node (1 or 2 tasks per node) depending upon resource consumption by other jobs. Such a job may be unable to execute more than a total of 4 tasks. This option may also be useful to spawn tasks without allocating resources to the job step from the job's allocation when running multiple job steps with the --exclusive option.

>**WARNING**: There are configurations and options interpreted differently by job and job step requests which can result in inconsistencies for this option. For example srun -c2 --threads-per-core=1 prog may allocate two cores for the job, but if each of those cores contains two threads, the job allocation will include four CPUs. The job step allocation will then launch two threads per CPU for a total of two tasks.

>**WARNING**: When srun is executed from within salloc or sbatch, there are configurations and options which can result in inconsistent allocations when -c has a value greater than -c on salloc or sbatch.


###**`-N, --nodes=<minnodes[-maxnodes]>`**
>Request that a minimum of minnodes nodes be allocated to this job. A maximum node count may also be specified with maxnodes. If only one number is specified, this is used as both the minimum and maximum node count. The partition's node limits supersede those of the job. If a job's node limits are outside of the range permitted for its associated partition, the job will be left in a PENDING state. This permits possible execution at a later time, when the partition limit is changed. If a job node limit exceeds the number of nodes configured in the partition, the job will be rejected. Note that the environment variable SLURM_NNODES will be set to the count of nodes actually allocated to the job. See the ENVIRONMENT VARIABLES section for more information. If -N is not specified, the default behavior is to allocate enough nodes to satisfy the requirements of the -n and -c options. The job will be allocated as many nodes as possible within the range specified and without delaying the initiation of the job. The node count specification may include a numeric value followed by a suffix of "k" (multiplies numeric value by 1,024) or "m" (multiplies numeric value by 1,048,576).


###**`-n, --ntasks=<number>`**
>Specify the number of tasks to run. Request that srun allocate resources for ntasks tasks. The default is one task per node, but note that the --cpus-per-task option will change this default.


###**`--ntasks-per-core=<ntasks>`**
>Request the maximum ntasks be invoked on each core. Meant to be used with the --ntasks option. Related to --ntasks-per-node except at the core level instead of the node level. Masks will automatically be generated to bind the tasks to specific core unless --cpu_bind=none is specified. NOTE: This option is not supported unless SelectTypeParameters=CR_Core or SelectTypeParameters=CR_Core_Memory is configured.


###**`--ntasks-per-node=<ntasks>`**
>Request the maximum ntasks be invoked on each node. Meant to be used with the --nodes option. This is related to --cpus-per-task=ncpus, but does not require knowledge of the actual number of cpus on each node. In some cases, it is more convenient to be able to request that no more than a specific number of tasks be invoked on each node. Examples of this include submitting a hybrid MPI/OpenMP app where only one MPI "task/rank" should be assigned to each node while allowing the OpenMP portion to utilize all of the parallelism present in the node, or submitting a single setup/cleanup/monitoring job to each node of a pre-existing allocation as one step in a larger job script.


###**`-t, --time=<time>`**
>Set a limit on the total run time of the job or job step. If the requested time limit for a job exceeds the partition's time limit, the job will be left in a PENDING state (possibly indefinitely). If the requested time limit for a job step exceeds the partition's time limit, the job step will not be initiated. The default time limit is the partition's time limit. When the time limit is reached, the job's tasks are sent SIGTERM followed by SIGKILL. If the time limit is for the job, all job steps are signaled. If the time limit is for a single job step within an existing job allocation, only that job step will be affected. A job time limit supercedes all job step time limits. The interval between SIGTERM and SIGKILL is specified by the SLURM configuration parameter KillWait. A time limit of zero requests that no time limit be imposed. Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".


###**`--mem=<MB>`**
>Specify the real memory required per node in MegaBytes. Default value is DefMemPerNode and the maximum value is MaxMemPerNode. If configured, both of parameters can be seen using the scontrol show config command. This parameter would generally be used if whole nodes are allocated to jobs (SelectType=select/linear). Also see --mem-per-cpu. --mem and --mem-per-cpu are mutually exclusive.
