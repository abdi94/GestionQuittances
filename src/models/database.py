import sqlite3
from datetime import date
from src.models.bailleur import Bailleur
from src.models.locataire import Locataire
import atexit

class Database:
    def __init__(self, db_path="quittances.db"):
        self.db_path = db_path
        self.connection = None
        self._create_tables()
        atexit.register(self.close)

    def _get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def _create_tables(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Table Bailleur
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bailleur (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                adresse TEXT NOT NULL,
                code_postal TEXT NOT NULL,
                ville TEXT NOT NULL
            )
        ''')
        
        # Table Locataire
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locataire (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                adresse TEXT NOT NULL,
                code_postal TEXT NOT NULL,
                ville TEXT NOT NULL,
                date_debut_bail DATE NOT NULL,
                montant_loyer REAL NOT NULL,
                montant_charges REAL NOT NULL
            )
        ''')
        
        # Table Quittance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quittance (
                id INTEGER PRIMARY KEY,
                numero TEXT NOT NULL,
                bailleur_id INTEGER,
                locataire_id INTEGER,
                periode_debut DATE NOT NULL,
                periode_fin DATE NOT NULL,
                date_emission DATE NOT NULL,
                FOREIGN KEY (bailleur_id) REFERENCES bailleur (id),
                FOREIGN KEY (locataire_id) REFERENCES locataire (id)
            )
        ''')
        conn.commit()

    def ajouter_bailleur(self, bailleur):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bailleur (nom, adresse, code_postal, ville)
            VALUES (?, ?, ?, ?)
        ''', (bailleur.nom, bailleur.adresse, bailleur.code_postal, bailleur.ville))
        conn.commit()
        return cursor.lastrowid

    def ajouter_locataire(self, locataire):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO locataire (nom, prenom, adresse, code_postal, ville,
                                 date_debut_bail, montant_loyer, montant_charges)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (locataire.nom, locataire.prenom, locataire.adresse,
              locataire.code_postal, locataire.ville, locataire.date_debut_bail,
              locataire.montant_loyer, locataire.montant_charges))
        conn.commit()
        return cursor.lastrowid

    def get_bailleur(self, bailleur_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bailleur WHERE id = ?', (bailleur_id,))
        row = cursor.fetchone()
        if row:
            return Bailleur(
                id=row[0],
                nom=row[1],
                adresse=row[2],
                code_postal=row[3],
                ville=row[4]
            )
        return None

    def get_locataire(self, locataire_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM locataire WHERE id = ?', (locataire_id,))
        row = cursor.fetchone()
        if row:
            return Locataire(
                id=row[0],
                nom=row[1],
                prenom=row[2],
                adresse=row[3],
                code_postal=row[4],
                ville=row[5],
                date_debut_bail=date.fromisoformat(row[6]),
                montant_loyer=row[7],
                montant_charges=row[8]
            )
        return None

    def sauvegarder_quittance(self, quittance):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quittance (numero, bailleur_id, locataire_id,
                                 periode_debut, periode_fin, date_emission)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (quittance.numero, quittance.bailleur.id, quittance.locataire.id,
              quittance.periode_debut, quittance.periode_fin, quittance.date_emission))
        conn.commit()
        return cursor.lastrowid

    def lister_bailleurs(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bailleur')
        return cursor.fetchall()

    def lister_locataires(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM locataire')
        return cursor.fetchall()

    def lister_quittances(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                q.id,
                q.numero,
                q.bailleur_id,
                q.locataire_id,
                q.periode_debut,
                q.periode_fin,
                q.date_emission,
                b.nom as bailleur_nom,
                l.nom as locataire_nom,
                l.prenom as locataire_prenom
            FROM quittance q
            LEFT JOIN bailleur b ON q.bailleur_id = b.id
            LEFT JOIN locataire l ON q.locataire_id = l.id
        ''')
        return cursor.fetchall()

    def vider_tables(self):
        """Vide toutes les tables de la base de données"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Désactiver les contraintes de clés étrangères temporairement
        cursor.execute('PRAGMA foreign_keys = OFF')
        
        # Vider les tables dans l'ordre inverse des dépendances
        cursor.execute('DELETE FROM quittance')
        cursor.execute('DELETE FROM locataire')
        cursor.execute('DELETE FROM bailleur')
        
        # Réinitialiser les compteurs d'ID
        cursor.execute('DELETE FROM sqlite_sequence')
        
        # Réactiver les contraintes de clés étrangères
        cursor.execute('PRAGMA foreign_keys = ON')
        
        conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 