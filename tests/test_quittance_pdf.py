import unittest
import os
from datetime import date
from src.models.quittance_pdf import QuittancePDF
from src.models.quittance import Quittance
from src.models.bailleur import Bailleur
from src.models.locataire import Locataire

class TestQuittancePDF(unittest.TestCase):
    def setUp(self):
        self.bailleur = Bailleur(
            nom="M. ET Mme DORN",
            adresse="41 Rue Le Corbusier",
            code_postal="92100",
            ville="BOULOGNE BILLANCOURT"
        )
        
        self.locataire = Locataire(
            nom="PEGENIA",
            prenom="Rey",
            adresse="8Ter Rue Traversière",
            code_postal="92100",
            ville="BOULOGNE BILLANCOURT",
            date_debut_bail=date(2023, 1, 1),
            montant_loyer=1200.00,
            montant_charges=100.00
        )

        self.quittance = Quittance(
            bailleur=self.bailleur,
            locataire=self.locataire,
            periode_debut=date(2024, 1, 1),
            periode_fin=date(2024, 1, 31)
        )

    def test_generation_pdf(self):
        pdf = QuittancePDF(self.quittance)
        chemin_test = "test_quittance.pdf"
        pdf.generer(chemin_test)
        
        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(chemin_test))
        # Vérifier la taille du fichier
        self.assertGreater(os.path.getsize(chemin_test), 0)
        
        # Nettoyage
        if os.path.exists(chemin_test):
            os.remove(chemin_test)

    def test_contenu_pdf(self):
        pdf = QuittancePDF(self.quittance)
        chemin_test = "quittances/test_quittance.pdf"
        pdf.generer(chemin_test)
        
        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(chemin_test))
        
        # Vérifier la taille du fichier
        taille = os.path.getsize(chemin_test)
        self.assertGreater(taille, 0)
        
        # Idéalement, nous devrions ajouter des tests pour vérifier le contenu du PDF
        # Cela nécessiterait une bibliothèque comme PyPDF2 pour lire le contenu
        
        # Nettoyage
        if os.path.exists(chemin_test):
            os.remove(chemin_test)

    def test_generation_multiple(self):
        pdf = QuittancePDF(self.quittance)
        
        for mois in range(1, 13):
            chemin_test = f"quittances/test_quittance_{mois}.pdf"
            pdf.generer(chemin_test)
            self.assertTrue(os.path.exists(chemin_test))
            os.remove(chemin_test)

    def test_periode_location(self):
        pdf = QuittancePDF(self.quittance)
        chemin_test = "quittances/test_quittance_periode.pdf"
        pdf.generer(chemin_test)
        
        # Vérifier que le fichier existe
        self.assertTrue(os.path.exists(chemin_test))
        
        # La vérification du contenu nécessiterait PyPDF2
        # Mais nous pouvons vérifier que la période est correctement formatée
        periode_attendue = "01 janvier 2024 au 31 janvier 2024"
        self.assertEqual(self.quittance.periode_str(), periode_attendue)
        
        # Nettoyage
        if os.path.exists(chemin_test):
            os.remove(chemin_test) 