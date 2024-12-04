from django import forms
from .models import Accommodation, Amenity

class PropertyForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # For multiple checkboxes
        required=False
    )

    class Meta:
        model = Accommodation
        fields = ['title', 'country_code', 'bedroom_count', 'review_score', 
                  'usd_rate', 'location', 'amenities', 
                  'main_image', 'published']
        
        def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['main_image'].required = False