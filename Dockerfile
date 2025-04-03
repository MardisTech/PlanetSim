FROM 3.12.9-bookworm

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir src

WORKDIR /src

COPY . /src/

CMD [ "python3", "sol_sys.py" ]