#!/bin/bash

script="$0"
FOLDER="$(dirname $script)"

source $FOLDER/utils.sh
PROJECT_ROOT="$(abspath $FOLDER/..)"

##### CONFIG #####

IMAGE_NAME=local/mylittlewebserver

##### BUILD #####

docker build -f $PROJECT_ROOT/Dockerfile \
             -t $IMAGE_NAME:latest \
             $PROJECT_ROOT
