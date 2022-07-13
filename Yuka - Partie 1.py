#!/usr/bin/env python
# coding: utf-8

# # Le dataset
# 
# Dans ce challenge on utilisera le dataset ci-après [dataset food](https://drive.google.com/open?id=1L4tDDnZWwPDjeRKlleoYHgic2_xNhZ8i). Attention il est volumineux !!!
# 
# Tu l'utiliseras pour mener une analyse descriptive et exploratoire. L'objectif est d'arriver à un dataset permettant de répondre à la question : "Est-ce que cet aliment est sain ou non ?"
# 
# 

# In[19]:


import pandas as pd
import numpy as np


# # Mission 1
# 
# 
# Trouve le moyen d'ouvrir le fichier et d'afficher les 10 premiers éléments du dataset ci-dessus.
# 
# Ensuite affiche le nombre de colonne objet et float.

# In[20]:


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
# Authenticate and create the PyDrive client.
# The goal is to connect your Google Drive with this Google colab notebook.
# This only needs to be done once per notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

# This part is here to copy the file into your Drive (because we can't open a shared file)
url = 'https://drive.google.com/file/d/1L4tDDnZWwPDjeRKlleoYHgic2_xNhZ8i/view'
file_id = '1L4tDDnZWwPDjeRKlleoYHgic2_xNhZ8i'
downloaded = drive.CreateFile({'id': file_id})
downloaded.GetContentFile('fr.openfoodfacts.org.products.csv')

df = pd.read_csv('fr.openfoodfacts.org.products.csv', sep='\t')


# In[21]:


df.head(5)


# In[22]:


df.info()


# # Mission 2
# 
# Trouve le moyen d'afficher d'une part **uniquement** les noms des colonnes objet, et d'autre part **uniquement** les noms des colonnes float.

# In[23]:


colonne_float = []
colonne_object = []
for i in df.columns:
    if df[i].dtype == np.float64 :
          colonne_float.append(i)
    elif df[i].dtype == np.object :
          colonne_object.append(i)
print('Les colonnes float sont : ',colonne_float)
print('Les colonnes object sont : ',colonne_object)


# # Mission 3
# 
# Crée une fonction qui prend en paramètre un dataframe, et affiche le taux de remplissage de chacune de ces colonnes sous forme de pourcentage. C'est à dire :
# - colonne 1 : 73%
# - colonne 2 : 99%

# In[24]:


def remplissage_colonne(data) :
    count = 0
    dico = {}
    for label, content in data.items():
        count = len(data)-(data[label].isna().sum())
        dico.update({label : (count/len(data)*100)})
        count = 0
    percent = pd.DataFrame(list(dico.items()),columns=['Nom de colonne', 'Percent'])
    return percent
remp = remplissage_colonne(df)
remp


# # Mission 4
# 
# Quel est le nombre de colonne appartenant à chaque quartile des taux de remplissage ? Autrement dit, combien de colonne sont remplies à 0%, entre 0 et 25%, entre 25 et 50%...

# In[25]:


print('Remplissage à 0% : ',remp[remp['Percent'] == 0].count())


# In[26]:


print('Remplissage de 0% à 25% : ',remp[(remp['Percent'] > 0) & (remp['Percent'] <=25)].count())


# In[27]:


print('Remplissage de 25% à 50% : ',remp[(remp['Percent'] > 25) & (remp['Percent'] <=50)].count())


# In[28]:


print('Remplissage de 50% à 75% : ',remp[(remp['Percent'] > 50) & (remp['Percent'] <=75)].count())


# In[29]:


print('Remplissage de 75% à 100% : ',remp[(remp['Percent'] > 75) & (remp['Percent'] <=100)].count())


# # Mission 5
# 
# Nous voulons nous concentrer sur les aliments disponibles en France, là ou nous allons lancer la plateforme. Pour cela sélectionner uniquement les lignes dont la valeur du countries_fr contient le mot "France".

# In[30]:


df_france = df.loc[df['countries_fr'].str.contains('France', case = False) == True]
df_france


# # Mission 6
# 
# Un dataset trop pauvre en data n'est pas vraiment intéressant. Après avoir analyser les colonnes, nous nous sommes rendu compte que nous pouvons supprimer les colonnes avec moins de 60% de valeurs non nulles, sauf les colonnes pnns_groups_1 et pnns_groups_2, nutrition-score-fr_100g et nutrition-score-uk_100g. En effet ces 2 colonnes vont nous être utiles par la suite.
# 
# Si ce n'est pas déjà fait, supprime également les colonnes suivantes car elles ne sont pas vraiment utiles pour répondre à notre problématique :
# * creator
# * created_t
# * created_datetime
# * last_modified_t
# * brands_tags
# * countries
# * countries_tags
# * additives_tags
# * states
# * states_tags

# In[31]:


liste = ['pnns_groups_1', 'pnns_groups_2', 'nutrition-score-fr_100g', 'nutrition-score-uk_100g']
remp_60 = remp[(remp['Percent'] >= 60) | (remp['Nom de colonne'].isin(liste))]
remp_60


# In[32]:


df_france_60 = df_france[df_france.columns[df_france.columns.isin(remp_60['Nom de colonne'])]]
df_france_60


# In[33]:


df_france_60 = df_france_60.drop(columns = ['creator', 'created_t', 'created_datetime', 'last_modified_t', 'brands_tags', 'countries',
                                            'countries_tags', 'states', 'states_tags'])
df_france_60


# # Mission 7
# 
# Exporte ton travail au format csv
# 
# 

# In[35]:


df_france_60.to_csv("df_france.csv", sep = ";")

