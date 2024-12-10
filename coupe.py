import tkinter as tk
from tkinter import messagebox
from equipe import Equipe
import random

# Lớp CoupeEliminatoire
class CoupeEliminatoire:
    def __init__(self, equipes):
        self.equipes = [Equipe(nom) for nom in equipes]
        self.rounds = []
        self.winners = []
        self.generer_rencontres()
    def generer_rencontres(self):
        random.shuffle(self.equipes)
        self.rounds.append([(self.equipes[i],self.equipes[i+1]) for i in range(0,len(self.equipes),2)])
    def maj_statistiques_match(self, equipe1, equipe2, score1, score2):

        # Xác định đội thắng
        if score1 > score2:
            self.winners.append(equipe1)
            equipe1.maj_statistiques("gagne", score1, score2)
            equipe2.maj_statistiques("perdu", score2, score1)
        else:
            self.winners.append(equipe2)
            equipe2.maj_statistiques("gagne", score2, score1)
            equipe1.maj_statistiques("perdu", score1, score2)

    def creer_prochaine_tour(self):
        self.rounds.append([(self.winners[i], self.winners[i + 1]) for i in range(0, len(self.winners), 2)])
        self.equipes = self.winners[:]
        self.winners = []

# Hàm mới: Khởi động loại trực tiếp từ danh sách đội
def main_coupe_with_teams(root, top_teams):
    coupe_instance = CoupeEliminatoire(top_teams)
    app = Application(coupe_instance)
    app.mainloop()

# Chỉnh sửa Application để nhận CoupeEliminatoire
class Application(tk.Tk):
    def __init__(self, coupe_instance=None):
        super().__init__()
        self.title("Gestion de Coupe Eliminatoire")
        if coupe_instance:
            self.coupes = coupe_instance
            self.show_score_input()
        else:
            self.equipes = []
            self.show_team_input()

    def show_team_input(self):
        self.frame_team_input = tk.Frame(self)
        self.frame_team_input.pack(pady=20)
        tk.Label(self.frame_team_input, text="Nombre d'equipes: ").grid(row=0, column=0, padx=5, pady=5)
        self.entry_team_count = tk.Entry(self.frame_team_input)
        self.entry_team_count.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.frame_team_input, text = "OK", command = self.create_team_entries).grid(row=0, column=2, padx=5, pady=5)
    def create_team_entries(self):
        try:
            self.num_equipe = int(self.entry_team_count.get())
            if (self.num_equipe<=1) or (self.num_equipe&self.num_equipe-1!=0):
                raise ValueError("Le nombre d'équipes doit être une puissance de 2 supérieure à 1.")

            self.frame_team_input.pack_forget()
            self.frame_team_names = tk.Frame(self)
            self.frame_team_names.pack(pady=5)

            tk.Label(self.frame_team_names,text = "Entrez les noms des équipes").pack()
            self.team_entries = []
            for i in range(self.num_equipe):
                tk.Label(self.frame_team_names, text=f"Équipe {i}:").pack()
                entry = tk.Entry(self.frame_team_names)
                entry.pack()
                self.team_entries.append(entry)

            tk.Button(self.frame_team_names, text = "Confirmer", command = self.csubmit_teams).pack(pady=10)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def csubmit_teams(self):
        self.equipes = [entry.get() for entry in self.team_entries if entry.get()]
        if len(self.equipes)!= self.num_equipe:
            messagebox.showerror("Erreur","Veuillez entrer le nom de toutes les équipes.")
        else:
            self.frame_team_names.pack_forget()
            self.coupes = CoupeEliminatoire(self.equipes)
            self.show_score_input()
    def show_score_input(self):
        self.round_frame = tk.Frame(self)
        self.round_frame.pack(pady=10)

        self.current_round = 0
        self.display_round()
    def display_round(self):
        round_matches = self.coupes.rounds[self.current_round]
        self.scores_submitted = [False] * len(round_matches)
        for idx, (equipe1,equipe2) in enumerate(round_matches):
            tk.Label(self.round_frame, text = f"{equipe1.nom} vs {equipe2.nom}").grid(row = idx, column=0, padx=5, pady=5)
            entry_score1 = tk.Entry(self.round_frame, width=5)
            entry_score2 = tk.Entry(self.round_frame, width=5)
            entry_score1.grid(row=idx, column=1, padx=5)
            tk.Label(self.round_frame, text="-").grid(row=idx, column=2)
            entry_score2.grid(row=idx, column=3, padx=5)
            button_submit = tk.Button(self.round_frame, text="Submit",
                                      command=lambda idx = idx, e1=equipe1, e2=equipe2, s1=entry_score1,
                                                     s2=entry_score2: self.submit_score(idx, e1, e2, s1, s2))
            button_submit.grid(row=idx, column=4, padx=5)

    def submit_score(self, match_index, equipe1, equipe2, entry_score1, entry_score2):
        try:
            score1 = int(entry_score1.get())
            score2 = int(entry_score2.get())
            self.coupes.maj_statistiques_match(equipe1, equipe2, score1, score2)
            entry_score1.config(state="disabled")
            entry_score2.config(state="disabled")
            self.scores_submitted[match_index] = True

            # Check if all scores for the current round are submitted
            if all(self.scores_submitted):
                if len(self.coupes.winners) > 1:
                    self.coupes.creer_prochaine_tour()
                    self.next_round()
                else:
                    self.show_winner()
        except ValueError:
            messagebox.showerror("Error", "Veuillez entrer des scores valides.")

    def next_round(self):
        self.current_round += 1
        if self.current_round < len(self.coupes.rounds):
            for widget in self.round_frame.winfo_children():
                widget.destroy()
            self.display_round()
        else:
            self.show_winner()

    def show_winner(self):
        if len(self.coupes.winners) == 1:
            winner = self.coupes.winners[0]
            messagebox.showinfo("Gagnant", f"L'équipe gagnante est {winner.nom}!")
        else:
            messagebox.showerror("Erreur", "Impossible de déterminer le gagnant.")


# Hàm main khởi tạo ứng dụng
def main_coupe(root):
    app = Application()
    app.mainloop()