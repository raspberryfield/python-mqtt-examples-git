import traceback
import sys
import paho.mqtt.subscribe as mqtt_sub #eclipse.org/paho/clients/python/docs
import time

print ("Starting ",sys.argv[0] ,", Press Ctrl+C to exit.")

HOSTNAME = "localhost"
SLEEP = 1
TOPIC = "my_test_topic"


def main():
	try:
		while True:
			try:
				#Get and print subscribed messages from topic.
				msg = mqtt_sub.simple(TOPIC, hostname=HOSTNAME) #There is a callback mode also. See docs.
				print ("%s %s" % (msg.topic, msg.payload))
			except:
				print ("Error connecting/subscribing: ", traceback.format_exc())
			finally:
				time.sleep(SLEEP)
	except KeyboardInterrupt:
		#Put code here to run, after user hit Ctrl+C, e.g. cleanups.
		print ("\n Keyboard interrupt, exiting program...")
	except Exception as e:
		print ("An unforeseen error has occurred!")
		print ("Error message: ", e, ".")
		print (traceback.format_exc())
		print ("-----")
	finally:
		print ("Thank you for using {}, Bye!".format(sys.argv[0]))

if __name__ == "__main__":
	main()
