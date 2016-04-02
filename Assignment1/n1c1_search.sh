#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --mem 10240
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
module load Python/3.4.3-goolf-2015a
srun search_mpi.py
