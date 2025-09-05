FROM eclipse-temurin:24-noble

WORKDIR /code



# Install base dependencies includi JDK
RUN apt update && apt install -y \
    curl \
    wget \
    unzip \
    software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.13-full -y
RUN python3.13 -m ensurepip --upgrade

COPY ./requirements.txt /code/requirements.txt

# Telecharge l'analyser
RUN curl -v https://github.com/pre-msc-2027/analyser/releases/download/1.1.2/analyser-1.1.2.jar --output analyse.jar


# Copie les scripts d'ia
COPY ../ /code/ai

ENV AI_DIRECTORY_PATH=/code/ai

RUN python3.13 -m pip install -r /code/requirements.txt

COPY . /code/

CMD ["python3.13", "main.py"]
