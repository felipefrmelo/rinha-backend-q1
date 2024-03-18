# 
FROM python:3.12 as requirements-stage

# 
WORKDIR /tmp

# 
RUN pip install poetry

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.12-slim

# 
WORKDIR /code

# 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./rinha_de_backend /code/rinha_de_backend

# 


#CMD ["uvicorn", "rinha_de_backend.entrypoints.web.servers.starlette:app", "--host", "0.0.0.0", "--port", "3000",  "--log-level", "error", "--loop", "uvloop"]
#CMD ["python", "-m",  "rinha_de_backend.entrypoints.web.servers.uvicorn"]
#CMD python -m rinha_de_backend.entrypoints.web.servers.robyn
#CMD ["hypercorn", "rinha_de_backend.entrypoints.web.servers.asgi:app", "--bind", "0.0.0.0:3000", "--log-level", "error", "--access-log", "-", "--worker-class", "uvloop"]
#CMD ["granian",  "--interface", "asgi",  "rinha_de_backend.entrypoints.web.servers.asgi:app", "--host", "0.0.0.0", "--port", "3000", "--loop", "uvloop", "--log-level", "error", "--opt", "--threading-mode", "workers", "--workers", "1"]



# for development
#CMD tail -f /dev/null

