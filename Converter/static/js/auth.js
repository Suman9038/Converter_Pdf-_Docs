const authTemplate = `
    <div id="authForms">
        <div class="auth-toggle">
            <button onclick="auth.showLogin()">Login</button>
            <button onclick="auth.showRegister()">Register</button>
        </div>

        <form id="loginForm" class="auth-form">
            <h2>Login</h2>
            <input type="text" id="loginUsername" placeholder="Username" required>
            <input type="password" id="loginPassword" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>

        <form id="registerForm" class="auth-form hidden">
            <h2>Register</h2>
            <input type="text" id="registerUsername" placeholder="Username" required>
            <input type="password" id="registerPassword" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
`;

const auth = {
    init() {
        if (!$('#authForms').length) {
            $('#app').append(authTemplate);
        }

        $('#loginForm').on('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        $('#registerForm').on('submit', (e) => {
            e.preventDefault();
            this.register();
        });

        // Check if user is already logged in
        if (localStorage.getItem('token')) {
            app.showConverterApp();
        }
    },

    showLogin() {
        $('#loginForm').removeClass('hidden');
        $('#registerForm').addClass('hidden');
    },

    showRegister() {
        $('#loginForm').addClass('hidden');
        $('#registerForm').removeClass('hidden');
    },

    async login() {
        const username = $('#loginUsername').val();
        const password = $('#loginPassword').val();

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            authToken = data.access_token;

            app.showConverterApp(); // Redirect to the converter app
        } catch (error) {
            alert(`Login failed: ${error.message}`);
        }
    },

    async register() {
        const username = $('#registerUsername').val();
        const password = $('#registerPassword').val();

        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText);
            }

            alert('Registration successful! Please login.');
            this.showLogin();
        } catch (error) {
            alert(`Registration failed: ${error.message}`);
        }
    },

    logout() {
        localStorage.removeItem('token');
        authToken = null;
        app.showAuthForms(); // Redirect to auth page
    }
};
