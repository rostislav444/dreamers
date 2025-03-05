#!/bin/bash

# Создаём директорию для скриншотов, если она не существует
SCREENSHOT_DIR="$HOME/screenshots"
mkdir -p "$SCREENSHOT_DIR"

# Проверяем текущие настройки
echo "Текущая директория для скриншотов:"
defaults read com.apple.screencapture location

# Изменяем директорию для сохранения скриншотов
defaults write com.apple.screencapture location "$SCREENSHOT_DIR"

# Перезагружаем системный UI сервер для применения изменений
killall SystemUIServer

# Устанавливаем права доступа
chmod 755 "$SCREENSHOT_DIR"

# Проверяем новые настройки
echo "Новая директория для скриншотов:"
defaults read com.apple.screencapture location

echo "Готово! Теперь все скриншоты будут сохраняться в $SCREENSHOT_DIR"

# Дополнительные настройки (раскомментируйте, если нужно):

# Изменить формат скриншотов на JPG (по умолчанию PNG)
# defaults write com.apple.screencapture type jpg

# Отключить эффект тени на скриншотах
# defaults write com.apple.screencapture disable-shadow -bool true

# Изменить префикс имени файла (по умолчанию "Screenshot")
# defaults write com.apple.screencapture name "скриншот"

# Отключить превью скриншота в углу экрана
# defaults write com.apple.screencapture show-thumbnail -bool false
