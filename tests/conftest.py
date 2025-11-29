# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# optional: pytest-html extras
from pytest_html import extras

@pytest.fixture(scope="session")
def browser():
    opts = Options()
    # Uncomment to run headless:
    # opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_window_size(1366, 768)
    yield driver
    driver.quit()

# create screenshots dir for the session
@pytest.fixture(scope="session", autouse=True)
def _init_screenshot_dir(tmp_path_factory):
    d = tmp_path_factory.mktemp("screenshots")
    os.environ["SCREENSHOT_DIR"] = str(d)
    return d

# Attach screenshot to pytest-html on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser", None)
        if driver:
            screenshot_dir = os.environ.get("SCREENSHOT_DIR", os.getcwd())
            path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(path)
            if hasattr(report, "extra"):
                report.extra.append(extras.image(path))
            else:
                report.extra = [extras.image(path)]
