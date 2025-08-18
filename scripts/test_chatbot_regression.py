import os
import sys
from typing import List, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
import django

django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot


def norm_response(res):
    if isinstance(res, dict):
        return res.get('response', '') or ''
    return res or ''


def run_tests(tests: List[Tuple[str, List[str]]]) -> int:
    bot = ParcInfoChatbot()
    total = 0
    failed = 0
    for idx, (query, expects) in enumerate(tests, 1):
        res = bot.process_query(query)
        text = norm_response(res)
        ok = all(exp in text for exp in expects)
        total += 1
        status = 'OK' if ok else 'FAIL'
        print(f"[{idx:02d}] {status}: {query}")
        if not ok:
            failed += 1
            print("Expected substrings:")
            for e in expects:
                print(f"  - {e}")
            print("Actual response:")
            print(text)
            print("----")
    print(f"Summary: {total - failed}/{total} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    TESTS: List[Tuple[str, List[str]]] = [
        # Garanties
        ("Quand expire la garantie de la commande informatique avec le numéro 123 ?", ["Fin de garantie:", "Active:"]),
        ("Liste toutes les commandes dont la garantie expire après août 2025.", ["123", "AOO2025"]),
        ("Quelles commandes ont une garantie exprimée en mois ?", ["BC23", "123"]),
        ("Les livraisons associées à la commande AOO2025 sont-elles encore sous garantie ?", ["AOO2025", "Fin de garantie:"]),
        ("Quelle est la durée de garantie pour les matériels livrés le 14 août 2025 ?", ["14/08/2025", "BC23"]),

        # Commandes: lignes/fournisseur
        ("Quelles lignes de commande sont associées à la commande BC23 ?", ["Lignes de commande BC23"]),
        ("Qui est le fournisseur associé à la commande AOO2025 ?", ["Fournisseur de AOO2025", "AEBDM"]),

        # Groupes et permissions
        ("Liste des groupes d'utilisateurs comme Employe ou Gestionnaire Informatique.", ["Groupes d'utilisateurs", "Employe", "Gestionnaire Informatique"]),
        ("Quelles permissions a le groupe \"Super Admin\" ?", ["Permissions du groupe Super Admin"]),

        # Livraisons: conformité / créateur
        ("La livraison de la commande 123 est-elle conforme ?", ["Livraison 123", "Conforme:"]),
        ("Qui a créé la livraison pour le numéro de commande 123 ?", ["Créateur de la livraison 123"]),

        # Localisation matériels
        ("Quels matériels sont stockés à l'étage 1 ?", ["Matériels à etage1"]),

        # Utilisateur par numéro de série
        ("À quel utilisateur est affecté le matériel avec numéro de série sn12 ?", ["sn12", "affecté"]),

        # Archives
        ("Liste des archives de décharges existantes.", ["Archives de décharges"]),

        # ——— Added 13 regression questions ———
        # 1. Demande ID approval date
        ("Quand la demande ID 21 a-t-elle été approuvée ?", ["Demande 21", "Approuv"]),

        # 2. Matériel affecté aux demandes de superadmin (we expect listing pattern)
        ("Quel matériel a été affecté à la demande de 'superadmin' ?", ["superadmin", "Matériels", "affect"]),

        # 3. Décharges signées pour demandes bureautiques
        ("Y a-t-il des décharges signées pour les demandes bureautiques ?", ["Archive", "bureaut", "Demande"]),

        # 4. Numéro de série de la fourniture 'cable'
        ("Quel est le numéro de série de la fourniture 'cable' ?", ["cable", "sn"]),

        # 5. Matériels informatiques sous garantie (generic listing)
        ("Quels matériels informatiques sont encore sous garantie ?", ["Matériels", "Informatique", "Fin:"]),

        # 6. Garantie active pour ADD/INFO/01094
        ("La garantie du matériel avec le code d’inventaire ADD/INFO/01094 est-elle toujours active ?", ["ADD/INFO/01094", "Fin de garantie", "Active"]),

        # 7. Matériels bureautiques expirant bientôt
        ("Liste les matériels bureautiques dont la garantie expire bientôt.", ["bureaut", "garantie", "expire"]),

        # 8. Matériel informatique avec numéro de série sn12 et garantie
        ("Quel matériel informatique avec le numéro de série sn12 a une garantie associée ?", ["sn12", "Fin de garantie"]),

        # 9. Matériels affectés à superadmin sous garantie
        ("Y a-t-il des matériels affectés à 'superadmin' encore sous garantie ?", ["superadmin", "garantie", "Fin:"]),

        # 10. Types de matériels
        ("Quels types de matériels sont disponibles ?", ["Types de matériels", "Informatique", "Bureau"]),

        # 11. Commandes bureautiques avec garantie en années
        ("Liste des commandes bureautiques avec garantie en années.", ["Bureau", "an", "AOO2025"]),

        # 12. Commandes sans garantie spécifiée
        ("Y a-t-il des commandes sans garantie spécifiée ?", ["garantie", "AOO2025", "123", "BC23"]),

        # 13. Code d’inventaire de la Baie
        ("Quel est le code d’inventaire de la Baie ?", ["Baie", "code", "cd", "ADD/INFO"]),
    ]

    sys.exit(run_tests(TESTS))


