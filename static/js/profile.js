document.addEventListener('alpine:init', () => {
    Alpine.data('profileCard', () => ({
        open: true,
        init() {
            console.log('Profil chargé avec succès.');
        }
    }));
});