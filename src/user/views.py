from django.shortcuts import render, redirect
from django.views import View

from src.user.forms import UserForm, IndividualForm, LegalEntityForm


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
            return redirect("home")
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
