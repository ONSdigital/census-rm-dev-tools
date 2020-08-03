FROM python:3.7-slim

RUN pip install pipenv

    # Apt packages are required to run gcloud commands for whitelisting
RUN apt-get update && \
    apt-get -yq install curl && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get -yq install apt-transport-https ca-certificates gnupg && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get -yq install google-cloud-sdk && \
    apt-get -yq install kubectl && \
    apt-get -yq clean && \
    groupadd --gid 1000 dev-tools && \
    useradd --create-home --system --uid 1000 --gid dev-tools dev-tools
WORKDIR /home/dev-tools

COPY Pipfile* /home/dev-tools/
RUN pipenv install --system --deploy
USER dev-tools

COPY --chown=dev-tools . /home/dev-tools
