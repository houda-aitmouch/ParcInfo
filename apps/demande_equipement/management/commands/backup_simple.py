from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Sauvegarde simple de la base de données et des fichiers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--files-only',
            action='store_true',
            help='Sauvegarder seulement les fichiers (media, static)',
        )
        parser.add_argument(
            '--db-only',
            action='store_true',
            help='Sauvegarder seulement la base de données',
        )

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = 'backups/'
        os.makedirs(backup_dir, exist_ok=True)
        
        if not options['files_only']:
            # Sauvegarde de la base de données
            self.backup_database(backup_dir, timestamp)
        
        if not options['db_only']:
            # Sauvegarde des fichiers
            self.backup_files(backup_dir, timestamp)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Sauvegarde terminée avec succès - {timestamp}')
        )

    def backup_database(self, backup_dir, timestamp):
        """Sauvegarde de la base de données PostgreSQL"""
        try:
            backup_file = f'{backup_dir}db_backup_{timestamp}.sql'
            
            # Commande pg_dump
            cmd = [
                'pg_dump',
                '-h', settings.DATABASES['default']['HOST'],
                '-U', settings.DATABASES['default']['USER'],
                '-d', settings.DATABASES['default']['NAME'],
                '-f', backup_file
            ]
            
            # Exécuter la commande
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.stdout.write(
                    self.style.SUCCESS(f'📊 Base de données sauvegardée: {backup_file}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erreur sauvegarde DB: {result.stderr}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur sauvegarde DB: {str(e)}')
            )

    def backup_files(self, backup_dir, timestamp):
        """Sauvegarde des fichiers media et static"""
        try:
            files_backup = f'{backup_dir}files_backup_{timestamp}.tar.gz'
            
            # Créer l'archive des fichiers
            cmd = [
                'tar', '-czf', files_backup,
                'media/', 'static/'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.stdout.write(
                    self.style.SUCCESS(f'📁 Fichiers sauvegardés: {files_backup}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erreur sauvegarde fichiers: {result.stderr}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur sauvegarde fichiers: {str(e)}')
            ) 