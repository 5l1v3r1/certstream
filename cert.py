#!/usr/bin/env python3

import configparser
import datetime
import logging
import os
import re
import sys
import time
import certstream
from slackclient import SlackClient

def print_time_message(message):
    """Print time and message."""
    try:
        sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S:", time.gmtime()))
        sys.stdout.write(message)
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as error: # pylint: disable=broad-except
        print("Debug: Error in print_time_message: ", str(error))

def send_to_slack(message):
    """Send message to Slack"""
    try:
        sc.api_call(
            "chat.postMessage",
            channel="#" + channel,
            text=message
        )
    except:
        print("Debug: Error in send_to_slack.")

def print_callback(message, context):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']
        
        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]
        for monitored in monitor:
            regex = re.compile(".*\." + monitored + "$")
            for domain in all_domains:
                if regex.search(domain):
                    print_time_message("Domain: " + domain + "\n" + "Received messaged -> {}".format(message))
                    send_to_slack("Domain: " + domain + "\n" + "Received messaged -> {}".format(message))
                    break

def on_open(instance):
    # Instance is the CertStreamClient instance that was opened
    print("Connection successfully established!")

def on_error(instance, exception):
    # Instance is the CertStreamClient instance that barfed
    print("Exception in CertStreamClient! -> {}".format(exception)) 

# Configure Slack
slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')
monitor = [e.strip() for e in config.get('domains', 'monitor').split(',')]
channel = config.get('slack', 'channel')

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

certstream.listen_for_events(print_callback)
