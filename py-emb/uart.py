# import serial
# import time

# # Change this to your port (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux)
# port = 'COM3'  
# baudrate = 9600

# try:
#     ser = serial.Serial(port, baudrate, timeout=1)
#     print(f"Connected to {port} at {baudrate} baud")

#     # Give time for connection to establish
#     time.sleep(2)

#     # Send data
#     ser.write(b'Hello device!\n')
#     print("Sent: Hello device!")

#     # Read response
#     while True:
#         if ser.in_waiting > 0:
#             data = ser.readline().decode('utf-8', errors='ignore').strip()
#             print("Received:", data)

# except serial.SerialException as e:
#     print("Error:", e)

# finally:
#     if 'ser' in locals() and ser.is_open:
#         ser.close()
#         print("Serial port closed")






import serial

def init_serial():
    ser = serial.Serial(
        port='COM3',          # Change to your port (e.g., '/dev/ttyUSB0' on Linux)
        baudrate=9600,        # Baud rate
        bytesize=serial.EIGHTBITS,  # Number of data bits
        parity=serial.PARITY_NONE,  # Parity check
        stopbits=serial.STOPBITS_ONE,  # Stop bits
        timeout=1,            # Read timeout in seconds
        xonxoff=False,        # Software flow control
        rtscts=False,         # Hardware (RTS/CTS) flow control
        dsrdtr=False,         # Hardware (DSR/DTR) flow control
        write_timeout=1       # Write timeout
    )
    return ser


def main():
    ser = init_serial()

    if ser.is_open:
        print(f"Connected to {ser.port}")

    try:
        # Write data
        ser.write(b'Hello Device\n')

        # Read data
        while True:
            data = ser.readline()
            if data:
                print("Received:", data.decode(errors='ignore').strip())

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        ser.close()
        print("Serial port closed")


if __name__ == "__main__":
    main()