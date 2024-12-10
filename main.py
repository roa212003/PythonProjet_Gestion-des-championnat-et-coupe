import tkinter as tk
from tkinter import ttk
import championnat
import coupe
import csv

def main():
    def show_main_menu():
        """Hiển thị menu chính."""
        for widget in root.winfo_children():
            widget.destroy()

        label_tournoi = tk.Label(root, text="Veuillez choisir les phases du tournoi:")
        label_tournoi.pack(pady=10)

        formats = [
            "Tournoi à la ronde (Round Robin)",
            "Tournoi à la ronde (Round Robin) + Éliminatoires",
            "Éliminatoires",
        ]
        combo = ttk.Combobox(root, values=formats, width=30)
        combo.pack(pady=10)

        button_confirm = tk.Button(
            root, text="OK",
            command=lambda: run_selected_format(combo.get())
        )
        button_confirm.pack(pady=10)

    def run_selected_format(selected_format):
        """Xử lý lựa chọn giải đấu."""
        for widget in root.winfo_children():
            widget.destroy()

        if selected_format == "Tournoi à la ronde (Round Robin)":
            championnat.main_championnat(root, show_main_menu)
        elif selected_format == "Tournoi à la ronde (Round Robin) + Éliminatoires":
            championnat_instance = championnat.main_championnat(root)
            num_top_teams = 4  # Top 4 teams advance to playoffs
            top_teams = championnat_instance.get_top_teams(num_top_teams)
            coupe.main_coupe_with_teams(root, top_teams, show_main_menu)
        elif selected_format == "Éliminatoires":
            coupe.main_coupe(root, show_main_menu)

    root = tk.Tk()
    root.title("Gestion des championnats et coupes")
    show_main_menu()
    root.mainloop()

def sauvegarder_classement_en_csv(championnat):
    """Lưu bảng xếp hạng vào file CSV."""
    with open("classement.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Équipe", "Joués", "Gagnés", "Nuls", "Perdus",
            "Buts Pour", "Buts Contre", "Différence de but", "Points"
        ])
        for equipe in championnat.equipes:
            writer.writerow([
                equipe.nom, equipe.joues, equipe.gagnes, equipe.nuls,
                equipe.perdus, equipe.butspours, equipe.butscontres,
                equipe.diffbut, equipe.points
            ])

if __name__ == "__main__":
    main()
