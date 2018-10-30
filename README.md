[![](https://dockerbuildbadges.quelltext.eu/status.svg?organization=gabrielrf&repository=controlid2telegram)](https://hub.docker.com/r/gabrielrf/controlid2telegram/builds/)

# ControlID to Telegram

![ControlID2Telegram](img/doorknock.gif)

* [About](#about)
* [Setup](#setup)
  * [Docker Compose](#docker-compose)
  * [Python](#python)
* [Contribute](#contribute)
* [Contact](#contact-me)

## About 

ControlID to Telegram is a Docker Container that sends a text message everytime a door is opened.

It works on a ControlID IDFlex (not sure if it works on other models) and on Telegram Messaging app.

## Setup

### Docker Compose

```
controlid2telegram:
    image: gabrielrf/controlid2telegram
    environment:
        - BOT_TOKEN=
        - ALERTS=1,2,3,4,5,6,7,8,9,10,11,12,13
        - CONTROLID_IP=
        - HOST_IP=
        - CONTROLID_USER=
        - CONTROLID_PASSWORD=
        - WEBHOOK_HOST=0.0.0.0
        - WEBHOOK_PORT=5432
        - MESSAGE_DESTINATION=
    ports:
        - 5432:5432
    restart: always
```

`BOT_TOKEN`: Telegram bot token provided by BotFather.

`ALERTS`: Categories of alerts that will be sent.
 - 1: Invalid equipment
 - 2: Invalid parameters
 - 3: Not identified
 - 4: Pending ID
 - 5: Timeout
 - 6: Access denied
 - 7: Access granted
 - 8: Pending access
 - 9: User is not admin
 - 10: Unidentified access
 - 11: Access granted by button
 - 12: Access granted by web interface/API
 - 13: Entry canceled

`CONTROLID_IP`: ControlID device ip.

`HOST_IP`: Docker host ip.

`CONTROLID_USER`: ControlID web user.

`CONTROLID_PASSWORD`: ControlID web user password.

`WEBHOOK_HOST`: Webhook host ip. Default is `0.0.0.0`.

`WEBHOOK_PORT`: Webhook port. Any number between 1023 to 65535. 

`MESSAGE_DESTINATION`: Telegram User/Group/Channel ID that will receive messages.

### Python

First:

```
pip install flask
pip install pytelegrambotapi
```

Open `index.py` and fill the variables.

Then:

```
python index.py
```

## Contribute

Pull Requests and issues are always welcome!

## Contact me

[GabRF.com](https://gabrf.com)

[@GabrielRF](https://t.me/gabrielrf) on Telegram.

