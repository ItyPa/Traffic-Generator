#!/usr/bin/env python

import sys

# exit the program in case no parameters supplied
if len(sys.argv) == 1:
	print("USAGE: traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B")
	sys.exit()

import time
import numpy
import requests
from threading import Thread

# Set initial values for our input arguments
_filename	= ""
_interval	= 0
_lambda		= 0
_lambda_init	= 1
_server_ip	= "google.com"
_have_http	= False
_verbose	= False

# interpret the CLI input arguments, they can be typed in any order
for key in range(1, len(sys.argv)):
	if sys.argv[key] == "--filename":								# set the lambda file
		_filename = sys.argv[key+1]
	elif sys.argv[key] == "--interval":								# set the re-checking lambda file's interval
		_interval = int(sys.argv[key+1])
	elif sys.argv[key] == "--init":
		_lambda = int(sys.argv[key+1])								# set the initial lambda
		_lambda_init = _lambda
	elif sys.argv[key] == "--ip":									# set the ip/url
		_server_ip = sys.argv[key+1]
		if _server_ip.startswith("http"):							# check if the ip/url starts with "http/s://", and mark for later use
			_have_http = True
	elif sys.argv[key] == "--verbose":
		_verbose = True if int(sys.argv[key+1]) == 1 else False					# check whether we need to output information

############ [ Handle Errors ] ############
if not _filename:
	print("=================================================================================================")
	print("\tUSAGE: traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B\n")
	print("\tYou must enter a filename for your lambda, exiting program")
	print("=================================================================================================")
	sys.exit()

if _lambda_init <= 0:
	print("=================================================================================================")
	print("\tUSAGE: traffic_generator.py --filename Y --interval X --init Z --ip W --verbose B\n")
	print("\tThe initial lambda value is illegal, exiting program")
	print("=================================================================================================")
	sys.exit()
###########################################


# a function to allow the requests run in Poisson order, as the gaps inside the batch are distributed uniformly
def doRequests(addr, count):
	if count <= 0:											# exit if we got irrational lambda
		return
	
	times = numpy.random.uniform(0, 1, count)							# get random times within the 1 second interval
	times.sort()
	time.sleep(times[0])										# sleep until the first interval
	for i in range(0, count):
		Thread(target = requests.get, args = (addr, )).start()					# run in another thread, so we won't wait for the response
		if i < count-1:
			time.sleep(times[i+1] - times[i])						# make it Poisson, so we won't send in bursts
################################

# set the necessary parameters
addr = ("" if _have_http else "http://") + _server_ip							# build the right url
timer = 0												# our time counter
firstRun = True												# mark that we need to access the lambda file

while True:
	if _interval > 0 and (timer % _interval == 0 or firstRun):					# update Lambda value every `_interval` seconds, or in the first run
		lambdaFile = open(_filename, "r")							# open the lambda file
		_lambda = int(lambdaFile.read())							# read the lambda value
		lambdaFile.close()									# close the file
		firstRun = False									# disable the first run flag
		if _lambda <= 0:									# if the lambda file had a wrong value - use the default one
			_lambda = _lambda_init
	
	reqsPerSec = numpy.random.poisson(_lambda)							# using Poisson, get how many requests to issue for this second
	
	if _verbose:											# output log
		print("{}. {} requests".format(timer, reqsPerSec))
	
	Thread(target = doRequests, args = (addr, reqsPerSec)).start()					# open thread to handle the requests for the current second

	timer += 1
	time.sleep(1)											# sleep for 1 second
	
