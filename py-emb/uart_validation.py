import pytest
import serial
import time

PORT = '/dev/ttyUSB0'   # change for Linux

TEST_MESSAGE=b'\n'

BAUD_RATES = [2400, 4800, 9600, 19200, 38400, 57600, 115200]

PARITY_OPTIONS = [
    ("NONE", serial.PARITY_NONE),
    ("EVEN", serial.PARITY_EVEN),
    ("ODD", serial.PARITY_ODD),
]

STOP_BITS = [
    ("1", serial.STOPBITS_ONE),
    ("2", serial.STOPBITS_TWO),
]

DATA_BITS = [
    ("5", serial.FIVEBITS),
    ("6", serial.SIXBITS),
    ("7", serial.SEVENBITS),
    ("8", serial.EIGHTBITS),
]

# ---------------- SERIAL HELPER ----------------
def run_uart_test(baud, parity, stop, data_bits):
    ser = serial.Serial(
        port=PORT,
        baudrate=baud,
        bytesize=data_bits,
        parity=parity,
        stopbits=stop,
        timeout=0.2
    )

    time.sleep(0.1)

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.write(TEST_MESSAGE)

    time.sleep(0.1)

    received = ser.read(10)

    ser.close()

    return received


# ---------------- PARAM COMBINATIONS ----------------
TEST_CASES = []

for baud in BAUD_RATES:
    for parity_name, parity in PARITY_OPTIONS:
        for stop_name, stop in STOP_BITS:
            for data_name, data_bits in DATA_BITS:

                test_id = f"baud={baud}|parity={parity_name}|stop={stop_name}|data={data_name}"

                TEST_CASES.append(
                    pytest.param(
                        baud, parity, stop, data_bits,
                        id=test_id
                    )
                )


# ---------------- TEST ----------------
@pytest.mark.parametrize("baud,parity,stop,data_bits", TEST_CASES)
@pytest.mark.xdist_group("uart")   # 🔥 ensures safe execution
def test_uart_config(baud, parity, stop, data_bits):
    received = run_uart_test(baud, parity, stop, data_bits)

    assert received == TEST_MESSAGE