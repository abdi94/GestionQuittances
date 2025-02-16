from datetime import date
import click
from src.models.bailleur import Bailleur
from src.models.locataire import Locataire
from src.models.quittance import Quittance
from src.models.quittance_pdf import QuittancePDF
from src.models.database import Database

@click.group()
def cli():
    """Application de gestion des quittances de loyer"""
    pass

@cli.command()
@click.option('--nom', prompt='Nom du bailleur')
@click.option('--adresse', prompt='Adresse')
@click.option('--code-postal', prompt='Code postal')
@click.option('--ville', prompt='Ville')
def ajouter_bailleur(nom, adresse, code_postal, ville):
    """Ajouter un nouveau bailleur"""
    bailleur = Bailleur(nom=nom, adresse=adresse, code_postal=code_postal, ville=ville)
    db = Database()
    db.ajouter_bailleur(bailleur)
    click.echo(f"Bailleur {nom} ajouté avec succès")

@cli.command()
@click.option('--nom', prompt='Nom du locataire')
@click.option('--prenom', prompt='Prénom')
@click.option('--adresse', prompt='Adresse')
@click.option('--code-postal', prompt='Code postal')
@click.option('--ville', prompt='Ville')
@click.option('--date-debut', prompt='Date début bail (YYYY-MM-DD)', type=click.DateTime())
@click.option('--loyer', prompt='Montant loyer', type=float)
@click.option('--charges', prompt='Montant charges', type=float)
def ajouter_locataire(nom, prenom, adresse, code_postal, ville, date_debut, loyer, charges):
    """Ajouter un nouveau locataire"""
    locataire = Locataire(
        nom=nom, prenom=prenom, adresse=adresse,
        code_postal=code_postal, ville=ville,
        date_debut_bail=date_debut.date(),
        montant_loyer=loyer, montant_charges=charges
    )
    db = Database()
    db.ajouter_locataire(locataire)
    click.echo(f"Locataire {prenom} {nom} ajouté avec succès")

@cli.command()
@click.option('--bailleur-id', prompt='ID du bailleur', type=int)
@click.option('--locataire-id', prompt='ID du locataire', type=int)
@click.option('--mois', prompt='Mois (1-12)', type=int)
@click.option('--annee', prompt='Année', type=int)
def generer_quittance(bailleur_id, locataire_id, mois, annee):
    """Générer une quittance de loyer"""
    try:
        db = Database()
        bailleur = db.get_bailleur(bailleur_id)
        if not bailleur:
            raise ValueError(f"Bailleur avec ID {bailleur_id} non trouvé")
            
        locataire = db.get_locataire(locataire_id)
        if not locataire:
            raise ValueError(f"Locataire avec ID {locataire_id} non trouvé")
        
        debut = date(annee, mois, 1)
        if mois == 12:
            fin = date(annee + 1, 1, 1)
        else:
            fin = date(annee, mois + 1, 1)
        
        quittance = Quittance(
            bailleur=bailleur,
            locataire=locataire,
            periode_debut=debut,
            periode_fin=fin
        )
        
        pdf = QuittancePDF(quittance)
        nom_fichier = f"quittance_{quittance.numero}.pdf"
        chemin_complet = pdf.generer(nom_fichier)
        
        db.sauvegarder_quittance(quittance)
        click.echo(f"Quittance générée avec succès : {chemin_complet}")
        
    except Exception as e:
        click.echo(f"Erreur : {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli() 