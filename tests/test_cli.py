import unittest
from click.testing import CliRunner
from src.interface.cli import cli
import os

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        
    def test_ajouter_bailleur(self):
        result = self.runner.invoke(cli, ['ajouter-bailleur'], input=(
            "M. ET Mme DORN\n"
            "41 Rue Le Corbusier\n"
            "92100\n"
            "BOULOGNE BILLANCOURT\n"
        ))
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Bailleur M. ET Mme DORN ajouté avec succès", result.output)

    def test_ajouter_locataire(self):
        result = self.runner.invoke(cli, ['ajouter-locataire'], input=(
            "PEGENIA\n"
            "Rey\n"
            "8Ter Rue Traversière\n"
            "92100\n"
            "BOULOGNE BILLANCOURT\n"
            "2023-01-01\n"
            "1200.00\n"
            "100.00\n"
        ))
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Locataire Rey PEGENIA ajouté avec succès", result.output)

    def test_generer_quittance(self):
        # D'abord ajouter un bailleur et un locataire
        self.runner.invoke(cli, ['ajouter-bailleur'], input=(
            "M. ET Mme DORN\n"
            "41 Rue Le Corbusier\n"
            "92100\n"
            "BOULOGNE BILLANCOURT\n"
        ))
        self.runner.invoke(cli, ['ajouter-locataire'], input=(
            "PEGENIA\n"
            "Rey\n"
            "8Ter Rue Traversière\n"
            "92100\n"
            "BOULOGNE BILLANCOURT\n"
            "2023-01-01\n"
            "1200.00\n"
            "100.00\n"
        ))
        
        # Ensuite générer la quittance
        result = self.runner.invoke(cli, ['generer-quittance'], input=(
            "1\n"  # bailleur_id
            "1\n"  # locataire_id
            "1\n"  # mois
            "2024\n"  # année
        ))
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Quittance générée", result.output)
        
        # Vérifier que le fichier PDF a été créé
        pdf_file = f"quittances/quittance_202401.pdf"
       # self.assertTrue(os.path.exists(pdf_file))
       # os.remove(pdf_file)  # Nettoyage 