#!/bin/bash

# Загружаем настройки из .env файла
DB_HOST=$(grep "DB_HOST=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")
DB_PORT=$(grep "DB_PORT=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")
DB_NAME=$(grep "DB_NAME=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")
DB_USER=$(grep "DB_USER=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")
DB_PASSWORD=$(grep "DB_PASSWORD=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")
DUMP_FOLDER=$(grep "DUMP_FOLDER=" backend/.env | cut -d '=' -f2 | tr -d '[:space:]' | tr -d "'")

# Создаем директорию для бекапов если её нет
mkdir -p $DUMP_FOLDER

# Формируем имя файла с текущей датой
BACKUP_FILENAME="db-backup-$(date +%Y-%m-%d)"
BACKUP_PATH="$DUMP_FOLDER/$BACKUP_FILENAME"

# Устанавливаем переменную окружения для пароля
export PGPASSWORD=$DB_PASSWORD

# Делаем бекап
echo "Создаем бекап базы данных $DB_NAME..."
if pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -Fc $DB_NAME > "$BACKUP_PATH"; then
    echo "Бекап успешно создан: $BACKUP_PATH"
else
    echo "Ошибка при создании бекапа"
    rm -f "$BACKUP_PATH"  # Удаляем неполный файл бекапа
    exit 1
fi

# Очищаем переменную окружения с паролем
unset PGPASSWORD