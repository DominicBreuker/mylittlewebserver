#!/usr/local/Cellar/bash/4.4.12/bin/bash

script="$0"
FOLDER="$(pwd)/$(dirname $script)"

source $FOLDER/utils.sh
PROJECT_ROOT="$(abspath $FOLDER/..)"

echo "building docker image"
# /bin/bash $FOLDER/build.sh

##### Args #####

CMD=$1
if [ "$CMD" == "" ]; then
  CMD="wsgi_example"
fi

##### CONFIG #####

PORT=8080
IMAGE_NAME=local/mylittlewebserver
declare -A cmds=( ["http"]="python http_server.py" \
                  ["wsgi_example"]="python wsgi_server.py" \
                  ["flask"]="python wsgi_app_start.py flask_app:app" \
                  ["pyramid"]="python wsgi_app_start.py pyramid_app:app" \
                  ["django"]="python wsgi_app_start.py django_appp:app" \
                  ["shell"]="/bin/sh")

##### RUN #####
echo "Starting container... (${cmds[$CMD]})"

docker run --rm \
           -it \
           -p $PORT:$PORT \
           -v $PROJECT_ROOT/src/:/usr/src/app/ \
           $IMAGE_NAME:latest \
           sh -c "${cmds[$CMD]}"
