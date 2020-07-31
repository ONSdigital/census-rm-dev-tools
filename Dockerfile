FROM python:3.7-slim

RUN pip install pipenv

RUN groupadd --gid 1000 dev-tools && \
    useradd --create-home --system --uid 1000 --gid dev-tools dev-tools
WORKDIR /home/dev-tools

COPY Pipfile* /home/dev-tools/
RUN pipenv install --system --deploy
USER dev-tools

COPY --chown=dev-tools . /home/dev-tools
