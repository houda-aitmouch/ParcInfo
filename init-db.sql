-- Script d'initialisation de la base de données PostgreSQL
-- Installation de l'extension pgvector pour le chatbot

-- Créer l'extension pgvector si elle n'existe pas
CREATE EXTENSION IF NOT EXISTS vector;

-- Vérifier que l'extension est bien installée
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Message de confirmation
DO $$
BEGIN
    RAISE NOTICE 'Base de données initialisée avec succès avec pgvector';
END $$;
