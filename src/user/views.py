from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, FormView

from src.user.forms import (
    UserForm,
    IndividualForm,
    LegalEntityForm,
    UserLoginForm,
    UserAddressForm,
    LegalEntityAddressForm,
    UserInfoForm,
    LegalEntityInfoForm,
    CustomPasswordChangeForm,
)
from .models import User


# Create your views here.
class RegistrationView(View):
    template_name = "registration.html"

    def get_context(self, **kwargs):
        return {
            "user_form_individual": UserForm(prefix="individual"),
            "user_form_legal": UserForm(prefix="legal"),
            "individual_form": IndividualForm(),
            "legal_form": LegalEntityForm(),
            **kwargs,
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    def post(self, request):
        tab = request.POST.get("tab")
        if tab == "individual":
            user_form = UserForm(request.POST, request.FILES, prefix="individual")
            profile_form = IndividualForm(request.POST, request.FILES)
        else:
            user_form = UserForm(request.POST, request.FILES, prefix="legal")
            profile_form = LegalEntityForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("/")

        return render(
            request,
            self.template_name,
            self.get_context(
                user_form_individual=user_form if tab == "individual" else UserForm(prefix="individual"),
                user_form_legal=user_form if tab == "legal" else UserForm(prefix="legal"),
                individual_form=profile_form if tab == "individual" else IndividualForm(),
                legal_form=profile_form if tab == "legal" else LegalEntityForm(),
            ),
        )


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "login.html"

    def get_success_url(self):
        return "/"


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = []

    def get_object(self, queryset=None):
        return self.request.user

    def get_template_names(self):
        user = self.request.user
        if hasattr(user, "individual"):
            return ["account/address_fiz.html"]
        elif hasattr(user, "legal"):
            return ["account/address_ur.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, "individual"):
            context["form"] = UserAddressForm(instance=user)

        elif hasattr(user, "legalentity"):
            context["user_form"] = UserAddressForm(instance=user)
            context["legal_form"] = LegalEntityAddressForm(instance=user.legalentity)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user

        if hasattr(user, "individual"):
            form = UserAddressForm(request.POST, instance=self.object)
            if form.is_valid():
                form.save()
                return redirect("user:account_address")
            return self.render_to_response(self.get_context_data(form=form))

        elif hasattr(user, "legalentity"):
            user_form = UserAddressForm(request.POST, instance=user)
            legal_form = LegalEntityAddressForm(request.POST, instance=user)
            if user_form.is_valid() and legal_form.is_valid():
                user_form.save()
                legal_form.save()
                return redirect("user:account_address")
            return self.render_to_response(self.get_context_data(user_form=user_form, legal_form=legal_form))
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return redirect("user:account_address")


class InfoUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = []

    def get_object(self, queryset=None):
        return self.request.user

    def get_template_names(self):
        user = self.request.user
        if hasattr(user, "individual"):
            return ["account/info_fiz.html"]
        elif hasattr(user, "legal"):
            return ["account/info_ur.html"]
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, "individual"):
            context["form"] = UserInfoForm(instance=user)

        elif hasattr(user, "legalentity"):
            context["user_form"] = UserInfoForm(instance=user)
            context["legal_form"] = LegalEntityInfoForm(instance=user.legalentity)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user

        if hasattr(user, "individual"):
            form = UserAddressForm(request.POST, instance=self.object)
            if form.is_valid():
                form.save()
                return redirect("user:account_address")
            return self.render_to_response(self.get_context_data(form=form))

        elif hasattr(user, "legalentity"):
            user_form = UserAddressForm(request.POST, instance=user)
            legal_form = LegalEntityAddressForm(request.POST, instance=user)
            if user_form.is_valid() and legal_form.is_valid():
                user_form.save()
                legal_form.save()
                return redirect("user:account_address")
            return self.render_to_response(self.get_context_data(user_form=user_form, legal_form=legal_form))
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return redirect("user:account_address")


class ChangePassword(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = "account/recovery_password.html"
    success_url = reverse_lazy("user:account_address")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
