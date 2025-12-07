-- Создать базы данных для Moodle и RAG Service
CREATE DATABASE moodle;
CREATE DATABASE rag_service;

-- Создать пользователя для Moodle
CREATE USER moodle WITH PASSWORD 'MoodleSecurePass456!';
GRANT ALL PRIVILEGES ON DATABASE moodle TO moodle;

-- Создать пользователя для RAG
CREATE USER rag_user WITH PASSWORD 'RAGSecurePass789!';
GRANT ALL PRIVILEGES ON DATABASE rag_service TO rag_user;

-- Подключиться к БД и дать права на схему
\c moodle
GRANT ALL ON SCHEMA public TO moodle;

\c rag_service
GRANT ALL ON SCHEMA public TO rag_user;

