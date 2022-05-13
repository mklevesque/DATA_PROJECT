# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 15:02:52 2022

@author: cazen
"""

# -*- coding: utf-8 -*-
from flask import Flask, render_template
from pandas import read_excel
import pandas as pd
import numpy as np
import nltk
import os
import nltk.corpus# sample text for performing tokenization
from lxml import html
import requests
from nltk.tokenize import word_tokenize# Passing the string text into word tokenize for breaking the sentences
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import FrenchStemmer
import unidecode
import os

IMG_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = IMG_FOLDER



french_stopwords = set(stopwords.words('french'))
filtre_stopfr = lambda text: [token for token in text if token.lower() not in french_stopwords]


def data_epurator():
    i = 0
    cols = ['Kcal/100 g', 'Protéines/100 g', 'Glucides/100 g', 'Lipides/100 g', 'Sucres/100 g', 'AG saturés/100 g']
    df_data = pd.read_excel("Data/Table_Ciqual_2020_FR_2020_07_07.xls")

    df_propre = df_data.copy().drop(
        ['alim_grp_code', 'alim_ssgrp_code', 'alim_ssssgrp_code', 'alim_ssssgrp_nom_fr', 'alim_ssgrp_code',
         'alim_nom_sci',
         'Energie, Règlement UE N° 1169/2011 (kJ/100 g)', 'Energie, N x facteur Jones, avec fibres  (kJ/100 g)',
         'Energie, N x facteur Jones, avec fibres  (kcal/100 g)',
         'Eau (g/100 g)', 'Protéines, N x facteur de Jones (g/100 g)', 'Fructose (g/100 g)',
         'Galactose (g/100 g)', 'Glucose (g/100 g)', 'Lactose (g/100 g)',
         'Maltose (g/100 g)', 'Saccharose (g/100 g)', 'Amidon (g/100 g)',
         'Fibres alimentaires (g/100 g)', 'Polyols totaux (g/100 g)',
         'Cendres (g/100 g)', 'Alcool (g/100 g)', 'Acides organiques (g/100 g)', 'AG monoinsaturés (g/100 g)',
         'AG polyinsaturés (g/100 g)', 'AG 4:0, butyrique (g/100 g)',
         'AG 6:0, caproïque (g/100 g)', 'AG 8:0, caprylique (g/100 g)',
         'AG 10:0, caprique (g/100 g)', 'AG 12:0, laurique (g/100 g)',
         'AG 14:0, myristique (g/100 g)', 'AG 16:0, palmitique (g/100 g)',
         'AG 18:0, stéarique (g/100 g)', 'AG 18:1 9c (n-9), oléique (g/100 g)',
         'AG 18:2 9c,12c (n-6), linoléique (g/100 g)',
         'AG 18:3 c9,c12,c15 (n-3), alpha-linolénique (g/100 g)',
         'AG 20:4 5c,8c,11c,14c (n-6), arachidonique (g/100 g)',
         'AG 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100 g)',
         'AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100 g)',
         'Cholestérol (mg/100 g)', 'Sel chlorure de sodium (g/100 g)',
         'Calcium (mg/100 g)', 'Chlorure (mg/100 g)', 'Cuivre (mg/100 g)',
         'Fer (mg/100 g)', 'Iode (µg/100 g)', 'Magnésium (mg/100 g)',
         'Manganèse (mg/100 g)', 'Phosphore (mg/100 g)', 'Potassium (mg/100 g)',
         'Sélénium (µg/100 g)', 'Sodium (mg/100 g)', 'Zinc (mg/100 g)',
         'Rétinol (µg/100 g)', 'Beta-Carotène (µg/100 g)',
         'Vitamine D (µg/100 g)', 'Vitamine E (mg/100 g)',
         'Vitamine K1 (µg/100 g)', 'Vitamine K2 (µg/100 g)',
         'Vitamine C (mg/100 g)', 'Vitamine B1 ou Thiamine (mg/100 g)',
         'Vitamine B2 ou Riboflavine (mg/100 g)',
         'Vitamine B3 ou PP ou Niacine (mg/100 g)',
         'Vitamine B5 ou Acide pantothénique (mg/100 g)',
         'Vitamine B6 (mg/100 g)', 'Vitamine B9 ou Folates totaux (µg/100 g)',
         'Vitamine B12 (µg/100 g)'], axis=1)

    df_propre.columns = ['alim_grp_nom_fr', 'alim_ssgrp_nom_fr', 'alim_code', 'alim_nom_fr', 'Kcal/100 g',
                         'Protéines/100 g', 'Glucides/100 g', 'Lipides/100 g', 'Sucres/100 g', 'AG saturés/100 g']

    for column in df_propre['alim_ssgrp_nom_fr']:
        df_propre['alim_ssgrp_nom_fr'] = df_propre['alim_ssgrp_nom_fr'].replace(to_replace=np.nan, value='rien')

    for column in df_propre['alim_ssgrp_nom_fr']:
        df_propre['alim_ssgrp_nom_fr'] = df_propre['alim_ssgrp_nom_fr'].replace(['-'], ['rien'])

    sous_groupe_sup = ['céréales et biscuits infantiles', 'rien', 'aides culinaires et ingrédients pour végétariens',
                       'huiles de poissons',
                       'desserts infantiles', 'denrées destinées à une alimentation particulière',
                       'aides culinaires et ingrédients pour végétariens',
                       'sorbets', 'barres céréalières', 'glaces', 'desserts glacés',
                       'petits pots salés et plats infantiles',
                       'autres produits à base de viande', 'laits et boissons infantiles',
                       'confiseries non chocolatées',
                       'biscuits apéritifs', 'salades composées et crudités', 'viennoiseries',
                       'feuilletées et autres entrées',
                       'sandwichs', 'pizzas, tartes et crêpes salées', 'gâteaux et pâtisseries', 'plats composés']

    while i < len(sous_groupe_sup):
        df_propre.drop(df_propre[df_propre['alim_ssgrp_nom_fr'] == sous_groupe_sup[i]].index, inplace=True)
        i = i + 1

    for column in df_propre['Kcal/100 g']:
        df_propre['Kcal/100 g'] = df_propre['Kcal/100 g'].replace(['traces'], ['0'])
        df_propre['Kcal/100 g'] = df_propre['Kcal/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre['Protéines/100 g']:
        df_propre['Protéines/100 g'] = df_propre['Protéines/100 g'].replace(['traces'], ['0'])
        df_propre['Protéines/100 g'] = df_propre['Protéines/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre['Glucides/100 g']:
        df_propre['Glucides/100 g'] = df_propre['Glucides/100 g'].replace(['traces'], ['0'])
        df_propre['Glucides/100 g'] = df_propre['Glucides/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre['Lipides/100 g']:
        df_propre['Lipides/100 g'] = df_propre['Lipides/100 g'].replace(['traces'], ['0'])
        df_propre['Lipides/100 g'] = df_propre['Lipides/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre['Sucres/100 g']:
        df_propre['Sucres/100 g'] = df_propre['Sucres/100 g'].replace(['traces'], ['0'])
        df_propre['Sucres/100 g'] = df_propre['Sucres/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre['AG saturés/100 g']:
        df_propre['AG saturés/100 g'] = df_propre['AG saturés/100 g'].replace(['traces'], ['0'])
        df_propre['AG saturés/100 g'] = df_propre['AG saturés/100 g'].replace(['-'], value=np.nan, regex=True)

    for column in df_propre:
        df_propre = df_propre.dropna()

    for col in cols:
        df_propre[col] = df_propre[col].map(lambda x: str(x).replace(',', '.').lstrip('<')).astype(float)

    return df_propre


def scrapper(url):
    recipe = []
    page = requests.get(url)
    # https://www.marmiton.org/recettes/recette_sauce-puttanesca_14929.aspx
    tree = html.fromstring(page.content)
    products = tree.xpath("//div[contains(@class, 'MuiGrid-root')]")
    for product in products[1:]:
        recipe.append(product.text_content())
    return(recipe)

def normalize_text(text, stemmer=True):
    text = unaccented_string = unidecode.unidecode(str(text))
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    words = filtre_stopfr( word_tokenize(text, language="french") )
    if stemmer:
        stemmer = FrenchStemmer()
        res = " ".join([stemmer.stem(w) for w in words])
    else:
        res = " ".join(words)
    return res

def words_in_column(df_propre, prod, col):
    mask = df_propre[col].str.contains(prod)
    return df_propre.loc[mask]

def list_match(name, df_propre):
    l_match = []
    words_test = normalize_text(name).split(" ")
    for word in words_test:
        l_match.append(words_in_column(df_propre, word, 'alim_nom_fr'))
    res = pd.concat(l_match)
    df = pd.DataFrame(res)
    #res.reset_index()["index"].value_counts().iloc[0]
    return df

def best_res(res, df_propre):
    id_res = res.reset_index()["index"].value_counts().index[0]
    print(df_propre.loc[id_res])
    return id_res


def matcher(name, df_propre):
    res = list_match(name, df_propre)
    id_res = best_res(res, df_propre)
    return id_res

def food_matcher(nom_aliment, df_propre):
    prod = normalize_text(nom_aliment)
    products_fit = words_in_column(df_propre, prod, 'alim_nom_fr')
    print(f"size products {products_fit.shape[0]}")
    shorter_description_sample = products_fit["alim_nom_fr"].apply(len).sort_values()[:10].index
    print(shorter_description_sample)
    ten_shorter_des_match = df_propre.loc[shorter_description_sample]
    print(ten_shorter_des_match["alim_ssgrp_nom_fr"].value_counts())
    best_cat = ten_shorter_des_match["alim_ssgrp_nom_fr"].value_counts().index[0]
    if best_cat == "nan":
        best_cat = ten_shorter_des_match["alim_ssgrp_nom_fr"].value_counts().index[1]
    ten_shorter_des_match = ten_shorter_des_match.loc[ten_shorter_des_match["alim_ssgrp_nom_fr"]==best_cat]
    best_bet = ten_shorter_des_match.iloc[0]
    print(f"Best match : {best_bet['alim_nom_fr']} \nBest cat : {best_cat}")
    return best_bet

def list_to_tab(list_ing):
    tab = []
    for value in list_ing:
        u_mes = value.split(' ', 1)[0]
        if u_mes is None:
            u_mes = 1
        attr = value.split(' ', 1)[1]
        temp = normalize_text(attr,False)
        tab.append([u_mes, temp])
    return tab


def nutr_calculator(df_ingr, quantity, unity, df_propre):
    kcal = df_ingr["Kcal/100 g"]
    proteines = df_ingr["Protéines/100 g"]
    glucides = df_ingr["Glucides/100 g"]
    lipides = df_ingr["Lipides/100 g"]
    sucres = df_ingr["Sucres/100 g"]
    ag_satures = df_ingr["AG saturés/100 g"]

    q = int(quantity)

    print("kcal : " + str(kcal) + "\nprotéines : " + str(proteines) + "\nglucides : " + str(
        glucides) + "\nlipides : " + str(lipides) + "\nsucres : " + str(sucres) + "\nag_saturés : " + str(ag_satures))

    if unity == 'g':
        kcal = kcal * (q / 100)
        proteines = proteines * (q / 100)
        glucides = glucides * (q / 100)
        lipides = lipides * (q / 100)
        sucres = sucres * (q / 100)
        ag_satures = ag_satures * (q / 100)

    elif unity == 'mg':
        kcal = kcal * (q / 1000)
        proteines = proteines * (q / 1000)
        glucides = glucides * (q / 1000)
        lipides = lipides * (q / 1000)
        sucres = sucres * (q / 1000)
        ag_satures = ag_satures * (q / 1000)

    elif unity == "cl":
        kcal = kcal * (q / 10)
        proteines = proteines * (q / 10)
        glucides = glucides * (q / 10)
        lipides = lipides * (q / 10)
        sucres = sucres * (q / 10)
        ag_satures = ag_satures * (q / 10)
    elif unity == "l":
        kcal = kcal * (q * 10)
        proteines = proteines * (q * 10)
        glucides = glucides * (q * 10)
        lipides = lipides * (q / 10)
        sucres = sucres * (q * 10)
        ag_satures = ag_satures * (q * 10)

    elif unity == "ml":
        kcal = kcal * (q / 100)
        proteines = proteines * (q / 100)
        glucides = glucides * (q / 100)
        lipides = lipides * (q / 100)
        sucres = sucres * (q / 100)
        ag_satures = ag_satures * (q / 100)

    elif unity == "c.à.s":
        kcal = (kcal * (q / 100)) * 1.5
        proteines = (proteines * (q / 100)) * 1.5
        glucides = (glucides * (q / 100)) * 1.5
        lipides = (lipides * (q / 1000)) * 1.5
        sucres = (sucres * (q / 100)) * 1.5
        ag_satures = (ag_satures * (q / 100)) * 1.5

    # Le cas pour les oeufs

    # elif (unity == 0 and df_ingr["Name"] == 1916):
    # kcal = (kcal * (q/100)) * 0.5
    # proteines = (proteines * (q/100)) * 0.5
    # glucides = (glucides * (q/100)) * 0.5
    # sucres = (sucres * (q/100)) * 0.5
    # ag_satures = (ag_satures * (q/100)) * 0.5

    else:
        kcal = 0
        proteines = 0
        glucides = 0
        lipides = 0
        sucres = 0
        ag_satures = 0

    tab = [kcal, proteines, glucides, lipides, sucres, ag_satures]

    return tab


def food_calculator(list_ing, df_propre):
    total_nutr = [0, 0, 0, 0, 0, 0]
    tmp = [0, 0, 0, 0, 0, 0]
    for value in list_ing:
        if value[0] == '':
            quantity = 0
            unity = 0
        else:
            quantity = value[0].split('\xa0', 1)[0]
            if len(value[0]) == 1:
                unity = 0
            else:
                unity = value[0].split('\xa0', 1)[1]
        df_ingr = df_propre.loc[matcher(value[1])]

        print("+++++++++")
        print("Quantite: " + str(quantity))
        print("Unity: " + str(unity))
        print("*********")
        tmp = nutr_calculator(df_ingr, quantity, unity, df_propre)
        total_nutr = [b_elt + a_elt for a_elt, b_elt in zip(total_nutr, tmp)]
        print(tmp)
        print("+++++++++++++++++")

    print("\n\n\n\n\nTotal des Nutriments: " + str(total_nutr) + "\n\n\n\n")
    return (total_nutr)


def note(tab):
    somme_macro = tab[1] + tab[2] + tab[3]
    pourcentage_prot = (tab[1] / somme_macro) * 100
    pourcentage_glu = (tab[2] / somme_macro) * 100
    pourcentage_lip = (tab[3] / somme_macro) * 100

    # liste note element 0 = maintenir, 1 = perdre et 2 = masse
    note = [20, 20, 20]

    if pourcentage_prot < 10 or pourcentage_prot > 40:
        note[0] = note[0] - 5
        note[1] = note[1] - 5
        note[2] = note[2] - 5

    if pourcentage_prot >= 10 and pourcentage_prot <= 30:
        note[1] = note[1] - 5
        note[2] = note[2] - 5

    if pourcentage_prot > 30 and pourcentage_prot <= 35:
        note[0] = note[0] - 5
        note[2] = note[2] - 5

    if pourcentage_prot > 35 and pourcentage_prot <= 40:
        note[0] = note[0] - 5
        note[1] = note[1] - 5

    if pourcentage_glu < 35 or pourcentage_glu > 65:
        note[0] = note[0] - 5
        note[1] = note[1] - 5
        note[2] = note[2] - 5

    if pourcentage_glu >= 35 and pourcentage_glu <= 45:
        note[0] = note[0] - 5
        note[2] = note[2] - 5

    if pourcentage_glu > 45 and pourcentage_glu <= 50:
        note[0] = note[0] - 5
        note[1] = note[1] - 5

    if pourcentage_glu > 50 and pourcentage_glu <= 65:
        note[1] = note[1] - 5
        note[2] = note[2] - 5
    if pourcentage_lip < 10 or pourcentage_lip > 35:
        note[0] = note[0] - 5
        note[1] = note[1] - 5
        note[2] = note[2] - 5

    if pourcentage_lip >= 10 and pourcentage_lip < 20:
        note[0] = note[0] - 5
        note[1] = note[1] - 5

    if pourcentage_lip >= 20 and pourcentage_lip < 25:
        note[0] = note[0] - 5
        note[2] = note[2] - 5

    if pourcentage_lip >= 25 and pourcentage_lip < 35:
        note[1] = note[1] - 5
        note[2] = note[2] - 5

    print(note)
    return note


def food_checker_main(url, df_propre):
    recipe = scrapper(url)
    df_propre["alim_nom_fr"] = df_propre["alim_nom_fr"].apply(normalize_text)
    df_propre["alim_ssgrp_nom_fr"] = df_propre["alim_ssgrp_nom_fr"].apply(normalize_text)
    ingr_list = list_to_tab(recipe)

    print("Liste des ingrédients: \n\n")
    print(ingr_list)
    print("Calcul des nutriments: \n\n")
    tab_nutriments = food_calculator(ingr_list, df_propre)
    return tab_nutriments


@app.route("/index/")
def index():
    return render_template("index.html")
@app.route("/djoe/")
def djoe():

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'djoe.jpg')
    return render_template("djoe.html", user_image = full_filename)

@app.route("/get_recipe/<path:url>")
def get_recipe(url):
    print(url)
    df_propre = data_epurator();
    tab_nutriments = food_checker_main(url, df_propre)
    noteR = note(tab_nutriments)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'djoe.jpg')
    return render_template("djoe.html", user_image = full_filename)

@app.route("/index/")    
def find_bdd_result():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'djoe.jpg')
    return render_template("djoe.html", user_image = full_filename)

if __name__ == "__main__":
    app.run(debug=True)