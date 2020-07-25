FROM nikolaik/python-nodejs:python3.7-nodejs12
COPY server/ /src
COPY client/ /tmp/client
RUN cd /tmp/client && \
    npm run build && \
    mv build/ /src/build
RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r /tmp/requirements.txt
WORKDIR /src
CMD python -m app 
