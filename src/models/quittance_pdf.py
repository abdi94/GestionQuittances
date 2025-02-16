from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
import locale

class QuittancePDF:
    def __init__(self, quittance):
        self.quittance = quittance
        self.styles = getSampleStyleSheet()
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
            fontSize=16,
            alignment=1,  # Centre
            spaceAfter=30
        ))

        self.styles.add(ParagraphStyle(
            'NormalCustom',
            parent=normal_style,
            fontSize=11,
            spaceAfter=12
        ))

        self.styles.add(ParagraphStyle(
            'Signature',
            parent=normal_style,
            fontSize=11,
            alignment=2  # Droite
        ))

        self.styles.add(ParagraphStyle(
            'MentionsLegales',
            parent=normal_style,
            fontSize=9,
            spaceAfter=12,
            textColor=colors.gray
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
        story.append(Spacer(1, 20))

    def _ajouter_numero_quittance(self, story):
        story.append(Paragraph(f"Quittance N° {self.quittance.numero}", 
                             self.styles["NormalCustom"]))
        story.append(Spacer(1, 20))

    def _ajouter_periode_location(self, story):
        debut = self._formater_date(self.quittance.periode_debut)
        fin = self._formater_date(self.quittance.periode_fin)
        story.append(Paragraph(
            f"Pour la période du {debut} au {fin}",
            self.styles["NormalCustom"]
        ))
        story.append(Spacer(1, 20))

    def _ajouter_informations_bailleur(self, story):
        story.append(Paragraph("BAILLEUR :", self.styles["NormalCustom"]))
        story.append(Paragraph(self.quittance.bailleur.nom, self.styles["NormalCustom"]))
        story.append(Paragraph(self.quittance.bailleur.adresse_complete(), self.styles["NormalCustom"]))
        story.append(Spacer(1, 20))

    def _ajouter_informations_locataire(self, story):
        story.append(Paragraph("LOCATAIRE :", self.styles["NormalCustom"]))
        story.append(Paragraph(self.quittance.locataire.nom_complet(), self.styles["NormalCustom"]))
        story.append(Paragraph(self.quittance.locataire.adresse_complete(), self.styles["NormalCustom"]))
        story.append(Spacer(1, 20))

    def _ajouter_montants(self, story):
        data = [
            ["Loyer", f"{self.quittance.locataire.montant_loyer:.2f} €"],
            ["Charges", f"{self.quittance.locataire.montant_charges:.2f} €"],
            ["TOTAL", f"{self.quittance.montant_total():.2f} €"]
        ]
        table = Table(data, colWidths=[10*cm, 5*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        story.append(table)
        story.append(Spacer(1, 30))

    def _ajouter_texte_legal(self, story):
        story.append(Paragraph(self.quittance.texte_legal(), 
                             self.styles["NormalCustom"]))
        story.append(Spacer(1, 30))

    def _ajouter_signature(self, story):
        date_str = self.quittance.date_emission.strftime("%d %B %Y")
        story.append(Paragraph(f"Fait à {self.quittance.bailleur.ville}, le {date_str}", 
                             self.styles["Signature"]))
        story.append(Spacer(1, 40))
        story.append(Paragraph("Signature du bailleur", self.styles["Signature"]))

    def _ajouter_mentions_legales(self, story):
        story.append(Paragraph(self.quittance.mentions_legales(), 
                             self.styles["MentionsLegales"]))

    def generer(self, chemin_fichier):
        doc = SimpleDocTemplate(
            chemin_fichier,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        story = []
        self._ajouter_entete(story)
        self._ajouter_numero_quittance(story)
        self._ajouter_periode_location(story)
        self._ajouter_informations_bailleur(story)
        self._ajouter_informations_locataire(story)
        self._ajouter_montants(story)
        self._ajouter_texte_legal(story)
        self._ajouter_signature(story)
        self._ajouter_mentions_legales(story)
        
        doc.build(story) 