FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml setup.py ./
RUN pip wheel --no-deps .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/wheels /app/wheels
COPY . .
RUN pip install --no-cache-dir *.whl
USER nobody
ENV PYTHONUNBUFFERED=1
CMD ["python", "server.py"]
