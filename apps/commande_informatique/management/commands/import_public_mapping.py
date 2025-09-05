import csv
from typing import Optional
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.commande_informatique.models import Designation, Description
from apps.materiel_informatique.models import MaterielInformatique


class Command(BaseCommand):
    help = (
        "Importe un mapping CSV (designation,description,public) pour mettre à jour Description.public, "
        "puis synchronise MaterielInformatique.public en conséquence."
    )

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Chemin du fichier CSV')
        parser.add_argument('--delimiter', type=str, default=',', help='Délimiteur CSV (par défaut ,)')
        parser.add_argument('--dry-run', action='store_true', help='Affiche ce qui serait fait sans enregistrer')

    def _to_bool(self, value: str) -> Optional[bool]:
        if value is None:
            return None
        v = value.strip().lower()
        if v in {'true', 'vrai', '1', 'yes', 'oui'}:
            return True
        if v in {'false', 'faux', '0', 'no', 'non'}:
            return False
        return None

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = options['csv_path']
        delimiter = options['delimiter']
        dry_run = options['dry_run']

        try:
            f = open(csv_path, newline='', encoding='utf-8')
        except OSError as e:
            raise CommandError(f"Impossible d'ouvrir {csv_path}: {e}")

        updated_desc = 0
        not_found = []

        with f:
            reader = csv.DictReader(f, delimiter=delimiter)
            required = {'designation', 'description', 'public'}
            if not required.issubset(set(h.strip().lower() for h in reader.fieldnames or [])):
                raise CommandError("En-têtes requis: designation, description, public")

            for row in reader:
                des_name = (row.get('designation') or '').strip()
                desc_name = (row.get('description') or '').strip()
                public_val = self._to_bool(row.get('public'))
                if not des_name or not desc_name or public_val is None:
                    continue

                try:
                    designation = Designation.objects.get(nom=des_name)
                except Designation.DoesNotExist:
                    not_found.append((des_name, desc_name, 'designation'))
                    continue

                try:
                    description = Description.objects.get(designation=designation, nom=desc_name)
                except Description.DoesNotExist:
                    not_found.append((des_name, desc_name, 'description'))
                    continue

                if description.public != public_val:
                    self.stdout.write(f"Description '{des_name} / {desc_name}': {description.public} -> {public_val}")
                    if not dry_run:
                        description.public = public_val
                        description.save(update_fields=['public'])
                    updated_desc += 1

        # Synchroniser les matériels
        updated_mat = 0
        if not dry_run:
            for mat in MaterielInformatique.objects.select_related('ligne_commande__description').all():
                desc = mat.ligne_commande.description if mat.ligne_commande else None
                if desc is None:
                    continue
                new_public = bool(getattr(desc, 'public', True))
                if mat.public != new_public:
                    mat.public = new_public
                    mat.save(update_fields=['public'])
                    updated_mat += 1

        self.stdout.write(self.style.SUCCESS(
            f"Descriptions mises à jour: {updated_desc}. Materiels synchronisés: {updated_mat}."
        ))

        if not_found:
            self.stdout.write(self.style.WARNING(
                f"Non trouvés ({len(not_found)}): " + ", ".join([f"{d}/{c}:{t}" for d,c,t in not_found])
            ))


