# Gray enroller

## Optional

- Create a Python virtual environment: `python -m venv .venv`.

## Requirements

1. Install the libraries included in `requirements.txt`: `pip install -r requirements.txt`.

	The `requirements.txt` includes the following libraries:

	- `selenium`.

	- `python-dotenv`.

	> If you created a Python virtual environment, remember to activate it.

2. Download a WebDriver.

	- [Chromium based browsers](https://googlechromelabs.github.io/chrome-for-testing/#stable).

	- [Firefox based browsers](https://github.com/mozilla/geckodriver/releases).

3. Create a `.env` file to store the credentials: `touch .env`.

	The file content must follow the following structure:

	```
	BROWSER=
	BROWSER_PATH=
	WEBDRIVER_PATH=
	SIRA_USERNAME=
	SIRA_PASSWORD=
	```

4. Create `subjects_to_enroll.json` and `subjects_to_cancel.json`: `touch subjects_to_enroll.json subjects_to_cancel.json`.

	Those files' content must follow the following structure:

	```
	[
		{
			"code": "<code>",
			"group": "<group>"
		}
	]
	```

5. Run the script: `python main.py`.
