FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends locales \
    && sed -i '/^# *ko_KR.UTF-8 UTF-8/s/^# *//' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=ko_KR.UTF-8 \
    LC_ALL=ko_KR.UTF-8

COPY pyproject.toml /app/
RUN pip install --no-cache-dir \
    "apscheduler>=3.11.0" \
    "instagrapi~=2.2.1" \
    "pillow~=11.3.0" \
    "python-dotenv~=1.1.1" \
    "pytz~=2025.2" \
    "requests~=2.32.4" \
    "schedule~=1.2.2"

COPY . /app

CMD ["python", "main.py"]
