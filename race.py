import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui

from selenium.webdriver.chrome.options import Options

typeracer_url = 'https://play.typeracer.com/'
driver = webdriver.Chrome()

try:
    driver.get(typeracer_url)
    wait = ui.WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element_by_link_text('Practice'))
    practice_btn = driver.find_element_by_link_text('Practice')
    practice_btn.click()
except TimeoutException:
    print "Could not find race start button"
