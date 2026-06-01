from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView

from src.user.forms import (
    UserForm,
    IndividualForm,
    LegalEntityForm,
    UserLoginForm,
    UserAddressForm,
    LegalEntityAddressForm,
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
                return redirect("/")
            return self.render_to_response(self.get_context_data(form=form))

        elif hasattr(user, "legalentity"):
            user_form = UserAddressForm(request.POST, instance=user)
            legal_form = LegalEntityAddressForm(request.POST, instance=user)
            if user_form.is_valid() and legal_form.is_valid():
                user_form.save()
                legal_form.save()
                return redirect("/")
            return self.render_to_response(self.get_context_data(user_form=user_form, legal_form=legal_form))
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return redirect("/")
