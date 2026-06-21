from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Triagem, Atendimento
from .forms import TriagemForm, AtendimentoForm
from cadastro.models import Paciente, ClassificacaoRisco


# ============================================
# Dashboard
# ============================================

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    context = {
        'total_pacientes': Paciente.objects.count(),
        'triagens_hoje': Triagem.objects.filter(data_triagem=hoje).count(),
        'total_atendimentos': Atendimento.objects.count(),
        'triagens_urgentes': Triagem.objects.filter(
            classificacao_risco__cor__icontains='vermelh'
        ).count(),
        'ultimas_triagens': Triagem.objects.select_related(
            'paciente', 'enfermeiro', 'classificacao_risco', 'atendimento'
        ).order_by('-data_triagem', '-id')[:10],
    }
    return render(request, 'dashboard.html', context)


# ============================================
# Triagem Views
# ============================================

class TriagemListView(LoginRequiredMixin, ListView):
    model = Triagem
    template_name = 'triagem/triagem_list.html'
    context_object_name = 'triagens'
    ordering = ['-data_triagem', '-id']

    def get_queryset(self):
        return Triagem.objects.select_related(
            'paciente', 'enfermeiro', 'classificacao_risco', 'atendimento'
        ).order_by('-data_triagem', '-id')


class TriagemCreateView(LoginRequiredMixin, CreateView):
    model = Triagem
    form_class = TriagemForm
    template_name = 'triagem/triagem_form.html'
    success_url = reverse_lazy('triagem_list')

    def form_valid(self, form):
        paciente_novo = form.cleaned_data.get('paciente_novo')
        if paciente_novo:
            # Cria o paciente com os dados preenchidos
            from cadastro.models import Paciente
            paciente = Paciente.objects.create(
                nome=form.cleaned_data.get('nome'),
                sobrenome=form.cleaned_data.get('sobrenome'),
                cpf=form.cleaned_data.get('cpf'),
                data_nascimento=form.cleaned_data.get('data_nascimento'),
                numero_telefone=form.cleaned_data.get('numero_telefone'),
                email=form.cleaned_data.get('email')
            )
            form.instance.paciente = paciente
            
        messages.success(self.request, 'Triagem registrada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Nova Triagem'
        return context


class TriagemDetailView(LoginRequiredMixin, DetailView):
    model = Triagem
    template_name = 'triagem/triagem_detail.html'
    context_object_name = 'triagem'

    def get_queryset(self):
        return Triagem.objects.select_related(
            'paciente', 'enfermeiro', 'classificacao_risco'
        )


class TriagemUpdateView(LoginRequiredMixin, UpdateView):
    model = Triagem
    form_class = TriagemForm
    template_name = 'triagem/triagem_form.html'
    success_url = reverse_lazy('triagem_list')

    def form_valid(self, form):
        messages.success(self.request, 'Triagem atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Triagem'
        return context


class TriagemDeleteView(LoginRequiredMixin, DeleteView):
    model = Triagem
    template_name = 'triagem/triagem_confirm_delete.html'
    success_url = reverse_lazy('triagem_list')
    context_object_name = 'triagem'

    def form_valid(self, form):
        messages.success(self.request, 'Triagem excluída com sucesso!')
        return super().form_valid(form)

from django.http import JsonResponse

def triagem_api_detail(request, pk):
    try:
        t = Triagem.objects.get(pk=pk)
        data = {
            'id': t.id,
            'paciente_nome': f"{t.paciente.nome} {t.paciente.sobrenome}",
            'paciente_cpf': t.paciente.cpf,
            'paciente_nascimento': t.paciente.data_nascimento.strftime('%d/%m/%Y') if t.paciente.data_nascimento else '',
            'paciente_iniciais': f"{t.paciente.nome[0]}{t.paciente.sobrenome[0]}" if t.paciente.sobrenome else t.paciente.nome[0],
            'pressao_arterial': t.pressao_arterial,
            'saturacao': t.saturacao,
            'peso': t.peso,
            'altura': t.altura,
            'sintomas': t.sintomas,
            'observacoes': t.observacoes,
            'enfermeiro': f"{t.enfermeiro.nome} {t.enfermeiro.sobrenome}",
            'enfermeiro_coren': t.enfermeiro.coren,
            'data_triagem': t.data_triagem.strftime('%d/%m/%Y') if t.data_triagem else '',
            'classificacao_cor': t.classificacao_risco.cor,
            'classificacao_cor_css': t.classificacao_risco.cor.lower(),
        }
        return JsonResponse(data)
    except Triagem.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# ============================================
# Atendimento Views
# ============================================

class AtendimentoListView(LoginRequiredMixin, ListView):
    model = Atendimento
    template_name = 'triagem/atendimento_list.html'
    context_object_name = 'atendimentos'

    def get_queryset(self):
        return Atendimento.objects.select_related(
            'triagem', 'triagem__paciente'
        ).prefetch_related('medicos').order_by('-data_hora_inicio', '-id')


class AtendimentoCreateView(LoginRequiredMixin, CreateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'triagem/atendimento_form.html'
    success_url = reverse_lazy('atendimento_list')

    def get_initial(self):
        initial = super().get_initial()
        triagem_id = self.request.GET.get('triagem')
        if triagem_id:
            initial['triagem'] = triagem_id
        return initial

    def form_valid(self, form):
        from django.utils import timezone
        if not form.instance.data_hora_fim:
            form.instance.data_hora_fim = timezone.now()
        messages.success(self.request, 'Atendimento concluído com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Atendimento'
        
        # Se uma triagem foi passada na URL, carrega o objeto para exibir a ficha
        triagem_id = self.request.GET.get('triagem')
        if triagem_id:
            try:
                context['triagem_obj'] = Triagem.objects.get(id=triagem_id)
            except Triagem.DoesNotExist:
                pass
                
        return context


class AtendimentoDetailView(LoginRequiredMixin, DetailView):
    model = Atendimento
    template_name = 'triagem/atendimento_detail.html'
    context_object_name = 'atendimento'

    def get_queryset(self):
        return Atendimento.objects.select_related(
            'triagem', 'triagem__paciente', 'triagem__enfermeiro',
            'triagem__classificacao_risco'
        ).prefetch_related('medicos')


class AtendimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'triagem/atendimento_form.html'
    success_url = reverse_lazy('atendimento_list')

    def form_valid(self, form):
        messages.success(self.request, 'Atendimento atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Atendimento'
        return context


class AtendimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Atendimento
    template_name = 'triagem/atendimento_confirm_delete.html'
    success_url = reverse_lazy('atendimento_list')
    context_object_name = 'atendimento'

    def form_valid(self, form):
        messages.success(self.request, 'Atendimento excluído com sucesso!')
        return super().form_valid(form)