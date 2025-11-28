// Login.js - Manejo del formulario de login
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Animación al escribir en inputs
    setupInputAnimations();
});

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Animación de carga
    submitBtn.innerHTML = '<span class="inline-block animate-spin">⏳</span> Iniciando sesión...';
    submitBtn.disabled = true;
    errorMessage.classList.add('hidden');
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Animación de éxito
            submitBtn.innerHTML = '✅ ¡Acceso concedido!';
            submitBtn.classList.remove('from-blue-500', 'to-purple-600');
            submitBtn.classList.add('from-green-500', 'to-green-600');
            
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        } else {
            showError(errorMessage, data.message || 'Error al iniciar sesión');
            submitBtn.innerHTML = 'Iniciar Sesión';
            submitBtn.disabled = false;
        }
    } catch (error) {
        showError(errorMessage, 'Error de conexión. Por favor, intenta de nuevo.');
        submitBtn.innerHTML = 'Iniciar Sesión';
        submitBtn.disabled = false;
    }
}

function showError(element, message) {
    element.textContent = message;
    element.classList.remove('hidden');
}

function setupInputAnimations() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
}
