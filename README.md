# README.md - Telegram User Information Retrieval Tool

This Python script is designed to retrieve information about a Telegram user, public channel, or group by their username, ID, phone number, or the URL of a message they sent. It utilizes the Telethon library to interact with the Telegram API. This README file provides an overview of the script, how to use it, and its features.

## Table of Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
3. [Functionality](#functionality)
4. [Script Description](#script-description)
5. [License](#license)

---

## Requirements

Before using this script, make sure you have the following dependencies installed:

- Python 3.x
- Telethon library
- Other libraries: argparse, colorama

You can install the required packages using pip:

```bash
pip install telethon argparse colorama
```

You will also need to obtain your Telegram API credentials (api_id and api_hash) from [Telegram's website](https://my.telegram.org/auth). Replace the placeholders in the script with your credentials.

## Usage

Run the script from the command line, providing one of the following options:

- `-u` or `--username`: To retrieve information by username.
- `-i` or `--id`: To retrieve information by user or channel ID.
- `-p` or `--phone`: To retrieve information by phone number.
- `-l` or `--url`: To retrieve information from the URL of a message sent in a public channel or group.

Example usages:

```bash
python3 script.py -u mytelegramuser
python3 script.py -i 123456789
python3 script.py -p +1234567890
python3 script.py -l https://t.me/mychannel/1234
```

Follow the prompts for authentication and input if required.

## Functionality

This script can retrieve the following information about Telegram users, channels, or groups:

- User Information:
  - User ID
  - First name
  - Last name (if available)
  - Username (if available)
  - Last seen status (online, offline, recently, last week, last month)
  - Biography (about)
  - Profile picture download (as JPG)

- Channel Information:
  - Channel ID
  - Title
  - Username (if available)
  - Description
  - Creation date
  - Profile picture download (as JPG)

- Group Information:
  - Group ID
  - Title
  - Number of administrators
  - Creation date
  - Profile picture download (as JPG)

- Phone Number Information (Temporary Contact):
  - User ID
  - First name
  - Last name (if available)
  - Username (if available)
  - Last seen status (online, offline, recently, last week, last month)
  - Biography (about)
  - Profile picture download (as JPG)
  - Restores contacts after retrieving information

- Message URL Information:
  - Retrieves information from the URL of a message in a public channel or group

## Script Description

- The script uses the Telethon library to interact with the Telegram API.
- It provides a command-line interface (CLI) for users to input their preferences.
- Users can specify the target user, channel, or group by username, ID, phone number, or URL.
- User authentication is handled within the script.
- The script downloads profile pictures and saves them as JPG files.
- Information retrieved is displayed in a readable format.

## License

This script is provided under the MIT License. You can find the full license text in the [LICENSE](LICENSE) file.

---

Feel free to use and modify this script according to your needs. If you have any questions or encounter issues, please don't hesitate to ask or report them. Happy Telegram user information retrieval!
