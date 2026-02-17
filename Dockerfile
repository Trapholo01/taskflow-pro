FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.11-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV FLASK_APP=app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:create_app()"]
