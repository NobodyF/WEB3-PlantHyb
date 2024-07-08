
from django import forms
from .models import Plant
from .models import ContactMessage
from .models import Hybrid

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['plant_name', 'plant_description', 'tree_height', 'tree_growth_type', 'tree_habit', 
                  'tree_fruit_production', 'single_year_stem_thickness', 'interleaf_length', 'sun_side_color', 
                  'branch_puffiness', 'branch_lenticels_count', 'leaf_condition', 'leaf_length', 'leaf_width', 
                  'leaf_length_width_ratio', 'leaf_green_intensity', 'leaf_margin_serration', 
                  'leaf_under_surface_puffiness', 'petiole_length', 'petiole_anthocyanin_coloration', 
                  'dominant_color_before_blooming', 'flower_diameter', 'flower_arrangement', 
                  'stamen_position_relative_to_pistils', 'anthocyanin_coloration_degree_of_fruit_abscission', 
                  'fruit_size', 'fruit_length', 'fruit_diameter', 'fruit_length_diameter_ratio', 'fruit_base_shape', 
                  'fruit_groove', 'calyx_contraction', 'calyx_size', 'calyx_length', 'bark_russeting', 
                  'bark_oiliness', 'fruit_surface_color_area', 'fruit_surface_color_tone', 
                  'fruit_surface_color_intensity', 'fruit_surface_color_coverage', 'stripe_width', 
                  'fruit_side_rust', 'calyx_rust', 'groove_count', 'groove_size', 'pedicel_length', 
                  'pedicel_thickness', 'pedicel_pit_depth', 'pedicel_pit_width', 'flesh_density', 
                  'flesh_color', 'seed_chamber_opening', 'flowering_onset', 'harvest_readiness', 
                  'consumption_readiness']
        exclude = ['id', 'owner' 'parent1', 'parent2']  

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)  
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.owner  
        if commit:
            instance.save()
        return instance

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'email', 'message']

class HybridForm(forms.ModelForm):
    class Meta:
        model = Hybrid
        fields = ['hybrid_name', 'hybrid_description']  
        exclude = ['id', 'owner']  

    def __init__(self, *args, **kwargs):
        self.parent1_id = kwargs.pop('parent1_id', None)
        self.parent2_id = kwargs.pop('parent2_id', None)
        self.owner = kwargs.pop('owner', None)  
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self.owner  
        if self.parent1_id:
            instance.parent1 = Plant.objects.get(id=self.parent1_id)
        if self.parent2_id:
            instance.parent2 = Plant.objects.get(id=self.parent2_id)
        if commit:
            instance.save()
        return instance







        