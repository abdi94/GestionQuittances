import unittest
from src.models.bailleur import Bailleur

class TestBailleur(unittest.TestCase):
    def setUp(self):
        self.bailleur = Bailleur(
            nom="M. ET Mme DORN",
            adresse="41 Rue Le Corbusier",
            code_postal="92100",
            ville="BOULOGNE BILLANCOURT"
        )

    def test_creation_bailleur(self):
        self.assertEqual(self.bailleur.nom, "M. ET Mme DORN")
        self.assertEqual(self.bailleur.adresse, "41 Rue Le Corbusier")
        self.assertEqual(self.bailleur.code_postal, "92100")
        self.assertEqual(self.bailleur.ville, "BOULOGNE BILLANCOURT")

    def test_adresse_complete(self):
        adresse_attendue = "41 Rue Le Corbusier\n92100 BOULOGNE BILLANCOURT"
        self.assertEqual(self.bailleur.adresse_complete(), adresse_attendue)

    def test_modification_informations(self):
        self.bailleur.modifier_informations(
            adresse="42 Rue Le Corbusier",
            code_postal="92100",
            ville="BOULOGNE BILLANCOURT"
        )
        self.assertEqual(self.bailleur.adresse, "42 Rue Le Corbusier") 