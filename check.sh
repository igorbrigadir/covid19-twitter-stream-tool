#!/bin/bash
printf "\nDocker:\n"
docker ps
printf "\n"
docker-compose logs --tail="5"

printf "\nHDD Space:\n"

du -h data/
du -h compliance/

printf "\nData:\n"

printf "Partition 1:"
tail -n 1 data/covid19_partition_1 | jq '.text, .id_str, .created_at'
printf "Partition 2:"
tail -n 1 data/covid19_partition_2 | jq '.text, .id_str, .created_at'
printf "Partition 3:"
tail -n 1 data/covid19_partition_3 | jq '.text, .id_str, .created_at'
printf "Partition 4:"
tail -n 1 data/covid19_partition_4 | jq '.text, .id_str, .created_at'
