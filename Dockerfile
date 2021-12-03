FROM python

EXPOSE 8000

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY . .

RUN poetry install

CMD poetry run uvicorn hospital_service.main:app --host=0.0.0.0