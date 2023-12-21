import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd  # Note the corrected import statement
import requests
from .forms import BinomialForm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO
import base64
from .forms import FileUploadForm,ExponentielleForm,TraitementForm
import json
import plotly.express as px
import matplotlib
import plotly.graph_objs as go
from scipy.stats import binom
from django.http import JsonResponse
import plotly.io as pio
from .forms import BernoulliForm 
from scipy.stats import bernoulli
matplotlib.use('Agg')
from statistics import mean, median, mode, variance, stdev
from .forms import NormaleForm 
from .forms import PoissonForm 
from .forms import UniformeForm 


def index(request):
    return render(request, 'index.html')
# views.py
def generate_chart(df, type_chart, col1, col2):
    buffer = BytesIO()

    if type_chart == 'Barplot':
        fig = px.bar(df, x=col1, y=col2)
        fig.update_layout(xaxis_title=col1, yaxis_title=col2, title='Bar Plot')
        return fig.to_json()

    elif type_chart == 'histogram':
        fig = px.histogram(df, x=col1)
        fig.update_layout(xaxis_title=col1, yaxis_title='Count', title='Histogram', barmode='overlay', bargap=0.1)
        return fig.to_json()

    elif type_chart == 'piechart':
        value_counts = df[col1].value_counts().reset_index()
        value_counts.columns = [col1, 'Count']
        fig = px.pie(value_counts, values='Count', names=col1, title='Pie Chart')
        return fig.to_json()


    elif type_chart == 'scatterplot':
        fig = px.scatter(df, x=col1, y=col2)
        fig.update_layout(xaxis_title=col1, yaxis_title=col2, title='Scatter Plot')
        return fig.to_json()

    elif type_chart == 'heatmap':
        df_encoded = df.copy()
        for column in df_encoded.columns:
            if df_encoded[column].dtype == 'object':
                df_encoded[column], _ = pd.factorize(df_encoded[column])
        fig = px.imshow(df_encoded.corr(), color_continuous_scale='Viridis')
        fig.update_layout(title='Heatmap')
        return fig.to_json()

    elif type_chart == 'lineplot':
       
        fig = px.line(df, x=col1, y=col2,markers=True)
        fig.update_layout(xaxis_title=col1, yaxis_title=col2, title='Line Plot')
        return fig.to_json()

        
    elif type_chart == 'boxplot':
        fig = px.box(df, x=col1)
        fig.update_layout(title='Box Plot')
        return fig.to_json()
        

    elif type_chart == 'violinplot':
        fig = px.violin(df, y=col1, box=True)
        fig.update_layout(yaxis_title=col1, title='Violin Plot')
        return fig.to_json()

    elif type_chart == 'kdeplot':
        fig = px.density_contour(df, x=col1)

        # You can customize the appearance of the KDE plot here if needed
        # fig.update_traces(contours_coloring="fill", contours_showlabels=True)
        fig.update_traces(contours_coloring="lines")

        # Convert the figure to JSON
        fig_json = fig.to_json()

        # Return the JSON representation of the figure
        return fig_json


def excel(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            fichier = request.FILES['file']

            if fichier.name.endswith(('.xls', '.xlsx')):
                try:
                    data = pd.read_excel(fichier)
                    df = pd.DataFrame(data)
                    columns_choices = [(col, col) for col in df.columns]
                    df_json = df.to_json()
                    request.session['df_json']=df_json
                    return render(
                        request,
                        'visualiser_data.html',
                        {'form': form,  'df': df.to_html(classes='table table-bordered'), 'column_names': df.columns},
                    )
                except pd.errors.ParserError as e:
                    e = f"Erreur : Impossible de lire le fichier Excel. Assurez-vous que le fichier est au format Excel valide."
                    return render(request, 'excel.html', {'form': form, 'error_message': e})
            else:
                return HttpResponse("Seuls les fichiers Excel (.xls, .xlsx) sont autorisés. Veuillez télécharger un fichier Excel.")
    else:
        form = FileUploadForm()

    return render(request, 'excel.html', {'form': form})

def visualiser(request): 
    return render(request, 'visualiser_data.html')
def visualiser_chart(request): 
    if request.method == 'POST':
        col1 = request.POST['col_name1']
        col2 = request.POST['col_name2']
        type_chart = request.POST['type_chart']
        df_json = request.session.get('df_json')
        
        df_json_io = StringIO(df_json)
        df = pd.read_json(df_json_io)
        
        # Vérifier si la colonne choisie est une chaîne de caractères
        if pd.api.types.is_string_dtype(df[col1]) and type_chart in ['kdeplot', 'violinplot', 'boxplot']:
            error_message = "La colonne choisie est de type 'string', veuillez choisir une autre colonne."
            return render(request, 'diagramme.html', {'error_message': error_message})
        elif type_chart=="Nothing":
            error_message = "Veuillez sélectionner un diagramme à afficher"
            return render(request, 'diagramme.html', {'error_message': error_message})
        # Si ce n'est pas une chaîne de caractères ou pour d'autres types de graphiques,
        # générer le graphique normalement
        chart = generate_chart(df, type_chart, col1, col2)
        return render(request, 'diagramme.html', {'chart': chart})
    
    return render(request, 'visualiser_data.html')

def diagramme(request):
    return render(request, 'diagramme.html')

def text(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            
            # Check if the file is a txt file
            if fichier.name.endswith('.txt'):
                # Process the txt file
                data = pd.read_csv(fichier)

                df = pd.DataFrame(data)
                columns_choices = [(col, col) for col in df.columns]
                df_json = df.to_json()
                request.session['df_json'] = df_json
                return render(
                        request,
                        'visualiser_data.html',
                        {'form': form,  'df': df.to_html(classes='table table-bordered'), 'column_names': df.columns},
                )    
            else:
                return HttpResponse("Seuls les fichiers text sont autorisés. Veuillez télécharger un fichier txt.")
    else:
        form = FileUploadForm()

    return render(request, 'text.html', {'form': form})


def csv(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            if fichier.name.endswith('.csv'):
                # Traitez le fichier CSV
                data = pd.read_csv(fichier)
                df = pd.DataFrame(data)
                columns_choices = [(col, col) for col in df.columns]
                df_json = df.to_json()
                request.session['df_json'] = df_json

                # Vous pouvez maintenant utiliser 'df' pour d'autres traitements ou l'afficher
                return render(
                        request,
                        'visualiser_data.html',
                        {'form': form,  'df': df.to_html(classes='table table-bordered'), 'column_names': df.columns},
                )
            else:
                return HttpResponse("Seuls les fichiers CSV sont autorisés. Veuillez télécharger un fichier CSV.")
    else:
        form = FileUploadForm()

    return render(request, 'csv.html', {'form': form})





def parcourir_chart(request):
    df = None
    columns_choices = None

    if 'df_json' in request.session:
        df_json = request.session['df_json']
        df = pd.read_json(StringIO(df_json))
        columns_choices = [(col) for col in df.columns]

    if request.method == 'POST':
        parcourir_chart_type = request.POST.get('parcourir_chart')
        col_name1 = request.POST.get('col_name1')
        row_numb = request.POST.get('RowNumb')

        if parcourir_chart_type == 'FindElem' and df is not None:
            # Logique pour rechercher l'élément
            try:
                row_numb = int(row_numb)
                max_row = df.shape[0] - 1  # La taille maximale du DataFrame
                row_numb = min(row_numb, max_row)  # Assurez-vous que row_numb ne dépasse pas la taille du DataFrame
                resultats_recherche = df.at[row_numb, col_name1]
                contexte = {'resultat': resultats_recherche, 'column_names': columns_choices, 'df': df.to_html(classes='table table-bordered'), 'max_row': max_row}
                return render(request, 'parcourir.html', contexte)
            except (ValueError, KeyError, IndexError):
                pass

        # Nouvelle logique pour le parcours spécifique
        parcourir_rows_type = request.POST.get('parcourir_rows')

        if parcourir_rows_type == 'NbrOfRowsTop':
            nb_rows_top = int(request.POST.get('Head'))
            df = df.head(nb_rows_top)
        elif parcourir_rows_type == 'NbrOfRowsBottom':
            nb_rows_bottom = int(request.POST.get('Tail'))
            df = df.tail(nb_rows_bottom)
        elif parcourir_rows_type == 'FromRowToRow':
            from_row = int(request.POST.get('FromRowNumb'))
            to_row = int(request.POST.get('ToRowNumb'))
            df = df.loc[from_row:to_row]

        # Récupération des colonnes sélectionnées
        selected_columns = request.POST.getlist('selected_columns')
        if selected_columns:
            df = df[selected_columns]

    # Si la méthode n'est pas POST, ou si aucune recherche n'est effectuée, affichez simplement la page avec le DataFrame actuel
    contexte = {'df': df.to_html(classes='table table-bordered') if df is not None else None, 'column_names': columns_choices}
    return render(request, 'parcourir.html', contexte)

#//////////////////////////////// LOIS ////////////////////////////////////////////////////////////////
def Binomiale(request):
    if request.method == 'POST':
        form = BinomialForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            p = form.cleaned_data['p']

            # Générer des échantillons de la distribution binomiale
            data_binomial = binom.rvs(n=n, p=p, loc=0, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_binomial, nbins=n+1, title='Distribution Binomiale')
            fig.update_layout(xaxis_title='Binomial', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'binomiale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = BinomialForm()

    return render(request, 'binomiale.html', {'form': form})


def Bernoulli(request):
    if request.method == 'POST':
        form = BernoulliForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data['p']
            # Générer des échantillons de la distribution de Bernoulli
            data_bernoulli = bernoulli.rvs(p, size=1000)
            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_bernoulli, nbins=2, title='Distribution de Bernoulli')
            fig.update_layout(xaxis_title='Bernoulli', yaxis_title='Fréquence relative',bargap=0.2)
            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'bernoulli.html', {'form': form, 'plot_data': plot_data})
    else:
        form = BernoulliForm()

    return render(request, 'bernoulli.html', {'form': form})

#///////////////////////////


def Normale(request):
    if request.method == 'POST':
        form = NormaleForm(request.POST)
        if form.is_valid():
            mean = form.cleaned_data['mean']
            std_dev = form.cleaned_data['std_dev']

            # Générer des échantillons de la distribution normale
            data_normale = np.random.normal(mean, std_dev, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_normale, title='Distribution Normale Continue')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'normale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = NormaleForm()

    return render(request, 'normale.html', {'form': form})



def Poisson(request):
    if request.method == 'POST':
        form = PoissonForm(request.POST)
        if form.is_valid():
            lambda_param = form.cleaned_data['lambda_param']

            # Générer des échantillons de la distribution de Poisson
            data_poisson = np.random.poisson(lambda_param, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_poisson, title='Distribution de Poisson')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'poisson.html', {'form': form, 'plot_data': plot_data})
    else:
        form = PoissonForm()

    return render(request, 'poisson.html', {'form': form})



def Uniforme(request):
    if request.method == 'POST':
        form = UniformeForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']

            # Générer des échantillons de la distribution uniforme
            data_uniforme = np.random.uniform(a, b, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_uniforme, title='Distribution Uniforme')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'uniforme.html', {'form': form, 'plot_data': plot_data})
    else:
        form = UniformeForm()

    return render(request, 'uniforme.html', {'form': form})



def Exponentielle(request):
    if request.method == 'POST':
        form = ExponentielleForm(request.POST)
        if form.is_valid():
            beta = form.cleaned_data['beta']

            # Générer des échantillons de la distribution exponentielle
            data_exponentielle = np.random.exponential(scale=beta, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_exponentielle, title='Distribution Exponentielle')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_json()

            return render(request, 'exponentielle.html', {'form': form, 'plot_data': plot_data})
    else:
        form = ExponentielleForm()

    return render(request, 'exponentielle.html', {'form': form})


def mode(valeurs):
    uniques, counts = np.unique(valeurs, return_counts=True)
    max_count = np.max(counts)
    modes = uniques[counts == max_count]
    if max_count == 1:
        return "Il n'y a pas de mode"
    else:
        return modes.tolist()

def Calcules(request):
    if request.method == 'POST':
        form = TraitementForm(request.POST)
        if form.is_valid():
            valeurs_input = form.cleaned_data['valeurs']
            
            # Traiter les valeurs saisies
            valeurs = [float(x.strip()) for x in valeurs_input.replace('-', ',').split(',') if x.strip()]
            
            # Calcul des statistiques
            mean_value = np.mean(valeurs)
            median_value = np.median(valeurs)
            mode_value = mode(valeurs)
            variance_value = np.var(valeurs)
            stdev_value = np.std(valeurs)

            return render(request, 'calcules.html', {'form': form, 'mean': mean_value,
                                                     'median': median_value, 'mode': mode_value,
                                                     'variance': variance_value, 'stdev': stdev_value})
    else:
        form = TraitementForm()

    return render(request, 'calcules.html', {'form': form})