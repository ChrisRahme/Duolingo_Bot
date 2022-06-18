import json
import time

from selenium.common.exceptions    import WebDriverException
from selenium.webdriver.common.by  import By
from selenium.webdriver.support    import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait



# Selenium

def findElementByXpath(container, xpath, many = False):
    if not isinstance(xpath, list):
        xpath = [xpath]

    error = None

    for xp in xpath:
        try:
            if many:
                return container.find_elements(By.XPATH, xp)
            else:
                return container.find_element(By.XPATH, xp)
        except WebDriverException as e:
            continue
        except Exception as e:
            error = e
    
    if error:
        print('[ERROR!]\n')
        raise WebDriverException(error)
    
    return None


def findElementsByXpath(container, xpath):
    return findElementByXpath(container, xpath, True)


def findTextByXpath(container, xpath, many = False):
    element = findElementByXpath(container, xpath, many)

    if not isinstance(element, list):
        return element.text

    return [e.text for e in element]


def findTextsByXpath(container, xpath, join = True):
    texts = findTextByXpath(container, xpath, True)

    if join:
        return ' '.join(texts)
    
    return texts


def waitForXpath(container, xpath, wait = 120):
    return WebDriverWait(container, wait).until(
        expected_conditions.presence_of_element_located((By.XPATH, xpath))
    )


def isDisabled(element):
    return element.get_attribute('aria-disabled') == 'true' or element.get_attribute('disabled') == 'true'



# Helpers

def block(message = None):
    if message:
        print(message)

    while True:
        continue


def getFromDictionary(challenge, sentence):
    if len(sentence.strip()) == 0:
        block('getFromDictionary: No sentence found')

    dictionary = {}

    with open('dictionary.json', 'r') as f:
        dictionary = json.load(f)

    c = dictionary.get(challenge, None)

    if c:
        return c.get(sentence, None)

    return None


def saveToDictionary(challenge, sentence, translation):
    if len(sentence.strip()) == 0:
        block('saveToDictionary: No sentence found')

    dictionary = {}

    with open('dictionary.json', 'r') as f:
        dictionary = json.load(f)

    if dictionary.get(challenge, None) is None:
        dictionary[challenge] = {}

    dictionary[challenge][sentence] = translation

    if challenge == 'translate':
        dictionary[challenge][translation] = sentence

    with open('dictionary.json', 'w') as f:
        json.dump(dictionary, f, indent = 4)


def readJSON(file):
    with open(file) as f:
        return json.load(f)



# Duolingo

def skip(driver):
    skip = findElementByXpath(driver, '//button[@data-test="player-skip"]')
    skip.click()


def skipAndAddToDictionary(driver, challenge, sentence):
    errors = 0

    while True:
        time.sleep(1)

        try:
            skip = findElementByXpath(driver, '//button[@data-test="player-skip"]')
            skip.click()
            break
        except Exception as e:
            errors += 1
            if errors > 5:
                print(e)
                break

    errors = 0

    while True:
        try:
            time.sleep(1)

            solution = findTextByXpath(driver, [
                '//div[@class="_1UqAr _1sqiF"]',
                '//div[@class="_1UqAr _3Qruy"]'
            ]).strip()

            saveToDictionary(challenge, sentence, solution)

            return solution

        except Exception as e:
            errors += 1
            if errors > 5:
                print(e)
                break