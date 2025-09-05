#!/usr/bin/env python3
"""
Corrections des méthodes du chatbot ParcInfo pour résoudre les problèmes identifiés
"""

def corrected_handle_codes_by_designation(self, entities: Dict[str, Any]) -> str:
    """
    Version corrigée de _handle_codes_by_designation pour mieux gérer les matériels 'Baie'
    """
    q = entities.get('original_query', '') or ''
    ql = q.lower()
    import re as _re
    
    # Extraction du terme de recherche
    m = _re.search(r"(?:code\s*d['\"]?inventaire['\"]?|codes\s*d['\"]?inventaire['\"]?|code\s*inventaire|codes\s*inventaire)\s*(?:de|du|de\s+la|des)\s*([\w\-À-ÿ /]+)", ql)
    term = m.group(1).strip() if m else None
    
    if not term:
        # fallback: pick a designation word in query (e.g., "Baie")
        words = [w for w in ql.split() if len(w) >= 3]
        term = words[-1] if words else None
    
    if not term:
        return "Veuillez préciser la désignation."
    
    # Recherche améliorée dans les matériels informatiques
    it_qs = MaterielInformatique.objects.filter(
        Q(ligne_commande__designation__nom__icontains=term) |
        Q(ligne_commande__description__nom__icontains=term)
    ).select_related('ligne_commande__designation', 'ligne_commande__description', 'utilisateur', 'ligne_commande__commande')
    
    # Recherche améliorée dans les matériels bureautiques
    bu_qs = MaterielBureau.objects.filter(
        Q(ligne_commande__designation__nom__icontains=term) |
        Q(ligne_commande__description__nom__icontains=term)
    ).select_related('ligne_commande__designation', 'ligne_commande__description', 'utilisateur', 'ligne_commande__commande')
    
    # Recherche dans les lignes de commande pour les matériels sans codes d'inventaire
    from apps.commande_informatique.models import LigneCommande
    ligne_qs = LigneCommande.objects.filter(
        Q(designation__nom__icontains=term) |
        Q(description__nom__icontains=term)
    ).select_related('designation', 'description', 'commande', 'commande__fournisseur')
    
    disp = term.strip()
    disp = disp[:1].upper() + disp[1:]
    
    lines = [f"Voici les codes d'inventaire pour {disp} :"]
    count = 0
    
    # Matériels informatiques avec codes d'inventaire
    for mtrl in it_qs:
        utilisateur = getattr(mtrl.utilisateur, 'username', 'non affecté') if mtrl.utilisateur else 'non affecté'
        designation = 'non disponible'
        description = 'non disponible'
        
        if hasattr(mtrl, 'ligne_commande') and mtrl.ligne_commande:
            if hasattr(mtrl.ligne_commande, 'designation') and mtrl.ligne_commande.designation:
                designation = getattr(mtrl.ligne_commande.designation, 'nom', 'non disponible')
            if hasattr(mtrl.ligne_commande, 'description') and mtrl.ligne_commande.description:
                description = getattr(mtrl.ligne_commande.description, 'nom', 'non disponible')
        
        lines.append(f"- {mtrl.code_inventaire} ({designation} - {description}, S/N: {mtrl.numero_serie or 'non disponible'}, affecté à: {utilisateur})")
        count += 1
    
    # Matériels bureautiques avec codes d'inventaire
    for mtrl in bu_qs:
        utilisateur = getattr(mtrl.utilisateur, 'username', 'non affecté') if mtrl.utilisateur else 'non affecté'
        designation = 'non disponible'
        description = 'non disponible'
        
        if hasattr(mtrl, 'ligne_commande') and mtrl.ligne_commande:
            if hasattr(mtrl.ligne_commande, 'designation') and mtrl.ligne_commande.designation:
                designation = getattr(mtrl.ligne_commande.designation, 'nom', 'non disponible')
            if hasattr(mtrl.ligne_commande, 'description') and mtrl.ligne_commande.description:
                description = getattr(mtrl.ligne_commande.description, 'nom', 'non disponible')
        
        lines.append(f"- {mtrl.code_inventaire} ({designation} - {description}, affecté à: {utilisateur})")
        count += 1
    
    # Si aucun matériel avec code d'inventaire n'est trouvé, afficher les lignes de commande
    if count == 0 and ligne_qs.exists():
        lines.append(f"\nAucun code d'inventaire trouvé pour {disp}, mais voici les informations des commandes :")
        for ligne in ligne_qs:
            fournisseur = ligne.commande.fournisseur.nom if ligne.commande and ligne.commande.fournisseur else 'non disponible'
            lines.append(f"- Commande {ligne.commande.numero_commande} : {ligne.designation.nom} - {ligne.description.nom}")
            lines.append(f"  Quantité : {ligne.quantite}, Prix : {ligne.prix_unitaire}, Fournisseur : {fournisseur}")
            count += 1
    
    if count == 0:
        return self._make_response_human(
            f"Aucun matériel trouvé pour la désignation '{term}'.",
            'no_results',
            True
        )
    
    return self._make_response_human("\n".join(lines), 'positive_confirmation', True)

def corrected_handle_baie_inventory_query(self, entities: Dict[str, Any]) -> str:
    """
    Méthode spécialisée pour les requêtes sur l'inventaire des 'Baies'
    """
    try:
        from apps.commande_informatique.models import LigneCommande
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.livraison.models import Livraison
        
        # Recherche des matériels informatiques avec désignation 'Baie'
        baie_materials = MaterielInformatique.objects.filter(
            Q(ligne_commande__designation__nom__icontains='Baie') |
            Q(ligne_commande__description__nom__icontains='Baie')
        ).select_related('ligne_commande__designation', 'ligne_commande__description', 'utilisateur', 'ligne_commande__commande')
        
        # Recherche des lignes de commande pour 'Baie'
        baie_lignes = LigneCommande.objects.filter(
            designation__nom__icontains='Baie'
        ).select_related('designation', 'description', 'commande', 'commande__fournisseur')
        
        lines = ["Voici l'inventaire des matériels 'Baie' :"]
        
        # Matériels avec codes d'inventaire
        if baie_materials.exists():
            lines.append("\n📦 Matériels avec codes d'inventaire :")
            for mat in baie_materials:
                designation = mat.ligne_commande.designation.nom if mat.ligne_commande and mat.ligne_commande.designation else 'non disponible'
                description = mat.ligne_commande.description.nom if mat.ligne_commande and mat.ligne_commande.description else 'non disponible'
                utilisateur = mat.utilisateur.username if mat.utilisateur else 'non affecté'
                commande = mat.ligne_commande.commande.numero_commande if mat.ligne_commande and mat.ligne_commande.commande else 'non disponible'
                
                lines.append(f"- {mat.code_inventaire} : {designation} - {description}")
                lines.append(f"  S/N : {mat.numero_serie or 'non disponible'}")
                lines.append(f"  Affecté à : {utilisateur}")
                lines.append(f"  Commande : {commande}")
                
                # Vérifier la livraison
                try:
                    livraison = Livraison.objects.get(numero_commande=commande)
                    if livraison.date_livraison_effective and livraison.date_livraison_prevue:
                        retard = (livraison.date_livraison_effective - livraison.date_livraison_prevue).days
                        if retard > 0:
                            lines.append(f"  ⚠️ Livraison en retard de {retard} jours")
                        else:
                            lines.append(f"  ✅ Livraison à temps")
                    lines.append(f"  Statut livraison : {livraison.statut_livraison}")
                except Livraison.DoesNotExist:
                    lines.append(f"  📦 Livraison : non trouvée")
                lines.append("")
        
        # Lignes de commande (matériels sans codes d'inventaire)
        if baie_lignes.exists():
            lines.append("📋 Lignes de commande pour 'Baie' :")
            for ligne in baie_lignes:
                fournisseur = ligne.commande.fournisseur.nom if ligne.commande and ligne.commande.fournisseur else 'non disponible'
                lines.append(f"- Commande {ligne.commande.numero_commande} : {ligne.designation.nom} - {ligne.description.nom}")
                lines.append(f"  Quantité : {ligne.quantite}, Prix unitaire : {ligne.prix_unitaire}")
                lines.append(f"  Fournisseur : {fournisseur}")
                lines.append(f"  Date commande : {ligne.commande.date_commande}")
                lines.append(f"  Date réception : {ligne.commande.date_reception}")
                lines.append("")
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"Erreur lors de la recherche des matériels 'Baie' : {e}"

def corrected_handle_fournisseurs_ice_001(self, entities: Dict[str, Any]) -> str:
    """
    Méthode corrigée pour les fournisseurs avec ICE commençant par 001
    """
    try:
        from apps.fournisseurs.models import Fournisseur
        
        # Recherche des fournisseurs avec ICE commençant par 001
        fournisseurs = Fournisseur.objects.filter(ice__startswith='001').order_by('nom')
        
        if not fournisseurs.exists():
            return "Aucun fournisseur avec ICE commençant par 001 n'a été trouvé."
        
        lines = [f"Fournisseurs avec ICE commençant par 001 ({fournisseurs.count()} trouvés) :"]
        
        for fournisseur in fournisseurs:
            lines.append(f"• {fournisseur.nom} - ICE: {fournisseur.ice}")
            if hasattr(fournisseur, 'adresse') and fournisseur.adresse:
                lines.append(f"  📍 {fournisseur.adresse}")
            lines.append("")
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"Erreur lors de la recherche des fournisseurs : {e}"

def corrected_handle_delivery_delays(self, entities: Dict[str, Any]) -> str:
    """
    Méthode corrigée pour les livraisons en retard
    """
    try:
        from apps.livraison.models import Livraison
        from datetime import date
        
        today = date.today()
        delayed_deliveries = []
        
        # Recherche de toutes les livraisons
        livraisons = Livraison.objects.all()
        
        for livraison in livraisons:
            if livraison.date_livraison_prevue and livraison.date_livraison_effective:
                if livraison.date_livraison_effective > livraison.date_livraison_prevue:
                    delay_days = (livraison.date_livraison_effective - livraison.date_livraison_prevue).days
                    delayed_deliveries.append((livraison, delay_days))
        
        if not delayed_deliveries:
            return "Aucune livraison en retard n'a été trouvée."
        
        lines = [f"Livraisons en retard ({len(delayed_deliveries)} trouvées) :"]
        
        for livraison, delay in delayed_deliveries:
            lines.append(f"\n📦 Commande {livraison.numero_commande} :")
            lines.append(f"   📅 Prévu : {livraison.date_livraison_prevue}")
            lines.append(f"   📅 Effectif : {livraison.date_livraison_effective}")
            lines.append(f"   ⚠️ Retard : {delay} jours")
            lines.append(f"   📊 Statut : {livraison.statut_livraison}")
            
            # Ajouter des informations sur le matériel si disponible
            try:
                from apps.commande_informatique.models import Commande
                commande = Commande.objects.get(numero_commande=livraison.numero_commande)
                if hasattr(commande, 'fournisseur') and commande.fournisseur:
                    lines.append(f"   🏢 Fournisseur : {commande.fournisseur.nom}")
            except:
                pass
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"Erreur lors de la recherche des livraisons en retard : {e}"

def corrected_handle_material_storage_location(self, entities: Dict[str, Any]) -> str:
    """
    Méthode corrigée pour le lieu de stockage d'un matériel
    """
    try:
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.materiel_bureautique.models import MaterielBureau
        
        query = entities.get('original_query', '')
        
        # Extraction du code d'inventaire
        import re
        match = re.search(r'(\w+/\w+/\d+|\w+\d+)', query)
        if not match:
            return "Veuillez préciser le code d'inventaire du matériel."
        
        code_inventaire = match.group(1)
        
        # Recherche dans les matériels informatiques
        mat_info = MaterielInformatique.objects.filter(code_inventaire=code_inventaire).first()
        if mat_info:
            if hasattr(mat_info, 'lieu_stockage') and mat_info.lieu_stockage:
                return f"Le lieu de stockage du matériel {code_inventaire} est : {mat_info.lieu_stockage}"
            else:
                return f"Le matériel {code_inventaire} n'a pas de lieu de stockage renseigné."
        
        # Recherche dans les matériels bureautiques
        mat_bureau = MaterielBureau.objects.filter(code_inventaire=code_inventaire).first()
        if mat_bureau:
            if hasattr(mat_bureau, 'lieu_stockage') and mat_bureau.lieu_stockage:
                return f"Le lieu de stockage du matériel {code_inventaire} est : {mat_bureau.lieu_stockage}"
            else:
                return f"Le matériel {code_inventaire} n'a pas de lieu de stockage renseigné."
        
        return f"Aucun matériel avec le code {code_inventaire} n'a été trouvé."
        
    except Exception as e:
        return f"Erreur lors de la recherche du lieu de stockage : {e}"

# Instructions d'implémentation
IMPLEMENTATION_INSTRUCTIONS = """
INSTRUCTIONS D'IMPLÉMENTATION DES CORRECTIONS :

1. REMPLACER la méthode _handle_codes_by_designation dans core_chatbot.py :
   - Copier le contenu de corrected_handle_codes_by_designation
   - Remplacer la méthode existante

2. AJOUTER les nouvelles méthodes spécialisées :
   - corrected_handle_baie_inventory_query
   - corrected_handle_fournisseurs_ice_001
   - corrected_handle_delivery_delays
   - corrected_handle_material_storage_location

3. MODIFIER la méthode process_query pour utiliser ces nouvelles méthodes :
   - Ajouter des routes early pour "Code inventaire de la Baie"
   - Ajouter des routes early pour "Fournisseurs avec ICE commençant par 001"
   - Ajouter des routes early pour "Livraisons en retard"
   - Ajouter des routes early pour "Lieu de stockage"

4. TESTER les corrections :
   - Vérifier que "Code inventaire de la Baie" retourne les 4 matériels
   - Vérifier que "Fournisseurs ICE 001" retourne les 24 fournisseurs
   - Vérifier que "Livraisons en retard" retourne les 4 livraisons
   - Vérifier que "Lieu de stockage ADD/INFO/01094" retourne "etage3"

5. DOCUMENTER les changements :
   - Mettre à jour le rapport de correction
   - Tester avec le chatbot en production
"""
