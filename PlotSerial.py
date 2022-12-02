import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import struct
import time

# open serial port, define baud rate and UART protocol
ser = serial.Serial("COM4", 115200, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
zs = []
vs = []
ws = []
# start timer for the Plot
start_time = time.time()


def time_convert(seconds):
    """converts seconds into time string shaped like:
    minutes:seconds """
    minutes = seconds // 60
    seconds = seconds % 60
    # hours = mins // 60 # if ever needed add hours -> "{0}:{1}:{2}".format(int(minutes),int(hours), round(seconds, 2))
    minutes = minutes % 60
    return "{0}:{1}".format(int(minutes), round(seconds, 2))


def read_serial_data(number_of_packages):
    """reads serial data from an arduino byte stream, number of Sensor values sent = number_of_packages
    performs task only ones
    returns array of length number_of_packages as type(float)"""
    signal = []
    read = True
    while read:
        signal.append(ser.read(4))  # reads four bytes (= float) from the serial stream, add each value to signal
        if signal.__len__() >= number_of_packages:  # waits until each package (= each Sensor) is read

            # loops over all bytes in signal and converts them into float -> returns vector
            values = [struct.unpack("f", bytes(signal[x]))[0] for x in range(0, number_of_packages, 1)]

            signal.clear()  # clears signal vector after converting
            read = False  # stop reading from serial Port, until called again
            return values  # returns Value vector of size number_of_packages type float


def animate(i, xs, ys, zs, vs, ws):
    """This function is called periodically from FuncAnimation"""
    end_time = time.time()  # current time when value is added to the plot
    time_lapsed = end_time - start_time  # calculates time for x-axis

    numbers = read_serial_data(4)  # reads data from serial port numbers type(array) length(number_of_packages)

    # add new values to data arrays
    xs.append(time_convert(time_lapsed))
    ys.append(numbers[0])
    zs.append(numbers[1])
    vs.append(numbers[2])
    ws.append(numbers[3])
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]
    zs = zs[-20:]
    vs = vs[-20:]
    ws = ws[-20:]

    # Draw all values into the plot / updates the plot
    ax.clear()
    ax.plot(xs, ys, "b")
    ax.plot(xs, zs, "r")
    ax.plot(xs, vs, "b")
    ax.plot(xs, ws, "r")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Sine over time')
    plt.ylabel('Amplitude')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, zs, vs, ws), interval=50)
plt.show()  # show plot







