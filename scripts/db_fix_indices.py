import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

SQL_STATEMENTS = [
    # Materiel Informatique indexes
    """
    CREATE INDEX IF NOT EXISTS idx_mi_code_inventaire 
    ON materiel_informatique_materielinformatique (code_inventaire);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_mi_numero_serie 
    ON materiel_informatique_materielinformatique (numero_serie);
    """,
    # Commande Informatique indexes
    """
    CREATE INDEX IF NOT EXISTS idx_cmd_numero_commande 
    ON commande_informatique_commande (numero_commande);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_cmd_fournisseur 
    ON commande_informatique_commande (fournisseur_id);
    """,
    # Fournisseur ICE
    """
    CREATE INDEX IF NOT EXISTS idx_fournisseur_ice 
    ON fournisseurs_fournisseur (ice);
    """,
    # Livraison → relies on actual schema; skip if column not present
    """
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='livraison_livraison' AND column_name='commande_id'
        ) THEN
            EXECUTE 'CREATE INDEX IF NOT EXISTS idx_livraison_commande ON livraison_livraison (commande_id)';
        END IF;
    END$$;
    """,
]

VERIFY_QUERIES = {
    'idx_mi_code_inventaire': "SELECT 1 FROM pg_indexes WHERE indexname='idx_mi_code_inventaire'",
    'idx_mi_numero_serie': "SELECT 1 FROM pg_indexes WHERE indexname='idx_mi_numero_serie'",
    'idx_cmd_numero_commande': "SELECT 1 FROM pg_indexes WHERE indexname='idx_cmd_numero_commande'",
    'idx_cmd_fournisseur': "SELECT 1 FROM pg_indexes WHERE indexname='idx_cmd_fournisseur'",
    'idx_fournisseur_ice': "SELECT 1 FROM pg_indexes WHERE indexname='idx_fournisseur_ice'",
    'idx_livraison_commande': "SELECT 1 FROM pg_indexes WHERE indexname='idx_livraison_commande'",
}

def apply_fixes():
    with connection.cursor() as cursor:
        for sql in SQL_STATEMENTS:
            try:
                cursor.execute(sql)
                print("Applied:", sql.split('\n')[0][:60], '...')
            except Exception as e:
                print("Skip/Err:", str(e))

    with connection.cursor() as cursor:
        for name, q in VERIFY_QUERIES.items():
            try:
                cursor.execute(q)
                exists = cursor.fetchone() is not None
                print(f"Verify {name}:", "OK" if exists else "MISSING")
            except Exception as e:
                print(f"Verify {name} error:", e)

if __name__ == '__main__':
    apply_fixes()
