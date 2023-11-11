import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from .forms import FileUploadForm
import pandas as pd  # Note the corrected import statement
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def index(request):
   
    return render(request, 'index.html')


def excel(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            traitement_choice = request.POST['processing_choice']

            # Vérifiez si le fichier est un fichier Excel
            if fichier.name.endswith(('.xls', '.xlsx')):
                # Faites ce que vous voulez avec le fichier Excel
                if traitement_choice == 'votre_traitement':
                    # Exemple : Lecture du fichier Excel avec pandas
                    df = pd.read_excel(fichier)
                    # Faites quelque chose avec le DataFrame 'df'
                    return render(request, 'excel.html', {'df': df})
                else:
                    return HttpResponse("Traitement non pris en charge")
            else:
                return HttpResponse("Seuls les fichiers Excel (.xls, .xlsx) sont autorisés. Veuillez télécharger un fichier Excel.")

    else:
        form = FileUploadForm()

    return render(request, 'excel.html', {'form': form})

 
def text(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fichier = request.FILES['file']
            
            # Check if the file is a txt file
            if fichier.name.endswith('.txt'):
                # Process the txt file
                df = pd.read_csv(fichier, sep='\t')  # Assuming tab-separated data, adjust 'sep' based on your file format
                # You can now use 'df' for further processing or display
                return render(request, 'text_result.html', {'df': df})
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