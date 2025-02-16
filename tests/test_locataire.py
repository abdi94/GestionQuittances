import unittest
from datetime import date
from src.models.locataire import Locataire

class TestLocataire(unittest.TestCase):
    def setUp(self):
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

    def test_creation_locataire(self):
        self.assertEqual(self.locataire.nom, "PEGENIA")
        self.assertEqual(self.locataire.prenom, "Rey")
        self.assertEqual(self.locataire.montant_loyer, 1200.00)
        self.assertEqual(self.locataire.montant_charges, 100.00)

    def test_loyer_total(self):
        self.assertEqual(self.locataire.loyer_total(), 1300.00)

    def test_adresse_complete(self):
        adresse_attendue = "8ter Rue Traversière\n92100 BOULOGNE BILLANCOURT"
        self.assertEqual(self.locataire.adresse_complete(), adresse_attendue)

    def test_nom_complet(self):
        self.assertEqual(self.locataire.nom_complet(), "Rey PEGENIA")

    def test_validation_montants_negatifs(self):
        with self.assertRaises(ValueError):
            Locataire(
                nom="PEGENIA",
                prenom="Rey",
                adresse="8Ter Rue Traversière",
                code_postal="92100",
                ville="BOULOGNE BILLANCOURT",
                date_debut_bail=date(2023, 1, 1),
                montant_loyer=-1200.00,
                montant_charges=100.00
            )

    def test_validation_date_bail(self):
        with self.assertRaises(ValueError):
            Locataire(
                nom="PEGENIA",
                prenom="Rey",
                adresse="8Ter Rue Traversière",
                code_postal="92100",
                ville="BOULOGNE BILLANCOURT",
                date_debut_bail=date(2025, 1, 1),
                montant_loyer=1200.00,
                montant_charges=100.00
            ) 