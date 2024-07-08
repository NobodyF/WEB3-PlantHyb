from django.contrib.auth.models import User
from django.db import models
import string
import random

def generate_random_id():
    characters = string.digits  
    random_id = ''.join(random.choices(characters, k=5))
    return random_id

class CommonFields(models.Model):
    tree_height = models.IntegerField(default=0)
    tree_growth_type = models.CharField(max_length=255, default='Unknown')
    tree_habit = models.CharField(max_length=255, default='Unknown')
    tree_fruit_production = models.CharField(max_length=255, default='Unknown')
    single_year_stem_thickness = models.IntegerField(default=0)
    interleaf_length = models.IntegerField(default=0)
    sun_side_color = models.CharField(max_length=255, default='Green')
    branch_puffiness = models.CharField(max_length=255, default='Not Specified')
    branch_lenticels_count = models.IntegerField(default=0)
    leaf_condition = models.CharField(max_length=255, default='Healthy')
    leaf_length = models.IntegerField(default=0)
    leaf_width = models.IntegerField(default=0)
    leaf_length_width_ratio = models.FloatField(default=0.0)
    leaf_green_intensity = models.FloatField(default=0.0)
    leaf_margin_serration = models.CharField(max_length=255, default='Not Specified')
    leaf_under_surface_puffiness = models.CharField(max_length=255, default='Not Specified')
    petiole_length = models.IntegerField(default=0)
    petiole_anthocyanin_coloration = models.CharField(max_length=255, default='Not Specified')
    dominant_color_before_blooming = models.CharField(max_length=255, default='Not Specified')
    flower_diameter = models.IntegerField(default=0)
    flower_arrangement = models.CharField(max_length=255, default='Not Specified')
    stamen_position_relative_to_pistils = models.CharField(max_length=255, default='Not Specified')
    anthocyanin_coloration_degree_of_fruit_abscission = models.CharField(max_length=255, default='Not Specified')
    fruit_size = models.CharField(max_length=255, default='Not Specified')
    fruit_length = models.IntegerField(default=0)
    fruit_diameter = models.IntegerField(default=0)
    fruit_length_diameter_ratio = models.FloatField(default=0.0)
    fruit_base_shape = models.CharField(max_length=255, default='Not Specified')
    fruit_groove = models.CharField(max_length=255, default='Not Specified')
    calyx_contraction = models.CharField(max_length=255, default='Not Specified')
    calyx_size = models.CharField(max_length=255, default='Not Specified')
    calyx_length = models.IntegerField(default=0)
    bark_russeting = models.CharField(max_length=255, default='Not Specified')
    bark_oiliness = models.CharField(max_length=255, default='Not Specified')
    fruit_surface_color_area = models.CharField(max_length=255, default='Not Specified')
    fruit_surface_color_tone = models.CharField(max_length=255, default='Not Specified')
    fruit_surface_color_intensity = models.FloatField(default=0.0)
    fruit_surface_color_coverage = models.CharField(max_length=255, default='Not Specified')
    stripe_width = models.IntegerField(default=0)
    fruit_side_rust = models.CharField(max_length=255, default='Not Specified')
    calyx_rust = models.CharField(max_length=255, default='Not Specified')
    groove_count = models.IntegerField(default=0)
    groove_size = models.IntegerField(default=0)
    pedicel_length = models.IntegerField(default=0)
    pedicel_thickness = models.IntegerField(default=0)
    pedicel_pit_depth = models.IntegerField(default=0)
    pedicel_pit_width = models.IntegerField(default=0)
    flesh_density = models.CharField(max_length=255, default='Not Specified')
    flesh_color = models.CharField(max_length=255, default='Not Specified')
    seed_chamber_opening = models.CharField(max_length=255, default='Not Specified')
    flowering_onset = models.CharField(max_length=255, default='Not Specified')
    harvest_readiness = models.CharField(max_length=255, default='Not Specified')
    consumption_readiness = models.CharField(max_length=255, default='Not Specified')

    class Meta:
        abstract = True

class Plant(CommonFields):
    id = models.CharField(max_length=5, primary_key=True, default=generate_random_id, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    plant_name = models.CharField(max_length=255)
    plant_description = models.TextField()

    def __str__(self):
        return self.plant_name

class Hybrid(CommonFields):
    id = models.CharField(max_length=5, primary_key=True, default=generate_random_id, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    parent1 = models.ForeignKey(Plant, related_name='parent1_hybrids', on_delete=models.CASCADE, null=True)
    parent2 = models.ForeignKey(Plant, related_name='parent2_hybrids', on_delete=models.CASCADE, null=True)
    hybrid_name = models.CharField(max_length=255)
    hybrid_description = models.TextField()

    def __str__(self):
        return self.hybrid_name
    
class PlantTransaction(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.plant.plant_name} - {self.tx_hash}"
    
class HybridTransaction(models.Model):
    hybrid = models.ForeignKey(Hybrid, on_delete=models.CASCADE, related_name='transactions')
    tx_hash = models.CharField(max_length=100)  
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.hybrid.hybrid_name} - {self.tx_hash}"

class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.sender_name} - {self.email}"
