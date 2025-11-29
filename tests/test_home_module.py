# tests/test_home_module.py
import time

def test_home_page_loads(browser):
    """
    Simple sanity test for the Home module.
    Make sure your Flask/Django server is running before executing this test.
    """
    url = "http://127.0.0.1:5000/"   # change if your app uses a different port/path
    browser.get(url)

    # optional wait for the page to settle (prefer WebDriverWait in real tests)
    time.sleep(1)

    # basic assertions - change to match your page's content
    assert "Home" in browser.title or "Sports" in browser.title or "Welcome" in browser.page_source
