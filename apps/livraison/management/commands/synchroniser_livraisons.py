from django.core.management.base import BaseCommand
from django.db import transaction
from apps.livraison.models import Livraison


class Command(BaseCommand):
    help = 'Synchronise toutes les livraisons avec leurs commandes associées'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les modifications sans les appliquer',
        )
        parser.add_argument(
            '--type',
            choices=['informatique', 'bureau', 'all'],
            default='all',
            help='Type de livraisons à synchroniser',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        livraison_type = options['type']
        
        self.stdout.write(
            self.style.SUCCESS('🔄 Début de la synchronisation des livraisons...')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('⚠️  Mode DRY-RUN activé - Aucune modification ne sera appliquée')
            )
        
        # Filtrer les livraisons selon le type
        livraisons = Livraison.objects.all()
        if livraison_type != 'all':
            livraisons = livraisons.filter(type_commande=livraison_type)
        
        total_livraisons = livraisons.count()
        self.stdout.write(f"📊 {total_livraisons} livraisons à vérifier")
        
        livraisons_modifiees = 0
        livraisons_orphelines = 0
        livraisons_ok = 0
        
        with transaction.atomic():
            for livraison in livraisons:
                self.stdout.write(f"🔍 Vérification: {livraison.numero_commande}")
                
                commande_associee = livraison.commande
                
                if not commande_associee:
                    livraisons_orphelines += 1
                    self.stdout.write(
                        self.style.ERROR(f"   ❌ Livraison orpheline (ID: {livraison.id})")
                    )
                    continue
                
                # Vérifier la cohérence du numéro de commande
                numero_commande_reel = commande_associee.numero_commande
                
                if livraison.numero_commande != numero_commande_reel:
                    livraisons_modifiees += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"   🔧 Numéro incohérent: '{livraison.numero_commande}' -> '{numero_commande_reel}'"
                        )
                    )
                    
                    if not dry_run:
                        livraison.numero_commande = numero_commande_reel
                        livraison.save(update_fields=['numero_commande', 'date_modification'])
                
                else:
                    livraisons_ok += 1
                    self.stdout.write(f"   ✅ Cohérente")
                
                # Vérifier la disponibilité des propriétés
                try:
                    fournisseur = livraison.fournisseur
                    materiels = livraison.materiels
                    montant = livraison.montant_total
                    
                    self.stdout.write(
                        f"   📋 Fournisseur: {fournisseur}, "
                        f"Matériels: {len(materiels)}, "
                        f"Montant: {montant}"
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"   ❌ Erreur d'accès aux propriétés: {str(e)}")
                    )
            
            if dry_run:
                # Rollback en mode dry-run
                transaction.set_rollback(True)
        
        # Afficher le résumé
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("📈 RÉSUMÉ DE LA SYNCHRONISATION"))
        self.stdout.write("="*60)
        self.stdout.write(f"✅ Livraisons cohérentes: {livraisons_ok}")
        self.stdout.write(f"🔧 Livraisons modifiées: {livraisons_modifiees}")
        self.stdout.write(f"❌ Livraisons orphelines: {livraisons_orphelines}")
        self.stdout.write(f"📊 Total vérifié: {total_livraisons}")
        
        if dry_run and livraisons_modifiees > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\n⚠️  Relancez sans --dry-run pour appliquer les {livraisons_modifiees} modifications"
                )
            )
        elif livraisons_modifiees > 0:
            self.stdout.write(
                self.style.SUCCESS(f"\n🎉 {livraisons_modifiees} livraisons synchronisées avec succès!")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("\n🎉 Toutes les livraisons sont déjà synchronisées!")
            )
