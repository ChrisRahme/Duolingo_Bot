import time

from selenium.webdriver.common.by   import By
from selenium.webdriver.common.keys import Keys

import helpers



def listen(driver):
    challenge = 'listen'
    helpers.skip(driver)

    return


def listenTap(driver):
    challenge = 'listenTap'
    helpers.skip(driver)

    return


def speak(driver):
    challenge = 'speak'
    helpers.skip(driver)

    return


def translate(driver):
    challenge = 'translate'

    sentence = helpers.findElementByXpath(driver, '//div[@data-test="hint-token"]')

    if sentence is not None:
        sentence = sentence.find_element(By.XPATH, '..').text

    if sentence is None or len(sentence.strip()) == 0:
        sentence = helpers.findTextByXpath(driver, '//span[@data-test="hint-token"]')

    print(f'Sentence: {sentence}')
    translation = helpers.getFromDictionary(challenge, sentence)

    if translation:
        print(f'Solution: {translation}')

        input_field     = helpers.findElementByXpath(driver, '//textarea[@data-test="challenge-translate-input"]')
        keyboard_button = helpers.findElementByXpath(driver, '//button[@data-test="player-toggle-keyboard"]')

        if input_field is not None:
            input_field.send_keys(translation)
            input_field.send_keys(Keys.RETURN)
        elif keyboard_button is not None:
            if (keyboard_button.text.lower() in ['make harder', 'use keyboard']):
                keyboard_button.click()
                time.sleep(1)

            translate(driver)

    else:
        translation = helpers.skipAndAddToDictionary(driver, challenge, sentence)

        print(f'Learned solution: {translation}')


def form(driver):
    challenge = 'form'

    choices      = helpers.findElementsByXpath(driver, '//div[@data-test="challenge-judge-text"]')
    choices_text = [choice.text for choice in choices]
    choices_text.sort()
    choices_text = ' [' + ', '.join(choices_text) + ']'

    sentence = helpers.findElementByXpath(driver, '//div[@class="_2SfAl _2Hg6H"]').get_attribute('data-prompt') + choices_text

    print(f'Sentence: {sentence}')
    translation = helpers.getFromDictionary(challenge, sentence)

    if translation:
        print(f'Solution: {translation}')

        for choice in choices:
            if choice.text == translation:
                choice.click()
                break

    else:
        translation = helpers.skipAndAddToDictionary(driver, challenge, sentence)

        print(f'Learned solution: {translation}')


def select(driver):
    challenge = 'select'

    sentence = helpers.findTextByXpath(driver, '//h1[@data-test="challenge-header"]')

    print(f'Sentence: {sentence}')
    translation = helpers.getFromDictionary(challenge, sentence)

    if translation:
        print(f'Solution: {translation}')

        choices = helpers.findElementsByXpath(driver, '//div[@data-test="challenge-choice"]')

        for choice in choices:
            if helpers.findElementsByXpath(choice, '//span[@class="HaQTI"]').text == translation:
                choice.click()
                break

    else:
        translation = helpers.skipAndAddToDictionary(driver, challenge, sentence)

        print(f'Learned solution: {translation}')


def name(driver):
    challenge = 'name'

    sentence = helpers.findTextByXpath(driver, '//h1[@data-test="challenge-header"]')

    print(f'Sentence: {sentence}')
    translation = helpers.getFromDictionary(challenge, sentence)

    if translation:
        print(f'Solution: {translation}')

        input_field = helpers.findElementByXpath(driver, '//input[@data-test="challenge-text-input"]')
        input_field.send_keys(translation)
        input_field.send_keys(Keys.RETURN)

    else:
        translation = helpers.skipAndAddToDictionary(driver, challenge, sentence)

        print(f'Learned solution: {translation}')


def completeReverseTranslation(driver):
    challenge = 'completeReverseTranslation'

    keyboard_button = helpers.findElementByXpath(driver, '//button[@data-test="player-toggle-keyboard"]')

    if keyboard_button is not None:
        if (keyboard_button.text.lower() in ['make harder', 'use keyboard']):
            keyboard_button.click()
            time.sleep(1)

        translate(driver)

    else:
        print('No keyboard button found')
        helpers.block()