# Description

This Python bot is designed to monitor UTE/concursos website for job postings, but it can be easily adapted to other websites.

It scrapes the content from the target webpage and filters out job postings containing specific keywords,
it is intended to be used as a daily scheduled task, for instance, using cron.

## Installation

```bash
git clone git@github.com:guidodinello/scrapper_bot.git
cd bot
pip3 install -r requirements.txt
chmod +x runner.sh
```

## Usage

crontab -e

> Note: Cron Syntax, minute hour \* \* \* command-to-be-executed

```bash
0 12 * * * /path/to/project/folder/runner.sh
```

> Note: The following example will run the bot every day at 12:00
