#!/usr/bin/python3
import serial
import os
from settings import Settings
from utils import create_rotating_log
from datetime import datetime, timedelta

def run():
	mainlogger.warning(f'Starting PiElectricity id {Settings.id}')
	# Check if the csv file exists
	if os.path.isfile(Settings.readings_file):
		mainlogger.debug(f'CSV File already exists')
	else:
		mainlogger.warning(f'No CSV File found, creating')
		csv_firstline = f'Timestamp,Power1,Power2,Power3'
		with open(Settings.readings_file, 'w') as f:
			f.write(csv_firstline)

	reading_counter = 0
	reading_total = [0,0,0]
	submit_time = datetime.now().replace(second=0,microsecond=0) + timedelta(minutes=1)

	# Continuously read from the serial
	while True:
		# Read one line from the serial buffer
		line = ser.readline().decode().strip()

		# Get the datetime
		recvtime = datetime.now()

		# Check if it is time to submit yet
		if recvtime >= submit_time:
			mainlogger.debug(f'Calculating power and writing to file for {submit_time}')
			# Calc the avg power
			power = [int(i*Settings.voltage/reading_counter) for i in reading_total]
			mainlogger.debug(f'Power calculated as {power} from {reading_counter} readings')
			with open(Settings.readings_file, 'a') as f:
				f.write(f'\n{submit_time},{power[0]},{power[1]},{power[2]}')
			reading_counter = 0
			reading_total = [0, 0, 0]
			submit_time = recvtime.replace(second=0,microsecond=0) + timedelta(minutes=1)

		# Create an array of the data
		Z = line.split(' ')
		# Print it nicely
		print("----------")
		for i in range(len(Z)):
			if i == 0:
				# Node ID
				pass
			elif i in [1, 2, 3]:
				reading_total[i-1] += float(Z[i])
				print("Current %d: %s A" % (i, Z[i]))
			elif i == 4:
				# Temperature
				pass

		reading_counter += 1

if __name__ == '__main__':
	mainlogger = create_rotating_log(Settings.log_name)
	ser = serial.Serial('/dev/ttyAMA0', 38400)
	while True:
		try:
			run()
		except:
			mainlogger.exception(f'Exception in main process')