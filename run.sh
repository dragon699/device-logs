#!/bin/bash


# Log file to write data to;
# Will be mounted on the host machine as well;
# in ./logs directory;
LOG_FILE="device.log"


# Serial port source to read data from;
# Could be an existing physical device port, or leave empty to use;
# the socat virtual port;
SOURCE=


[[ -z ${SOURCE} ]] && SOURCE=${HOME}/socat-pty2

docker build -t device-logs .
docker run -d -v $(pwd)/logs/:/tmp/:rw -e SOURCE=${SOURCE} -e LOG_FILE=/tmp/${LOG_FILE} device-logs /bin/bash -c './entrypoint.sh'
