from django.shortcuts import render
from django.views.generic import (ListView, DetailView, DetailView, CreateView, UpdateView, DeleteView )
from .models import Triagem, Atendimento
from .forms import TriagemForm, AtendimentoForm
from django.urls import reverse_lazy



class TriagemListView(ListView):
    model = Triagem
    form_class = TriagemForm

class TriagemCreateView(CreateView):
    model = Triagem
    form_class = TriagemForm
    success_url = reverse_lazy('triagem_list') 