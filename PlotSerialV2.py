import time
from matplotlib import pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import serial
import struct
import time

ser = serial.Serial("COM4", 115200, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)


def read_serial_data(number_of_byte_packages_per_bus):
    """reads serial data from an arduino byte stream, number of Sensor values sent = number_of_packages
        performs task only ones
        returns array of length number_of_packages as type(float)"""
    incoming_byte = []
    read = True

    while read:  # start reading for the data stream
        incoming_byte.append(ser.read(4))  # read byte sized packages from the stream

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


def time_convert(seconds, return_value):
    """converts seconds into time string shaped like:
    minutes:seconds """
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    milliseconds = seconds*1000
    if return_value == "minutes":
        return round(minutes, 1)
    if return_value == "seconds":
        return round(seconds, 2)
    if return_value == "milliseconds":
        return round(milliseconds, 1)
    if return_value == "hours":
        return round(hours, 2)
    else:
        return 1


def serial_plotting(plotting=True):
    time_new_update = 0
    time_prev_update = 0
    start_time = time.time()
    end_time = 0

    # settings for the figure:
    fig = plt.figure(figsize=(15, 8))
    sig1 = fig.add_subplot(1, 1, 1)  # add subplot for signal 1
    line, = sig1.plot([], lw=3)  # first draw signal 1 as empty line
    txt_frame_rate = fig.text(0, 0, "")  # set up text box for frame rate

    # predefine vectors for x- & y-axis of the plot:
    sig1_x_axis = np.empty(300)
    sig1_x_axis.fill(0)
    sig1_y_axis = np.empty(300)
    sig1_y_axis.fill(0)

    # initialize boundaries for the plot:
    sig1.set_xlim(sig1_x_axis.max(), sig1_x_axis.min())
    sig1.set_ylim(sig1_y_axis.min(), sig1_y_axis.max())

    # TODO: add grid to plot
    # # define settings for the grid: -> see ecg example
    # # Change major ticks to show every 20.
    # sig1.xaxis.set_major_locator(MultipleLocator(1))
    # sig1.yaxis.set_major_locator(MultipleLocator(1))
    # # Change minor ticks to show every 5. (20/4 = 5)
    # sig1.xaxis.set_minor_locator(AutoMinorLocator(5))
    # sig1.yaxis.set_minor_locator(AutoMinorLocator(5))
    # # Turn grid on for both major and minor ticks and style minor slightly
    # # differently.
    # sig1.grid(which='major', color='#CCCCCC', linestyle='--')
    # sig1.grid(which='minor', color='#CCCCCC', linestyle=':')

    fig.canvas.draw()  # draw the empty figure with initial settings
    if plotting:
        sig1background = fig.canvas.copy_from_bbox(sig1.bbox)  # cache the background
    plt.show(block=False)

    while plotting:
        # TODO: measure update time per package incoming and transferred to plot -> after paralleling reading & plotting
        time_new_update = time.time()  # start timer to measure update frequency
        numbers = read_serial_data(4)[0]  # read serial Data form Arduino Signal (i.t.m. only signal 1)
        end_time = time.time()  # current time when value is added to the plot
        time_lapsed = end_time - start_time  # calculates time for x-axis
        # TODO: first update of the plot should not be empty !
        sig1_x_axis = np.append(sig1_x_axis, time_lapsed, axis=None)  # appends x-values by each time step (=refresh rate ?)
        sig1_y_axis = np.append(sig1_y_axis, numbers, axis=None)  # appends y-values with each new data point
        sig1_x_axis = sig1_x_axis[-300:]  # cuts of the last elements of the time signal
        sig1_y_axis = sig1_y_axis[-300:]  # cuts of the last s(t) of the arduino -> corresponding to the time signal

        sig1.set_xlim(sig1_x_axis.min(), sig1_x_axis.max())  # refreshes limit of the x-axis
        sig1.set_ylim(sig1_y_axis.min(), sig1_y_axis.max())  # refreshes limit of the y-axis

        line.set_data(sig1_x_axis, sig1_y_axis)  # writes new data to a new plot "image"

        txt_frame_rate.set_text('Mean Frame Rate:\n {fps:.3f}FPS'.format(fps=1 / (time_new_update - time_prev_update)))  # print txt_frame_rate

        if plotting:  # redraw the plot with new values
            # restore background
            fig.canvas.restore_region(sig1background)

            # redraw just the points
            sig1.draw_artist(line)
            sig1.draw_artist(txt_frame_rate)

            # fill in the axes rectangle
            fig.canvas.blit(sig1.bbox)
        else:  # redraw the plot with old values
            # redraw everything
            fig.canvas.draw()

        fig.canvas.flush_events()
        time_prev_update = time_new_update


serial_plotting(True)


