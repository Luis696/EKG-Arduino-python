import struct
import time

import numpy as np


def read_serial_data(number_of_byte_packages_per_bus, serial_connection):
    """reads serial data from an arduino byte stream, number of Sensor values sent = number_of_packages
        performs task only ones
        returns array of length number_of_packages as type(float)"""
    incoming_byte = []
    read = True

    while read:  # start reading for the data stream
        incoming_byte.append(serial_connection.read(4))  # read byte sized packages from the stream

        if incoming_byte[-1].__len__() > 0:  # checks if incoming incoming_byte is available

            if incoming_byte.__len__() >= number_of_byte_packages_per_bus:
                values = [struct.unpack("f", bytes(incoming_byte[x]))[0] for x in
                          range(0, number_of_byte_packages_per_bus, 1)]
                incoming_byte.clear()  # clear the vector to start the reading proces again
                read = False  # stop reading data stream
                return values  # return array of floating points size = number of packages per bus
        else:
            print("No Data incoming! Check serial connection")  # else give feedback to user
            read = False  # and stop program


def measure_serial_speed(measure_time_in_seconds, number_of_byte_packages_per_bus, serial_connection):
    print("READ DATA\n")
    start_measuring = time.time()
    incoming_byte = []
    read = True
    time_per_bus = []
    first_run = True
    while read:

        if first_run or (incoming_byte.__len__() >= number_of_byte_packages_per_bus):
            # start timer for one bus and waits until bus is filled with the number of bytes
            bus_start_time = time.time()
            first_run = False

        incoming_byte.append(serial_connection.read(4))

        if incoming_byte[-1].__len__() > 0:  # checks if incoming incoming_byte is available
            print('\rData is incoming. Evaluate Serial speed...', end='', flush=True)  # confirm incoming data for user

            if incoming_byte.__len__() >= number_of_byte_packages_per_bus:
                values = [struct.unpack("f", bytes(incoming_byte[x]))[0] for x in
                          range(0, number_of_byte_packages_per_bus, 1)]
                incoming_byte.clear()  # clear the vector to start the reading proces again
                time_per_bus = np.append(time_per_bus, (time.time() - bus_start_time), axis=None)  # measures time per bus type: vector
                first_run = True  # resets timer for the bus

            if bus_start_time >= (
                    start_measuring + measure_time_in_seconds):  # waits until measuring time is done to print data
                read = False
                time_per_package_bus = np.mean(time_per_bus, axis=0)  # takes the average of the time one bus needs
                print("\rthe mean time for one bus of {number_of_packages:.2f} packegs in {measure_time:.2f} seconds was = {time_per_package_bus:.4f} seconds"
                      .format(number_of_packages=number_of_byte_packages_per_bus, measure_time=measure_time_in_seconds, time_per_package_bus=time_per_package_bus))
                print("transmission time: {packages_per_second:.2f} buses/second, equals {packages_per_second:.2f} Hz"
                      .format(packages_per_second=1 / time_per_package_bus))
                print(f"measuring for {number_of_byte_packages_per_bus} packages as one bus finished"
                      .format(number_of_byte_packages_per_bus=number_of_byte_packages_per_bus))
                return 1/time_per_package_bus  # return frequency
        else:
            print("No Data incoming\r")  # else give feedback to user
            read = False  # and stop program

