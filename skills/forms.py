from django import forms
from .models import Roadmap


from django import forms
from .models import Roadmap

class RoadmapForm(forms.ModelForm):
    class Meta:
        model = Roadmap
        fields = ["tech_stack"]
        widgets = {
            "tech_stack": forms.Select(attrs={
                "class": "w-full px-4 py-3 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-400 "
                         "focus:border-transparent appearance-none",
                "style": "background-color:rgba(17,25,40,0.7); color:#e5e7eb;"
            })
        }

