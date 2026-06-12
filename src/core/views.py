from django.views.generic import TemplateView


def dashboard_callback(request, context):
    context.update(
        {
            "custom_variable": "value",
        }
    )

    return context


class Page404TemplateView(TemplateView):
    template_name = "404_page.html"
