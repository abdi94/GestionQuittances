from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
import locale
import os

class QuittancePDF:
    def __init__(self, quittance):
        self.quittance = quittance
        self.styles = getSampleStyleSheet()
        self.signature_path = os.path.join("src", "templates", "firma.PNG")
        try:
            # Essayer différentes locales pour Windows et Linux
            locales_to_try = ['fr_FR.UTF-8', 'fra_fra', 'fr_FR', 'fr']
            for loc in locales_to_try:
                try:
                    locale.setlocale(locale.LC_TIME, loc)
                    break
                except locale.Error:
                    continue
        except:
            pass  # Garder la locale par défaut si aucune n'est disponible
        self._setup_styles()

    def _setup_styles(self):
        # Utiliser les styles existants comme base
        normal_style = self.styles['Normal']
        title_style = self.styles['Title']

        # Ajouter nos styles personnalisés
        self.styles.add(ParagraphStyle(
            'Titre',
            parent=title_style,
            fontSize=14,
            alignment=1,  # Centre
            spaceAfter=20,
            spaceBefore=20
        ))

        self.styles.add(ParagraphStyle(
            'SousTitre',
            parent=normal_style,
            fontSize=12,
            alignment=1,  # Centre
            spaceAfter=30
        ))

        self.styles.add(ParagraphStyle(
            'NormalCustom',
            parent=normal_style,
            fontSize=11,
            spaceAfter=6,
            leading=14  # Espacement entre les lignes
        ))

        self.styles.add(ParagraphStyle(
            'Signature',
            parent=normal_style,
            fontSize=11,
            alignment=2,  # Droite
            spaceBefore=30
        ))

        self.styles.add(ParagraphStyle(
            'MentionsLegales',
            parent=normal_style,
            fontSize=8,
            spaceAfter=6,
            textColor=colors.gray,
            alignment=1  # Centre
        ))

    def _formater_date(self, date_obj):
        """Formate une date en français avec gestion de l'encodage"""
        mois = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        return f"{date_obj.day:02d} {mois[date_obj.month - 1]} {date_obj.year}"

    def _ajouter_entete(self, story):
        story.append(Paragraph("QUITTANCE DE LOYER", self.styles["Titre"]))

    def _ajouter_periode_location(self, story):
        # Obtenir seulement le mois et l'année
        mois = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        mois_str = mois[self.quittance.periode_debut.month - 1]
        annee = self.quittance.periode_debut.year
        
        # Combiner le numéro de quittance et la période sur la même ligne
        story.append(Paragraph(
            f"Quittance n° {self.quittance.numero} &nbsp;pour le mois de {mois_str} {annee}",
            self.styles["SousTitre"]
        ))
        story.append(Spacer(1, 20))

    def _ajouter_informations_bailleur(self, story):
        # Créer un tableau pour encadrer les informations avec largeur réduite
        data = [
            [Paragraph("BAILLEUR :", self.styles["NormalCustom"])],
            [Paragraph(self.quittance.bailleur.nom, self.styles["NormalCustom"])],
            [Paragraph(self.quittance.bailleur.adresse_complete(), self.styles["NormalCustom"])]
        ]
        table = Table(data, colWidths=[8*cm])  # Réduit de 16cm à 8cm
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Aligner le contenu à gauche
        ]))
        
        # Créer un conteneur pour aligner le tableau à gauche
        container = Table([[table]], colWidths=[16*cm])
        container.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Aligner le tableau à gauche
            ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Supprimer le padding à gauche
        ]))
        
        story.append(container)
        story.append(Spacer(1, 20))

    def _ajouter_informations_locataire(self, story):
        # Créer un tableau pour encadrer les informations avec largeur réduite et décalage
        data = [
            [Paragraph("LOCATAIRE :", self.styles["NormalCustom"])],
            [Paragraph(self.quittance.locataire.nom_complet(), self.styles["NormalCustom"])],
            [Paragraph(self.quittance.locataire.adresse_complete(), self.styles["NormalCustom"])]
        ]
        
        # Créer un tableau avec une colonne vide pour le décalage et une colonne pour les données
        table_with_offset = Table(
            [[Spacer(1, 1), table] for table in data],
            colWidths=[8*cm, 8*cm]  # Première colonne pour le décalage, deuxième pour les données
        )
        
        table_with_offset.setStyle(TableStyle([
            ('BOX', (1, 0), (1, -1), 1, colors.black),  # Bordure uniquement autour de la deuxième colonne
            ('TOPPADDING', (1, 0), (1, -1), 6),
            ('BOTTOMPADDING', (1, 0), (1, -1), 6),
            ('LEFTPADDING', (1, 0), (1, -1), 10),
            ('RIGHTPADDING', (1, 0), (1, -1), 10),
        ]))
        story.append(table_with_offset)
        story.append(Spacer(1, 20))

    def _ajouter_montants(self, story):
        data = [
            ["", "Montant"],
            ["Loyer principal", f"{self.quittance.locataire.montant_loyer:.2f} €"],
            ["Provision pour charges", f"{self.quittance.locataire.montant_charges:.2f} €"],
            ["TOTAL", f"{self.quittance.montant_total():.2f} €"]
        ]
        table = Table(data, colWidths=[12*cm, 4*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ]))
        story.append(table)
        story.append(Spacer(1, 30))

    def _ajouter_texte_legal(self, story):
        story.append(Paragraph(self.quittance.texte_legal(), 
                             self.styles["NormalCustom"]))
        story.append(Spacer(1, 30))

    def _ajouter_signature(self, story):
        date_str = self._formater_date(self.quittance.date_emission)
        story.append(Paragraph(
            f"Fait à {self.quittance.bailleur.ville}, le {date_str}", 
            self.styles["Signature"]
        ))
        story.append(Spacer(1, 20))
        
        # Ajouter d'abord le texte "Signature du bailleur"
        story.append(Paragraph("Signature du bailleur", self.styles["Signature"]))
        story.append(Spacer(1, 10))
        
        # Puis ajouter l'image de la signature si elle existe
        if os.path.exists(self.signature_path):
            signature = Image(self.signature_path)
            signature.drawWidth = 1 * inch  
            signature.drawHeight = 0.5 * inch  
            
            # Aligner à droite
            signature.hAlign = 'RIGHT'
            story.append(signature)

    def _ajouter_mentions_legales(self, story):
        story.append(Paragraph(self.quittance.mentions_legales(), 
                             self.styles["MentionsLegales"]))

    def generer(self, chemin_fichier):
        """Génère le PDF de la quittance"""
        # Créer le répertoire de sortie s'il n'existe pas
        output_dir = "quittances"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Construire le chemin complet du fichier
        chemin_complet = os.path.join(output_dir, chemin_fichier)
        
        # Préparer le document avec des marges ajustées
        # Réduire la marge supérieure de 2cm (72 points = 1 pouce ≈ 2.54cm)
        doc = SimpleDocTemplate(
            chemin_complet,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,  # Réduit de 72 à 30 points (environ 2cm de moins)
            bottomMargin=72
        )

        # Préparer le contenu
        story = []
        try:
            self._ajouter_entete(story)
            self._ajouter_periode_location(story)
            self._ajouter_informations_bailleur(story)
            self._ajouter_informations_locataire(story)
            self._ajouter_montants(story)
            self._ajouter_texte_legal(story)
            self._ajouter_signature(story)
            self._ajouter_mentions_legales(story)
            
            # Générer le PDF
            doc.build(story)
            return chemin_complet
        
        except Exception as e:
            raise ValueError(f"Erreur lors de la génération du PDF : {str(e)}") 