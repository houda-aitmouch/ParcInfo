import os
import django
from django.apps import apps

# 1️⃣ Configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ParcInfo.settings")  # adapte si le nom du projet change
django.setup()

# 2️⃣ Récupérer tous les modèles
all_models = apps.get_models()
print(f"📦 {len(all_models)} modèles trouvés.\n")

# 3️⃣ Afficher les modèles avec leurs champs
for model in all_models:
    table_name = model._meta.db_table
    verbose_name = model._meta.verbose_name
    print(f"📂 Table : {table_name} ({verbose_name})")

    fields = model._meta.get_fields()
    for field in fields:
        try:
            field_name = field.name
            field_type = field.get_internal_type()
            print(f"   - {field_name} : {field_type}")
        except AttributeError:
            # Certains champs comme les relations inverses n'ont pas de get_internal_type
            print(f"   - {field.name} : Relation/Reverse field")
    print("-" * 50)