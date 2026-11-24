import os
import mmap
import random
import time

class SRAMTester:
    def __init__(self, size=1024 * 1024, use_dev_mem=False, base_addr=0x0):
        self.size = size
        self.use_dev_mem = use_dev_mem
        self.base_addr = base_addr

        if use_dev_mem:
            self.fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
            self.mem = mmap.mmap(self.fd, size, mmap.MAP_SHARED,
                                 mmap.PROT_READ | mmap.PROT_WRITE,
                                 offset=base_addr)
        else:
            self.mem = bytearray(size)

    def write_byte(self, addr, value):
        self.mem[addr] = value

    def read_byte(self, addr):
        return self.mem[addr]

    def log_error(self, addr, expected, actual):
        print(f"[ERROR] Addr: {addr:#06x} Expected: {expected:#04x} Got: {actual:#04x}")

    # -----------------------------
    # Progress + Speed Helper
    # -----------------------------
    def show_progress(self, current, total, start_time):
        percent = (current / total) * 100
        elapsed = time.time() - start_time
        speed = (current / (1024 * 1024)) / elapsed if elapsed > 0 else 0

        print(f"\rProgress: {percent:.2f}% | Speed: {speed:.2f} MB/s", end="")

    # -----------------------------
    # Write + Verify Template
    # -----------------------------
    def write_and_verify(self, pattern_func):
        start_time = time.time()

        # WRITE
        for addr in range(self.size):
            value = pattern_func(addr)
            self.write_byte(addr, value)

            if addr % (self.size // 100 or 1) == 0:
                self.show_progress(addr, self.size, start_time)

        print("\nWrite Completed")

        # VERIFY
        start_time = time.time()
        for addr in range(self.size):
            expected = pattern_func(addr)
            val = self.read_byte(addr)

            if val != expected:
                self.log_error(addr, expected, val)

            if addr % (self.size // 100 or 1) == 0:
                self.show_progress(addr, self.size, start_time)

        print("\nVerify Completed\n")

    # -----------------------------
    # Tests
    # -----------------------------
    def test_walking_ones(self):
        print("==================Running Walking 1s Test==========================")
        for bit in range(8):
            pattern = lambda addr: (1 << bit)
            self.write_and_verify(pattern)

    def test_walking_zeros(self):
        print("==========================Running Walking 0s Test=====================")
        for bit in range(8):
            pattern = lambda addr: (~(1 << bit) & 0xFF)
            self.write_and_verify(pattern)

    def test_checkerboard(self):
        print("==============================Running Checkerboard Test=====================")
        for pattern_val in [0xAA, 0x55]:
            pattern = lambda addr: pattern_val
            self.write_and_verify(pattern)

    def test_address(self):
        print("==============================Running Address Test==========================")
        pattern = lambda addr: addr & 0xFF
        self.write_and_verify(pattern)

    def test_random(self):
        print("==============================Running Random Test============================")
        rand_data = [random.randint(0, 255) for _ in range(self.size)]
        pattern = lambda addr: rand_data[addr]
        self.write_and_verify(pattern)

    def test_march(self):
        print("=================================Running March Test=============================")

        start_time = time.time()

        # Write 0
        for addr in range(self.size):
            self.write_byte(addr, 0x00)
            if addr % (self.size // 100 or 1) == 0:
                self.show_progress(addr, self.size, start_time)

        print("\nStep 1 Completed")

        # Read 0, Write 1
        start_time = time.time()
        for addr in range(self.size):
            if self.read_byte(addr) != 0x00:
                self.log_error(addr, 0x00, self.read_byte(addr))
            self.write_byte(addr, 0xFF)

            if addr % (self.size // 100 or 1) == 0:
                self.show_progress(addr, self.size, start_time)

        print("\nStep 2 Completed")

        # Read 1 (reverse)
        start_time = time.time()
        for addr in reversed(range(self.size)):
            if self.read_byte(addr) != 0xFF:
                self.log_error(addr, 0xFF, self.read_byte(addr))

        print("March Test Completed\n")

    def run_all_tests(self):
        self.test_walking_ones()
        self.test_walking_zeros()
        self.test_checkerboard()
        self.test_address()
        self.test_random()
        self.test_march()

        print("✅ ALL TESTS COMPLETED")


if __name__ == "__main__":
    tester = SRAMTester(size=1024 * 1024, use_dev_mem=False)
    tester.run_all_tests()