# Arxan — Telegram bot (panelga kirish). aiogram 2.x Python 3.11 da ishlaydi
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN useradd --uid 1000 bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
USER bot
CMD ["python", "-X", "utf8", "app.py"]
