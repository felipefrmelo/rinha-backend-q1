#!/usr/bin/env bash
#
# get all files in the current directory and take the prefix of the file name to use as the simulation name
# the files names has this format: app.dockerfile
#
for file in $(ls *.dockerfile); do
    simulation_name=$(echo $file | cut -d'.' -f1)
    echo "Running simulation: $simulation_name"
    app=$simulation_name docker compose up -d --build
    ./executar-teste-local.sh $simulation_name
    app=$simulation_name docker compose down
done

python plot.py
