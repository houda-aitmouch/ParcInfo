from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.demande_equipement.models import DemandeEquipement, ArchiveDecharge
from apps.demande_equipement.views import archiver_decharge_automatique
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Archive automatiquement toutes les demandes signées qui ne sont pas encore archivées'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait archivé sans effectuer l\'archivage',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Nom d\'utilisateur de l\'archivage (par défaut: system)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        user_name = options.get('user') or 'system'
        
        # Récupérer l'utilisateur pour l'archivage
        archive_user = None
        if user_name != 'system':
            try:
                archive_user = User.objects.get(username=user_name)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Utilisateur "{user_name}" non trouvé')
                )
                return

        # Récupérer toutes les demandes signées qui ne sont pas encore archivées
        demandes_signees = DemandeEquipement.objects.filter(
            statut='approuvee',
            decharge_signee=True,
            date_signature__isnull=False
        ).exclude(
            archive_decharge__isnull=False
        )

        self.stdout.write(
            self.style.SUCCESS(f'🔍 Recherche des demandes signées non archivées...')
        )
        
        count = demandes_signees.count()
        self.stdout.write(f'📊 {count} demandes signées trouvées à archiver')

        if count == 0:
            self.stdout.write(
                self.style.WARNING('⚠️  Aucune demande signée à archiver')
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 Mode DRY-RUN - Aucun archivage effectué')
            )
            
            for demande in demandes_signees:
                self.stdout.write(
                    f'📄 Demande #{demande.id} - {demande.demandeur.get_full_name()} '
                    f'({demande.categorie}/{demande.type_article}) - '
                    f'Signée le {demande.date_signature.strftime("%d/%m/%Y")}'
                )
            return

        # Procéder à l'archivage
        self.stdout.write(
            self.style.SUCCESS('🚀 Début de l\'archivage automatique...')
        )

        success_count = 0
        error_count = 0

        for demande in demandes_signees:
            try:
                self.stdout.write(
                    f'📄 Archivage de la demande #{demande.id} - '
                    f'{demande.demandeur.get_full_name()}...'
                )
                
                # Archiver la décharge
                archive = archiver_decharge_automatique(demande, archive_user)
                
                if archive:
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Archivée avec succès: {archive.numero_archive}'
                        )
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'❌ Échec de l\'archivage')
                    )
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ Erreur lors de l\'archivage: {str(e)}')
                )

        # Résumé final
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'📊 RÉSUMÉ DE L\'ARCHIVAGE')
        )
        self.stdout.write(f'✅ Demandes archivées avec succès: {success_count}')
        self.stdout.write(f'❌ Erreurs d\'archivage: {error_count}')
        self.stdout.write(f'📄 Total traité: {success_count + error_count}')
        
        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'🎉 Archivage terminé avec succès ! '
                    f'{success_count} décharges ont été archivées.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Aucune décharge n\'a pu être archivée')
            ) 