from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Triagem CRUD
    path('triagem/', views.TriagemListView.as_view(), name='triagem_list'),
    path('triagem/nova/', views.TriagemCreateView.as_view(), name='triagem_create'),
    path('triagem/<int:pk>/', views.TriagemDetailView.as_view(), name='triagem_detail'),
    path('triagem/<int:pk>/editar/', views.TriagemUpdateView.as_view(), name='triagem_update'),
    path('triagem/<int:pk>/excluir/', views.TriagemDeleteView.as_view(), name='triagem_delete'),
    path('api/triagem/<int:pk>/', views.triagem_api_detail, name='triagem_api_detail'),

    # Atendimento CRUD
    path('atendimento/', views.AtendimentoListView.as_view(), name='atendimento_list'),
    path('atendimento/novo/', views.AtendimentoCreateView.as_view(), name='atendimento_create'),
    path('atendimento/<int:pk>/', views.AtendimentoDetailView.as_view(), name='atendimento_detail'),
    path('atendimento/<int:pk>/editar/', views.AtendimentoUpdateView.as_view(), name='atendimento_update'),
    path('atendimento/<int:pk>/excluir/', views.AtendimentoDeleteView.as_view(), name='atendimento_delete'),
    path('atendimento/<int:pk>/imprimir/', views.atendimento_print, name='atendimento_print'),
]
