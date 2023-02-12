
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),

    
    path('getExcel/', views.getExcel,name="getExcel"),

    # # add 
    path('add_bilti/', views.add_bilti,name="add_bilti"),
    path('add_train/', views.add_train,name="add_train"),
    path('add_party/', views.add_party,name="add_party"),
    path('add_transactions/', views.add_transactions,name="add_transactions"),

    # # save
    path('save_bilti/', views.save_bilti,name="save_bilti"),
    # path('save_train/', views.save_train,name="save_train"),
    # path('save_party/', views.save_party,name="save_party"),

    # # check
    # path('check_bilti/', views.check_bilti,name="check_bilti"),
    path('check_train/', views.check_train,name="check_train"),
    path('check_party/', views.check_party,name="check_party"),

    # read
    # path('bilti/<int:no>', views.get_bilti,name="get_bilti"),
    path('train/', views.get_train,name="get_train"), # see for dates as well
    # path('party/<str:name>', views.get_party_name,name="save_party"), # get leadger as well as report
    path('party/', views.get_party,name="save_party"), # get leadger as well as report



    path('user/', views.homepage,name="user"), # get leadger as well as report





    # path('check_party/', views.check_party, name='check_party'),
    # path('add_consignee', views.add_consignee, name='add_consignee'),
]