#!/bin/bash

# Fonction pour afficher les messages d'information
print_info() {
    echo -e "\nℹ️  $1"
}

# Fonction pour afficher les messages de succès
print_success() {
    echo -e "✅ $1"
}

# Fonction pour afficher les messages d'erreur
print_error() {
    echo -e "❌ $1"
}

echo -e "\n🔍 Test des Signatures dans les Décharges"
echo "=========================================="

# Test 1: Vérification des signatures disponibles
print_info "Test 1: Vérification des signatures disponibles..."
SIGNATURES=(
    "signature_demande_11_20250731_161245.png"
    "signature_demande_12_20250825_102513.png"
    "signature_demande_20_20250731_194644.png"
    "signature_demande_21_20250801_104658.png"
    "signature_demande_22_20250801_105430.png"
    "signature_demande_23_20250802_184346.png"
    "signature_demande_26_20250821_164052.png"
    "signature_demande_32_20250823_134238.png"
    "signature_demande_45_20250825_103435.png"
    "signature_demande_48_20250904_174915.png"
    "signature_demande_50_20250904_182416.png"
    "signature_demande_51_20250904_181531.png"
)

SIGNATURE_COUNT=0
for signature in "${SIGNATURES[@]}"; do
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:80/media/signatures/$signature" | grep -q "200"; then
        print_success "Signature accessible: $signature"
        ((SIGNATURE_COUNT++))
    else
        print_error "Signature inaccessible: $signature"
    fi
done

print_info "Résultat: $SIGNATURE_COUNT/${#SIGNATURES[@]} signatures accessibles"

# Test 2: Vérification des décharges PDF
print_info "Test 2: Vérification des décharges PDF..."
DECLARATIONS=(
    "decharge_demande_20_superadmin_20250731_172138.pdf"
    "decharge_demande_21_superadmin_20250801_104627.pdf"
    "decharge_demande_22_superadmin_20250801_105349.pdf"
    "decharge_demande_23_superadmin_20250802_184315.pdf"
    "decharge_demande_25_superadmin_20250825_154557.pdf"
    "decharge_demande_26_superadmin_20250821_164019.pdf"
    "decharge_demande_32_gestionnaire info_20250823_133712.pdf"
    "decharge_demande_45_employe_20250825_103410.pdf"
    "decharge_demande_47_superadmin_20250904_174332.pdf"
    "decharge_demande_48_gestionnaire info_20250904_174813.pdf"
    "decharge_demande_50_gestionnaire bureau_20250904_181316.pdf"
    "decharge_demande_51_gestionnaire info_20250904_180953.pdf"
    "decharge_demande_52_superadmin_20250904_181237.pdf"
    "decharge_demande_54_gestionnaire info_20250904_184923.pdf"
)

DECLARATION_COUNT=0
for declaration in "${DECLARATIONS[@]}"; do
    if curl -s -o /dev/null -w "%{http_code}" "http://localhost:80/media/decharges/$declaration" | grep -q "200"; then
        print_success "Décharge accessible: $declaration"
        ((DECLARATION_COUNT++))
    else
        print_error "Décharge inaccessible: $declaration"
    fi
done

print_info "Résultat: $DECLARATION_COUNT/${#DECLARATIONS[@]} décharges accessibles"

# Test 3: Vérification du type MIME des signatures
print_info "Test 3: Vérification du type MIME des signatures..."
SAMPLE_SIGNATURE="signature_demande_11_20250731_161245.png"
CONTENT_TYPE=$(curl -s -I "http://localhost:80/media/signatures/$SAMPLE_SIGNATURE" | grep -i "content-type" | cut -d' ' -f2 | tr -d '\r\n')

if [[ "$CONTENT_TYPE" == *"image/png"* ]]; then
    print_success "Type MIME correct pour les signatures: $CONTENT_TYPE"
else
    print_error "Type MIME incorrect pour les signatures: $CONTENT_TYPE"
fi

# Test 4: Vérification du type MIME des décharges
print_info "Test 4: Vérification du type MIME des décharges..."
SAMPLE_DECLARATION="decharge_demande_20_superadmin_20250731_172138.pdf"
CONTENT_TYPE=$(curl -s -I "http://localhost:80/media/decharges/$SAMPLE_DECLARATION" | grep -i "content-type" | cut -d' ' -f2 | tr -d '\r\n')

if [[ "$CONTENT_TYPE" == *"application/pdf"* ]]; then
    print_success "Type MIME correct pour les décharges: $CONTENT_TYPE"
else
    print_error "Type MIME incorrect pour les décharges: $CONTENT_TYPE"
fi

# Test 5: Vérification de la taille des fichiers
print_info "Test 5: Vérification de la taille des fichiers..."
SAMPLE_SIGNATURE_SIZE=$(curl -s -I "http://localhost:80/media/signatures/$SAMPLE_SIGNATURE" | grep -i "content-length" | cut -d' ' -f2 | tr -d '\r\n')
SAMPLE_DECLARATION_SIZE=$(curl -s -I "http://localhost:80/media/decharges/$SAMPLE_DECLARATION" | grep -i "content-length" | cut -d' ' -f2 | tr -d '\r\n')

if [[ "$SAMPLE_SIGNATURE_SIZE" -gt 0 ]]; then
    print_success "Signature a une taille valide: $SAMPLE_SIGNATURE_SIZE bytes"
else
    print_error "Signature a une taille invalide: $SAMPLE_SIGNATURE_SIZE bytes"
fi

if [[ "$SAMPLE_DECLARATION_SIZE" -gt 0 ]]; then
    print_success "Décharge a une taille valide: $SAMPLE_DECLARATION_SIZE bytes"
else
    print_error "Décharge a une taille invalide: $SAMPLE_DECLARATION_SIZE bytes"
fi

# Résumé final
echo -e "\n📊 RÉSUMÉ DES TESTS DE SIGNATURES"
echo "=================================="
echo "✅ Signatures accessibles: $SIGNATURE_COUNT/${#SIGNATURES[@]}"
echo "✅ Décharges accessibles: $DECLARATION_COUNT/${#DECLARATIONS[@]}"
echo "✅ Type MIME signatures: $CONTENT_TYPE"
echo "✅ Taille signature: $SAMPLE_SIGNATURE_SIZE bytes"
echo "✅ Taille décharge: $SAMPLE_DECLARATION_SIZE bytes"

if [[ $SIGNATURE_COUNT -eq ${#SIGNATURES[@]} && $DECLARATION_COUNT -eq ${#DECLARATIONS[@]} ]]; then
    print_success "🎉 TOUS LES FICHIERS MÉDIA SONT ACCESSIBLES !"
    print_success "Les signatures dans les décharges fonctionnent parfaitement !"
else
    print_error "⚠️  Certains fichiers média ne sont pas accessibles"
    exit 1
fi

echo -e "\n🌐 URLs de test :"
echo "  📝 Signatures: http://localhost:80/media/signatures/"
echo "  📄 Décharges: http://localhost:80/media/decharges/"
echo "  🖼️  Exemple signature: http://localhost:80/media/signatures/$SAMPLE_SIGNATURE"
echo "  📋 Exemple décharge: http://localhost:80/media/decharges/$SAMPLE_DECLARATION"
