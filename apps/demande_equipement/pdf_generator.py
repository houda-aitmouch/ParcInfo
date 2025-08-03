from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from django.utils import timezone
from django.conf import settings
import os

def generate_decharge_pdf(demande):
    """
    Génère un PDF de décharge pour une demande approuvée
    """
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    
    # Créer le document PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style pour le titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Times-Bold',
        textColor=colors.black,
        spaceBefore=20
    )
    
    # Style pour le logo ADD
    logo_style = ParagraphStyle(
        'LogoStyle',
        parent=styles['Normal'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        textColor=colors.black
    )
    
    # Style pour le texte normal
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica',
        textColor=colors.black,
        leading=14
    )
    
    # Style pour le texte en gras
    bold_style = ParagraphStyle(
        'BoldStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        leading=14
    )
    
    # Style pour la signature
    signature_style = ParagraphStyle(
        'SignatureStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=30,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        textColor=colors.black,
        spaceBefore=20
    )
    
    # Style pour le footer
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica',
        textColor=colors.grey,
        leading=12
    )
    
    # Style pour les lignes de séparation
    line_style = ParagraphStyle(
        'LineStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica',
        textColor=colors.grey,
        spaceBefore=15
    )
    
    # 1. En-tête avec logo ADD
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'ADD.png')
    if os.path.exists(logo_path):
        # Ajouter le logo ADD
        logo = Image(logo_path, width=2*inch, height=1*inch)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 10))
    else:
        # Fallback si le logo n'existe pas
        story.append(Paragraph("# ADD", logo_style))

    story.append(Spacer(1, 20))
    
    # 2. Ligne horizontale
    story.append(Paragraph("_" * 50, line_style))
    
    # 3. Titre personnalisé selon le type de demande
    if demande.type_article == 'fourniture':
        titre = "Décharge - Fournitures de Bureau"
    elif demande.categorie == 'informatique':
        titre = "Décharge - Matériel Informatique"
    elif demande.categorie == 'bureau':
        titre = "Décharge - Matériel de Bureau"
    else:
        titre = "Décharge"
    
    story.append(Paragraph(titre, title_style))
    
    # 4. Ligne horizontale
    story.append(Paragraph("_" * 50, line_style))
    story.append(Spacer(1, 30))
    
    # 5. Introduction personnalisée selon le type de demande
    nom_demandeur = demande.demandeur.get_full_name()
    
    if demande.type_article == 'fourniture':
        intro_text = f"Je soussigné(e) : M./Mme. {nom_demandeur}, certifie avoir reçu les fournitures de bureau suivantes :"
    elif demande.categorie == 'informatique':
        intro_text = f"Je soussigné(e) : M./Mme. {nom_demandeur}, certifie avoir reçu le matériel informatique suivant :"
    elif demande.categorie == 'bureau':
        intro_text = f"Je soussigné(e) : M./Mme. {nom_demandeur}, certifie avoir reçu le matériel de bureau suivant :"
    else:
        intro_text = f"Je soussigné(e) : M./Mme. {nom_demandeur}, certifie avoir reçu l'équipement suivant :"
    
    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 20))
    
    # 6. Liste des équipements personnalisée selon le type de demande
    if demande.type_article == 'fourniture':
        # Pour les fournitures, afficher un message générique
        equipements = [
            "• Fournitures de bureau diverses (papeterie, consommables, etc.)",
            "• Quantité et types selon la demande approuvée"
        ]
    elif demande.type_article == 'materiel' and demande.materiel_selectionne_id:
        # Récupérer les informations du matériel affecté
        if demande.categorie == 'informatique':
            from apps.materiel_informatique.models import MaterielInformatique
            try:
                materiel = MaterielInformatique.objects.get(id=demande.materiel_selectionne_id)
                designation = materiel.ligne_commande.designation.nom
                description = materiel.ligne_commande.description.nom
                code_inventaire = materiel.code_inventaire
                numero_serie = materiel.numero_serie if materiel.numero_serie else "N/A"
                
                # Créer la liste des équipements
                equipements = [
                    f"• {designation} {description}, SN: {numero_serie}, numéro d'inventaire: {code_inventaire};"
                ]
                
                # Ajouter les accessoires si c'est un ordinateur
                if 'ordinateur' in designation.lower() or 'pc' in designation.lower():
                    equipements.append("• Accessoires: clavier, souris, sacoche, câble anti-vol, disque dur")
                
            except MaterielInformatique.DoesNotExist:
                equipements = ["• Matériel non trouvé"]
                
        elif demande.categorie == 'bureau':
            from apps.materiel_bureautique.models import MaterielBureau
            try:
                materiel = MaterielBureau.objects.get(id=demande.materiel_selectionne_id)
                designation = materiel.ligne_commande.designation.nom
                description = materiel.ligne_commande.description.nom
                code_inventaire = materiel.code_inventaire
                
                equipements = [
                    f"• {designation} {description}, numéro d'inventaire: {code_inventaire};"
                ]
                
            except MaterielBureau.DoesNotExist:
                equipements = ["• Matériel non trouvé"]
        else:
            equipements = ["• Matériel demandé"]
    else:
        equipements = ["• Équipement demandé (non encore affecté)"]
    
    # Ajouter chaque équipement
    for equipement in equipements:
        story.append(Paragraph(equipement, normal_style))
    
    story.append(Spacer(1, 15))
    
    # 7. Date
    date_affectation = demande.date_affectation or timezone.now()
    
    # Mapping des mois en français
    mois_fr = {
        1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril',
        5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août',
        9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
    }
    
    jour = date_affectation.day
    mois = mois_fr[date_affectation.month]
    annee = date_affectation.year
    
    date_text = f"Le : {jour} {mois} {annee}"
    story.append(Paragraph(date_text, normal_style))
    story.append(Spacer(1, 15))
    
    # 8. Signature
    story.append(Paragraph("Signature", signature_style))
    story.append(Spacer(1, 10))
    
    # Ajouter la signature électronique si elle existe
    if demande.signature_image:
        try:
            signature_path = os.path.join(settings.MEDIA_ROOT, demande.signature_image)
            if os.path.exists(signature_path):
                # Ajouter la signature électronique alignée à droite
                signature_img = Image(signature_path, width=2.5*inch, height=0.8*inch)
                signature_img.hAlign = 'RIGHT'
                story.append(signature_img)
                story.append(Spacer(1, 5))
            else:
                # Fallback si l'image n'existe pas - ligne alignée à droite
                fallback_signature = Paragraph("_" * 30, signature_style)
                fallback_signature.alignment = TA_RIGHT
                story.append(fallback_signature)
        except Exception as e:
            # Fallback en cas d'erreur - ligne alignée à droite
            fallback_signature = Paragraph("_" * 0, signature_style)
            fallback_signature.alignment = TA_RIGHT
            story.append(fallback_signature)
    else:
        # Ligne de signature par défaut alignée à droite
        default_signature = Paragraph("_" * 0, signature_style)
        default_signature.alignment = TA_RIGHT
        story.append(default_signature)

    story.append(Spacer(1, 10))
    # 9. Footer
    story.append(Paragraph("_" * 60, line_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph('« Espace les Lauriers » aile B, angle des Avenues Ennakhil et Mehdi Ben Barka, Hay Ryad', footer_style))
    story.append(Paragraph('Rabat-Maroc', footer_style))
    story.append(Paragraph('Tél. : +212 5 37 56 93 00 Fax. : +212 5 37 71 33 36', footer_style))
    
    # Construire le PDF
    doc.build(story)
    
    # Récupérer le contenu du buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content

def save_decharge_pdf(demande, file_path):
    """
    Sauvegarde le PDF de décharge dans un fichier
    """
    pdf_content = generate_decharge_pdf(demande)
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Sauvegarder le fichier
    with open(file_path, 'wb') as f:
        f.write(pdf_content)
    
    return file_path 