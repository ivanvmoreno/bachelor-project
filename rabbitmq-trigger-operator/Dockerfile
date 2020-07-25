FROM python:3.7
RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r /tmp/requirements.txt
COPY app/ /src
CMD kopf run /src/run.py --verbose
