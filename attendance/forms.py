from django import forms
from .models import Subject
from datetime import date
import datetime

class SubjectForm(forms.ModelForm):
    # ✅ Removed Sunday
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    # Multiple day selection
    days = forms.MultipleChoiceField(
        choices=DAYS,
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "space-y-2 text-gray-200"
        }),
        required=True,
        help_text="Select the days this subject occurs"
    )

    # Dynamically add lecture count fields for each day
    lectures_MON = forms.IntegerField(
        required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )
    lectures_TUE = forms.IntegerField(required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )
    lectures_WED = forms.IntegerField(required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )
    lectures_THU = forms.IntegerField(required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )
    lectures_FRI = forms.IntegerField(required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )
    lectures_SAT = forms.IntegerField(required=False, min_value=1, max_value=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Lectures",
            "class": "w-24 px-3 py-2 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500 hidden lectures-input"
        })
    )

    class Meta:
        model = Subject
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg bg-black border border-white text-white "
                         "placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "Enter subject name"
            }),
        }


class MarkAttendanceForm(forms.Form):
    # Choices for days
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "w-full px-4 py-3 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500"
        })
    )

    day = forms.ChoiceField(
        choices=DAYS,
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 rounded-lg bg-black border border-white text-white "
                     "focus:outline-none focus:ring-2 focus:ring-indigo-500"
        })
    )

    present = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            "class": "h-5 w-5 rounded border-gray-600 text-indigo-500 focus:ring-indigo-500"
        }),
        help_text="Check if you were present"
    )

    def __init__(self, *args, **kwargs):
        super(MarkAttendanceForm, self).__init__(*args, **kwargs)
        today = date.today()
        self.fields['date'].initial = today  # Set today's date

        # Get today's day abbreviation in the same format as choices
        day_abbr = today.strftime('%a').upper()[:3]  # e.g., MON, TUE
        # Only set if it's in our defined DAYS
        if any(day_abbr == d[0] for d in self.DAYS):
            self.fields['day'].initial = day_abbr