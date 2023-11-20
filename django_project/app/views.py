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
import matplotlib
matplotlib.use('Agg')

def index(request):
   
    return render(request, 'index.html')
# views.py
def generate_chart(df, type_chart, col1, col2):
    buffer = BytesIO()

    if type_chart == 'bar':
        plt.bar(df[col1], df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title('Bar Plot')

    elif type_chart == 'histogram':
        plt.hist(df[col1])
        plt.xlabel(col1)
        plt.ylabel('Fréquence')
        plt.title('Histogramme')

    elif type_chart == 'piechart':
        plt.pie(df[col1], labels=df[col2])
        plt.title('Pie Chart')

    elif type_chart == 'histplot':
        sns.histplot(df[col1])
        plt.xlabel(col1)
        plt.ylabel('Count')
        plt.title('Histogram Plot')

    elif type_chart == 'scatterplot':
        plt.scatter(df[col1], df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title('Scatter Plot')

    elif type_chart == 'heatmap':
        pivot_table = df.pivot_table(index=col1, columns=col2, aggfunc=len)
        sns.heatmap(pivot_table, cmap='coolwarm')
        plt.title('Heatmap')

    elif type_chart == 'lineplot':
        plt.plot(df[col1], df[col2]) 
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title('Line Plot')

    elif type_chart == 'boxplot':
        sns.boxplot(x=df[col1], y=df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title('Box Plot')

    elif type_chart == 'violinplot':
        sns.violinplot(x=df[col1], y=df[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)
        plt.title('Violin Plot')
        
    elif type_chart == 'kdeplot':
        # Vérifier si la colonne contient des données numériques
        if pd.api.types.is_numeric_dtype(df[col1]):
            sns.kdeplot(df[col1], shade=True)
            plt.xlabel(col1)
            plt.title('KDE Plot')
        else:
           
            plt.text(0.5, 0.5, "Cette colonne ne contient pas de données numériques", ha='center', va='center', fontsize=12)
            plt.axis('off')  

    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer


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
        
        chart = generate_chart(df, type_chart, col1, col2)
        plot_data = base64.b64encode(chart.getvalue()).decode('utf-8')
        
        context = {
            'chart': plot_data 
        }
        
        return render(request, 'diagramme.html', context)  
    
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