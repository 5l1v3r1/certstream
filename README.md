# Monitor new certificates

A tool that uses https://certstream.calidog.io/ to monitor new certificates and 
sends notifications to Slack.

## Install

    git clone https://github.com/reuteras/certstream.git
    cd certstream
    mkvirtualenv -p python3 certstream
    setvirtualenvproject 
    pip install -r pip-requires.txt

## Usage

Add your Slack API key to _api.key_.

Run the script:
    workon certstream
    SLACK_API_TOKEN=$(cat api.txt) python cert.py

Or run it from screen:

    screen -t certstream    4       /usr/bin/bash -c "source ~/.virtualenvs/certstream/bin/activate; cd src/certstream; SLACK_API_TOKEN=$(cat ~/src/certstream/api.txt) python cert.py | tee -a ~/tmp/certstream.log"

Screen can be automatically started with the following line in the users crontab:

    @reboot sleep 2 && /usr/bin/screen -dm
