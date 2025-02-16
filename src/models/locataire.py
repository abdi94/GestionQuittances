from datetime import date

class Locataire:
    def __init__(self, nom, prenom, adresse, code_postal, ville, 
                 date_debut_bail, montant_loyer, montant_charges):
        if montant_loyer < 0 or montant_charges < 0:
            raise ValueError("Les montants ne peuvent pas être négatifs")
            
        if date_debut_bail > date.today():
            raise ValueError("La date de début du bail ne peut pas être dans le futur")
            
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville
        self.date_debut_bail = date_debut_bail
        self.montant_loyer = montant_loyer
        self.montant_charges = montant_charges

    def loyer_total(self):
        return self.montant_loyer + self.montant_charges

    def adresse_complete(self):
        return f"{self.adresse}\n{self.code_postal} {self.ville}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}" 