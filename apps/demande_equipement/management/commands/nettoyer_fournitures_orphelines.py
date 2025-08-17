from django.core.management.base import BaseCommand
from django.db import transaction
from apps.demande_equipement.models import DemandeEquipement, ArchiveDecharge


class Command(BaseCommand):
    help = 'Nettoie les demandes de fournitures qui n\'ont pas de fourniture sélectionnée'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait supprimé sans effectuer la suppression',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la suppression même si des décharges sont signées',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        # Trouver toutes les demandes de fournitures sans fourniture sélectionnée
        demandes_orphelines = DemandeEquipement.objects.filter(
            type_article='fourniture',
            fourniture__isnull=True
        )
        
        if not demandes_orphelines.exists():
            self.stdout.write(
                self.style.SUCCESS('✅ Aucune demande de fourniture orpheline trouvée.')
            )
            return
        
        self.stdout.write(f'🔍 Trouvé {demandes_orphelines.count()} demande(s) de fourniture orpheline(s):')
        
        # Afficher les détails des demandes
        for demande in demandes_orphelines:
            self.stdout.write(f'  - ID: {demande.id}, Date: {demande.date_demande}, Demandeur: {demande.demandeur.get_full_name()}, Statut: {demande.get_statut_display()}')
            
            # Vérifier s'il y a des décharges signées
            if demande.decharge_signee:
                self.stdout.write(f'    ⚠️  ATTENTION: Décharge signée le {demande.date_signature}')
                
                # Vérifier s'il y a des archives
                try:
                    archive = demande.archive_decharge
                    self.stdout.write(f'    📚 Archive trouvée: {archive.numero_archive}')
                except ArchiveDecharge.DoesNotExist:
                    pass
        
        # Demander confirmation si ce n'est pas un dry-run
        if not dry_run:
            if not force:
                self.stdout.write('\n⚠️  ATTENTION: Cette action va supprimer définitivement les demandes orphelines.')
                self.stdout.write('⚠️  Si des décharges sont signées, elles seront également supprimées.')
                
                confirm = input('\nÊtes-vous sûr de vouloir continuer ? (oui/non): ')
                if confirm.lower() not in ['oui', 'o', 'yes', 'y']:
                    self.stdout.write('❌ Opération annulée.')
                    return
            
            # Procéder à la suppression
            with transaction.atomic():
                count_supprimees = 0
                count_archives_supprimees = 0
                
                for demande in demandes_orphelines:
                    # Supprimer l'archive de décharge si elle existe
                    try:
                        archive = demande.archive_decharge
                        archive.delete()
                        count_archives_supprimees += 1
                        self.stdout.write(f'  🗑️  Archive supprimée: {archive.numero_archive}')
                    except ArchiveDecharge.DoesNotExist:
                        pass
                    
                    # Supprimer la demande
                    demande.delete()
                    count_supprimees += 1
                    self.stdout.write(f'  🗑️  Demande supprimée: ID {demande.id}')
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ Nettoyage terminé !\n'
                        f'   - {count_supprimees} demande(s) supprimée(s)\n'
                        f'   - {count_archives_supprimees} archive(s) supprimée(s)'
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'\n🔍 DRY RUN - Aucune suppression effectuée.\n'
                    f'   - {demandes_orphelines.count()} demande(s) seraient supprimée(s)\n'
                    f'   - Utilisez --force pour effectuer la suppression réelle'
                )
            )
