import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

typeracer_url = 'https://play.typeracer.com/'
driver = webdriver.Chrome()

try:
    # Boot chromedriver and wait for page to load
    driver.get(typeracer_url)
    wait = ui.WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element_by_link_text('Practice'))

    # Locate and press practice button
    practice_btn = driver.find_element_by_link_text('Practice')
    practice_btn.click()

    # Wait for race to load & start
    wait.until(lambda driver: driver.find_element_by_xpath("//*[contains(text(), 'The race is on! Type the text below:')]"))
    input_field = driver.find_element_by_class_name('txtInput')

    # Soupify the race page
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # Scrape race text from soup
    race_text = "";
    for span in soup.body.find_all('span', attrs={'unselectable': 'on'}):
        race_text += span.getText()

    print race_text

    # Enter race text into input field
    input_field.click()
    input_field.send_keys(race_text)

    # Win

except TimeoutException:
    print "Error: An element could not be located within timeout duration"

# finally: driver.quit()
