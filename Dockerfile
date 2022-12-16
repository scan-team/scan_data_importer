FROM python:3.8

RUN pip install pipenv
COPY . .
RUN pipenv install --system
RUN pipenv update grrmlog_parser
