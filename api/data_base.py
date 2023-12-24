import numpy as np
import pandas as pd
import datetime as dt

total_stock = 6*24
interv = 600
mat = np.zeros((total_stock,2))
df_total = pd.DataFrame(['total'], index=['heure'])
df_total.to_csv('db/test.csv')

def init_db(page):
    # pour initier les bases de données
    df = pd.DataFrame({'contenu':'blablaao'}, index=[f'{page}'])
    df.index.name = 'titre'
    df.to_csv(f'db/{page}.csv')

def add_count():
    """fonction qui compte le nombre de connections et envoie à la db tous les interv et stock un nombre total_stock"""
    df_total = pd.read_csv('db/count.csv', index_col=[0])
    derniere_heure = df_total.index.max()
    total = int(df_total.loc[derniere_heure]['total']) + 1
    now = dt.datetime.now()
    delta = now-dt.datetime.strptime(derniere_heure,'%Y-%m-%d %H:%M:%S.%f')

    if delta.total_seconds() > interv:
        n = int(delta.total_seconds() // interv) # le nombre de dix minutes où il ne s'est rien passé
        if n >= total_stock:
            n = total_stock # si jamais on a pas plus d'une journée

        for k in range(n-1,-1,-1):
            date = now - dt.timedelta(seconds=k*interv)
            df_total.loc[str(pd.Timestamp(date))] = total
            if len(df_total) > total_stock:
                df_total = df_total.drop(df_total.index.min())
    else : 
        df_total.loc[df_total.index.max()] += 1
    df_total.to_csv('db/count.csv')

def ten_count():
    df_total = pd.read_csv('db/count.csv', index_col=[0])
    derniere_heure = df_total.index.max()
    avant_derniere_heure = df_total.drop(derniere_heure).index.max()
    return df_total.loc[derniere_heure]['total']-df_total.loc[avant_derniere_heure]['total']

def day_count():
    df_total = pd.read_csv('db/count.csv', index_col=[0])
    derniere_heure = df_total.index.max()
    premiere_heure = df_total.index.min()
    return df_total.loc[derniere_heure]['total']-df_total.loc[premiere_heure]['total']

def hour_count():
    df_total = pd.read_csv('db/count.csv', index_col=[0])
    derniere_heure = df_total.index.max()
    total_derniere_heure = df_total.loc[derniere_heure]['total']
    for k in range(6):
        derniere_heure = df_total.index.max()
        df_total = df_total.drop(derniere_heure)
    derniere_heure_avant = df_total.index.max()
    total_derniere_heure_avant = df_total.loc[derniere_heure_avant]['total']
    return total_derniere_heure-total_derniere_heure_avant

def total_count():
    df_total = pd.read_csv('db/count.csv', index_col=[0])
    derniere_heure = df_total.index.max()
    return df_total.loc[derniere_heure]['total']



def modify_text(texte, page):
    df = pd.read_csv(f'db/contenu.csv', index_col='titre')
    df.loc[f'{page}'] = texte
    df.to_csv(f'db/contenu.csv')


def read_text(page):
    df = pd.read_csv(f'db/contenu.csv', index_col='titre')
    try:
        contenu = df.loc[f'{page}']['contenu']
        return contenu
    except:
        modify_text('initialisation page', page)
        df = pd.read_csv(f'db/contenu.csv', index_col='titre')
        return df.loc[f'{page}']['contenu']

def add_recette(nom_recette):
    # on enlève les espaces
    nom_sans_espace = ""
    for element in nom_recette.split(' '):
        nom_sans_espace += element + '_'
    df = pd.read_csv(f'db/recettes.csv', index_col=0)
    df.loc[nom_recette] = 1
    df.to_csv(f'db/recettes.csv')

def list_recette():
    df = pd.read_csv('db/recettes.csv', index_col=0)
    liste = []
    for recette in list(df.index):
        print(df.loc[recette].keys())
        if df.loc[recette]['exist'] == 1:
            liste.append(recette)
    return liste

def sans_espace(nom_recette):
    nom_espace = ""
    for element in nom_recette.split('_'):
        nom_espace += element + ' '
    return nom_espace
