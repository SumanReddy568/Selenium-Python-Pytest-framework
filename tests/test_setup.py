def test_example(browser):
    assert "Google" == browser.title, "Expected 'Google' in page title"