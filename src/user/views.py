from django.shortcuts import render, redirect
from django.views import View

from user.forms import UserForm, IndividualForm, LegalEntityForm


# Create your views here.
class RegistrationView(View):
    template_name = "registration.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"user_form": UserForm(), "individual_form": IndividualForm(), "legal_form": LegalEntityForm()},
        )

    def post(self, request):
        tab = request.POST.get("tab")
        user_form = UserForm(request.POST, request.FILES)

        if tab == "individual":
            profile_form = IndividualForm(request.POST, request.FILES)
        else:
            profile_form = LegalEntityForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("home")

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "individual_form": IndividualForm() if tab != "individual" else LegalEntityForm(),
                "legal_form": LegalEntityForm() if tab != "legal" else IndividualForm(),
            },
        )
