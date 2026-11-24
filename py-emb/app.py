
from flask import Flask, jsonify
import pytest
import logging

#  LOGGER SETUP

logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_api.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.propagate = False

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.handlers = []
werkzeug_logger.propagate = False



#PYTEST RESULT COLLECTOR


class TestResultCollector:
    def __init__(self):
        self.results = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            test_name = report.nodeid.split("::")[-1]

            if report.passed:
                status = "PASS"
            elif report.failed:
                status = "FAIL"
            else:
                status = "SKIP"

            self.results.append({
                "test": test_name,
                "status": status
            })


app = Flask(__name__)




def run_and_log_tests(pytest_args, operation_name):
    logger.info(f"Running {operation_name.upper()} tests")

    collector = TestResultCollector()

    result = pytest.main(
        pytest_args + ["-q"],
        plugins=[collector]
    )

    # Log each test
    for idx, res in enumerate(collector.results, start=1):
        log_msg = f"{operation_name.upper()} Test{idx}: {res['test']} → {res['status']}"

        if res["status"] == "PASS":
            logger.info(log_msg)
        else:
            logger.error(log_msg)

    passed = sum(1 for r in collector.results if r["status"] == "PASS")

    if result == 0:
        logger.info(f"SUCCESS: All {operation_name.upper()} tests passed")
        status = "success"
    else:
        logger.error(f"ERROR: {operation_name.upper()} tests failed")
        status = "failed"

    return {
        "operation": operation_name,
        "status": status,
        "total": len(collector.results),
        "passed": passed,
        "details": collector.results
    }




@app.route("/all")
def run_all():
    logger.info("Running ALL tests")

    return jsonify(
        run_and_log_tests(["test.py"], "all")
    )


@app.route("/add")
def run_add():
    return jsonify(
        run_and_log_tests(["test.py::test_add"], "add")
    )


@app.route("/sub")
def run_sub():
    return jsonify(
        run_and_log_tests(["test.py::test_sub"], "sub")
    )


@app.route("/mul")
def run_mul():
    return jsonify(
        run_and_log_tests(["test.py::test_mul"], "mul")
    )




if __name__ == "__main__":
    app.run(debug=True, port=9000, use_reloader=False)