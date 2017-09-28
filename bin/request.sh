#!/bin/bash

set -e

##### CONFIG #####

PORT=8080

##### Launch requests #####

for i in {1..500}; do
  echo -n "."
  curl -s http://localhost:8080/ 1>/dev/null &
done
echo "done"
