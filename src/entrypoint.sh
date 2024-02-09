#!/bin/bash


function dummy_writer() {
    while true; do
        RANDOM_MSG="Generated sample is $(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)"

        echo ${RANDOM_MSG} > ${HOME}/socat-pty1

        sleep 10
    done
}


# Create 2 virtual serial ports;
/bin/bash -c "socat -d -d pty,raw,echo=1,link=${HOME}/socat-pty1 pty,raw,echo=1,link=${HOME}/socat-pty2 &"
sleep 2

# Simulate fake logging messages;
# that will be used for the bi-directional communication of the;
# virtual serial ports created by socat;
# It will write messages continuously to the first virtual port;
# The python script will then read the messages from the second one;
dummy_writer &

python main.py -s ${SOURCE} -f ${LOG_FILE}
