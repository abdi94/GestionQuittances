import unittest
from datetime import date
from src.models.quittance import Quittance
from src.models.bailleur import Bailleur
from src.models.locataire import Locataire

class TestQuittance(unittest.TestCase):
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

        # Initialiser la quittance dans setUp
        self.quittance = Quittance(
            bailleur=self.bailleur,
            locataire=self.locataire,
            periode_debut=date(2024, 1, 1),
            periode_fin=date(2024, 1, 31)
        )

    def test_creation_quittance(self):
        self.assertEqual(self.quittance.montant_total(), 1300.00)
        periode_attendue = "01 janvier 2024 au 31 janvier 2024"
        self.assertEqual(self.quittance.periode_str(), periode_attendue)

    def test_validation_periode(self):
        with self.assertRaises(ValueError):
            Quittance(
                bailleur=self.bailleur,
                locataire=self.locataire,
                periode_debut=date(2024, 2, 1),
                periode_fin=date(2024, 1, 1)
            )

    def test_validation_debut_bail(self):
        with self.assertRaises(ValueError):
            Quittance(
                bailleur=self.bailleur,
                locataire=self.locataire,
                periode_debut=date(2022, 1, 1),  # Avant le début du bail
                periode_fin=date(2022, 1, 31)
            )

    def test_numero_quittance(self):
        self.assertEqual(self.quittance.numero, "Q202401")

    def test_numero_quittance_personnalise(self):
        quittance = Quittance(
            bailleur=self.bailleur,
            locataire=self.locataire,
            periode_debut=date(2024, 1, 1),
            periode_fin=date(2024, 1, 31),
            numero="Q2024-01-CUSTOM"
        )
        self.assertEqual(quittance.numero, "Q2024-01-CUSTOM")

  