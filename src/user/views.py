from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from src.user.forms import UserForm, IndividualForm, LegalEntityForm, UserLoginForm


# Create your views here.
class RegistrationView(View):
    template_name = "registration.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "user_form_individual": UserForm(prefix="individual"),
                "user_form_legal": UserForm(prefix="legal"),
                "individual_form": IndividualForm(),
                "legal_form": LegalEntityForm(),
            },
        )

    def post(self, request):
        tab = request.POST.get("tab")
        user_form = UserForm(request.POST, request.FILES)

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
        else:
            print("user_form errors:", user_form.errors)
            print("profile_form errors:", profile_form.errors)

        return render(
            request,
            self.template_name,
            {
                "user_form_individual": UserForm(prefix="individual"),
                "user_form_legal": UserForm(prefix="legal"),
                "individual_form": IndividualForm(),
                "legal_form": LegalEntityForm(),
            },
        )


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("main:home")
