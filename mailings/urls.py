from django.urls import path

from mailings import views
from mailings.apps import MailingsConfig
from mailings.views import MailingSendView

app_name = MailingsConfig.name

urlpatterns = [
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path("<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path(
        "messages/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"
    ),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path('<int:pk>/send/', MailingSendView.as_view(), name='send_mailing'),
    path(
        "messages/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/create/", views.ClientCreateView.as_view(), name="client_create"),
    path(
        "clients/<int:pk>/update/",
        views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "clients/<int:pk>/delete/",
        views.ClientDeleteView.as_view(),
        name="client_delete",
    ),
    path("mailings/send/<int:pk>/", views.send_mailing_now, name="send_mailing_now"),
]
