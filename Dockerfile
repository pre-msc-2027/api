FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN groupadd -r myuser && useradd -r -g myuser myuser; pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

USER myuser

CMD ["python3", "main.py"]
