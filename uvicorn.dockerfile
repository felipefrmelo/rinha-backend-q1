# 
FROM python:3.12 as requirements-stage

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with uvicorn

# 
FROM python:3.12-alpine

# 
WORKDIR /code

# 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./rinha_de_backend /code/rinha_de_backend

# 

CMD ["python", "-m",  "rinha_de_backend.entrypoints.web.servers.uvicorn"]
