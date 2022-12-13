from multiprocessing import Process, Pipe
import serial
import struct


# define the sender function
def sender(conn):
    # opens serial Port
    ser = serial.Serial("COM4", baudrate=115200)

    while True:

        # send data
        data = read_float(ser)
        conn.send(data)

        # wait for feedback
        feedback = conn.recv()
        print('Received feedback:', feedback)


# define the receiver function
def receiver(conn):
    while True:
        # receive data
        data = conn.recv()
        print('Received data:', data)

        # send feedback if data has been received
        if data is not None:
            feedback = len(data)
        else:  # send 0 as marker that no data has been received
            feedback = 0
        conn.send(feedback)


def read_float(serial_port):
    # Define a list to store the floating-point values
    values = []
    read = True
    while read:
        # Read in 4 bytes of serial data
        data = serial_port.read(4)

        # Convert the bytes into a floating-point number
        value = struct.unpack('f', data)[0]

        # Add the value to the list
        values.append(value)

        # Check if we have collected 4 values
        if len(values) == 4:
            # stop reading loop
            read = False
            # store 4 floats in one dataset
            dataset = values
            # Clear the list and start again
            values = []
            # Return the list of values as the data set
            return dataset


if __name__ == '__main__':
    # create a pipe for communication between the two processes
    parent_conn, child_conn = Pipe()

    # create the sender and receiver processes
    sender_process = Process(target=sender, args=(parent_conn,))
    receiver_process = Process(target=receiver, args=(child_conn,))

    # start the sender and receiver processes
    sender_process.start()
    receiver_process.start()

    # wait for the sender and receiver processes to finish
    sender_process.join()
    receiver_process.join()