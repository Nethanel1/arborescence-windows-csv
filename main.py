import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import csv  # Importation du module csv


def get_file_size(file_path):
    """Retourne la taille du fichier."""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


def get_file_modification_date(file_path):
    """Retourne la date de modification du fichier."""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except OSError:
        return "Unknown"


def write_directory_structure(output_file, root_directory, include_sizes=False, include_dates=False,
                              file_extension=None):
    """Génère le fichier CSV contenant l'arborescence selon les options sélectionnées."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Path', 'File Name', 'File Size', 'Modification Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Écrire l'en-tête du CSV

        for root, dirs, files in os.walk(root_directory):
            # Filtrer les fichiers par extension si nécessaire
            if file_extension:
                files = [f for f in files if f.endswith(file_extension)]

            for name in files:
                file_path = os.path.join(root, name)
                file_size = get_file_size(file_path) if include_sizes else ''
                mod_date = get_file_modification_date(file_path) if include_dates else ''

                writer.writerow({
                    'File Path': root,
                    'File Name': name,
                    'File Size': file_size,
                    'Modification Date': mod_date
                })


def run():
    """Récupère les paramètres de l'interface et lance la génération de l'arborescence."""
    root_directory = filedialog.askdirectory(title="Choisissez un dossier")
    if not root_directory:
        return

    output_file = filedialog.asksaveasfilename(
        title="Enregistrez le fichier", defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
    )
    if not output_file:
        return

    include_sizes = size_var.get()
    include_dates = date_var.get()
    file_extension = ext_var.get()

    try:
        write_directory_structure(
            output_file, root_directory, include_sizes=include_sizes, include_dates=include_dates,
            file_extension=file_extension
        )
        messagebox.showinfo("Succès", f"Arborescence générée dans : {output_file}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


# Interface graphique
root = tk.Tk()
root.title("Explorateur d'Arborescence")

# Instructions
ttk.Label(root, text="Sélectionnez les informations à inclure :", font=("Arial", 12)).grid(
    row=0, column=0, columnspan=2, pady=10
)

# Options avec sélection par défaut
size_var = tk.BooleanVar(value=True)  # La taille des fichiers est sélectionnée par défaut
date_var = tk.BooleanVar(value=True)  # La date de modification est sélectionnée par défaut
ext_var = tk.StringVar(value="")  # Filtrage par extension, vide par défaut

# Cases à cocher
ttk.Checkbutton(root, text="Inclure la taille des fichiers", variable=size_var).grid(row=1, column=0, sticky="w",
                                                                                     padx=20)
ttk.Checkbutton(root, text="Inclure la date de modification", variable=date_var).grid(row=2, column=0, sticky="w",
                                                                                      padx=20)

# Filtrage par extension
ttk.Label(root, text="Filtrer par type de fichier (par exemple, .txt, .pdf) :").grid(row=3, column=0, sticky="w",
                                                                                     padx=20)
ttk.Entry(root, textvariable=ext_var).grid(row=4, column=0, sticky="w", padx=20, pady=5)

# Bouton pour lancer
ttk.Button(root, text="Générer l'arborescence", command=run).grid(row=5, column=0, columnspan=2, pady=20)

# Lancement de l'interface
root.mainloop()
