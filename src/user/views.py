from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from src.user.forms import UserForm, IndividualForm, LegalEntityForm, UserLoginForm
from .models import TermsPage


# Create your views here.
class RegistrationView(View):
    template_name = "registration.html"

    def get_context(self, **kwargs):
        page = TermsPage.objects.live().first()
        return {
            "terms_url": page.url if page else "#",
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
            return redirect("main:home")

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
        return reverse_lazy("main:home")
