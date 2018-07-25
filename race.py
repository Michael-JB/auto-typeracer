from __future__ import division
import sys
import time
import argparse
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

typeracer_url = 'https://play.typeracer.com/'
element_load_timeout = 360 # (seconds)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="set the url of a multiplayer game. By default, a practice game is launched")
parser.add_argument("--wpm", help="set target wpm, by default maximum speed is used", type=int)
args = parser.parse_args()

# Set and calculate typing pace
max_speed_threshold = 1000 # (wpm)
target_wpm = args.wpm if args.wpm else max_speed_threshold
type_at_max_speed = target_wpm >= max_speed_threshold
avg_word_length = 5.1
target_spc = 1 / ((target_wpm / 60) * avg_word_length)

# Load game url from command arguments, if any
multiplayer_race = args.url
race_url = args.url if multiplayer_race else typeracer_url

# Initialise chromedriver stuff
driver = webdriver.Chrome()
wait = ui.WebDriverWait(driver, element_load_timeout)

# Launches and starts a race
def launch_race(multiplayer=True):
    # Boot chromedriver and wait for page to load
    driver.get(race_url)

    # Wait for and subsequently press start button
    start_btn = wait.until(lambda driver: driver.find_element_by_partial_link_text('join race') if multiplayer else driver.find_element_by_link_text('Practice'))
    start_btn.click()

# Bosses an ongoing race
def win_race():
    # Wait for race to load & start
    wait.until(lambda driver: driver.find_element_by_xpath("//*[contains(text(), 'The race is on! Type the text below:')]"))
    input_field = driver.find_element_by_class_name('txtInput')

    # Soupify the race page
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # Scrape race text from soup
    race_text = ""
    for span in soup.body.find_all('span', attrs={'unselectable': 'on'}):
        race_text += span.getText()

    print "Race text: " + race_text

    # Enter race text into input field
    input_field.click()
    if type_at_max_speed:
        input_field.send_keys(race_text)
    else:
        for char in race_text:
            input_field.send_keys(char)
            time.sleep(target_spc)

try:
    launch_race(multiplayer_race)
    win_race()

except TimeoutException:
    print "Error: An element could not be located within timeout duration"
    driver.quit()

except WebDriverException:
    print "Error: Invalid TypeRacer url"
    driver.quit()
