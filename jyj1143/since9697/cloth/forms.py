from django import forms
from .models import Cloth

class ClothForm(forms.ModelForm):
    SEASON_C = (
        ('사계절', '사계절'),
        ('봄', '봄'),
        ('여름', '여름'),
        ('가을', '가을'),
        ('겨울', '겨울'),
    )
    PART_C = (
        ('상의', '상의'),
        ('하의', '하의'),
    )
    
    photo = forms.ImageField(label='',required=False)
    # season = forms.CharField(label='',required=False)
    # part=forms.CharField(label='',required=False)
    
    season = forms.TypedChoiceField(widget = forms.Select(),
                 choices = SEASON_C,  required = False)
    part=forms.TypedChoiceField(widget = forms.Select(),
                 choices = PART_C, required = False)
    
    # r_color = forms.IntegerField()
    # g_color = forms.IntegerField()
    # b_color = forms.IntegerField()
    
    
    
    
    class Meta:
        model = Cloth
        fields = ['photo', 'season' , 'part' ]
    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        