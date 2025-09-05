from django.core.management.base import BaseCommand
from apps.materiel_informatique.models import MaterielInformatique


class Command(BaseCommand):
    help = "Backfill MaterielInformatique.public from ligne_commande.description.public"

    def handle(self, *args, **options):
        updated = 0
        total = 0
        for mat in MaterielInformatique.objects.select_related(
            'ligne_commande__description'
        ).all():
            total += 1
            try:
                desc = mat.ligne_commande.description if mat.ligne_commande else None
                if desc is None:
                    continue
                new_public = bool(getattr(desc, 'public', True))
                if mat.public != new_public:
                    mat.public = new_public
                    mat.save(update_fields=['public'])
                    updated += 1
            except Exception:
                continue

        self.stdout.write(self.style.SUCCESS(
            f"Sync done. Updated {updated}/{total} MaterielInformatique rows."
        ))


