import unittest
import os
from datetime import date
from src.models.database import Database
from src.models.bailleur import Bailleur
from src.models.locataire import Locataire
from src.models.quittance import Quittance
import time

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_quittances.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass
        self.db = Database(self.db_path).__enter__()
        
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

    def tearDown(self):
        if self.db:
            self.db.__exit__(None, None, None)
            self.db = None
        
        # Attendre un peu que les ressources soient libérées
        time.sleep(0.1)
        
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
        except PermissionError:
            pass

    def test_ajouter_bailleur(self):
        bailleur_id = self.db.ajouter_bailleur(self.bailleur)
        self.assertIsNotNone(bailleur_id)
        
        bailleur_recupere = self.db.get_bailleur(bailleur_id)
        self.assertEqual(bailleur_recupere.nom, self.bailleur.nom)
        self.assertEqual(bailleur_recupere.adresse, self.bailleur.adresse)

    def test_ajouter_locataire(self):
        locataire_id = self.db.ajouter_locataire(self.locataire)
        self.assertIsNotNone(locataire_id)
        
        locataire_recupere = self.db.get_locataire(locataire_id)
        self.assertEqual(locataire_recupere.nom, self.locataire.nom)
        self.assertEqual(locataire_recupere.prenom, self.locataire.prenom)
        self.assertEqual(locataire_recupere.montant_loyer, self.locataire.montant_loyer)

    def test_sauvegarder_quittance(self):
        bailleur_id = self.db.ajouter_bailleur(self.bailleur)
        locataire_id = self.db.ajouter_locataire(self.locataire)
        
        quittance = Quittance(
            bailleur=self.bailleur,
            locataire=self.locataire,
            periode_debut=date(2024, 1, 1),
            periode_fin=date(2024, 1, 31)
        )
        
        quittance_id = self.db.sauvegarder_quittance(quittance)
        self.assertIsNotNone(quittance_id) 