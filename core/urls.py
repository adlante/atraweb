from django.urls import path
from .views import (
    home,
    portfolio_view,
    submit_ticket_view,
    subscribe_newsletter,
    blog_view,

    # Backend & API Services
    backend_modular_view,
    backend_postgresql_view,
    backend_otp_view,
    backend_celery_redis_view,

    # Flutter Services
    flutter_crossplatform_view,
    flutter_offline_first_view,
    flutter_ai_streaming_view,
    flutter_memory_optimization_view,

    # AI & LLM Services
    ai_rag_system_view,
    ai_vector_databases_view,
    ai_finetuning_lora_view,
    ai_generative_studio_view,

    # Development Plans
    plan_backend_api_view,
    plan_rag_service_view,
    plan_fullstack_ai_view,
    plan_finetune_consulting_view,

    # DevOps & Server
    devops_linux_ubuntu_view,
    devops_nginx_ssl_view,
    devops_docker_container_view,
    devops_store_publishing_view,

    # Legal & Support
    terms_view,
    privacy_view,
    help_center_view,
)

app_name = 'core'

urlpatterns = [
    # ------------------ اصلی و عمومی ------------------
    path('', home, name='home'),
    path('portfolio/', portfolio_view, name='portfolio'),
    path('support/ticket/', submit_ticket_view, name='submit_ticket'),
    path('newsletter/subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('blog/', blog_view, name='blog'),

    # ------------------ Backend & API URLs ------------------
    path('solutions/modular-architecture/', backend_modular_view, name='backend_modular'),
    path('solutions/postgresql-database/', backend_postgresql_view, name='backend_postgresql'),
    path('solutions/otp-authentication/', backend_otp_view, name='backend_otp'),
    path('solutions/celery-redis-queues/', backend_celery_redis_view, name='backend_celery_redis'),

    # ------------------ Flutter URLs ------------------
    path('flutter/crossplatform/', flutter_crossplatform_view, name='flutter_crossplatform'),
    path('flutter/offline-first/', flutter_offline_first_view, name='flutter_offline_first'),
    path('flutter/ai-streaming/', flutter_ai_streaming_view, name='flutter_ai_streaming'),
    path('flutter/memory-optimization/', flutter_memory_optimization_view, name='flutter_memory_optimization'),

    # ------------------ AI & LLM URLs ------------------
    path('ai/rag-knowledge-base/', ai_rag_system_view, name='ai_rag_system'),
    path('ai/vector-databases/', ai_vector_databases_view, name='ai_vector_databases'),
    path('ai/finetuning-lora/', ai_finetuning_lora_view, name='ai_finetuning_lora'),
    path('ai/generative-studio/', ai_generative_studio_view, name='ai_generative_studio'),

    # ------------------ Development Plans URLs ------------------
    path('plans/backend-api/', plan_backend_api_view, name='plan_backend_api'),
    path('plans/rag-knowledge-base/', plan_rag_service_view, name='plan_rag_service'),
    path('plans/fullstack-product/', plan_fullstack_ai_view, name='plan_fullstack_ai'),
    path('plans/finetuning-consulting/', plan_finetune_consulting_view, name='plan_finetune_consulting'),

    # ------------------ DevOps & Server URLs ------------------
    path('server/linux-ubuntu/', devops_linux_ubuntu_view, name='devops_linux_ubuntu'),
    path('server/nginx-ssl/', devops_nginx_ssl_view, name='devops_nginx_ssl'),
    path('server/docker-containers/', devops_docker_container_view, name='devops_docker_container'),
    path('server/store-publishing/', devops_store_publishing_view, name='devops_store_publishing'),

    # ------------------ حقوقی و پشتیبانی ------------------
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    path('help-center/', help_center_view, name='help_center'),
]
