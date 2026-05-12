from django.urls import path
from .views import (
    home,
    subscribe_newsletter,
    infrastructure_costs,
    about_us,
    feature_offline_first,
    feature_decentralized,
    feature_smart_backup,
    feature_stability,
    pricing_method,
    plan_economic,
    plan_advanced,
    plan_professional,
    plan_custom,
    article_ai,
    article_reporting,
    article_debt_collection,
    solution_smb,
    solution_ecommerce,
    solution_b2b,
    solution_freelancer,
    terms_view,
    privacy_view,
    blog_view,
    help_center_view,
    developers_view,
    submit_ticket_view,

)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('newsletter/subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('infrastructure-costs/', infrastructure_costs, name='infrastructure_costs'),
    path('about/', about_us, name='about_us'),
    path('pricing/', pricing_method, name='pricing'),

    # ------------------ Features URLs ------------------
    path('features/offline-first/', feature_offline_first, name='feature_offline_first'),
    path('features/decentralized-architecture/', feature_decentralized, name='feature_decentralized'),
    path('features/smart-local-backup/', feature_smart_backup, name='feature_smart_backup'),
    path('features/guaranteed-stability/', feature_stability, name='feature_stability'),
    path('plans/economic/', plan_economic, name='plan_economic'),
    path('plans/advanced/', plan_advanced, name='plan_advanced'),
    path('plans/professional/', plan_professional, name='plan_professional'),
    path('plans/custom/', plan_custom, name='plan_custom'),

    # ------------------ Articles URLs ------------------
    path('article/ai-vs-traditional/', article_ai, name='article_ai'),
    path('article/financial-reporting/', article_reporting, name='article_reporting'),
    path('article/debt-collection/', article_debt_collection, name='article_debt_collection'),
    # ------------------ Solutions URLs ------------------
    path('solutions/smb/', solution_smb, name='solution_smb'),
    path('solutions/ecommerce/', solution_ecommerce, name='solution_ecommerce'),
    path('solutions/b2b/', solution_b2b, name='solution_b2b'),
    path('solutions/freelancers/', solution_freelancer, name='solution_freelancer'),
    # لینک‌های حقوقی و قانونی
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    # مسیرهای بخش منابع
    path('blog/', blog_view, name='blog'),
    path('help-center/', help_center_view, name='help_center'),
    path('developers/', developers_view, name='developers'),
    path('support/ticket/', submit_ticket_view, name='submit_ticket'),
]
