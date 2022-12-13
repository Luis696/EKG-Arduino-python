import multiprocessing
import serial

## TODO: implement the serial port as object and add measure frequency routine to normal read function (no seperate method-> would block the port for to long)

def measure_frequency(serial_port):
    # Initialize variables to track the time and frequency
    previous_time = None
    frequency = 0

    # Continuously read data from the serial port
    while True:
        # Read 4 bytes from the serial port
        data = serial_port.read(4)

        # If there is data, measure the frequency
        if data:
            # Get the current time
            current_time = time.time()

            # If this is the first data point, set the previous time
            if previous_time is None:
                previous_time = current_time

            # If enough time has passed, update the frequency
            elif current_time - previous_time >= 1:
                frequency = 1 / (current_time - previous_time)
                previous_time = current_time

            # Print the frequency
            print(f'Frequency: {frequency} Hz')

# Open the serial port
serial_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)

# Create a process for measuring the frequency
process = multiprocessing.Process(target=measure_frequency, args=(serial_port,))

# Start the process
process.start()

# Wait for the process to finish
process.join()

# Close the serial port
serial_port.close()
