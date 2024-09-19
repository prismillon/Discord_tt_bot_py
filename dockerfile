FROM python:3.12.3-slim-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "/app/bot.py" ]