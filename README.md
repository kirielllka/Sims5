# README.md

## Sims5 - Telegram Bot

Этот телеграм-бот позволяет наблюдать за демографическим развитием в реальном времени. Бот анализирует данные , предоставляя пользователям статистику.

### 🔧 Установка и настройка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/kirielllka/sims5.git
   cd sims5
   ```

2. **Установите зависимости**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Настройте базу данных PostgreSQL**
   - Установите PostgreSQL
   - Создайте базу данных:
     ```sql
     CREATE DATABASE database_name;
     CREATE USER user WITH PASSWORD 'your_password';

4. **Создайте Telegram бота**
   - Через @BotFather в Telegram
   - Получите API-токен

5. **Настройте переменные окружения**
   Создайте файл `.env` в корне проекта и заполните его:
   ```ini
   DATABASE_URL=postgresql://user:your_password@localhost:5432/database_name
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token

### 🚀 Запуск бота
```bash
python main.py
```

### ⚙️ Функционал бота
-  Просмотр людей
-  Создание пары 
-  Отоброжение статистикиа
-  Симуляция 1 месяца, 1/5/25 лет

### 📦 Зависимости
Основные зависимости указаны в `pyproject.toml`:
- sqlalchemy (orm для взаимодействия с бд)
- psycopg2 (PostgreSQL adapter)
- matplotlib (для анализа данных)
- requests (для API запросов)

### 📝 Лицензия
MIT License

---

Для форматирования кода перед коммитом используйте:
```bash
black .
```
