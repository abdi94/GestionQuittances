from datetime import date

class Quittance:
    def __init__(self, bailleur, locataire, periode_debut, periode_fin):
        if periode_debut > periode_fin:
            raise ValueError("La période de début doit être antérieure à la période de fin")
            
        if periode_debut < locataire.date_debut_bail:
            raise ValueError("La période ne peut pas commencer avant le début du bail")
            
        self.bailleur = bailleur
        self.locataire = locataire
        self.periode_debut = periode_debut
        self.periode_fin = periode_fin
        self.date_emission = date.today()

    def montant_total(self):
        return self.locataire.loyer_total()

    def periode_str(self):
        debut = self.periode_debut.strftime("%d %B %Y")
        fin = self.periode_fin.strftime("%d %B %Y")
        return f"{debut} au {fin}" 