
# 🏠 GestionQuittances GUI

**QuittanceGUI** est une application graphique (GUI) développée en Python pour aider à la gestion des loyers, locataires, quittances, et autres fonctionnalités essentielles pour les propriétaires et les gestionnaires immobiliers.

> **Ce projet est un fork de [franpi92/GestionQuittances](https://github.com/franpi92/GestionQuittances).**  
> Retrouvez ce projet modifié dans [mon dépôt GitHub ici](https://github.com/abdi94/GestionQuittances.git).

---

## ⚡ Fonctionnalités

- Ajouter un nouveau **bailleur** avec des informations spécifiques.
- Ajouter un nouveau **locataire** en remplissant un formulaire facile à utiliser.
- Générer automatiquement une **quittance de loyer** prête à l'utilisation.
- Interface graphique intuitive créée avec **Tkinter**.

---

## 🛠️ Structure du Code

La classe principale du projet est `LoyerGUI`, contenant notamment les méthodes suivantes :

- **`_build_widgets`** : Crée et configure les composants de l'interface graphique.
- **`_create_form`** : Formulaire dynamique pour la saisie des informations des bailleurs/locataires.
- **`_exec_ajouter_bailleur`** : Ajoute un nouveau bailleur à la base de données de l'application.
- **`_exec_ajouter_locataire`** : Ajoute un locataire avec des détails personnalisés.
- **`_exec_generer_quittance`** : Génère et exporte des quittances de loyer.
- **`_log`** : Maintient un journal détaillé des actions exécutées par l'utilisateur.

---

## 🚀 Installation et Exécution

### **Prérequis :**
- **Python 3.12.6** ou une version ultérieure.
- Les bibliothèques requises (voir `requirements.txt`).

### **Étapes d'installation avec environnement virtuel :**
1. Clonez ce dépôt sur votre machine locale :
```shell script
git clone https://github.com/abdi94/GestionQuittances.git
```
2. Accédez au dossier du projet :
```shell script
cd GestionQuittances
```
3. Créez un **environnement virtuel** dans votre dossier actuel :
```shell script
python -m venv env
```
4. Activez l'environnement virtuel :
   - Sur **Windows** :
```shell script
./env/Scripts/activate
```
   - Sur **Linux/macOS** :
```shell script
source env/bin/activate
```
5. Installez les dépendances requises dans cet environnement virtuel :
```shell script
pip install -r requirements.txt
```
6. Exécutez le fichier principal pour lancer l'application :
```shell script
python gui_launcher.py
```

---

## 🎨 Interface Utilisateur

Quelques éléments de l'interface :
- Un **formulaire clair et simple** pour enregistrer les informations des bailleurs et locataires.
- Des boutons pour déclencher les principales actions comme ajouter des données ou générer des quittances.
- Des **pop-ups interactifs** pour montrer les notifications, erreurs ou confirmations.

---

## 📂 Organisation des Fichiers

Voici la structure recommandée pour ce projet :

```
📁 GestionQuittances/
├── gui_launcher.py         # Script principal pour exécuter l'application
├── README.md               # Documentation du projet
├── requirements.txt        # Liste des dépendances nécessaires au projet
└── resources/              # Contient les ressources telles que les templates et les images
```

---

## 📝 Exemple d'Utilisation

```python
from gui_launcher import LoyerGUI

# Initialisez et démarrez l'application
app = LoyerGUI()
app.run()
```

---

## 🙌 Contributions

Ce projet est ouvert à vos contributions !  
Si vous souhaitez :
- **Signaler un bug** : Ouvrez une **issue**.
- **Ajouter une fonctionnalité** : Créez une **pull request** après avoir forké ce projet.

Toutes les idées sont les bienvenues pour améliorer l'application !

---

## 📜 Licence

Le projet est sous la **licence MIT**, tout comme le projet original. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🌟 Remerciements

Un grand merci à [franpi92](https://github.com/franpi92) pour la création du projet initial et de cet outil utile !

---

Si vous souhaitez d'autres ajustements ou nouvelles sections, n'hésitez pas à demander ! 😊
