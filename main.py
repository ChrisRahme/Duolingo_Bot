import time

from selenium                          import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui     import WebDriverWait

import challenges
import helpers



def getChromeOptions():
    options = Options()

    options.add_argument('--log-level=3')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')

    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    if settings['incognito']:
        options.add_argument('--incognito')

    if settings['mute']:
        options.add_argument('--mute-audio')

    if settings['headless']:
        options.add_argument('--headless')

    return options


def login():
    driver.get('https://www.duolingo.com')
    helpers.waitForXpath(driver, '//button[@data-test="have-account"]').click()

    username_input = helpers.waitForXpath(driver,       '//input[@data-test="email-input"]')
    password_input = helpers.findElementByXpath(driver, '//input[@data-test="password-input"]')
    login_button   = helpers.findElementByXpath(driver, '//button[@data-test="register-button"]')
    
    username_input.send_keys(credentials['username'])
    password_input.send_keys(credentials['password'])
    login_button.click()

    wait = WebDriverWait(driver, 120)
    wait.until(lambda driver: driver.current_url == 'https://www.duolingo.com/learn')


def checkChallenge():
    challenges = ['translate', 'listen', 'listenTap', 'speak', 'form', 'name', 'select', 'completeReverseTranslation']

    for challenge in challenges:
        if helpers.findElementByXpath(driver, f'//div[@data-test="challenge challenge-{challenge}"]'):
            print(f'\n>>> Challenge: {challenge}')
            return challenge


def practiceCourse(practice):
    challenge = None
    url       = 'https://www.duolingo.com/practice' if practice else 'https://www.duolingo.com/learn'

    driver.get(url)
    wait = WebDriverWait(driver, 120)
    wait.until(lambda driver: driver.current_url == url)

    while challenge is None:
        if not practice:
            input('Choose a skill and press enter.')

        time.sleep(1)
        challenge = checkChallenge()

    while challenge is not None:
        time.sleep(1)

        continue_button = helpers.waitForXpath(driver, '//button[@data-test="player-next"]', 5)

        if continue_button and not helpers.isDisabled(continue_button):
            continue_button.click()
            continue

        challenge = checkChallenge()

        if challenge is not None:
            challenge_function = getattr(challenges, challenge)
            challenge_function(driver)



if __name__ == '__main__':
    global credentials
    global settings
    global driver

    settings    = helpers.readJSON('settings.json')
    credentials = helpers.readJSON('credentials.json')

    driver = webdriver.Chrome(
        service = ChromeService(executable_path = settings['chromedriver_path']),
        options = getChromeOptions()
    )

    login()

    while True:
        try:
            practiceCourse(not settings['headless'] and settings['practice'])
        except Exception as e:
            time.sleep(5)
            continue