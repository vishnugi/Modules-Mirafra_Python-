# import os
# import mmap
# import random
# import time
# import threading
# from flask import Flask, jsonify, render_template

# app = Flask(__name__)

# # -----------------------------
# # Shared Status (VERY IMPORTANT)
# # -----------------------------
# status = {
#     "progress": 0,
#     "speed": 0,
#     "test": "Idle"
# }

# # -----------------------------
# # SRAM Tester
# # -----------------------------
# class SRAMTester:
#     def __init__(self, size=1024 * 1024):
#         self.size = size
#         self.mem = bytearray(size)

#     def write_byte(self, addr, value):
#         self.mem[addr] = value

#     def read_byte(self, addr):
#         return self.mem[addr]

#     def update_status(self, current, total, start_time, test_name):
#         percent = (current / total) * 100
#         elapsed = time.time() - start_time
#         speed = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0

#         status["progress"] = round(percent, 2)
#         status["speed"] = round(speed, 2)
#         status["test"] = test_name

#     def log_error(self, addr, expected, actual):
#         print(f"[ERROR] Addr: {addr:#06x} Expected: {expected:#04x} Got: {actual:#04x}")

#     # -----------------------------
#     # Example Test (Address Test)
#     # -----------------------------
#     def test_address(self):
#         test_name = "Address Test"

#         start_time = time.time()

#         # WRITE
#         for addr in range(self.size):
#             self.write_byte(addr, addr & 0xFF)

#             if addr % (self.size // 100 or 1) == 0:
#                 self.update_status(addr, self.size, start_time, test_name)

#         # VERIFY
#         start_time = time.time()
#         for addr in range(self.size):
#             expected = addr & 0xFF
#             val = self.read_byte(addr)

#             if val != expected:
#                 self.log_error(addr, expected, val)

#             if addr % (self.size // 100 or 1) == 0:
#                 self.update_status(addr, self.size, start_time, test_name)

#     def run_all_tests(self):
#         self.test_address()
#         status["test"] = "Completed"
#         status["progress"] = 100


# tester = SRAMTester()

# # -----------------------------
# # Flask Routes
# # -----------------------------
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/start")
# def start():
#     thread = threading.Thread(target=tester.run_all_tests)
#     thread.start()
#     return "Started"

# @app.route("/status")
# def get_status():
#     return jsonify(status)


# if __name__ == "__main__":
#     app.run(port=5001,debug=True)


import os
import mmap
import random
import time
import threading
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# -----------------------------
# Shared Status
# -----------------------------
status = {
    "progress": 0,
    "speed": 0,
    "test": "Idle",
    "tested_mb": 0   # ✅ NEW
}

# -----------------------------
# SRAM Tester
# -----------------------------
class SRAMTester:
    def __init__(self, size=500 * 1024 * 1024):  # ✅ 100 MB
        self.size = size
        self.mem = bytearray(size)

    def write_byte(self, addr, value):
        self.mem[addr] = value

    def read_byte(self, addr):
        return self.mem[addr]

    def update_status(self, current, total, start_time, test_name):
        percent = (current / total) * 100
        elapsed = time.time() - start_time
        speed = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0

        tested_mb = current / (1024 * 1024)

        status["progress"] = round(percent, 2)
        status["speed"] = round(speed, 2)
        status["test"] = test_name
        status["tested_mb"] = round(tested_mb, 2)   # ✅ NEW
        status["total_mb"] = round(total / (1024 * 1024), 2)

    def log_error(self, addr, expected, actual):
        print(f"[ERROR] Addr: {addr:#06x} Expected: {expected:#04x} Got: {actual:#04x}")

    # -----------------------------
    # Address Test (100MB)
    # -----------------------------
    def test_address(self):
        test_name = "Address Test (500MB)"

        step = self.size // 500  # ✅ update every 0.5%

        start_time = time.time()

        # WRITE
        for addr in range(self.size):
            self.write_byte(addr, addr & 0xFF)

            if addr % step == 0:
                self.update_status(addr, self.size, start_time, test_name)

        # VERIFY
        start_time = time.time()
        for addr in range(self.size):
            expected = addr & 0xFF
            val = self.read_byte(addr)

            if val != expected:
                self.log_error(addr, expected, val)

            if addr % step == 0:
                self.update_status(addr, self.size, start_time, test_name)

    def run_all_tests(self):
        self.test_address()
        status["test"] = "Completed"
        status["progress"] = 100


tester = SRAMTester()

# -----------------------------
# Flask Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    thread = threading.Thread(target=tester.run_all_tests)
    thread.start()
    return "Started"

@app.route("/status")
def get_status():
    return jsonify(status)


if __name__ == "__main__":
    app.run(port=5005,debug=True)