from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from data_base import read_text, modify_text, add_count, ten_count, day_count, hour_count, total_count, add_recette, list_recette, sans_espace
from wsgiref.simple_server import make_server
import os


app = Flask(__name__)

app.secret_key = '0624359673f6036ad6b5f75515585460'


@app.context_processor
def inject_global_vars():
    return {'total_count': total_count(), 'hour_count':hour_count(),'ten_count':ten_count(),'day_count':day_count()}

def version():
    if request.method == "POST":
        donnes = request.form
        version = donnes.get('version')
        if version == "visiteur":
            session["version"] = "visiteur"
        elif version == "admin" :
            session["version"] = "admin"

def print_text(page):
    if request.method == "POST" :
        donnes = request.form
        texte_page = donnes.get(f'texte_{page}')
        if texte_page is not None :
            modify_text(texte_page, page)
    texte_page = read_text(page)
    if (request.method == 'GET' and session.get('version')!='admin') or session.get('version')=='visiteur':
        texte_page = texte_page.splitlines()
    return texte_page
        



@app.route('/', methods=['POST','GET'])
def index():
    version()
    if session.get('version') is None :
        add_count()
    return render_template('index.html', texte=print_text('accueil'))

@app.route('/a-cueillir', methods=['POST','GET'])
def a_cueillir():
    version()

    return render_template('a_cueillir.html',texte_date=print_text('date'), texte_cueillir=print_text("cueillir"), texte_chalet=print_text('chalet'), texte_tard=print_text('tard') )

@app.route('/horaires', methods=['POST','GET'])
def horaires():
    version()
    texte_horaires = print_text('horaires')
    return render_template('horaires.html', texte=texte_horaires)

@app.route('/recettes', methods=['POST','GET'])
def liste_recettes():
    version()
    if request.method == "POST" :
        donnes = request.form
        texte_page = donnes.get('recette')
        if texte_page is not None :
            print('texte_page')
            add_recette(texte_page)
    return render_template('liste-recettes.html', liste_recette = list_recette(), espace=sans_espace)

@app.route('/recettes/<nom_recette>', methods=['POST','GET'])
def recettes(nom_recette):
    version()
    if request.method == "POST" :
        donnes = request.form
        texte_page = donnes.get('supprimer')
        if texte_page is not None :
            df = pd.read_csv('db/recettes.csv', index_col=0)
            df.loc[nom_recette]=0
            df.to_csv(f'db/recettes.csv')
            return redirect(url_for("liste_recettes"))
    return render_template('recettes.html',nom_recette = nom_recette, texte_ingredients=print_text(f'ingredients-{nom_recette}'), texte_etapes=print_text(f"etapes-{nom_recette}"),nom_recette_sans_espace=sans_espace(nom_recette))

@app.route('/photos', methods=['POST','GET'])
def photos():
    version()
    return render_template('photos.html')

@app.route('/calendrier', methods=['POST','GET'])
def calendrier():
    version()
    return render_template('calendrier.html')

@app.route('/a-propos', methods=['POST','GET'])
def a_propos():
    version()
    return render_template('a_propos.html')

@app.route('/credit', methods=['POST','GET'])
def credit():
    version()
    return render_template('credit.html')

@app.route('/admin', methods=['POST','GET'])
def admin():
    version()
    if request.method == "POST":
        donnes = request.form
        nom, mdp = donnes.get('nom'), donnes.get('mdp')
        if nom == "admin" and mdp == "fraises" :
            session['utilisateur'] = "admin"
            session['version'] = 'admin'
            return redirect(url_for('index'))
        elif nom is not None : 
            session['utilisateur'] = "mauvais"
            return redirect(url_for('admin'))
        else : 
            return redirect(url_for('admin'))
    else : 
        return render_template('admin.html')
    
@app.route("/upload/photo<number>", methods=["POST"])
def upload(number):
  # Récupérez le fichier déposé par l'utilisateur
    file = request.files.get("file")
  # Enregistrez le fichier dans le dossier `/uploads`
    file.save(f"static/img/uploads/photos/photo{number}.jpeg")  
    return redirect(url_for('photos'))

@app.route("/upload/recettes/<nom_recette>", methods=["POST"])
def upload_recette(nom_recette):
  # Récupérez le fichier déposé par l'utilisateur
    file = request.files.get("file")
  # Enregistrez le fichier dans le dossier `/uploadss` 
    file.save(f"static/img/uploads/recettes/{nom_recette}.jpeg")  
    return redirect(url_for("recettes", nom_recette=nom_recette))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)

