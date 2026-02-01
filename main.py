import os
from typing import Optional

from supabase import create_client, Client
from fastapi import FastAPI,Request
from pydantic import BaseModel
import time

app=FastAPI()

SUPABASE_URL='https://nciavyshfzeeasjjdgck.supabase.co'
SUPABASE_KEY='sb_publishable_M6zNV1rveNAYU6KPdKH7mQ_wgamdve6'
url: str = os.environ.get(SUPABASE_URL)
key: str = os.environ.get(SUPABASE_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# definition de la classe Utilisateur
class Utilisateur(BaseModel):
    nom: Optional[str] = None
    numero: Optional[str] = None
    mot_de_passe: Optional[str] = None
    numero_utilisation: Optional[str] = None


# definition de la classe Commande
class Commande_produit(BaseModel):
    nom: str
    numero: str
    produit: str
    quantite: str
    prix_produit: str

clients={}

fenetre_de_temps=60
limite=5

#requette pour ajouter un utilisateur
@app.post("/ajouter_utilisateur")

#fonction pour ajouter un uilsateur
def ajouter_utisateur(request:Request,utilisateur:Utilisateur):
    ip = request.client.host
    temps_client = int(time.time())

    if ip not in clients:
        clients[ip] = {"temps": temps_client, "nombre de requette": 1}
        pass
    else:
        if clients[ip]["nombre de requette"] >= limite:
            if int(time.time()) - clients[ip]["temps"] > fenetre_de_temps:
                clients[ip]["nombre de requette"] = 1
                pass
            else:
                return {"resultat": "trop de requette petit hacker"}
        else:
            clients[ip]["nombre de requette"] = clients[ip]["nombre de requette"] + 1
            clients[ip]["temps"] = int(time.time())
            print(clients[ip])
            pass
    supabase.table("utilisateurs").insert({
    "nom": utilisateur.nom,
    "numero": utilisateur.numero,
    "mot_de_passe": utilisateur.mot_de_passe
    }).execute()
    return {"statut":"ajouter"}

#requette pour verifier l'etat d'un utilisateur dans la base
@app.post("/verifier_utilisateur")

#fonction pour verifier l'etat d'un utilisateur dans la base
def verifier_utilisateur(request:Request,utilisateur:Utilisateur):
    ip = request.client.host
    temps_client = int(time.time())

    if ip not in clients:
        clients[ip] = {"temps": temps_client, "nombre de requette": 1}
        pass
    else:
        if clients[ip]["nombre de requette"] >= limite:
            if int(time.time()) - clients[ip]["temps"] > fenetre_de_temps:
                clients[ip]["nombre de requette"] = 1
                pass
            else:
                return {"resultat": "trop de requette petit hacker"}
        else:
            clients[ip]["nombre de requette"] = clients[ip]["nombre de requette"] + 1
            clients[ip]["temps"] = int(time.time())
            print(clients[ip])
            pass
    resultat=supabase.table("utilisateurs").select("*").eq("numero",utilisateur.numero).execute()
    if resultat.data==[]:
        return {"resultat":"existe pas"}
    else:
        return {"resultat":resultat.data}


#fonction pour reconnecter un utilisateur
@app.post("/reconnecter_utilisateur")

def reconnecter_utilisateur(request:Request,utilisateur:Utilisateur):
    ip = request.client.host
    temps_client = int(time.time())

    if ip not in clients:
        clients[ip] = {"temps": temps_client, "nombre de requette": 1}
        pass
    else:
        if clients[ip]["nombre de requette"] >= limite:
            if int(time.time()) - clients[ip]["temps"] > fenetre_de_temps:
                clients[ip]["nombre de requette"] = 1
                pass
            else:
                return {"resultat": "trop de requette petit hacker"}
        else:
            clients[ip]["nombre de requette"] = clients[ip]["nombre de requette"] + 1
            clients[ip]["temps"] = int(time.time())
            print(clients[ip])
            pass
    resultat=supabase.table("utilisateurs").select("nom","numero").eq("numero",utilisateur.numero).eq("mot_de_passe",utilisateur.mot_de_passe).execute()
    if resultat.data==[]:
        return {"resultat":"existe pas"}
    else:
        return {"resultat":resultat.data}

#fonction pour enregistrer les commandes dans la base de donnees
@app.post("/enregistrer_commande")
def enregistrer_commande(request:Request,commande:Commande_produit):
    ip = request.client.host
    temps_client = int(time.time())

    if ip not in clients:
        clients[ip] = {"temps": temps_client, "nombre de requette": 1}
        pass
    else:
        if clients[ip]["nombre de requette"] >=limite:
            if int(time.time()) - clients[ip]["temps"] > fenetre_de_temps:
                clients[ip]["nombre de requette"] = 1
                pass
            else:
                return {"resultat": "trop de requette petit hacker"}
        else:
            clients[ip]["nombre de requette"] = clients[ip]["nombre de requette"] + 1
            clients[ip]["temps"] = int(time.time())
            print(clients[ip])
            pass
    supabase.table("commande").insert({
    "numero":commande.numero,
    "quantite":commande.quantite,
    "produit":commande.produit,
    "nom":commande.nom,
    "prix_produit":commande.prix_produit
    }).execute()
    return {"resultat":"commande ajoutée"}


@app.post("/modifier_utilisateur")
def modifier_utilisateur(request:Request,modifier:Utilisateur):

    ip = request.client.host
    temps_client = int(time.time())

    if ip not in clients:
        clients[ip] = {"temps": temps_client, "nombre de requette": 1}
        pass
    else:
        if clients[ip]["nombre de requette"] >= 3:
            if int(time.time()) - clients[ip]["temps"] > fenetre_de_temps:
                clients[ip]["nombre de requette"] = 1
                pass
            else:
                return {"resultat": "trop de requette petit hacker"}
        else:
            clients[ip]["nombre de requette"] = clients[ip]["nombre de requette"] + 1
            clients[ip]["temps"] = int(time.time())
            print(clients[ip])
            pass
    supabase.table("utilisateurs").update({
        "nom":modifier.nom,
        "mot_de_passe":modifier.mot_de_passe,
    }).eq("numero",modifier.numero).execute()
    return {"resultat":"modifications ajoutées"}

#fonction pour envoyer les commandes
@app.post("/ensemble_des_commandes")
def envoie_des_commandes():
    resultat=supabase.table("commande").select("*").execute()
    if resultat.data == []:
        return {"resultat": "existe pas"}
    else:
        return {"resultat": resultat.data}


