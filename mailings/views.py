from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.mail import send_mail
from django.core.management import call_command
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .forms import MailingForm
from .models import Mailing, Message, Client, Attempt, MailingLog
from .services import get_statistics


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["total_mailings"] = qs.count()
        context["active_mailings"] = qs.filter(status="Запущена").count()
        context["unique_recipients"] = (
            Client.objects.filter(owner=self.request.user).distinct().count()
        )
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 5), name="dispatch")
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_statistics())
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailings/message_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 5), name="dispatch")
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailings/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailings/client_detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:client_list")

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)


@login_required
def send_mailing_now(request, pk):
    """Ручная отправка рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)

    success_count = 0
    fail_count = 0

    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.title,
                message=mailing.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )
            status = "Успешно"
            server_response = "Письмо успешно отправлено"
            success_count += 1
        except Exception as e:
            status = "Не успешно"
            server_response = str(e)
            fail_count += 1

        Attempt.objects.create(
            mailing=mailing,
            attempt_time=timezone.now(),
            status=status,
            server_response=server_response,
        )

    MailingLog.objects.create(
        user=request.user,
        mailing=mailing,
        success=(fail_count == 0),  # True, если все письма ушли успешно
        message_count=success_count,
        error_message=None if fail_count == 0 else f"{fail_count} писем не отправлено",
    )

    messages.success(request, f"Рассылка «{mailing.title}» отправлена.")
    return redirect("mailings:mailing_list")


@login_required
def user_stats(request):
    logs = MailingLog.objects.filter(user=request.user)

    total_messages = logs.aggregate(Sum("message_count"))["message_count__sum"] or 0
    success_count = logs.filter(success=True).count()
    fail_count = logs.filter(success=False).count()

    context = {
        "total_messages": total_messages,
        "success_count": success_count,
        "fail_count": fail_count,
    }
    return render(request, "users/user_stats.html", context)


class MailingSendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)

        call_command("sending_mail")
        return redirect("mailings:mailing_list")


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "mailings/attempt_list.html"
    context_object_name = "attempts"
    paginate_by = 20

    def get_queryset(self):
        return Attempt.objects.filter(mailing__owner=self.request.user).select_related(
            "mailing"
        )
