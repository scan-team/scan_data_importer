FROM python:3.8

RUN pip install pipenv
COPY check_update.py  import_data.py  import_data_multi.py  test.py ./
COPY Pipfile Pipfile.lock ./
COPY grrm_data ./
RUN pipenv install --system
#RUN pipenv update grrmlog_parser
