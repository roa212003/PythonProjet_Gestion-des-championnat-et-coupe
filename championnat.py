import tkinter as tk
from tkinter import messagebox
from equipe import Equipe
import random

class Championnat:
    def __init__(self, equipes):
        # Chuyển chuỗi thành đối tượng Equipe nếu cần
        if isinstance(equipes[0], str):  # Nếu danh sách chứa chuỗi
            self.equipes = [Equipe(nom) for nom in equipes]
        else:  # Nếu đã là đối tượng Equipe
            self.equipes = equipes
        self.rencontres = self.generer_rencontres()


    def generer_rencontres(self):
        rencontres = [(self.equipes[i], self.equipes[j]) for i in range(len(self.equipes)) for j in
                      range(i + 1, len(self.equipes))]
        random.shuffle(rencontres)
        return rencontres

    def maj_statistiques_match(self, equipe1, equipe2, score1, score2):
        if score1 > score2:
            equipe1.maj_statistiques("gagne", score1, score2)
            equipe2.maj_statistiques("perdu", score2, score1)
        elif score1 < score2:
            equipe1.maj_statistiques("perdu", score1, score2)
            equipe2.maj_statistiques("gagne", score2, score1)
        else:
            equipe1.maj_statistiques("nul", score1, score2)
            equipe2.maj_statistiques("nul", score2, score1)

    def calculate_standings(self):
        # Tính toán bảng xếp hạng sau vòng tròn
        self.standings = sorted(self.equipes, key=lambda equipe: equipe.points, reverse=True)

    def get_top_teams(self, num_teams):
        # Đảm bảo bảng xếp hạng được cập nhật trước
        self.calculate_standings()
        return self.standings[:num_teams]


class Application(tk.Frame):
    def __init__(self, master, callback=None):
        super().__init__(master)
        self.master = master
        self.callback = callback
        self.pack()
        self.show_team_input()


    def show_team_input(self):
        # Giao diện nhập số lượng và tên đội
        self.frame_team_input = tk.Frame(self)
        self.frame_team_input.pack(pady=20)

        tk.Label(self.frame_team_input, text="Nombre d'équipes:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_team_count = tk.Entry(self.frame_team_input)
        self.entry_team_count.grid(row=0, column=1, padx=5)

        tk.Button(self.frame_team_input, text="OK", command=self.create_team_entries).grid(row=0, column=2, padx=5)

    def create_team_entries(self):
        try:
            self.num_equipes = int(self.entry_team_count.get())
            if self.num_equipes <= 1:
                raise ValueError("Le nombre d'équipes doit être supérieur à 1.")

            # Giao diện nhập tên các đội
            self.frame_team_input.pack_forget()
            self.frame_team_names = tk.Frame(self)
            self.frame_team_names.pack(pady=20)

            tk.Label(self.frame_team_names, text="Entrez les noms des équipes:").pack()
            self.team_entries = []
            for i in range(self.num_equipes):
                tk.Label(self.frame_team_names, text=f"Équipe {i + 1}:").pack()
                entry = tk.Entry(self.frame_team_names)
                entry.pack(padx=5, pady=2)
                self.team_entries.append(entry)

            tk.Button(self.frame_team_names, text="Confirmer", command=self.submit_teams).pack(pady=10)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def submit_teams(self):
        self.equipes = [Equipe(entry.get()) for entry in self.team_entries if entry.get()]
        if len(self.equipes) != self.num_equipes:
            messagebox.showerror("Erreur", "Veuillez entrer le nom de toutes les équipes.")
        else:
            self.frame_team_names.pack_forget()
            self.championnat = Championnat(self.equipes)  # Truyền danh sách đối tượng Equipe
            self.show_score_input()

    def show_score_input(self):
        # Giao diện nhập điểm với cuộn
        canvas = tk.Canvas(self, width=400, height=300)
        scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        # Thêm các trận đấu vào giao diện cuộn
        for idx, (equipe1, equipe2) in enumerate(self.championnat.rencontres):
            tk.Label(scrollable_frame, text=f"{equipe1.nom} vs {equipe2.nom}").grid(row=idx, column=0, padx=5, pady=5)
            entry_score1 = tk.Entry(scrollable_frame, width=5)
            entry_score2 = tk.Entry(scrollable_frame, width=5)
            entry_score1.grid(row=idx, column=1, padx=5)
            tk.Label(scrollable_frame, text="-").grid(row=idx, column=2)
            entry_score2.grid(row=idx, column=3, padx=5)
            button_submit = tk.Button(scrollable_frame, text="Submit",
                                      command=lambda e1=equipe1, e2=equipe2, s1=entry_score1,
                                                     s2=entry_score2: self.submit_score(e1, e2, s1, s2))
            button_submit.grid(row=idx, column=4, padx=5)

        canvas.grid(row=0, column=0, sticky="news")
        scroll_y.grid(row=0, column=1, sticky="ns")

        tk.Button(self, text="Afficher Classement", command=self.afficher_classement).grid(row=1, column=0,
                                                                                           columnspan=2, pady=10)

    def submit_score(self, equipe1, equipe2, entry_score1, entry_score2):
        try:
            score1 = int(entry_score1.get())
            score2 = int(entry_score2.get())
            self.championnat.maj_statistiques_match(equipe1, equipe2, score1, score2)
            entry_score1.config(state="disabled")
            entry_score2.config(state="disabled")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des scores valides.")

    def afficher_classement(self):
        for equipe in self.equipes:
            if not isinstance(equipe, Equipe):
                raise TypeError(f"L'équipe {equipe} n'est pas une instance de la classe Equipe.")

        equipes_triees = sorted(self.equipes, key=lambda e: (e.points, e.diffbut), reverse=True)
        classement = "Classement:\n"
        for i, equipe in enumerate(equipes_triees, 1):
            classement += f"{i}. {equipe}\n"
        messagebox.showinfo("Classement", classement)

    def run(self):
        """Chạy ứng dụng mà không gọi mainloop trực tiếp"""
        self.show_team_input()  # Hiển thị giao diện nhập đội

    def return_to_main_menu(self):
        """Quay lại menu chính."""
        if self.callback:
            self.master.destroy()  # Hủy cửa sổ hiện tại
            self.callback()  # Gọi menu chính


def main_championnat(root, callback=None):
    app = Application(root, callback)
    app.mainloop()


