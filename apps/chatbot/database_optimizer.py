#!/usr/bin/env python3
"""
Module d'optimisation de la base de données ParcInfo
Crée des index composites et optimise les requêtes pour de meilleures performances
"""

import os
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """Classe pour optimiser les performances de la base de données ParcInfo"""
    
    def __init__(self):
        self.connection = connection
        self.optimization_results = {}
        
    def create_composite_indexes(self) -> Dict[str, bool]:
        """Crée des index composites pour les requêtes complexes"""
        try:
            logger.info("Création des index composites pour optimiser les performances...")
            
            indexes_to_create = [
                # Index pour les matériels informatiques
                {
                    "name": "idx_materiel_informatique_composite",
                    "table": "materiel_informatique",
                    "columns": ["code_inventaire", "commande_id", "fournisseur_id"],
                    "description": "Index composite pour les requêtes matériel-commande-fournisseur"
                },
                
                # Index pour les livraisons
                {
                    "name": "idx_livraison_composite",
                    "table": "livraison",
                    "columns": ["commande_id", "date_prevue", "date_effective"],
                    "description": "Index composite pour les requêtes livraison par date"
                },
                
                # Index pour les demandes d'équipement
                {
                    "name": "idx_demande_equipement_composite",
                    "table": "demande_equipement",
                    "columns": ["utilisateur_id", "date_demande", "statut"],
                    "description": "Index composite pour les demandes par utilisateur et date"
                },
                
                # Index pour les commandes informatiques
                {
                    "name": "idx_commande_informatique_composite",
                    "table": "commande_informatique",
                    "columns": ["numero_commande", "fournisseur_id", "date_commande"],
                    "description": "Index composite pour les commandes par numéro et fournisseur"
                },
                
                # Index pour les commandes bureautiques
                {
                    "name": "idx_commande_bureau_composite",
                    "table": "commande_bureau",
                    "columns": ["numero_commande", "fournisseur_id", "date_commande"],
                    "description": "Index composite pour les commandes bureautiques"
                },
                
                # Index pour les fournisseurs
                {
                    "name": "idx_fournisseur_composite",
                    "table": "fournisseurs",
                    "columns": ["ice", "nom", "ville"],
                    "description": "Index composite pour les recherches de fournisseurs"
                },
                
                # Index pour les utilisateurs
                {
                    "name": "idx_utilisateur_composite",
                    "table": "users_customuser",
                    "columns": ["username", "role", "is_active"],
                    "description": "Index composite pour les recherches d'utilisateurs"
                },
                
                # Index pour les matériels bureautiques
                {
                    "name": "idx_materiel_bureau_composite",
                    "table": "materiel_bureautique",
                    "columns": ["code_inventaire", "utilisateur_id", "affecte"],
                    "description": "Index composite pour les matériels bureautiques affectés"
                }
            ]
            
            results = {}
            
            for index_config in indexes_to_create:
                try:
                    success = self._create_single_composite_index(index_config)
                    results[index_config["name"]] = success
                    
                    if success:
                        logger.info(f"✅ Index créé: {index_config['name']}")
                    else:
                        logger.warning(f"⚠️ Échec création index: {index_config['name']}")
                        
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la création de l'index {index_config['name']}: {e}")
                    results[index_config["name"]] = False
            
            self.optimization_results["composite_indexes"] = results
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des index composites: {e}")
            return {}
    
    def _create_single_composite_index(self, index_config: Dict[str, Any]) -> bool:
        """Crée un index composite individuel"""
        try:
            with self.connection.cursor() as cursor:
                # Vérifier si l'index existe déjà
                check_sql = f"""
                    SELECT COUNT(*) FROM pg_indexes 
                    WHERE indexname = '{index_config['name']}'
                """
                cursor.execute(check_sql)
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    logger.info(f"Index {index_config['name']} existe déjà")
                    return True
                
                # Créer l'index composite
                columns_str = ", ".join(index_config["columns"])
                create_sql = f"""
                    CREATE INDEX CONCURRENTLY {index_config['name']} 
                    ON {index_config['table']} ({columns_str})
                """
                
                cursor.execute(create_sql)
                self.connection.commit()
                
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'index {index_config['name']}: {e}")
            return False
    
    def optimize_database_parameters(self) -> Dict[str, bool]:
        """Optimise les paramètres de la base de données PostgreSQL"""
        try:
            logger.info("Optimisation des paramètres de la base de données...")
            
            optimizations = [
                {
                    "name": "enable_seqscan",
                    "value": "off",
                    "description": "Désactive le scan séquentiel pour forcer l'utilisation des index"
                },
                {
                    "name": "random_page_cost",
                    "value": "1.1",
                    "description": "Réduit le coût des accès aléatoires pour favoriser les index"
                },
                {
                    "name": "effective_cache_size",
                    "value": "256MB",
                    "description": "Définit la taille du cache effectif pour l'optimiseur"
                },
                {
                    "name": "work_mem",
                    "value": "16MB",
                    "description": "Augmente la mémoire de travail pour les opérations de tri"
                },
                {
                    "name": "maintenance_work_mem",
                    "value": "64MB",
                    "description": "Augmente la mémoire pour les opérations de maintenance"
                },
                {
                    "name": "shared_buffers",
                    "value": "128MB",
                    "description": "Optimise la taille des buffers partagés"
                }
            ]
            
            results = {}
            
            with self.connection.cursor() as cursor:
                for opt in optimizations:
                    try:
                        # Appliquer l'optimisation
                        set_sql = f"SET {opt['name']} = {opt['value']}"
                        cursor.execute(set_sql)
                        
                        # Vérifier que l'optimisation a été appliquée
                        check_sql = f"SHOW {opt['name']}"
                        cursor.execute(check_sql)
                        current_value = cursor.fetchone()[0]
                        
                        success = str(current_value) == opt['value']
                        results[opt['name']] = success
                        
                        if success:
                            logger.info(f"✅ {opt['name']} = {opt['value']}")
                        else:
                            logger.warning(f"⚠️ {opt['name']} = {current_value} (attendu: {opt['value']})")
                            
                    except Exception as e:
                        logger.error(f"❌ Erreur lors de l'optimisation de {opt['name']}: {e}")
                        results[opt['name']] = False
                
                self.connection.commit()
            
            self.optimization_results["database_parameters"] = results
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation des paramètres: {e}")
            return {}
    
    def analyze_table_statistics(self) -> Dict[str, bool]:
        """Met à jour les statistiques des tables pour l'optimiseur de requêtes"""
        try:
            logger.info("Mise à jour des statistiques des tables...")
            
            tables_to_analyze = [
                "materiel_informatique",
                "materiel_bureautique",
                "commande_informatique",
                "commande_bureau",
                "fournisseurs",
                "livraison",
                "demande_equipement",
                "users_customuser"
            ]
            
            results = {}
            
            with self.connection.cursor() as cursor:
                for table in tables_to_analyze:
                    try:
                        analyze_sql = f"ANALYZE {table}"
                        cursor.execute(analyze_sql)
                        results[table] = True
                        logger.info(f"✅ Statistiques mises à jour pour {table}")
                        
                    except Exception as e:
                        logger.error(f"❌ Erreur lors de l'analyse de {table}: {e}")
                        results[table] = False
                
                self.connection.commit()
            
            self.optimization_results["table_statistics"] = results
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des statistiques: {e}")
            return {}
    
    def create_partitioned_tables(self) -> Dict[str, bool]:
        """Crée des tables partitionnées pour les données volumineuses"""
        try:
            logger.info("Création de tables partitionnées pour les performances...")
            
            # Vérifier si les tables partitionnées existent déjà
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name LIKE '%_partitioned'
                """)
                existing_partitions = [row[0] for row in cursor.fetchall()]
            
            results = {}
            
            # Partitionner la table des commandes par année
            if "commande_informatique_partitioned" not in existing_partitions:
                try:
                    self._create_partitioned_orders_table()
                    results["commande_informatique_partitioned"] = True
                    logger.info("✅ Table partitionnée des commandes créée")
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la création de la table partitionnée: {e}")
                    results["commande_informatique_partitioned"] = False
            
            # Partitionner la table des livraisons par mois
            if "livraison_partitioned" not in existing_partitions:
                try:
                    self._create_partitioned_delivery_table()
                    results["livraison_partitioned"] = True
                    logger.info("✅ Table partitionnée des livraisons créée")
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la création de la table partitionnée: {e}")
                    results["livraison_partitioned"] = False
            
            self.optimization_results["partitioned_tables"] = results
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des tables partitionnées: {e}")
            return {}
    
    def _create_partitioned_orders_table(self):
        """Crée une table partitionnée pour les commandes"""
        with self.connection.cursor() as cursor:
            # Créer la table partitionnée
            create_sql = """
                CREATE TABLE commande_informatique_partitioned (
                    LIKE commande_informatique INCLUDING ALL
                ) PARTITION BY RANGE (EXTRACT(YEAR FROM date_commande));
            """
            cursor.execute(create_sql)
            
            # Créer les partitions pour 2024 et 2025
            partitions = [
                ("2024", "2024-01-01", "2025-01-01"),
                ("2025", "2025-01-01", "2026-01-01"),
                ("future", "2026-01-01", "2030-01-01")
            ]
            
            for partition_name, start_date, end_date in partitions:
                partition_sql = f"""
                    CREATE TABLE commande_informatique_partitioned_{partition_name}
                    PARTITION OF commande_informatique_partitioned
                    FOR VALUES FROM ('{start_date}') TO ('{end_date}');
                """
                cursor.execute(partition_sql)
            
            self.connection.commit()
    
    def _create_partitioned_delivery_table(self):
        """Crée une table partitionnée pour les livraisons"""
        with self.connection.cursor() as cursor:
            # Créer la table partitionnée
            create_sql = """
                CREATE TABLE livraison_partitioned (
                    LIKE livraison INCLUDING ALL
                ) PARTITION BY RANGE (EXTRACT(MONTH FROM date_prevue));
            """
            cursor.execute(create_sql)
            
            # Créer les partitions par mois
            for month in range(1, 13):
                month_name = f"month_{month:02d}"
                start_month = month
                end_month = month + 1 if month < 12 else 1
                start_year = 2025 if month < 12 else 2026
                
                partition_sql = f"""
                    CREATE TABLE livraison_partitioned_{month_name}
                    PARTITION OF livraison_partitioned
                    FOR VALUES FROM ({start_month}) TO ({end_month});
                """
                cursor.execute(partition_sql)
            
            self.connection.commit()
    
    def optimize_query_performance(self) -> Dict[str, Any]:
        """Optimise les requêtes fréquentes avec des vues matérialisées"""
        try:
            logger.info("Création de vues matérialisées pour optimiser les requêtes...")
            
            materialized_views = [
                {
                    "name": "mv_supplier_orders_summary",
                    "sql": """
                        CREATE MATERIALIZED VIEW mv_supplier_orders_summary AS
                        SELECT 
                            f.nom as fournisseur_nom,
                            f.ice,
                            COUNT(c.numero_commande) as nombre_commandes,
                            SUM(c.montant) as montant_total,
                            MAX(c.date_commande) as derniere_commande
                        FROM fournisseurs f
                        LEFT JOIN commande_informatique c ON f.id = c.fournisseur_id
                        GROUP BY f.id, f.nom, f.ice
                        ORDER BY montant_total DESC;
                    """,
                    "description": "Résumé des commandes par fournisseur"
                },
                
                {
                    "name": "mv_material_inventory_summary",
                    "sql": """
                        CREATE MATERIALIZED VIEW mv_material_inventory_summary AS
                        SELECT 
                            'informatique' as type_materiel,
                            COUNT(*) as nombre_total,
                            COUNT(CASE WHEN affecte = true THEN 1 END) as nombre_affecte,
                            COUNT(CASE WHEN affecte = false THEN 1 END) as nombre_disponible
                        FROM materiel_informatique
                        UNION ALL
                        SELECT 
                            'bureautique' as type_materiel,
                            COUNT(*) as nombre_total,
                            COUNT(CASE WHEN affecte = true THEN 1 END) as nombre_affecte,
                            COUNT(CASE WHEN affecte = false THEN 1 END) as nombre_disponible
                        FROM materiel_bureautique;
                    """,
                    "description": "Résumé de l'inventaire des matériels"
                },
                
                {
                    "name": "mv_user_equipment_requests",
                    "sql": """
                        CREATE MATERIALIZED VIEW mv_user_equipment_requests AS
                        SELECT 
                            u.username,
                            u.role,
                            COUNT(d.id) as nombre_demandes,
                            COUNT(CASE WHEN d.statut = 'approuvee' THEN 1 END) as demandes_approuvees,
                            COUNT(CASE WHEN d.statut = 'en_attente' THEN 1 END) as demandes_en_attente
                        FROM users_customuser u
                        LEFT JOIN demande_equipement d ON u.id = d.utilisateur_id
                        GROUP BY u.id, u.username, u.role
                        ORDER BY nombre_demandes DESC;
                    """,
                    "description": "Résumé des demandes d'équipement par utilisateur"
                }
            ]
            
            results = {}
            
            with self.connection.cursor() as cursor:
                for view_config in materialized_views:
                    try:
                        # Vérifier si la vue existe déjà
                        check_sql = f"""
                            SELECT COUNT(*) FROM information_schema.views 
                            WHERE table_name = '{view_config['name']}'
                        """
                        cursor.execute(check_sql)
                        exists = cursor.fetchone()[0] > 0
                        
                        if exists:
                            logger.info(f"Vue matérialisée {view_config['name']} existe déjà")
                            results[view_config['name']] = True
                            continue
                        
                        # Créer la vue matérialisée
                        cursor.execute(view_config['sql'])
                        results[view_config['name']] = True
                        logger.info(f"✅ Vue matérialisée créée: {view_config['name']}")
                        
                    except Exception as e:
                        logger.error(f"❌ Erreur lors de la création de la vue {view_config['name']}: {e}")
                        results[view_config['name']] = False
                
                self.connection.commit()
            
            self.optimization_results["materialized_views"] = results
            return results
            
        except Exception as e:
            logger.error(f"Erreur lors de la création des vues matérialisées: {e}")
            return {}
    
    def run_full_optimization(self) -> Dict[str, Any]:
        """Exécute toutes les optimisations de la base de données"""
        try:
            logger.info("🚀 Début de l'optimisation complète de la base de données...")
            start_time = time.time()
            
            # 1. Créer les index composites
            logger.info("📊 Étape 1/5: Création des index composites...")
            composite_indexes = self.create_composite_indexes()
            
            # 2. Optimiser les paramètres
            logger.info("⚙️ Étape 2/5: Optimisation des paramètres...")
            db_parameters = self.optimize_database_parameters()
            
            # 3. Mettre à jour les statistiques
            logger.info("📈 Étape 3/5: Mise à jour des statistiques...")
            table_stats = self.analyze_table_statistics()
            
            # 4. Créer des tables partitionnées
            logger.info("🗂️ Étape 4/5: Création de tables partitionnées...")
            partitioned_tables = self.create_partitioned_tables()
            
            # 5. Créer des vues matérialisées
            logger.info("🔍 Étape 5/5: Création de vues matérialisées...")
            materialized_views = self.optimize_query_performance()
            
            # Résumé des résultats
            total_time = time.time() - start_time
            
            summary = {
                "execution_time": total_time,
                "composite_indexes": composite_indexes,
                "database_parameters": db_parameters,
                "table_statistics": table_stats,
                "partitioned_tables": partitioned_tables,
                "materialized_views": materialized_views,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Calculer le taux de succès global
            all_results = []
            all_results.extend(composite_indexes.values())
            all_results.extend(db_parameters.values())
            all_results.extend(table_stats.values())
            all_results.extend(partitioned_tables.values())
            all_results.extend(materialized_views.values())
            
            if all_results:
                success_rate = (sum(all_results) / len(all_results)) * 100
                summary["success_rate"] = f"{success_rate:.1f}%"
            else:
                summary["success_rate"] = "0%"
            
            logger.info(f"✅ Optimisation terminée en {total_time:.2f}s")
            logger.info(f"📊 Taux de succès global: {summary['success_rate']}")
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'optimisation complète: {e}")
            return {"error": str(e), "success_rate": "0%"}
    
    def apply_query_optimizations(self) -> Dict[str, bool]:
        """Applique toutes les optimisations de requêtes (alias pour run_full_optimization)"""
        return self.run_full_optimization()
    
    def get_optimization_status(self) -> Dict[str, Any]:
        """Retourne le statut actuel des optimisations"""
        return {
            "last_optimization": self.optimization_results,
            "database_info": self._get_database_info()
        }
    
    def _get_database_info(self) -> Dict[str, Any]:
        """Récupère les informations sur la base de données"""
        try:
            with self.connection.cursor() as cursor:
                # Taille de la base
                cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
                db_size = cursor.fetchone()[0]
                
                # Nombre de tables
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
                table_count = cursor.fetchone()[0]
                
                # Nombre d'index
                cursor.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';")
                index_count = cursor.fetchone()[0]
                
                return {
                    "database_size": db_size,
                    "table_count": table_count,
                    "index_count": index_count
                }
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des infos DB: {e}")
            return {}

def main():
    """Fonction principale pour tester l'optimisation"""
    logging.basicConfig(level=logging.INFO)
    
    # Créer l'optimiseur
    optimizer = DatabaseOptimizer()
    
    # Exécuter l'optimisation complète
    results = optimizer.run_full_optimization()
    
    # Afficher les résultats
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS DE L'OPTIMISATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    print(f"⏱️ Temps d'exécution: {results.get('execution_time', 0):.2f}s")
    print(f"📈 Taux de succès: {results.get('success_rate', '0%')}")
    print(f"🕐 Timestamp: {results.get('timestamp', 'N/A')}")
    
    # Afficher le statut des index composites
    if 'composite_indexes' in results:
        print(f"\n🔗 Index composites: {sum(results['composite_indexes'].values())}/{len(results['composite_indexes'])} créés")
    
    # Afficher le statut des vues matérialisées
    if 'materialized_views' in results:
        print(f"🔍 Vues matérialisées: {sum(results['materialized_views'].values())}/{len(results['materialized_views'])} créées")
    
    # Afficher le statut de la base
    db_info = optimizer.get_optimization_status()['database_info']
    if db_info:
        print(f"\n💾 Informations sur la base:")
        print(f"   Taille: {db_info.get('database_size', 'N/A')}")
        print(f"   Tables: {db_info.get('table_count', 'N/A')}")
        print(f"   Index: {db_info.get('index_count', 'N/A')}")

if __name__ == "__main__":
    main()
