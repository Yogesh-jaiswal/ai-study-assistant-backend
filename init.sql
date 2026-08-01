-- Creating Databases

SELECT 'CREATE DATABASE ai_study_assistant'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'ai_study_assistant'
)\gexec

SELECT 'CREATE DATABASE ai_study_assistant_test'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'ai_study_assistant_test'
)\gexec

SELECT 'CREATE DATABASE ai_study_assistant_prod'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'ai_study_assistant_prod'
)\gexec

-- Creating Extensions

\connect ai_study_assistant
CREATE EXTENSION IF NOT EXISTS vector;

\connect ai_study_assistant_test
CREATE EXTENSION IF NOT EXISTS vector;

\connect ai_study_assistant_prod
CREATE EXTENSION IF NOT EXISTS vector;