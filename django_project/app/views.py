import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd  # Note the corrected import statement
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.http import HttpResponse
from .forms import FileUploadForm, VisualizationForm


def index(request):
   
    return render(request, 'index.html')
# views.py
def generate_chart(df, chart_type, column_name_1, column_name_2=None):
    # Ajoutez votre logique pour générer le graphique en fonction du type de diagramme
    # et des colonnes spécifiées.
    if chart_type == 'barplot':
        # Exemple : Créer un diagramme à barres
        plt.bar(df[column_name_1], df[column_name_2])
        plt.xlabel(column_name_1)
        plt.ylabel(column_name_2)
        plt.title('Bar Plot')
    elif chart_type == 'histogram':
        # Exemple : Créer un histogramme
        plt.hist(df[column_name_1])
        plt.xlabel(column_name_1)
        plt.ylabel('Fréquence')
        plt.title('Histogramme')

    # Convertir le graphique en base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return plot_data

def excel(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Utilisez 'file' comme nom de champ pour accéder au fichier dans le formulaire
            fichier = request.FILES['file']  # Mettez à jour cette ligne

            if fichier.name.endswith(('.xls', '.xlsx')):
                try:
                    data = pd.read_excel(fichier)
                    df = pd.DataFrame(data)

                    # Créez une liste de choix de colonnes basée sur les colonnes du DataFrame
                    columns_choices = [(col, col) for col in df.columns]

                    # Initialisez le formulaire avec les choix de colonnes
                    visualization_form = VisualizationForm()
                    visualization_form.fields['column_name_1'].choices = columns_choices
                    visualization_form.fields['column_name_2'].choices = columns_choices

                    if visualization_form.is_valid():
                        chart_type = visualization_form.cleaned_data['chart_type']
                        column_name_1 = visualization_form.cleaned_data['column_name_1']
                        column_name_2 = visualization_form.cleaned_data['column_name_2']

                        try:
                            plot_data = generate_chart(df, chart_type, column_name_1, column_name_2)
                            if plot_data is not None:
                                return render(
                                    request,
                                    'diagramme.html',
                                    {'form': form, 'visualization_form': visualization_form, 'df': df.to_html(classes='table table-bordered'), 'plot_data': plot_data},
                                )
                            else:
                                return HttpResponse("Type de diagramme non pris en charge.")
                        except KeyError as e:
                            error_message = f"Erreur : La colonne spécifiée n'existe pas dans le DataFrame. Colonnes disponibles : {', '.join(df.columns)}"
                            return render(
                                request,
                                'visualiser_data.html',
                                {'form': form, 'visualization_form': visualization_form, 'error_message': error_message, 'column_names': df.columns},
                            )
                    else:
                        return render(
                            request,
                            'visualiser_data.html',
                            {'form': form, 'visualization_form': visualization_form, 'df': df.to_html(classes='table table-bordered'), 'column_names': df.columns},
                        )
                except pd.errors.ParserError as e:
                    error_message = f"Erreur : Impossible de lire le fichier Excel. Assurez-vous que le fichier est au format Excel valide."
                    return render(request, 'excel.html', {'form': form, 'error_message': error_message})
            else:
                return HttpResponse("Seuls les fichiers Excel (.xls, .xlsx) sont autorisés. Veuillez télécharger un fichier Excel.")
    else:
        form = FileUploadForm()

    return render(request, 'excel.html', {'form': form})



def visualiser(request): 
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


def image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if image_file:
            try:
                # Process the image (calculate color histogram)
                img_array, histogram_data = process_image(image_file)

                # Create a histogram plot
                fig, axes = plt.subplots(1, 2, figsize=(12, 3))

                # Display the image
                axes[0].imshow(img_array)
                axes[0].set_title('Image')

                # Plot the color histogram
                sns.histplot(img_array.ravel(), color='blue', bins=50, ax=axes[1])
                axes[1].set_title('Histogram of the Image')
                plt.tight_layout()

                # Save the plot to a BytesIO object
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                plt.close()

                # Convert the plot to a base64-encoded string
                plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

                return render(request, 'image_result.html', {'plot_data': plot_data})

            except Exception as e:
                return render(request, 'image_result.html', {'error_message': f"An error occurred: {str(e)}"})

    return render(request, 'image.html')

def process_image(image_file):
    img = Image.open(image_file)

    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Calculate the color histogram using NumPy
    red_hist = np.histogram(img_array[:,:,0].ravel(), bins=256, range=[0,256])
    green_hist = np.histogram(img_array[:,:,1].ravel(), bins=256, range=[0,256])
    blue_hist = np.histogram(img_array[:,:,2].ravel(), bins=256, range=[0,256])

    # Normalize the histograms
    red_hist = red_hist[0] / red_hist[0].sum()
    green_hist = green_hist[0] / green_hist[0].sum()
    blue_hist = blue_hist[0] / blue_hist[0].sum()

    histogram_data = {'red': red_hist.tolist(), 'green': green_hist.tolist(), 'blue': blue_hist.tolist()}

    return img_array, histogram_data