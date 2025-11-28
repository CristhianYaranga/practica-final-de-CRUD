// App.js - Funcionalidad principal del CRUD
let editandoId = null;

// Cargar clientes al iniciar
document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
    setupFormHandler();
    setupInputAnimations();
});

// Configurar manejador del formulario
function setupFormHandler() {
    const clienteForm = document.getElementById('clienteForm');
    if (clienteForm) {
        clienteForm.addEventListener('submit', handleSubmit);
    }
}

// Manejar envío del formulario
async function handleSubmit(e) {
    e.preventDefault();
    
    const formData = {
        dni: document.getElementById('dni').value,
        nombre: document.getElementById('nombre').value,
        apellidos: document.getElementById('apellidos').value,
        telefono: document.getElementById('telefono').value,
        correo: document.getElementById('correo').value,
        direccion: document.getElementById('direccion').value,
        estado: document.getElementById('estado').value
    };

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.innerHTML = '<span class="loading inline-block">⏳</span> Guardando...';
    submitBtn.disabled = true;

    try {
        const url = editandoId ? `/clientes/${editandoId}` : '/clientes';
        const method = editandoId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            mostrarMensaje('✅ ' + data.message, 'success');
            document.getElementById('clienteForm').reset();
            editandoId = null;
            document.getElementById('formTitle').textContent = '➕ Agregar Nuevo Cliente';
            cargarClientes();
        } else {
            mostrarMensaje('❌ ' + data.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('❌ Error de conexión: ' + error.message, 'error');
    } finally {
        submitBtn.innerHTML = '💾 Guardar Cliente';
        submitBtn.disabled = false;
    }
}

// Cargar clientes
async function cargarClientes() {
    const spinner = document.getElementById('loadingSpinner');
    const tbody = document.getElementById('clientesBody');
    
    spinner.classList.remove('hidden');
    tbody.innerHTML = '';

    try {
        const response = await fetch('/clientes');
        const data = await response.json();

        if (data.success) {
            tbody.innerHTML = data.data.map((cliente, index) => `
                <tr class="row-animate hover:bg-gray-50" style="animation-delay: ${index * 0.1}s;">
                    <td class="px-4 py-4 text-sm text-gray-900">${cliente.id}</td>
                    <td class="px-4 py-4 text-sm text-gray-900">${cliente.dni}</td>
                    <td class="px-4 py-4 text-sm text-gray-900">${cliente.nombre}</td>
                    <td class="px-4 py-4 text-sm text-gray-900">${cliente.apellidos}</td>
                    <td class="px-4 py-4 text-sm text-gray-900">${cliente.telefono}</td>
                    <td class="px-4 py-4 text-sm text-gray-600">${cliente.correo}</td>
                    <td class="px-4 py-4 text-sm">
                        <span class="px-3 py-1 rounded-full text-xs font-semibold ${
                            cliente.estado === 'Activo' 
                                ? 'bg-green-100 text-green-800' 
                                : 'bg-red-100 text-red-800'
                        }">
                            ${cliente.estado === 'Activo' ? '✅' : '❌'} ${cliente.estado}
                        </span>
                    </td>
                    <td class="px-4 py-4 text-sm text-center">
                        <button onclick="editarCliente(${cliente.id})" 
                            class="btn-animate bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded-lg mr-2 text-xs font-semibold">
                            ✏️ Editar
                        </button>
                        <button onclick="eliminarCliente(${cliente.id})" 
                            class="btn-animate bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-xs font-semibold">
                            🗑️ Eliminar
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        mostrarMensaje('❌ Error al cargar clientes: ' + error.message, 'error');
    } finally {
        spinner.classList.add('hidden');
    }
}

// Editar cliente
async function editarCliente(id) {
    try {
        const response = await fetch(`/clientes/${id}`);
        const data = await response.json();

        if (data.success) {
            const cliente = data.data;
            document.getElementById('dni').value = cliente.dni;
            document.getElementById('nombre').value = cliente.nombre;
            document.getElementById('apellidos').value = cliente.apellidos;
            document.getElementById('telefono').value = cliente.telefono;
            document.getElementById('correo').value = cliente.correo;
            document.getElementById('direccion').value = cliente.direccion;
            document.getElementById('estado').value = cliente.estado;
            
            editandoId = id;
            document.getElementById('formTitle').textContent = '✏️ Editar Cliente';
            
            // Scroll al formulario con animación
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    } catch (error) {
        mostrarMensaje('❌ Error al cargar cliente: ' + error.message, 'error');
    }
}

// Eliminar cliente
async function eliminarCliente(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
        return;
    }

    try {
        const response = await fetch(`/clientes/${id}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            mostrarMensaje('✅ ' + data.message, 'success');
            cargarClientes();
        } else {
            mostrarMensaje('❌ ' + data.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('❌ Error al eliminar: ' + error.message, 'error');
    }
}

// Cancelar edición
function cancelarEdicion() {
    document.getElementById('clienteForm').reset();
    editandoId = null;
    document.getElementById('formTitle').textContent = '➕ Agregar Nuevo Cliente';
    mostrarMensaje('', '');
}

// Mostrar mensaje
function mostrarMensaje(texto, tipo) {
    const mensaje = document.getElementById('mensaje');
    
    if (!texto) {
        mensaje.classList.add('hidden');
        return;
    }

    mensaje.textContent = texto;
    mensaje.classList.remove('hidden', 'bg-green-100', 'bg-red-100', 'text-green-800', 'text-red-800');
    
    if (tipo === 'success') {
        mensaje.classList.add('bg-green-100', 'text-green-800', 'border', 'border-green-400');
    } else {
        mensaje.classList.add('bg-red-100', 'text-red-800', 'border', 'border-red-400');
    }

    setTimeout(() => {
        mensaje.classList.add('hidden');
    }, 5000);
}

// Logout
async function logout() {
    if (confirm('¿Deseas cerrar sesión?')) {
        await fetch('/logout');
        window.location.href = '/';
    }
}

// Animación de inputs
function setupInputAnimations() {
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.3)';
        });
        
        input.addEventListener('blur', function() {
            this.style.boxShadow = '';
        });
    });
}
