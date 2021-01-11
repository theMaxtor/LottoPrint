# coding=utf-8
import re
import requests
import datetime
import os
from bs4 import BeautifulSoup

URL = "https://lottointellegente.blogspot.com/"
fileName = 'Prediction-{}.tex'.format(str(datetime.datetime.now().strftime('%d%m%Y')))
pdfName = 'Prediction-{}.pdf'.format(str(datetime.datetime.now().strftime('%d%m%Y')))


def LottoPrint():
    # Create Tex file with predictions
    tex_file = open('./{}'.format(fileName), 'w')

    # Generate header of Tex file
    tex_file.write('\\documentclass{{article}}\n'
                  '\\usepackage[utf8]{{inputenc}}\n'
                  '\\usepackage{{natbib}}\n'
                  '\\usepackage{{graphicx}}\n'
                  '\\begin{{document}}\n'
                  '\\thispagestyle{{plain}}\n'
                  '\\begin{{center}}\n'
                  '\\Large\n'
                  '\\textbf{{Previsioni del Lotto}} \\\\ \n'
                  '\\vspace{{0.4cm}}\n'
                  '\\large\n'
                  '{}\n'
                  '\\end{{center}}\n'.format(str(datetime.datetime.now().strftime('%d-%m-%Y'))))

    # Get content from lottointellegente.blogspost.com
    page = requests.get(URL)

    # Create html parser
    soup = BeautifulSoup(page.content, 'html.parser')

    # Filter content by dib class
    predictions = soup.find_all('div', class_='post-body entry-content')

    # Get predictions for latest lottery draw only and generate tex file
    predictions_collection = []
    for prediction in predictions:
        predictions_collection.append(prediction.prettify())
    designed_prediction = predictions_collection[0]
    prettify_prediction = designed_prediction.replace('\n', '').replace('<br/>', '').replace('<p>', '\n').replace('</p>', '')
    prettify_prediction = prettify_prediction.split("\n")
    for line in prettify_prediction:
        if "span" in line:
            tex_file.write('\\subsection{' + str(re.findall("[A-Z]+(?:[A-Z\s]*)?", line)[0]).strip() + '}\n')
        else:
            line = re.sub('<div.*>\s?$', '', line)
            tex_file.write('\\hspace*{10mm} ' + line + '\\\\ \n')

    tex_file.write('\\end{document}')
    tex_file.close()

    # Execute shell command to generate pdf
    os.system('pdflatex -interaction=nonstopmode {}'.format(fileName))

    # Print pdf using system default printer
    #os.system('lp {}'.format(pdfName))

# Print Lotto predictions
LottoPrint()