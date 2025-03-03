const app = {
    init() {
        auth.init();
        if (authToken) {
            this.showAuthForms();
        }
    },

    showAuthForms() {
        $('#authForms').removeClass('hidden');
        $('#converterApp').addClass('hidden');
    },

    showConverterApp() {
        $('#authForms').addClass('hidden');
        $('#converterApp').removeClass('hidden');
        converter.init();
    }
};

// Initialize the app when document is ready
$(document).ready(() => {
    app.init();
});