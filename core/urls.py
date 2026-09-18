from django.urls import path

from . import views

urlpatterns = [
    path("recursos", views.RecursoListCreate.as_view()),
    path("reservas", views.ReservaListCreate.as_view()),
    path("reservas/<int:pk>", views.ReservaDestroy.as_view()),
]
