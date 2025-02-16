# Spécifications GestionQuittances

## Description générale
Application permettant de générer automatiquement des quittances de loyer au format PDF.

## Fonctionnalités principales

### 1. Gestion des informations du bailleur
- Stocker les informations du bailleur (nom, adresse, etc.)
- Permettre la modification des informations
- Supporter plusieurs bailleurs

### 2. Gestion des locataires
- Enregistrer les informations des locataires
- Gérer les informations du bail (date début, montant loyer, charges)
- Supporter plusieurs locataires

### 3. Génération de quittances
- Générer une quittance mensuelle au format PDF
- Inclure automatiquement :
  * Période de location
  * Montant du loyer
  * Montant des charges
  * Montant total
  * Coordonnées du bailleur et du locataire
  * Date d'émission
  * Signature (optionnelle)

### 4. Interface utilisateur
- Interface simple et intuitive
- Formulaire de saisie des informations
- Aperçu avant génération
- Sauvegarde automatique des quittances générées

## Spécifications techniques

### Format de sortie
- Document PDF A4
- Police standard (Arial ou similaire)
- En-tête avec titre "QUITTANCE DE LOYER"
- Utilisation de la bibliothèque reportlab pour la génération PDF
- Corps du document structuré
- Pied de page avec mentions légales

### Stockage des données
- Base de données SQLite pour stocker :
  * Informations des bailleurs
  * Informations des locataires
  * Historique des quittances générées

### Tests
Scénarios de test à implémenter :
1. Création d'un nouveau bailleur
2. Création d'un nouveau locataire
3. Génération d'une quittance simple
4. Modification des informations bailleur/locataire
5. Validation des montants
6. Vérification du format PDF 