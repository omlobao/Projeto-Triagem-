from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count

from .decorators import admin_required, AdminRequiredMixin
from .forms import (
    UserCreateForm, UserUpdateForm, GroupForm,
    PacienteForm, EnfermeiroForm, MedicoForm, ClassificacaoRiscoForm,
)
from cadastro.models import Paciente, Enfermeiro, Medico, ClassificacaoRisco
from triagem.models import Triagem, Atendimento
from .models import ConfiguracaoHospital
from .forms import ConfiguracaoHospitalForm


# ============================================
# Painel Home
# ============================================

@admin_required
def painel_home(request):
    hoje = timezone.now().date()
    context = {
        'total_usuarios': User.objects.count(),
        'usuarios_ativos': User.objects.filter(is_active=True).count(),
        'total_grupos': Group.objects.count(),
        'total_pacientes': Paciente.objects.count(),
        'total_enfermeiros': Enfermeiro.objects.count(),
        'total_medicos': Medico.objects.count(),
        'total_triagens': Triagem.objects.count(),
        'total_atendimentos': Atendimento.objects.count(),
        'triagens_hoje': Triagem.objects.filter(data_triagem=hoje).count(),
        'ultimos_usuarios': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'painel/painel_home.html', context)


# ============================================
# Configurações
# ============================================

@admin_required
def configuracoes(request):
    import django
    context = {
        'django_version': django.get_version(),
        'total_usuarios': User.objects.count(),
        'total_pacientes': Paciente.objects.count(),
        'total_enfermeiros': Enfermeiro.objects.count(),
        'total_medicos': Medico.objects.count(),
        'total_classificacoes': ClassificacaoRisco.objects.count(),
        'total_triagens': Triagem.objects.count(),
        'total_atendimentos': Atendimento.objects.count(),
        'atalhos': [
            {'tecla': 'F2', 'acao': 'Nova Triagem', 'url': '/triagem/nova/'},
            {'tecla': 'F3', 'acao': 'Novo Atendimento', 'url': '/atendimento/novo/'},
            {'tecla': 'F4', 'acao': 'Dashboard', 'url': '/'},
            {'tecla': 'F5', 'acao': 'Lista de Triagens', 'url': '/triagem/'},
            {'tecla': 'F6', 'acao': 'Lista de Atendimentos', 'url': '/atendimento/'},
            {'tecla': 'F7', 'acao': 'Painel Administrativo', 'url': '/painel/'},
            {'tecla': 'F8', 'acao': 'Mostrar Atalhos', 'url': '—'},
        ],
    }
    return render(request, 'painel/configuracoes.html', context)


# ============================================
# Usuários CRUD
# ============================================

class UsuarioListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'painel/usuario_list.html'
    context_object_name = 'usuarios'
    ordering = ['-date_joined']


class UsuarioCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'painel/usuario_form.html'
    success_url = reverse_lazy('painel_usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Usuário'
        return context


class UsuarioUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'painel/usuario_form.html'
    success_url = reverse_lazy('painel_usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Usuário'
        return context


class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'painel/usuario_confirm_delete.html'
    success_url = reverse_lazy('painel_usuarios')
    context_object_name = 'usuario'

    def form_valid(self, form):
        messages.success(self.request, 'Usuário excluído com sucesso!')
        return super().form_valid(form)


# ============================================
# Grupos CRUD
# ============================================

class GrupoListView(AdminRequiredMixin, ListView):
    model = Group
    template_name = 'painel/grupo_list.html'
    context_object_name = 'grupos'
    ordering = ['name']

    def get_queryset(self):
        return Group.objects.annotate(user_count=Count('user')).order_by('name')


class GrupoCreateView(AdminRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'painel/grupo_form.html'
    success_url = reverse_lazy('painel_grupos')

    def form_valid(self, form):
        messages.success(self.request, 'Grupo criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Grupo'
        return context


class GrupoUpdateView(AdminRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'painel/grupo_form.html'
    success_url = reverse_lazy('painel_grupos')

    def form_valid(self, form):
        messages.success(self.request, 'Grupo atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Grupo'
        return context


class GrupoDeleteView(AdminRequiredMixin, DeleteView):
    model = Group
    template_name = 'painel/grupo_confirm_delete.html'
    success_url = reverse_lazy('painel_grupos')
    context_object_name = 'grupo'

    def form_valid(self, form):
        messages.success(self.request, 'Grupo excluído com sucesso!')
        return super().form_valid(form)


# ============================================
# Pacientes CRUD
# ============================================

class PacienteListView(AdminRequiredMixin, ListView):
    model = Paciente
    template_name = 'painel/paciente_list.html'
    context_object_name = 'pacientes'
    ordering = ['nome', 'sobrenome']


class PacienteCreateView(AdminRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_pacientes')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente cadastrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Paciente'
        context['entity_name'] = 'Paciente'
        context['list_url'] = 'painel_pacientes'
        return context


class PacienteUpdateView(AdminRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_pacientes')

    def form_valid(self, form):
        messages.success(self.request, 'Paciente atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Paciente'
        context['entity_name'] = 'Paciente'
        context['list_url'] = 'painel_pacientes'
        return context


class PacienteDeleteView(AdminRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'painel/cadastro_confirm_delete.html'
    success_url = reverse_lazy('painel_pacientes')
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Paciente'
        context['list_url'] = 'painel_pacientes'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Paciente excluído com sucesso!')
        return super().form_valid(form)


# ============================================
# Enfermeiros CRUD
# ============================================

class EnfermeiroListView(AdminRequiredMixin, ListView):
    model = Enfermeiro
    template_name = 'painel/enfermeiro_list.html'
    context_object_name = 'enfermeiros'
    ordering = ['nome', 'sobrenome']


class EnfermeiroCreateView(AdminRequiredMixin, CreateView):
    model = Enfermeiro
    form_class = EnfermeiroForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_enfermeiros')

    def form_valid(self, form):
        messages.success(self.request, 'Enfermeiro cadastrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Enfermeiro'
        context['entity_name'] = 'Enfermeiro'
        context['list_url'] = 'painel_enfermeiros'
        return context


class EnfermeiroUpdateView(AdminRequiredMixin, UpdateView):
    model = Enfermeiro
    form_class = EnfermeiroForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_enfermeiros')

    def form_valid(self, form):
        messages.success(self.request, 'Enfermeiro atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Enfermeiro'
        context['entity_name'] = 'Enfermeiro'
        context['list_url'] = 'painel_enfermeiros'
        return context


class EnfermeiroDeleteView(AdminRequiredMixin, DeleteView):
    model = Enfermeiro
    template_name = 'painel/cadastro_confirm_delete.html'
    success_url = reverse_lazy('painel_enfermeiros')
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Enfermeiro'
        context['list_url'] = 'painel_enfermeiros'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Enfermeiro excluído com sucesso!')
        return super().form_valid(form)


# ============================================
# Médicos CRUD
# ============================================

class MedicoListView(AdminRequiredMixin, ListView):
    model = Medico
    template_name = 'painel/medico_list.html'
    context_object_name = 'medicos'
    ordering = ['nome', 'sobrenome']


class MedicoCreateView(AdminRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_medicos')

    def form_valid(self, form):
        messages.success(self.request, 'Médico cadastrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Médico'
        context['entity_name'] = 'Médico'
        context['list_url'] = 'painel_medicos'
        return context


class MedicoUpdateView(AdminRequiredMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_medicos')

    def form_valid(self, form):
        messages.success(self.request, 'Médico atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Médico'
        context['entity_name'] = 'Médico'
        context['list_url'] = 'painel_medicos'
        return context


class MedicoDeleteView(AdminRequiredMixin, DeleteView):
    model = Medico
    template_name = 'painel/cadastro_confirm_delete.html'
    success_url = reverse_lazy('painel_medicos')
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Médico'
        context['list_url'] = 'painel_medicos'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Médico excluído com sucesso!')
        return super().form_valid(form)


# ============================================
# Classificação de Risco CRUD
# ============================================

class ClassificacaoListView(AdminRequiredMixin, ListView):
    model = ClassificacaoRisco
    template_name = 'painel/classificacao_list.html'
    context_object_name = 'classificacoes'
    ordering = ['prioridade']


class ClassificacaoCreateView(AdminRequiredMixin, CreateView):
    model = ClassificacaoRisco
    form_class = ClassificacaoRiscoForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_classificacoes')

    def form_valid(self, form):
        messages.success(self.request, 'Classificação criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Nova Classificação de Risco'
        context['entity_name'] = 'Classificação'
        context['list_url'] = 'painel_classificacoes'
        return context


class ClassificacaoUpdateView(AdminRequiredMixin, UpdateView):
    model = ClassificacaoRisco
    form_class = ClassificacaoRiscoForm
    template_name = 'painel/cadastro_form.html'
    success_url = reverse_lazy('painel_classificacoes')

    def form_valid(self, form):
        messages.success(self.request, 'Classificação atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Classificação de Risco'
        context['entity_name'] = 'Classificação'
        context['list_url'] = 'painel_classificacoes'
        return context


class ClassificacaoDeleteView(AdminRequiredMixin, DeleteView):
    model = ClassificacaoRisco
    template_name = 'painel/cadastro_confirm_delete.html'
    success_url = reverse_lazy('painel_classificacoes')
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_name'] = 'Classificação de Risco'
        context['list_url'] = 'painel_classificacoes'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Classificação excluída com sucesso!')
        return super().form_valid(form)


# ============================================
# Configuração Hospital / Receita
# ============================================

@admin_required
def configuracao_hospital_update(request):
    config = ConfiguracaoHospital.get_solo()
    if request.method == 'POST':
        form = ConfiguracaoHospitalForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações institucionais salvas com sucesso!')
            return redirect('painel_configuracao_hospital')
    else:
        form = ConfiguracaoHospitalForm(instance=config)
    
    context = {
        'form': form,
        'form_title': 'Configurações do Hospital & Receita'
    }
    return render(request, 'painel/configuracao_hospital_form.html', context)

