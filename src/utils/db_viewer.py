from src.models.database import Database

def afficher_contenu_db():
    db = Database()
    
    print("\n=== BAILLEURS ===")
    bailleurs = db.lister_bailleurs()
    if not bailleurs:
        print("Aucun bailleur enregistré")
    else:
        for b in bailleurs:
            print(f"ID: {b[0]}, Nom: {b[1]}, Adresse: {b[2]}, CP: {b[3]}, Ville: {b[4]}")
    
    print("\n=== LOCATAIRES ===")
    locataires = db.lister_locataires()
    if not locataires:
        print("Aucun locataire enregistré")
    else:
        for l in locataires:
            print(f"ID: {l[0]}, Nom: {l[1]}, Prénom: {l[2]}, Adresse: {l[3]}, CP: {l[4]}, Ville: {l[5]}")
            print(f"  Début bail: {l[6]}, Loyer: {l[7]}€, Charges: {l[8]}€")
    
    print("\n=== QUITTANCES ===")
    quittances = db.lister_quittances()
    if not quittances:
        print("Aucune quittance enregistrée")
    else:
        for q in quittances:
            print(f"ID: {q[0]}, N°: {q[1]}, Bailleur: {q[7]}, Locataire: {q[8]} {q[9]}")
            print(f"  Période: du {q[4]} au {q[5]}, Émise le: {q[6]}")

def vider_base():
    db = Database()
    db.vider_tables()
    print("Base de données vidée avec succès")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--vider':
        vider_base()
    else:
        afficher_contenu_db() 