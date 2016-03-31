#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
module load Python/3.4.3-goolf-2015a
module load Java/1.8.0_71
module load mpj/0.44
mpirun -np 4 helloworld.py
#javac -cp .:$MPJ_HOME/lib/mpj.jar HelloWorld.java
#mpjrun.sh -np 4 HelloWorld
