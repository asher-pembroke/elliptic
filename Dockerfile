FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y gcc python3-dev


# RUN pip install --user -r requirements.txt
RUN pip install --user git+https://github.com/predsci/psidash.git
RUN pip install notebook
RUN pip install jupytext

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

COPY . /home/elliptic

WORKDIR /home/elliptic

RUN jupyter nbextension enable --py jupytext
RUN jupyter nbextension install --py jupytext


# CMD jupyter notebook . --port=8888 --no-browser --ip=0.0.0.0 --allow-root

# # CMD python elliptic.py


