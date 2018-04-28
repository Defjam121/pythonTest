#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Filename:          subscriber.py
# Author:            macbook 
# Date:              2018-04-28
# Version:           1.0
###
"""Example of MQTT client (subscriber) using Mosquitto
Authored by Daniel Shih <hotingwow@gmail.com>
"""

from mosquitto import Mosquitto
from sys import argv
from socket import gethostname
from time import time

# callback
def cb_on_message(cb_mosq, cb_obj, cb_message):
    """logging"""
    print "Get message '%s' from topic '%s'" \
          % (cb_message.payload, cb_message.topic)

def main():
    """start mqtt server and subscribe the topic"""
    # check the number of arguments
    if len(argv) != 6:
        print "usage: %s [hostname] [port] [keepalive] [client_id] [topic]" % argv[0]
        exit(1)

    try:
        mqtt_client = Mosquitto(argv[4])

        # set callback
        mqtt_client.on_message = cb_on_message

        # connect to MQTT broker
        # client.connect(hostname, port=1883, keepalive=60)
        mqtt_client.connect(argv[1], argv[2], int(argv[3]))

        # subscribe the topic
        mqtt_client.subscribe(argv[5])
        print "%s subscribing topic '%s' from %s:%s" % (argv[4], argv[5], argv[1], argv[2])

        while True:
            # call loop method frequently
            # client.loop(timeout=-1); 0 to return immediately; -1 to return
            # after 1 second.
            result = mqtt_client.loop()
            if result != 0:
                # rc != 0; loop failed
                print "Loop failed (%s), disconnecting..." % result
                mqtt_client.disconnect()
                break

    except KeyboardInterrupt:
        # disconnect from the broker
        mqtt_client.disconnect()
        print "Disconnected..."

if __name__ == "__main__":
    main()