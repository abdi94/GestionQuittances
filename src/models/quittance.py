from datetime import date

class Quittance:
    MENTIONS_LEGALES = (
        "Pour valoir ce que de droit.\n"
        "Cette quittance annule tous les reçus qui auraient pu être établis précédemment "
        "pour la même période.\n"
        "La présente quittance est à conserver pendant 3 ans."
    )

    def __init__(self, bailleur, locataire, periode_debut, periode_fin, numero=None):
        if periode_debut > periode_fin:
            raise ValueError("La période de début doit être antérieure à la période de fin")
            
        if periode_debut < locataire.date_debut_bail:
            raise ValueError("La période ne peut pas commencer avant le début du bail")
            
        self.bailleur = bailleur
        self.locataire = locataire
        self.periode_debut = periode_debut
        self.periode_fin = periode_fin
        self.date_emission = date.today()
        self.numero = numero or self._generer_numero()

    def _generer_numero(self):
        return f"Q{self.periode_debut.strftime('%Y%m')}"

    def montant_total(self):
        return self.locataire.loyer_total()

    def periode_str(self):
        mois = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        debut = f"{self.periode_debut.day:02d} {mois[self.periode_debut.month - 1]} {self.periode_debut.year}"
        fin = f"{self.periode_fin.day:02d} {mois[self.periode_fin.month - 1]} {self.periode_fin.year}"
        return f"{debut} au {fin}"

    def mentions_legales(self):
        return self.MENTIONS_LEGALES

    def texte_legal(self):
        return (
            "Je soussigné(e) {}, propriétaire du logement désigné ci-dessus, "
            "déclare avoir reçu la somme de {:.2f} euros, au titre du paiement "
            "du loyer et des charges pour la période de location indiquée dans la "
            "présente quittance.\n\n"
            "{}"
        ).format(self.bailleur.nom, self.montant_total(), self.mentions_legales()) 