FROM python:3.12-bullseye

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app/

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .
