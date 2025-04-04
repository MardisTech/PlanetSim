FROM python:3.12.9

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.8.3

RUN pip install poetry

RUN mkdir /src

WORKDIR /src

COPY . /src/

RUN poetry install --no-root

CMD ["poetry", "run", "python3", "sol_sys.py"]

#pygame does not easily share graphics with your computer and contaner