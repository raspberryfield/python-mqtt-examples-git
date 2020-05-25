import argparse #See. https://docs.python.org/3.7/howto/argparse.html
import sys
import time
import traceback
import paho.mqtt.client as mqtt
import json
from random import randint
from datetime import datetime

print ("Starting publisher.py, Press Ctrl+C to exit.")

CLIENT_NAME = "Client01"
HOSTNAME = "localhost" #IP/hostname e.g. 127.0.0.1 or localhost
RETAIN_FLAG = True
SLEEP = 1
TOPIC = "my_test_topic"

DEFAULT_MESSAGE = {"client":CLIENT_NAME, "number":0, "datetime":"1990-01-01 00:00:00"}
VERSION = "0.1.1" #Version of program.

def handle_args():
	global CLIENT_NAME, HOSTNAME, SLEEP, TOPIC, RETAIN_FLAG

	#See. https://realpython.com/command-line-interfaces-python-argparse/
	parser = argparse.ArgumentParser(prog='publisher.py', usage="%(prog)s",
					 description =  "Program uses paho library to send a json message to an MQTT broker each N second(s)." \
							" Message contains of a string, random number, and a timestamp.",
					epilog="-----------------------------------------------------------------------",
					prefix_chars="-")

	parser.add_argument("-c", "--clientname", action="store",
				help="Mandatory client name for MQTT broker. e.g. -c MyClient (default: Client01)")
	parser.add_argument("-ho", "--hostname", action="store",
				help="mDNS name of broker. e.g. -ho raspberry.local (default: localhost)")
	parser.add_argument("-r", "--retain", action="store_false",
				help="Set flag that MQTT broker should NOT retain last sent message. e.g. -r (default: [True])")
	parser.add_argument("-s", "--sleep", action="store", type=int,
				help="Seconds to wait for sending next message. e.g. -s 5 (default: 1 sec.)")
	parser.add_argument("-t", "--topic", action="store",
				help="Topic name to publish message. e.g. -t my_topic (default: my_test_topic)")
	parser.add_argument("-v", "--version", action="store_true",
				help="Version of %(prog)s. e.g. -v (default: [Flag])")

	args = parser.parse_args() #Init args and print help message.

	if args.clientname:
		CLIENT_NAME = args.clientname
	if args.hostname:
		HOSTNAME = args.hostname
	if args.retain is False:
		RETAIN_FLAG = False
	if args.sleep:
		SLEEP = args.sleep
	if args.topic:
		TOPIC = args.topic
	if args.version:
		print ("version: ", VERSION)
		sys.exit()

def set_msg(msg):
	msg["number"] = randint(1, 10) #random number ; 1<= N <= 10

	date_time = datetime.now()
	msg["datetime"] = date_time.strftime("%Y-%m-%d %H:%M:%S") #YYY-MM-DD hh:mm:ss

	return msg

def send_msg(client, msg):
	client.connect(HOSTNAME)
	client.publish(TOPIC, msg, retain=RETAIN_FLAG) #retain=True ; Tell MQTT broker to save the last message that was published.
	print ("Sent msg: %s" % msg)

def main():

	try:
		mqtt_client = mqtt.Client(CLIENT_NAME) #Init MQTT Client.
		msg = DEFAULT_MESSAGE  #Declare variable msg(message) with default values.

		while True:

			try:
				msg = set_msg(msg) #Update message.
				send_msg(mqtt_client, json.dumps(msg)) #Convert msg(python dictionary) to json format
			except:
				print ("Error connecting/publishing: ", traceback.format_exc())
			finally:
				time.sleep(SLEEP)

	except KeyboardInterrupt:
		#Put code here to run after user hit Ctrl+C, e.g. cleanups.
		print ("\n Keyboard interrupt, exiting program...")

	except Exception as e:
		print ("An unforeseen error has occurred!")
		print ("Error message: ", e, ".")
		print (traceback.format_exc())
		print ("-----")

	finally:
		print ("Thank you for using %s, Bye!" % sys.argv[0])


#Python convention to call main():
if __name__ == "__main__":
	handle_args()
	main()
