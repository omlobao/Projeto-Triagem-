from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.painel_home, name='painel_home'),

    # Configurações
    path('configuracoes/', views.configuracoes, name='painel_configuracoes'),

    # Usuários
    path('usuarios/', views.UsuarioListView.as_view(), name='painel_usuarios'),
    path('usuarios/novo/', views.UsuarioCreateView.as_view(), name='painel_usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='painel_usuario_update'),
    path('usuarios/<int:pk>/excluir/', views.UsuarioDeleteView.as_view(), name='painel_usuario_delete'),

    # Grupos
    path('grupos/', views.GrupoListView.as_view(), name='painel_grupos'),
    path('grupos/novo/', views.GrupoCreateView.as_view(), name='painel_grupo_create'),
    path('grupos/<int:pk>/editar/', views.GrupoUpdateView.as_view(), name='painel_grupo_update'),
    path('grupos/<int:pk>/excluir/', views.GrupoDeleteView.as_view(), name='painel_grupo_delete'),

    # Pacientes
    path('pacientes/', views.PacienteListView.as_view(), name='painel_pacientes'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='painel_paciente_create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='painel_paciente_update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='painel_paciente_delete'),

    # Enfermeiros
    path('enfermeiros/', views.EnfermeiroListView.as_view(), name='painel_enfermeiros'),
    path('enfermeiros/novo/', views.EnfermeiroCreateView.as_view(), name='painel_enfermeiro_create'),
    path('enfermeiros/<int:pk>/editar/', views.EnfermeiroUpdateView.as_view(), name='painel_enfermeiro_update'),
    path('enfermeiros/<int:pk>/excluir/', views.EnfermeiroDeleteView.as_view(), name='painel_enfermeiro_delete'),

    # Médicos
    path('medicos/', views.MedicoListView.as_view(), name='painel_medicos'),
    path('medicos/novo/', views.MedicoCreateView.as_view(), name='painel_medico_create'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='painel_medico_update'),
    path('medicos/<int:pk>/excluir/', views.MedicoDeleteView.as_view(), name='painel_medico_delete'),

    # Classificações de Risco
    path('classificacoes/', views.ClassificacaoListView.as_view(), name='painel_classificacoes'),
    path('classificacoes/novo/', views.ClassificacaoCreateView.as_view(), name='painel_classificacao_create'),
    path('classificacoes/<int:pk>/editar/', views.ClassificacaoUpdateView.as_view(), name='painel_classificacao_update'),
    path('classificacoes/<int:pk>/excluir/', views.ClassificacaoDeleteView.as_view(), name='painel_classificacao_delete'),

    # Configuração Hospital / Receita
    path('hospital/', views.configuracao_hospital_update, name='painel_configuracao_hospital'),
]
