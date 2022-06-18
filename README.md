# Duolingo XP Farmer & Learner

## 1. Requirements

1. Install Chrome and its according Chromedriver version

1. Install Python 3.8, 3.9, or 3.10 (more versions could be compatible)

1. Install Selenium 4.0.0 (more versions could be compatible):

    ```shell
    pip install selenium==4.0.0
    ```

## 2. Setup

1. Create a `dictionary.json` file, then copy and paste the following content:

    ```json
    {}
    ```

1. Create a `credentials.json` file, then copy and paste the following content then enter your correct username and password:

    ```json
    {
        "username" : "your_username",
        "password" : "your_password"
    }
    ```

1. Open `settings.json` and set your own settings:

    ```json
    {
        "chromedriver_path" : "C:/Path/to/chromedriver.exe",

        "headless"          : false,
        "incognito"         : false,
        "mute"              : false,

        "practice"          : true
    }
    ```

    - `chromedriver_path` is the full path to the appropriate Chromedriver for your Chrome version
    - `headless` will make the program run in the background if set to `true`
    - `incognito` will open Chrome in incognito mode if set to `true`
    - `mute` will mute Chrome if set to `true`
    - `practice` will let the program learn and run forver if set to `true`, otherwise you will be asked to manually enter a skill every time

    Note: If `headless` is set to `true`, the program will always run in practice mode

## 3. Start

Open `main.py`. A new Chrome window with Duolingo will open and the bot will log you in.

The bot will keep making mistakes at first, but once a sentence has been learned, it will be memorized (unless `dictionary.json` is erased).

In practice mode, it will keep going to [duolingo.com/practice](https://www.duolingo.com/practice) and practice infinitely. Otherwise, it will open [duolingo.com/learn](https://www.duolingo.com/learn), and ask you to open a skill every time.

The supported challenges are:

- **Translate**, where you are asked to translate from one language to another
- **Name**, where you must translate a single word
- **Form**, where you must fill in the blanks
- **Select**, where you select the picture and translation representing a given word

The listening and speaking challenges are always skipped. There may be other types of challenges I do not know of - When encoutering these, the skill will be restarted.
