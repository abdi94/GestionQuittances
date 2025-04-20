
"""
GUI pour la gestion de quittances de loyer.
- Tkinter
- Trois onglets: ajouter‑bailleur, ajouter‑locataire, générer‑quittance
- Un bouton «Exécuter» par onglet, qui affiche les valeurs saisies et retourne le resultat
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import cli as cl
import io
import contextlib
import traceback
import sys



class LoyerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Gestion de quittances de loyer")
        self.geometry("820x520")
        self.resizable(False, False)

        self._build_widgets()

    # ------------------------------------------------------------------ #
    #   CONSTRUCTION DE L’IU
    # ------------------------------------------------------------------ #
    def _build_widgets(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- onglet 1 : ajouter-bailleur --------------------------------
        onglet_bailleur = self._create_form(
            notebook,
            "ajouter‑bailleur",
            fields=("nom", "adresse", "code_postal", "ville"),
            callback=self._exec_ajouter_bailleur,
        )
        notebook.add(onglet_bailleur, text="ajouter‑bailleur")

        # --- onglet 2 : ajouter-locataire -------------------------------
        onglet_locataire = self._create_form(
            notebook,
            "ajouter‑locataire",
            fields=(
                "nom",
                "prenom",
                "adresse",
                "code_postal",
                "ville",
                "date_debut",
                "loyer",
                "charges",
            ),
            callback=self._exec_ajouter_locataire,
        )
        notebook.add(onglet_locataire, text="ajouter‑locataire")

        # --- onglet 3 : generer-quittance -------------------------------
        onglet_quittance = self._create_form(
            notebook,
            "generer‑quittance",
            fields=("bailleur_id", "locataire_id", "mois", "annee"),
            callback=self._exec_generer_quittance,
        )
        notebook.add(onglet_quittance, text="generer‑quittance")

        # --- zone de log -------------------------------------------------
        self.log = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.log.pack(fill="both", padx=10, pady=(0, 10))

    # ------------------------------------------------------------------ #
    #   FABRICATION D’UN FORMULAIRE RÉUTILISABLE
    # ------------------------------------------------------------------ #
    def _create_form(
        self,
        parent: ttk.Notebook,
        title: str,
        fields: tuple[str, ...],
        callback,
    ) -> ttk.Frame:
        frame = ttk.Labelframe(parent, text=title, padding=10)
        entries: dict[str, tk.Entry] = {}

        for idx, name in enumerate(fields):
            ttk.Label(frame, text=name).grid(row=idx, column=0, sticky="w", pady=2)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=idx, column=1, sticky="we", pady=2)
            entries[name] = entry

        # Bouton Exécuter
        btn = ttk.Button(frame, text="Exécuter", command=lambda e=entries: callback(e))
        btn.grid(row=len(fields), column=0, columnspan=2, pady=8)

        frame.columnconfigure(1, weight=1)
        return frame

    # ------------------------------------------------------------------ #
    #   CALLBACKS (exemples : affiche simplement les valeurs)
    # ------------------------------------------------------------------ #
    def _exec_ajouter_bailleur(self, entries: dict[str, tk.Entry]) -> None:
        data = {k: v.get() for k, v in entries.items()}
        cl.ajouter_bailleur(data.get('nom'), data.get('adresse'), data.get('code_postal'), data.get('ville'))
        self._log(f"[ajouter_bailleur] {data}")

    def _exec_ajouter_locataire(self, entries: dict[str, tk.Entry]) -> None:
        data = {k: v.get() for k, v in entries.items()}
        cl.ajouter_locataire(data.get('nom'),data.get('prenom'),data.get('adresse'),data.get('code_postal'),data.get('ville'),data.get('date_debut'),data.get('loyer'),data.get('charges'))
        self._log(f"[ajouter_locataire] {data}")

    def _exec_generer_quittance(self, entries: dict[str, tk.Entry]) -> None:
        data = {k: v.get() for k, v in entries.items()}
        mois = {
            "janvier": 1, "février": 2, "mars": 3, "avril": 4,
            "mai": 5, "juin": 6, "juillet": 7, "août": 8,
            "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12,
        }
        cl.generer_quittance(int(data.get('bailleur_id')),int(data.get('locataire_id')),mois[data.get('mois').lower()],int(data.get('annee')))
        self._log(f"[generer_quittance] {data}")

    # ------------------------------------------------------------------ #
    #   UTILITAIRE DE LOG
    # ------------------------------------------------------------------ #
    def _log(self, message: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", message + "\n")
        self.log.configure(state="disabled")
        self.log.see("end")




if __name__ == "__main__":
    LoyerGUI().mainloop()
