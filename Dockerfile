FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN groupadd -r myuser && useradd -r -g myuser myuser; pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

USER myuser

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]