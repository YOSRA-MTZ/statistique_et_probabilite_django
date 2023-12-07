import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd  # Note the corrected import statement
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO
import base64
from .forms import FileUploadForm, VisualizationForm
import json
import plotly.express as px
import matplotlib
import plotly.graph_objs as go

import plotly.io as pio
matplotlib.use('Agg')

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
        fig = px.line(df, x=col1, y=col2)
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
        fig = px.histogram(df, x=col1, marginal='rug', nbins=50, 
                               template='plotly'
                               )
        fig.update_layout( title='KdePlot')
            # Convertir la figure en JSON
        fig_json = fig.to_json()

            # Retourner la représentation JSON de la figure
        return fig_json
    else:
        return '{"error": "Type de graphique non pris en charge"}'


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
                data = pd.read_csv(fichier, sep='\t') 
                df = pd.DataFrame(data)
                return render(request, 'visualiser_data.html', {'df': df.to_html(classes='table table-bordered')})
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
            
            # Check if the file is a CSV file
            if fichier.name.endswith('.csv'):
                # Process the CSV file
                df = pd.read_csv(fichier)
                # You can now use 'df' for further processing or display
                return render(request, 'csv.html', {'df': df})
            else:
                return HttpResponse("Seuls les fichiers CSV sont autorisés. Veuillez télécharger un fichier CSV.")
    else:
        form = FileUploadForm()

    return render(request, 'csv.html', {'form': form})

def url(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        
        # Check if the URL is not empty
        if url:
            try:
                # Fetch data from the URL (you may need additional logic based on your data source)
                response = requests.get(url)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Process the data, for example, display the first 100 characters
                    data = response.text[:100]
                    return render(request, 'url_result.html', {'data': data})
                else:
                    return HttpResponse(f"Failed to fetch data from URL. Status Code: {response.status_code}")
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Please provide a valid URL.")
    
    return render(request, 'url.html')

