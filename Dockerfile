# --------- requirements ---------

FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# --------- final image build ---------
FROM python:3.11

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Copy the entrypoint script
# COPY ./.docker/mysql/docker-entrypoint-initdb.d/init-db.sh /docker-entrypoint-initdb.d/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


COPY ./src/app /code/app
COPY ./.env /code/app/.env
RUN mkdir -p /code/tmp/uploads/
COPY ./src/tmp /code/tmp

# -------- replace with comment to run with gunicorn --------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker". "-b", "0.0.0.0:8000"]
