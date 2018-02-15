#!/usr/bin/python

import csv
from jnpr.junos import Device
from pprint import pprint
from threading import Thread




def zeroize_func(row):

	print("Executing thread for "+row["current_ip"])

	dev = Device(host=row["current_ip"], user=row["user_id"], password=row["password"])
	dev.open()

	#print (dev.facts)
	try:
		print(dev.rpc.request_system_zeroize())
	except:
		print("zeroizing "+row["current_ip"])

	try:
		dev.close()
	except:
		print("Device connection closed")

if __name__=="__main__":
	
	csv_filename="saim_device_data.csv"
	device_data = csv.DictReader(open(csv_filename))
	for row in device_data:
		t = Thread(target=zeroize_func, args=(row,))
		t.start()









