from django import forms

class FileUploadForm(forms.Form):
    csv_file = forms.FileField(label='Fichier CSV', required=False)
    excel_file = forms.FileField(label='Fichier Excel', required=False)
    file = forms.FileField()

    text_file = forms.FileField(label='Fichier Texte', required=False)
    image_file = forms.ImageField(label='Image', required=False)
    
    # forms.py
class BinomialForm(forms.Form):
    n = forms.IntegerField(label='Nombre d\'essais', initial=10, min_value=1)
    p = forms.FloatField(label='Probabilité de succès', initial=0.5, min_value=0, max_value=1)

class BernoulliForm(forms.Form):
    p = forms.FloatField(label='Probabilité de succès', initial=0.5, min_value=0, max_value=1)

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

    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label='Type de Diagramme', required=False)
    column_name_1 = forms.ChoiceField(choices=[], label='Nom de la colonne 1', required=False)
    column_name_2 = forms.ChoiceField(choices=[], label='Nom de la colonne 2', required=False)

   


