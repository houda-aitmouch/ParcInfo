import csv
from typing import Optional
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.commande_informatique.models import Designation, Description
from apps.materiel_informatique.models import MaterielInformatique


class Command(BaseCommand):
    help = (
        "Importe le fichier 'liste_materiel_info.csv' (colonnes: Catégorie,Designation,Is public,Description) "
        "et met à jour Description.public puis synchronise MaterielInformatique.public."
    )

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Chemin du fichier CSV source')
        parser.add_argument('--delimiter', type=str, default=',', help='Délimiteur CSV (par défaut ,)')
        parser.add_argument('--dry-run', action='store_true', help='Ne pas écrire, juste simuler')
        parser.add_argument('--create-missing', action='store_true', help="Créer les descriptions manquantes si introuvables")

    def _oui_non_to_bool(self, value: str) -> Optional[bool]:
        if value is None:
            return None
        v = value.strip().lower()
        if v in {'oui', 'yes', 'true', 'vrai', '1'}:
            return True
        if v in {'non', 'no', 'false', 'faux', '0'}:
            return False
        return None

    def _normalize(self, s: str) -> str:
        if s is None:
            return ''
        out = s.strip()
        # Remplacer les guillemets spéciaux et normaliser espaces
        for ch in ['\u2019', '\u2018', '\u201C', '\u201D', '“', '”', '’', '‘']:
            out = out.replace(ch, "'")
        out = ' '.join(out.split())
        return out

    def _find_designation(self, name: str) -> Optional[Designation]:
        name_n = self._normalize(name)
        if not name_n:
            return None
        try:
            return Designation.objects.get(nom=name_n)
        except Designation.DoesNotExist:
            qs = Designation.objects.filter(nom__iexact=name_n)
            if qs.count() == 1:
                return qs.first()
            qs2 = Designation.objects.filter(nom__icontains=name_n)
            if qs2.count() == 1:
                return qs2.first()
        return None

    def _find_description(self, designation: Designation, name: str) -> Optional[Description]:
        name_n = self._normalize(name)
        if not designation or not name_n:
            return None
        try:
            return Description.objects.get(designation=designation, nom=name_n)
        except Description.DoesNotExist:
            qs = Description.objects.filter(designation=designation, nom__iexact=name_n)
            if qs.count() == 1:
                return qs.first()
            qs2 = Description.objects.filter(designation=designation, nom__icontains=name_n)
            if qs2.count() == 1:
                return qs2.first()
        return None

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = options['csv_path']
        delimiter = options['delimiter']
        dry_run = options['dry_run']
        create_missing = options['create_missing']

        try:
            f = open(csv_path, newline='', encoding='utf-8')
        except OSError as e:
            raise CommandError(f"Impossible d'ouvrir {csv_path}: {e}")

        updated_desc = 0
        not_found = []
        last_designation_name = None

        with f:
            reader = csv.DictReader(f, delimiter=delimiter)
            # Normaliser en-têtes possibles
            headers = [h.strip().lower() for h in (reader.fieldnames or [])]
            required_any = {'designation', 'is public', 'description'}
            if not required_any.issubset(set(headers)):
                raise CommandError("En-têtes requis: Designation, Is public, Description")

            for row in reader:
                designation_name = (row.get('Designation') or row.get('designation') or '').strip()
                if not designation_name:
                    # forward-fill de la dernière désignation rencontrée
                    designation_name = last_designation_name
                else:
                    last_designation_name = designation_name

                desc_name = (row.get('Description') or row.get('description') or '').strip()
                is_public_raw = (row.get('Is public') or row.get('is public') or '').strip()

                if not designation_name or not desc_name:
                    continue  # lignes vides/section titre, on saute

                public_val = self._oui_non_to_bool(is_public_raw)
                if public_val is None:
                    # si non spécifié sur la ligne, ne change pas la valeur actuelle
                    continue

                designation = self._find_designation(designation_name)
                if not designation:
                    not_found.append((designation_name, desc_name, 'designation'))
                    continue

                description = self._find_description(designation, desc_name)
                if not description:
                    if create_missing and not dry_run:
                        description = Description.objects.create(
                            designation=designation,
                            nom=self._normalize(desc_name),
                            public=public_val if public_val is not None else True,
                        )
                        self.stdout.write(self.style.WARNING(
                            f"Description créée: {designation_name} / {description.nom} (public={description.public})"
                        ))
                    else:
                        not_found.append((designation_name, desc_name, 'description'))
                        continue

                if description.public != public_val:
                    self.stdout.write(
                        f"Description '{designation_name} / {desc_name}': {description.public} -> {public_val}"
                    )
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


