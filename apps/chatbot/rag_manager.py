import logging
import json
from typing import List, Dict, Optional, Any
from django.db import connection

# Handle missing sentence_transformers gracefully
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

import re

logger = logging.getLogger(__name__)

class RAGManager:
    """Enhanced RAG Manager with comprehensive indexing and validation"""
    
    def __init__(self):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.error("❌ La bibliothèque sentence_transformers n'est pas installée. RAG features disabled.")
            self.embed_model = None
        else:
            try:
                self.embed_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
                logger.info("✅ RAG Manager initialized with embedding model")
            except Exception as e:
                logger.error(f"❌ Failed to initialize embedding model: {e}")
                self.embed_model = None
        
    def populate_index(self) -> int:
        """Populate the RAG index with data from ALL relevant models - Comprehensive indexing"""
        try:
            from django.apps import apps
            documents = []
            indexed_ids = set()
            
            logger.info("🔄 Starting comprehensive RAG indexing...")
            
            # Define models to index with proper app.model format - ALL MODELS EXCEPT CHATBOT
            models_to_index = [
                # Fournisseurs
                ('fournisseurs', 'Fournisseur'),
                
                # Matériel
                ('materiel_informatique', 'MaterielInformatique'),
                ('materiel_bureautique', 'MaterielBureau'),
                
                # Commandes
                ('commande_informatique', 'Commande'),
                ('commande_bureau', 'CommandeBureau'),
                ('commande_informatique', 'LigneCommande'),
                ('commande_bureau', 'LigneCommandeBureau'),
                ('commande_informatique', 'Designation'),
                ('commande_bureau', 'DesignationBureau'),
                ('commande_informatique', 'Description'),
                ('commande_bureau', 'DescriptionBureau'),
                
                # Livraisons
                ('livraison', 'Livraison'),
                
                # Demandes d'équipement
                ('demande_equipement', 'DemandeEquipement'),
                ('demande_equipement', 'ArchiveDecharge'),
                
                # Utilisateurs
                ('users', 'CustomUser'),
                
                # Admin logs
                ('admin', 'LogEntry'),
            ]
            
            # Auto-detect additional models from installed apps (project apps only, exclude system apps)
            installed_apps = [
                app for app in apps.get_app_configs()
                if app.label != 'chatbot'
                and app.name.startswith('apps.')
            ]
            for app_config in installed_apps:
                try:
                    app_models = app_config.get_models()
                    for model in app_models:
                        app_name = app_config.label
                        model_name = model.__name__
                        
                        # Skip if already in our list
                        if (app_name, model_name) not in models_to_index:
                            # Only add if it's a Django model and not abstract
                            if hasattr(model, '_meta') and not model._meta.abstract:
                                models_to_index.append((app_name, model_name))
                                logger.info(f"Auto-detected model: {app_name}.{model_name}")
                except Exception as e:
                    logger.warning(f"Could not inspect models for app {app_config.label}: {e}")
                    continue

            # Clear existing index first
            self.clear_index()
            
            # Index all models systematically
            for app_name, model_name in models_to_index:
                try:
                    model = apps.get_model(app_name, model_name)
                    count = model.objects.count()
                    logger.info(f"Indexing {app_name}.{model_name}: {count} records")
                    
                    if count == 0:
                        logger.warning(f"Table {app_name}.{model_name} is empty")
                        continue
                    
                    # Index each record
                    for item in model.objects.all():
                        try:
                            content_parts = self._build_content_parts(model_name, item)
                            if content_parts and any(content_parts):
                                obj_uid = self._get_object_uid(item, model_name)
                                doc_id = f"{model_name.lower()}_{obj_uid}"
                                if doc_id not in indexed_ids:
                                    content = ' '.join(filter(None, content_parts))
                                    if len(content.strip()) > 5:  # Minimum content length
                                        documents.append({
                                            'id': doc_id,
                                            'content': content,
                                            'metadata': {
                                                'type': model_name.lower(),
                                                'app': app_name,
                                                'id': obj_uid,
                                                'pk': obj_uid,
                                                'model': model_name
                                            }
                                        })
                                        indexed_ids.add(doc_id)
                        except Exception as e:
                            logger.warning(f"Error indexing {model_name} ID {item.id}: {e}")
                            continue
                            
                except Exception as e:
                    logger.error(f"Error accessing model {app_name}.{model_name}: {e}")
                    continue
            
            # Batch insert documents
            logger.info(f"Inserting {len(documents)} documents into RAG index...")
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self._insert_documents_batch(batch)
                
            final_count = self.get_rag_count()
            logger.info(f"✅ RAG index populated with {final_count} documents")
            
            # Calculate coherence ratio - exclude DocumentVector from DB count to avoid double counting
            db_models_to_count = [(app, model) for app, model in models_to_index 
                                if not (app == 'chatbot' and model == 'DocumentVector')]
            total_db_records = 0
            
            # Log detailed counts for debugging
            for app, model in db_models_to_count:
                try:
                    count = apps.get_model(app, model).objects.count()
                    total_db_records += count
                    logger.info(f"  {app}.{model}: {count} records")
                except Exception as e:
                    logger.warning(f"  {app}.{model}: Error counting - {e}")
            
            coherence_ratio = (final_count / total_db_records * 100) if total_db_records > 0 else 0
            logger.info(f"📈 RAG-DB coherence: {coherence_ratio:.2f}% ({final_count}/{total_db_records})")
            
            if coherence_ratio < 95:
                logger.warning(f"⚠️ Low coherence ratio: {coherence_ratio:.2f}%")
            
            return final_count
            
        except Exception as e:
            logger.error(f"Error populating RAG index: {e}")
            return 0

    def _build_content_parts(self, model_name: str, item) -> List[str]:
        """Build comprehensive content parts for all model types with all fields"""
        content_parts = []
        
        try:
            if model_name == 'Fournisseur':
                content_parts = [
                    f"Fournisseur: {item.nom}",
                    f"ICE: {item.ice}" if hasattr(item, 'ice') and item.ice else None,
                    f"IF Fiscal: {item.if_fiscal}" if hasattr(item, 'if_fiscal') and item.if_fiscal else None,
                    f"Registre Commerce: {item.registre_commerce}" if hasattr(item, 'registre_commerce') and item.registre_commerce else None,
                    f"Adresse: {item.adresse}" if hasattr(item, 'adresse') and item.adresse else None,
                    f"Téléphone: {item.telephone}" if hasattr(item, 'telephone') and item.telephone else None,
                    f"Email: {item.email}" if hasattr(item, 'email') and item.email else None,
                    f"Site web: {item.site_web}" if hasattr(item, 'site_web') and item.site_web else None,
                    f"Contact principal: {item.contact_principal}" if hasattr(item, 'contact_principal') and item.contact_principal else None,
                    f"Notes: {item.notes}" if hasattr(item, 'notes') and item.notes else None
                ]
            elif model_name == 'MaterielInformatique':
                content_parts = [
                    f"Matériel informatique: {item.code_inventaire}",
                    f"Numéro série: {item.numero_serie}",
                    f"Statut: {item.statut}",
                    f"Lieu stockage: {item.lieu_stockage}",
                    f"Observation: {item.observation}",
                    f"Public: {'Oui' if item.public else 'Non'}",
                    f"Utilisateur: {item.utilisateur.username if item.utilisateur else 'Non affecté'}",
                    f"Commande: {item.commande.numero_commande if item.commande else 'N/A'}",
                    f"Ligne commande: {item.ligne_commande.designation.nom if item.ligne_commande and item.ligne_commande.designation else 'N/A'}",
                    f"Date service calculée: {item.date_service_calculee.strftime('%Y-%m-%d') if item.date_service_calculee else 'N/A'}",
                    f"Date fin garantie calculée: {item.date_fin_garantie_calculee.strftime('%Y-%m-%d') if item.date_fin_garantie_calculee else 'N/A'}"
                ]
            elif model_name == 'MaterielBureau':
                content_parts = [
                    f"Matériel bureau: {item.code_inventaire}",
                    f"Statut: {item.statut}",
                    f"Lieu stockage: {item.lieu_stockage}",
                    f"Observation: {item.observation}",
                    f"Date création: {item.date_creation.strftime('%Y-%m-%d') if item.date_creation else 'N/A'}",
                    f"Date modification: {item.date_modification.strftime('%Y-%m-%d') if item.date_modification else 'N/A'}",
                    f"Utilisateur: {item.utilisateur.username if item.utilisateur else 'Non affecté'}",
                    f"Commande: {item.commande.numero_commande if item.commande else 'N/A'}",
                    f"Ligne commande: {item.ligne_commande.designation.nom if item.ligne_commande and item.ligne_commande.designation else 'N/A'}",
                    f"Désignation: {item.designation}",
                    f"Description: {item.description}",
                    f"Prix unitaire: {item.prix_unitaire} DH HT" if item.prix_unitaire else None,
                    f"Fournisseur: {item.fournisseur}",
                    f"Numéro facture: {item.numero_facture}" if item.numero_facture else None,
                    f"Date service calculée: {item.date_service_calculee.strftime('%Y-%m-%d') if item.date_service_calculee else 'N/A'}",
                    f"Date fin garantie calculée: {item.date_fin_garantie_calculee.strftime('%Y-%m-%d') if item.date_fin_garantie_calculee else 'N/A'}"
                ]
            elif model_name == 'Commande':
                content_parts = [
                    f"Commande informatique: {item.numero_commande}",
                    f"Mode passation: {item.mode_passation}",
                    f"Date commande: {item.date_commande.strftime('%Y-%m-%d') if item.date_commande else 'N/A'}",
                    f"Date réception: {item.date_reception.strftime('%Y-%m-%d') if item.date_reception else 'N/A'}",
                    f"Numéro facture: {item.numero_facture}" if item.numero_facture else None,
                    f"Durée garantie: {item.duree_garantie_valeur} {item.duree_garantie_unite}",
                    f"Fournisseur: {item.fournisseur.nom if item.fournisseur else 'N/A'}",
                    f"ICE fournisseur: {item.fournisseur.ice if item.fournisseur and hasattr(item.fournisseur, 'ice') else 'N/A'}",
                    f"Adresse fournisseur: {item.fournisseur.adresse if item.fournisseur and hasattr(item.fournisseur, 'adresse') else 'N/A'}"
                ]
            elif model_name == 'CommandeBureau':
                content_parts = [
                    f"Commande bureau: {item.numero_commande}",
                    f"Date commande: {item.date_commande.strftime('%Y-%m-%d') if item.date_commande else 'N/A'}",
                    f"Date réception: {item.date_reception.strftime('%Y-%m-%d') if item.date_reception else 'N/A'}",
                    f"Numéro facture: {item.numero_facture}" if item.numero_facture else None,
                    f"Durée garantie: {item.duree_garantie_valeur} {item.duree_garantie_unite}",
                    f"Fournisseur: {item.fournisseur.nom if item.fournisseur else 'N/A'}",
                    f"ICE fournisseur: {item.fournisseur.ice if item.fournisseur and hasattr(item.fournisseur, 'ice') else 'N/A'}",
                    f"Adresse fournisseur: {item.fournisseur.adresse if item.fournisseur and hasattr(item.fournisseur, 'adresse') else 'N/A'}"
                ]
            elif model_name == 'Livraison':
                # Safe access for montant_total (may not exist on related models)
                mt_val = None
                try:
                    mt_val = item.montant_total
                except Exception:
                    mt_val = None

                content_parts = [
                    f"Livraison: {item.numero_commande}",
                    f"Type commande: {item.type_commande}",
                    f"Statut livraison: {item.statut_livraison}",
                    f"Date livraison prévue: {item.date_livraison_prevue.strftime('%Y-%m-%d') if item.date_livraison_prevue else 'N/A'}",
                    f"Date livraison effective: {item.date_livraison_effective.strftime('%Y-%m-%d') if item.date_livraison_effective else 'N/A'}",
                    f"Conforme: {'Oui' if item.conforme else 'Non'}",
                    f"PV réception reçu: {'Oui' if item.pv_reception_recu else 'Non'}",
                    f"Notes: {item.notes}" if item.notes else None,
                    f"Créé par: {item.cree_par.username if item.cree_par else 'N/A'}",
                    f"Modifié par: {item.modifie_par.username if item.modifie_par else 'N/A'}",
                    f"Date création: {item.date_creation.strftime('%Y-%m-%d %H:%M') if item.date_creation else 'N/A'}",
                    f"Date modification: {item.date_modification.strftime('%Y-%m-%d %H:%M') if item.date_modification else 'N/A'}",
                    f"Fournisseur: {item.fournisseur.nom if item.fournisseur else 'N/A'}",
                    f"Montant total: {mt_val} DH HT" if mt_val else None
                ]
            elif model_name == 'DemandeEquipement':
                content_parts = [
                    f"Demande équipement ID: {item.id}",
                    f"Date demande: {item.date_demande.strftime('%Y-%m-%d') if item.date_demande else 'N/A'}",
                    f"Statut: {item.statut}",
                    f"Demandeur: {item.demandeur.username if item.demandeur else 'N/A'}",
                    f"Nom demandeur: {item.demandeur.last_name} {item.demandeur.first_name}" if item.demandeur and hasattr(item.demandeur, 'last_name') and hasattr(item.demandeur, 'first_name') else None,
                    f"Email demandeur: {item.demandeur.email}" if item.demandeur and hasattr(item.demandeur, 'email') else None,
                    f"Catégorie: {item.categorie}",
                    f"Type article: {item.type_article}",
                    f"Description: {item.description}" if hasattr(item, 'description') and item.description else None,
                    f"Quantité demandée: {item.quantite_demandee}" if hasattr(item, 'quantite_demandee') else None,
                    f"Justification: {item.justification}" if hasattr(item, 'justification') and item.justification else None,
                    f"Date approbation: {item.date_approbation.strftime('%Y-%m-%d') if hasattr(item, 'date_approbation') and item.date_approbation else 'N/A'}",
                    f"Approbateur: {item.approbateur.username if hasattr(item, 'approbateur') and item.approbateur else 'N/A'}",
                    f"Date affectation: {item.date_affectation.strftime('%Y-%m-%d') if hasattr(item, 'date_affectation') and item.date_affectation else 'N/A'}",
                    f"Matériel sélectionné: {item.materiel_selectionne.code_inventaire if hasattr(item, 'materiel_selectionne') and item.materiel_selectionne else 'N/A'}",
                    f"Date signature: {item.date_signature.strftime('%Y-%m-%d') if hasattr(item, 'date_signature') and item.date_signature else 'N/A'}",
                    f"Signature image: {'Oui' if hasattr(item, 'signature_image') and item.signature_image else 'Non'}"
                ]
            elif model_name == 'ArchiveDecharge':
                content_parts = [
                    f"Archive décharge ID: {item.id}",
                    f"Numéro archive: {item.numero_archive}" if hasattr(item, 'numero_archive') and item.numero_archive else None,
                    f"Date archivage: {item.date_archivage.strftime('%Y-%m-%d') if hasattr(item, 'date_archivage') and item.date_archivage else 'N/A'}",
                    f"Statut archive: {item.statut_archive}" if hasattr(item, 'statut_archive') else None,
                    f"Demande liée: {item.demande.id if hasattr(item, 'demande') and item.demande else 'N/A'}",
                    f"Utilisateur: {item.utilisateur.username if hasattr(item, 'utilisateur') and item.utilisateur else 'N/A'}",
                    f"Notes archivage: {item.notes_archivage}" if hasattr(item, 'notes_archivage') and item.notes_archivage else None
                ]
            elif model_name == 'LogEntry':
                content_parts = [
                    f"Action admin: {item.action_flag}",
                    f"Objet: {item.object_repr}",
                    f"Date: {item.action_time.strftime('%Y-%m-%d %H:%M') if item.action_time else 'N/A'}",
                    f"Utilisateur: {item.user.username if item.user else 'N/A'}",
                    f"Nom utilisateur: {item.user.last_name} {item.user.first_name}" if item.user and hasattr(item.user, 'last_name') and hasattr(item.user, 'first_name') else None,
                    f"Email utilisateur: {item.user.email}" if item.user and hasattr(item.user, 'email') else None,
                    f"Type contenu: {item.content_type.model if item.content_type else 'N/A'}",
                    f"App contenu: {item.content_type.app_label if item.content_type else 'N/A'}",
                    f"ID objet: {item.object_id}",
                    f"Message: {item.change_message}" if hasattr(item, 'change_message') and item.change_message else None
                ]
            elif model_name in ['LigneCommande', 'LigneCommandeBureau']:
                content_parts = [
                    f"Ligne commande: {item.commande.numero_commande if hasattr(item, 'commande') and item.commande else 'N/A'}",
                    f"Désignation: {item.designation.nom if hasattr(item, 'designation') and item.designation else 'N/A'}",
                    f"Description: {item.description.nom if hasattr(item, 'description') and item.description else 'N/A'}",
                    f"Quantité: {item.quantite}",
                    f"Prix unitaire: {item.prix_unitaire} DH HT",
                    f"Prix total: {item.quantite * item.prix_unitaire} DH HT",
                    f"Fournisseur: {item.commande.fournisseur.nom if hasattr(item, 'commande') and item.commande and item.commande.fournisseur else 'N/A'}",
                    f"Date commande: {item.commande.date_commande.strftime('%Y-%m-%d') if hasattr(item, 'commande') and item.commande and item.commande.date_commande else 'N/A'}",
                    f"Mode passation: {item.commande.mode_passation if hasattr(item, 'commande') and item.commande and hasattr(item.commande, 'mode_passation') else 'N/A'}"
                ]
            elif model_name in ['Designation', 'DesignationBureau', 'Description', 'DescriptionBureau']:
                content_parts = [
                    f"{model_name}: {item.nom}",
                    f"ID: {item.id}",
                    f"App: {item._meta.app_label if hasattr(item, '_meta') else 'N/A'}"
                ]
            elif model_name == 'CustomUser':
                content_parts = [
                    f"Utilisateur: {item.username}",
                    f"Nom: {item.last_name} {item.first_name}" if hasattr(item, 'last_name') and hasattr(item, 'first_name') and item.last_name and item.first_name else None,
                    f"Email: {item.email}" if hasattr(item, 'email') and item.email else None,
                    f"Date inscription: {item.date_joined.strftime('%Y-%m-%d') if hasattr(item, 'date_joined') and item.date_joined else 'N/A'}",
                    f"Dernière connexion: {item.last_login.strftime('%Y-%m-%d %H:%M') if hasattr(item, 'last_login') and item.last_login else 'N/A'}",
                    f"Actif: {'Oui' if item.is_active else 'Non'}",
                    f"Staff: {'Oui' if item.is_staff else 'Non'}",
                    f"Superuser: {'Oui' if item.is_superuser else 'Non'}",
                    f"Groupes: {', '.join([g.name for g in item.groups.all()]) if hasattr(item, 'groups') and item.groups.exists() else 'Aucun groupe'}",
                    f"Permissions: {', '.join([p.name for p in item.user_permissions.all()]) if hasattr(item, 'user_permissions') and item.user_permissions.exists() else 'Aucune permission'}"
                ]
            else:
                # Fallback for unknown models - try to get all fields dynamically
                obj_uid = self._get_object_uid(item, model_name)
                content_parts = [f"{model_name} PK: {obj_uid}"]
                
                # Try to get all model fields dynamically
                try:
                    for field in item._meta.fields:
                        field_name = field.name
                        field_value = getattr(item, field_name, None)
                        
                        if field_value is not None:
                            if hasattr(field_value, 'strftime'):  # Date field
                                try:
                                    content_parts.append(f"{field_name}: {field_value.strftime('%Y-%m-%d')}")
                                except:
                                    content_parts.append(f"{field_name}: {field_value}")
                            elif hasattr(field_value, 'username'):  # User field
                                content_parts.append(f"{field_name}: {field_value.username}")
                            elif hasattr(field_value, 'nom'):  # Related field with nom
                                content_parts.append(f"{field_name}: {field_value.nom}")
                            elif hasattr(field_value, 'name'):  # Related field with name
                                content_parts.append(f"{field_name}: {field_value.name}")
                            elif isinstance(field_value, bool):
                                content_parts.append(f"{field_name}: {'Oui' if field_value else 'Non'}")
                            elif isinstance(field_value, (int, float, str)):
                                content_parts.append(f"{field_name}: {field_value}")
                            else:
                                content_parts.append(f"{field_name}: {str(field_value)}")
                except Exception as e:
                    logger.warning(f"Could not extract fields dynamically for {model_name}: {e}")
                
        except Exception as e:
            uid = self._get_object_uid(item, model_name)
            logger.warning(f"Error building content for {model_name} PK {uid}: {e}")
            content_parts = [f"{model_name} PK: {uid}"]
            
        return [part for part in content_parts if part is not None]

    def _insert_documents_batch(self, documents: List[Dict]):
        """Insert a batch of documents into the RAG index"""
        try:
            for doc in documents:
                if len(doc['content']) > 5:  # Minimum content length
                    emb = self._to_vector_str(self.embed_model.encode(doc['content']))
                    with connection.cursor() as cursor:
                        # Generate a hash-based integer ID from the string ID
                        import hashlib
                        from django.utils import timezone
                        hash_id = int(hashlib.md5(doc['id'].encode()).hexdigest()[:8], 16)
                        now = timezone.now()
                        # Derive a stable numeric object_id from metadata pk (hash if not numeric)
                        raw_pk = str(doc['metadata'].get('pk') or doc['metadata'].get('id') or '')
                        try:
                            object_id = int(raw_pk)
                        except Exception:
                            object_id = int(hashlib.md5(raw_pk.encode()).hexdigest()[:8], 16)
                        
                        cursor.execute("""
                            INSERT INTO chatbot_documentvector 
                            (id, object_id, content, embedding, model_name, app_label, 
                             indexed_at, updated_at, is_active, content_type_id, priority, source)
                            VALUES (%s, %s, %s, %s::vector, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (content_type_id, object_id) 
                            DO UPDATE SET 
                                embedding = EXCLUDED.embedding,
                                content = EXCLUDED.content,
                                model_name = EXCLUDED.model_name,
                                app_label = EXCLUDED.app_label,
                                updated_at = EXCLUDED.updated_at,
                                is_active = EXCLUDED.is_active,
                                priority = EXCLUDED.priority
                            WHERE chatbot_documentvector.updated_at < EXCLUDED.updated_at
                                  OR chatbot_documentvector.content != EXCLUDED.content
                        """, (hash_id, object_id, doc['content'], emb, 
                             doc['metadata'].get('model', ''), doc['metadata'].get('app', ''),
                             now, now, True,
                             self._get_content_type_id(doc['metadata'].get('app', ''), doc['metadata'].get('model', '')),
                             1, 'database'))
                        connection.commit()
        except Exception as e:
            logger.error(f"Error inserting document batch: {e}")
            raise

    def _get_object_uid(self, item: Any, model_name: str) -> str:
        """Return a robust unique identifier for any model instance as string."""
        # Prefer Django pk when available
        if hasattr(item, 'pk') and item.pk is not None:
            return str(item.pk)
        # Fallbacks for known special models
        # Django Session model uses 'session_key'
        if hasattr(item, 'session_key'):
            return str(item.session_key)
        # Try common alternatives
        for attr in ('id', 'uuid', 'code', 'numero', 'numero_commande'):
            if hasattr(item, attr) and getattr(item, attr) is not None:
                try:
                    return str(getattr(item, attr))
                except Exception:
                    continue
        # Last resort: combine model name and Python id
        return f"{model_name.lower()}_{id(item)}"

    def clear_index(self):
        """Clear the RAG index"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM chatbot_documentvector")
                connection.commit()
            logger.info("RAG index cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing RAG index: {e}")
            raise

    def get_rag_count(self) -> int:
        """Get the current count of documents in the RAG index"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM chatbot_documentvector")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting RAG count: {e}")
            return 0

    def _to_vector_str(self, vector) -> str:
        """Convert vector to string format for PostgreSQL"""
        return '[' + ','.join(map(str, vector)) + ']'

    def _get_content_type_id(self, app_label: str, model_name: str) -> int:
        """Resolve Django content_type id for (app_label, model_name). Fallback to 1 if missing."""
        from django.contrib.contenttypes.models import ContentType
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name.lower())
            return ct.id
        except Exception:
            try:
                ct = ContentType.objects.get(model=model_name.lower())
                return ct.id
            except Exception:
                return 1

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for better search"""
        if not text:
            return ""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def semantic_search(self, query: str, filters: Optional[Dict] = None, top_k: int = 5) -> List[Dict]:
        """Enhanced semantic search via pgvector with intelligent filtering and ranking"""
        try:
            if not self.embed_model:
                logger.warning("Embedding model not available, returning empty results")
                return []
                
            if self.get_rag_count() == 0:
                logger.warning("RAG index is empty, populating...")
                self.populate_index()
                
            q = (query or "").strip()
            if not q:
                return []
                
            # Clean and normalize query text
            q = self._clean_text(q)
            qvec = self._to_vector_str(self.embed_model.encode(q))

            where_clauses = []
            params = []
            
            # Enhanced intelligent filtering
            if filters:
                if 'type' in filters:
                    where_clauses.append("(metadata->>'type') = %s")
                    params.append(filters['type'])
                if 'model' in filters:
                    where_clauses.append("(metadata->>'model') = %s")
                    params.append(filters['model'])
                if 'app' in filters:
                    where_clauses.append("(metadata->>'app') = %s")
                    params.append(filters['app'])
                if 'date_range' in filters:
                    # Add date-based filtering if needed
                    pass

            where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # Enhanced search with multiple strategies
            search_strategies = [
                # Strategy 1: Exact content match (highest priority)
                {
                    'sql': f"""
                        SELECT content, model_name, app_label, 0.0 AS dist, 'exact' as strategy
                        FROM chatbot_documentvector
                        {where_sql}
                        WHERE content ILIKE %s
                        ORDER BY content ILIKE %s DESC, length(content) ASC
                        LIMIT %s
                    """,
                    'params': [f"%{q}%", f"%{q}%", top_k],
                    'weight': 2.0
                },
                # Strategy 2: Semantic similarity (cosine)
                {
                    'sql': f"""
                        SELECT content, model_name, app_label, (embedding <=> %s::vector) AS dist, 'semantic' as strategy
                        FROM chatbot_documentvector
                        {where_sql}
                        ORDER BY dist ASC
                        LIMIT %s
                    """,
                    'params': [qvec, top_k],
                    'weight': 1.0
                },
                # Strategy 3: Keyword-based search
                {
                    'sql': f"""
                        SELECT content, model_name, app_label, 
                               CASE 
                                   WHEN content ILIKE %s THEN 0.1
                                   WHEN content ILIKE %s THEN 0.3
                                   WHEN content ILIKE %s THEN 0.5
                                   ELSE 1.0
                               END AS dist, 'keyword' as strategy
                        FROM chatbot_documentvector
                        {where_sql}
                        WHERE content ILIKE %s OR content ILIKE %s OR content ILIKE %s
                        ORDER BY dist ASC, length(content) ASC
                        LIMIT %s
                    """,
                    'params': [f"%{q}%", f"%{q[:len(q)//2]}%", f"%{q[:len(q)//3]}%", 
                              f"%{q}%", f"%{q[:len(q)//2]}%", f"%{q[:len(q)//3]}%", top_k],
                    'weight': 0.8
                }
            ]

            all_results = []
            
            for strategy in search_strategies:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SET statement_timeout = 3000")  # 3 second timeout per strategy
                        cursor.execute(strategy['sql'], strategy['params'])
                        rows = cursor.fetchall()
                        
                        for content, model_name, app_label, dist, strategy_name in rows:
                            # Calculate weighted score
                            if strategy_name == 'exact':
                                score = 1.0
                            elif strategy_name == 'semantic':
                                score = 1.0 / (1.0 + float(dist))
                            else:  # keyword
                                score = 1.0 - float(dist)
                            
                            # Apply strategy weight
                            weighted_score = score * strategy['weight']
                            
                            all_results.append({
                                "content": content,
                                "score": weighted_score,
                                "metadata": {
                                    "model": model_name or "",
                                    "app": app_label or "",
                                    "type": model_name.lower() if model_name else "",
                                    "strategy": strategy_name
                                }
                            })
                            
                except Exception as e:
                    logger.warning(f"Strategy {strategy['strategy']} failed: {e}")
                    continue

            # Remove duplicates and sort by score
            seen_contents = set()
            unique_results = []
            
            for result in sorted(all_results, key=lambda x: x['score'], reverse=True):
                content_hash = hash(result['content'][:100])  # Hash first 100 chars
                if content_hash not in seen_contents:
                    seen_contents.add(content_hash)
                    unique_results.append(result)
                    if len(unique_results) >= top_k:
                        break

            logger.info(f"Semantic search returned {len(unique_results)} results using multiple strategies")
            return unique_results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def validate_coherence(self) -> Dict[str, Any]:
        """Validate RAG-DB coherence and return detailed report"""
        try:
            from django.apps import apps
            
            # Count RAG vectors
            rag_count = self.get_rag_count()
            
            # Count database records
            models_to_count = [
                ('fournisseurs', 'Fournisseur'),
                ('livraison', 'Livraison'),
                ('materiel_informatique', 'MaterielInformatique'),
                ('materiel_bureautique', 'MaterielBureau'),
                ('commande_informatique', 'Commande'),
                ('commande_bureau', 'CommandeBureau'),
                ('demande_equipement', 'DemandeEquipement'),
                ('demande_equipement', 'ArchiveDecharge'),
                ('admin', 'LogEntry'),
                ('commande_informatique', 'LigneCommande'),
                ('commande_bureau', 'LigneCommandeBureau'),
                ('commande_informatique', 'Designation'),
                ('commande_bureau', 'DesignationBureau'),
                ('commande_informatique', 'Description'),
                ('commande_bureau', 'DescriptionBureau'),
                ('users', 'CustomUser')
            ]
            
            total_db_records = 0
            model_counts = {}
            
            for app, model in models_to_count:
                try:
                    count = apps.get_model(app, model).objects.count()
                    total_db_records += count
                    model_counts[f"{app}.{model}"] = count
                except Exception as e:
                    logger.warning(f"Error counting {app}.{model}: {e}")
                    model_counts[f"{app}.{model}"] = 0
            
            coherence_ratio = (rag_count / total_db_records) if total_db_records > 0 else 0
            
            # Check for missing entities
            missing_entities = self._check_missing_entities()
            
            return {
                'status': 'success',
                'total_rag_vectors': rag_count,
                'total_db_records': total_db_records,
                'coherence_ratio': coherence_ratio,
                'model_counts': model_counts,
                'missing_entities': missing_entities
            }
            
        except Exception as e:
            logger.error(f"Error validating coherence: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'total_rag_vectors': 0,
                'total_db_records': 0,
                'coherence_ratio': 0
            }

    def _check_missing_entities(self) -> List[str]:
        """Check for specific missing entities in RAG index"""
        missing = []
        try:
            # Check for specific entities that should be in the index
            test_entities = [
                ('WANA CORPORATE SA', 'fournisseur'),
                ('cd14', 'materielinformatique'),
                ('cd12', 'materielinformatique'),
                ('cd13', 'materielinformatique')
            ]
            
            for entity_name, entity_type in test_entities:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM chatbot_documentvector 
                        WHERE content ILIKE %s AND model_name ILIKE %s
                    """, (f'%{entity_name}%', f'%{entity_type}%'))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        missing.append(f"{entity_type.title()}: {entity_name}")
                        
        except Exception as e:
            logger.error(f"Error checking missing entities: {e}")
            
        return missing
