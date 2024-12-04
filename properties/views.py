from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from .models import Accommodation, LocalizedAccommodation
from django.views.generic import FormView, DetailView,DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages

@method_decorator(csrf_protect, name='dispatch')
class AddProperty(FormView):
    template_name = 'addproperty.html'
    form_class = PropertyForm

    def get_form_kwargs(self):
        """
        Pass an instance of the property to the form if editing an existing property.
        """
        kwargs = super().get_form_kwargs()
        property_id = self.kwargs.get('property_id', None)
        if property_id:  # If a property_id is provided, fetch the property instance.
            property_instance = get_object_or_404(Accommodation, id=property_id)
            kwargs['instance'] = property_instance
        return kwargs
    
    from django.contrib.gis.geos import Point

    def form_valid(self, form):
        center_value = self.request.POST.get('center')
        print('Center value:', center_value)
        if center_value:
            lon, lat = map(float, center_value.split(','))
            form.instance.center = Point(lon, lat)  # Save as a Point object
        form.instance.user = self.request.user  # Associate property with the current user
        form.save()
        messages.success(self.request, 'Property added successfully!')
        return redirect('properties') 

    def form_invalid(self, form):
        print(form.errors)  # Log form errors
        messages.error(self.request, 'Failed to add property. Please correct the errors.')
        return self.render_to_response(self.get_context_data(form=form))
    
    

@login_required
def all_properties(request):
    if request.user.profile.user_type == 'owner':
        properties = Accommodation.objects.filter(user=request.user)
    else:
        properties = Accommodation.objects.filter(published=True)

    return render(request, 'allproperties.html', {'properties':properties})  



class PropertyDetailView(DetailView):
    model = Accommodation
    template_name = 'propertydetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch localized content based on language parameter (default: 'en')
        language = self.request.GET.get('lang', 'en')
        localized_content = LocalizedAccommodation.objects.filter(
            property=self.object,
            language=language
        ).first()

        # Get available languages for the property
        available_languages = LocalizedAccommodation.objects.filter(
            property=self.object
        ).values_list('language', flat=True).distinct()

        context.update({
            'localized_content': localized_content,
            'selected_language': language,
            'available_languages': available_languages
        })

        return context


class PropertyUpdateView(UpdateView):
    model = Accommodation
    form_class = PropertyForm
    template_name = 'addproperty.html'

    def get_success_url(self):
        messages.success(self.request, 'property updated successfully')
        return reverse_lazy('properties')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = self.object
        return context
    
class PropertyDeleteView(DeleteView):
    model = Accommodation
    template_name = 'propertydetails.html'
    success_url = reverse_lazy('properties')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Property deleted successfully')
        return super().delete(request, *args, **kwargs)