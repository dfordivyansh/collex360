from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "views/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Only keep site info
        ctx["siteinfo"] = {
            "title": "Collex360",
            "tagline": "Your Student Companion with AI",
            "hero_background": None,
        }

        return ctx
