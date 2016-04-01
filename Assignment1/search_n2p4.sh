#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=4
module load Python/3.4.3-goolf-2015a
srun search_mpi.py
