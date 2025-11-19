## 1. Клонирование репозитория

```bash
git clone git@github.com:McKrei/media-detector.git
cd media-detector
```

---

## 2. Создание `.env`

```bash
cat > .env << 'EOF'
SERPER_API_KEY=your_serper_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=123456789
EOF
```

Значения `SERPER_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` заменить на реальные.

---

## 3. Файл для истории

```bash
touch media_history.json
```

---

## 4. Установка зависимостей локально (опционально, для проверки без Docker)

Если используешь `uv` локально:

```bash
uv sync
uv run main.py
```

---

## 5. Сборка Docker-образа

```bash
docker build -t media-detector:latest .
```

---

## 6. Тестовый запуск контейнера вручную

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/media_history.json:/app/media_history.json" \
  media-detector:latest
```

Проверка: в Telegram должен прийти отчёт. Если ошибок нет — идём дальше.

---

## 7. Настройка cron (автозапуск)

### Вариант для теста: каждые 2 минуты

Открыть crontab:

```bash
crontab -e
```

Добавить строку (путь `/home/user/media-detector` заменить на свой):

```bash
*/2 * * * * cd /home/user/media-detector && docker run --rm --env-file .env -v $(pwd)/media_history.json:/app/media_history.json media-detector:latest >> cron.log 2>&1
```

Сохранить файл и выйти.
`Ctrl+O`, `Enter`, `Ctrl+X` в nano.

Проверить, что задача установлена:

```bash
crontab -l
```

Через несколько минут посмотреть лог:

```bash
tail -n 50 cron.log
```


### Вариант боевой: раз в день в 09:00

В crontab вместо строки выше использовать:

```bash
0 9 * * * cd /home/user/media-detector && docker run --rm --env-file .env -v $(pwd)/media_history.json:/app/media_history.json media-detector:latest >> cron.log 2>&1
```

---
