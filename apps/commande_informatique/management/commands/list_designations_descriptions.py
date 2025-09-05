from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.commande_informatique.models import Designation, Description
from apps.materiel_informatique.models import MaterielInformatique


class Command(BaseCommand):
    help = "Affiche la liste des désignations avec leurs descriptions, champ public et nombre de matériels liés (CSV)."

    def add_arguments(self, parser):
        parser.add_argument('--show-zero', action='store_true', help='Inclure les descriptions sans matériels liés')

    def handle(self, *args, **options):
        show_zero = options['show_zero']

        # Pré-calcul du nombre de matériels par description
        counts = (
            MaterielInformatique.objects.values('ligne_commande__description_id')
            .annotate(n=Count('id'))
        )
        desc_id_to_count = {row['ligne_commande__description_id']: row['n'] for row in counts}

        self.stdout.write('designation,description,public,materiels_count')
        for designation in Designation.objects.all().order_by('nom'):
            for description in Description.objects.filter(designation=designation).order_by('nom'):
                n = desc_id_to_count.get(description.id, 0)
                if not show_zero and n == 0:
                    continue
                public_str = 'true' if description.public else 'false'
                # Échapper les virgules via guillemets CSV simples
                d_name = designation.nom.replace('"', "''")
                desc_name = description.nom.replace('"', "''")
                self.stdout.write(f'"{d_name}","{desc_name}",{public_str},{n}')


