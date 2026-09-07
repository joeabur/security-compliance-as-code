FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY . .
RUN pip install --no-cache-dir .
USER appuser
ENTRYPOINT ["compliance"]
