#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
module load Python/3.4.3-goolf-2015a
srun search.py
