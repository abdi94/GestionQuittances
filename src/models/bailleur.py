class Bailleur:
    def __init__(self, nom, adresse, code_postal, ville):
        self.nom = nom
        self.adresse = adresse
        self.code_postal = code_postal
        self.ville = ville

    def adresse_complete(self):
        return f"{self.adresse}\n{self.code_postal} {self.ville}"

    def modifier_informations(self, **kwargs):
        for cle, valeur in kwargs.items():
            if hasattr(self, cle):
                setattr(self, cle, valeur) 