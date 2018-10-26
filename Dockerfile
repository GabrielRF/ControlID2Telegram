FROM python:3.7-alpine

RUN pip install flask
RUN pip install pytelegrambotapi

ADD index.py / 

CMD [ "python", "./index.py" ]

