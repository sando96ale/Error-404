from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistroForm, UsuarioForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilUsuario
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.

class Registro(CreateView):
    form_class = RegistroForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/registro.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crea un perfil de usuario asociado al nuevo usuario
        PerfilUsuario.objects.create(user=self.object)
        return response

def mi_cuenta(request):
    return render(request, 'usuarios/mi-cuenta.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        if usuario_form.is_valid():
            usuario = usuario_form.save(commit=False)
            usuario.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia a la página de inicio o a donde desees redirigir
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        usuario_form = UsuarioForm(instance=request.user)

    return render(request, 'usuarios/editar_perfil.html', {'usuario_form': usuario_form})

def cambio_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión iniciada
            messages.success(request, 'Contraseña actualizada con éxito.')
            return redirect('usuarios:mi_cuenta')
        else:
            messages.error(request, 'Corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'usuarios/cambio_contrasena.html', {'form': form})