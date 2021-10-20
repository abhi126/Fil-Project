from django.urls import path
from . import views
urlpatterns = [
   
    path('about',views.about, name='about'),
    path('cal_con',views.cal_con, name='cal_con'),
    path('',views.home, name='home'),
    path('faq',views.faq, name='faq'),
    path('blog',views.blog, name='blog'),
    path('guide',views.guide, name='guide'),
    path('prediction/<str:name>',views.prediction_data, name='prediction'),
    path('Compare-Crypto',views.compare_crypto, name='compare'),
]
