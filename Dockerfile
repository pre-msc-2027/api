FROM python:3.9

WORKDIR /code

# Install base dependencies including JDK
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    #    openjdk-21-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME (if needed by your custom CLI)
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Install Trivy
# RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin

# Add your custom Java CLI
# COPY analyzer.jar /usr/local/bin/
# RUN echo '#!/bin/bash\njava -jar /usr/local/bin/analyzer.jar "$@"' > /usr/local/bin/analyzer \
#    && chmod +x /usr/local/bin/analyzer

COPY ./requirements.txt /code/requirements.txt

RUN groupadd -r myuser && useradd -r -g myuser myuser; pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

USER myuser

CMD ["python3", "main.py"]
