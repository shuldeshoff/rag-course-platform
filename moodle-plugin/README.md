# Moodle AI Assistant Block Plugin

Блок-плагин для интеграции AI-ассистента с RAG в Moodle LMS.

## Установка

### Автоматическая установка

1. Скачать ZIP архив плагина
2. В Moodle: Site administration → Plugins → Install plugins
3. Загрузить ZIP файл
4. Следовать инструкциям мастера

### Ручная установка

```bash
cd /path/to/moodle
cp -r moodle-plugin blocks/aiassistant
sudo -u www-data php admin/cli/upgrade.php
```

## Настройка

1. Site administration → Plugins → Blocks → AI Assistant

2. Установить параметры:
   - **RAG Service URL**: http://your-server:8000
   - **API Token**: ваш токен из RAG сервиса
   - **Request Timeout**: 10 секунд
   - **Enable Logging**: включено
   - **Max Question Length**: 500 символов

3. Сохранить изменения

## Добавление на курс

1. Открыть курс
2. Включить редактирование (Turn editing on)
3. Add a block → AI Assistant
4. Блок появится на странице курса

## Использование

Студенты и преподаватели могут:
- Задавать вопросы по материалам курса
- Получать ответы на основе RAG
- Видеть источники информации

## Требования

- Moodle 3.9 или выше
- PHP 7.4+
- Настроенный RAG сервис
- cURL extension

## Права доступа

- `block/aiassistant:addinstance` - добавление блока
- `block/aiassistant:askquestion` - задавать вопросы

## Структура

```
block_aiassistant/
├── version.php              # Версия плагина
├── block_aiassistant.php    # Основной класс
├── settings.php             # Настройки админа
├── ajax.php                 # AJAX обработчик
├── db/
│   ├── access.php          # Права
│   └── install.xml         # Схема БД
├── lang/
│   ├── en/                 # Английский
│   └── ru/                 # Русский
├── classes/
│   ├── api_client.php      # HTTP клиент
│   └── output/renderer.php # Рендерер
├── amd/src/chat.js         # JavaScript
├── templates/              # Mustache шаблоны
└── styles.css              # CSS стили
```

## Лицензия

GPL v3
