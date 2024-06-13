def test_example(chrome_driver):
    assert "Google" == chrome_driver.title, "Expected 'Google' in page title"
