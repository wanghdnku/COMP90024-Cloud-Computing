#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
module load Python/3.4.3-goolf-2015a
srun -n 4 mpiSearch.py
