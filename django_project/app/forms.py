from django import forms

class FileUploadForm(forms.Form):
    csv_file = forms.FileField(label='Fichier CSV', required=False)
    excel_file = forms.FileField(label='Fichier Excel', required=False)
    file = forms.FileField(required=True)
    text_file = forms.FileField(label='Fichier Texte', required=False)
    image_file = forms.ImageField(label='Image', required=False)
    
    # forms.py



class VisualizationForm(forms.Form):
    CHART_CHOICES = [
        ('histplot', 'Histogramme'),
        ('scatterplot', 'Nuage de points'),
        ('barplot', 'Diagramme à barres'),
        ('heatmap', 'Carte de chaleur'),
        ('lineplot', 'Graphique linéaire'),
        ('boxplot', 'Boîte à moustaches'),
        ('histogram', 'Histogramme'),
        ('kdeplot', 'Graphique KDE'),
        ('violinplot', 'Violon'),
        ('piechart', 'Diagramme circulaire'),
    ]

    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='Type de Diagramme')
    column_name_1 = forms.ChoiceField(choices=[], label='Nom de la colonne 1')
    column_name_2 = forms.ChoiceField(choices=[], label='Nom de la colonne 2', required=False)

   


