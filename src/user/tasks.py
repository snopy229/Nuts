from celery import shared_task

from src.user.forms import CustomPasswordResetForm


@shared_task
def send_password_reset_email(email: str, domain: str, use_https: bool = False):
    form = CustomPasswordResetForm({"email": email})
    if form.is_valid():
        form.save(
            domain_override=domain,
            use_https=use_https,
            email_template_name="reset_password_email.html",
        )
