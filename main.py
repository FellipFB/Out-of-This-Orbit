import requests
import pandas as pd
from io import StringIO
import tkinter as tk
from tkinter import messagebox, ttk

# Função para baixar dados da NASA Exoplanet Archive
def fetch_exoplanet_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,pl_rade,pl_dens,pl_eqt+from+ps&format=csv"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = pd.read_csv(StringIO(response.text))
        return data
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao baixar os dados: {e}")
        return None

# Função para calcular o ESI
def calculate_esi(row, weights):
    earth_radius = 1.0
    earth_density = 1.0
    earth_temp = 288.0
    
    planet_radius = row.get('pl_rade', None)
    planet_density = row.get('pl_dens', None)
    planet_temp = row.get('pl_eqt', None)
    
    required_params = ['pl_rade', 'pl_dens', 'pl_eqt']
    if any(row[param] is None or pd.isna(row[param]) for param in required_params):
        return None
    
    esi_radius = (1 - abs((planet_radius - earth_radius) / (planet_radius + earth_radius))) ** weights.get('radius', 0)
    esi_density = (1 - abs((planet_density - earth_density) / (planet_density + earth_density))) ** weights.get('density', 0)
    esi_temp = (1 - abs((planet_temp - earth_temp) / (planet_temp + earth_temp))) ** weights.get('temp', 0)
    
    esi = (esi_radius * esi_density * esi_temp) ** (1 / sum(weights.values()))
    return esi

def run_calculation():
    try:
        radius_weight = float(radius_entry.get())
        density_weight = float(density_entry.get())
        temp_weight = float(temp_entry.get())
        
        weights = {'radius': radius_weight, 'density': density_weight, 'temp': temp_weight}
        
        if any(w < 0 for w in weights.values()):
            messagebox.showerror("Erro", "Os pesos não podem ser negativos.")
            return
        
        status_label.config(text="Baixando dados...", fg="blue")
        root.update_idletasks()
        exoplanet_data = fetch_exoplanet_data()
        
        if exoplanet_data is not None:
            status_label.config(text="Calculando ESI...", fg="blue")
            root.update_idletasks()
            exoplanet_data['ESI'] = exoplanet_data.apply(calculate_esi, axis=1, weights=weights)
            exoplanet_data = exoplanet_data.dropna(subset=['ESI'])
            ranked_exoplanets = exoplanet_data.sort_values(by='ESI', ascending=False)
            
            if not ranked_exoplanets.empty:
                status_label.config(text="Top 10 exoplanetas encontrados!", fg="green")
                
                for row in table.get_children():
                    table.delete(row)
                
                for _, row in ranked_exoplanets[['pl_name', 'ESI']].head(10).iterrows():
                    table.insert("", "end", values=(row['pl_name'], round(row['ESI'], 5)))
            else:
                status_label.config(text="Nenhum exoplaneta válido encontrado.", fg="red")
        else:
            status_label.config(text="Erro ao baixar os dados.", fg="red")
    
    except ValueError:
        messagebox.showerror("Erro", "Digite valores numéricos válidos \npara os pesos.")

root = tk.Tk()
root.title("Cálculo de ESI de Exoplanetas")
root.geometry("700x500")

tk.Label(root, text="Defina os pesos para cada parâmetro (0 a 1):").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Raio:").grid(row=0, column=0)
radius_entry = tk.Entry(frame, width=5)
radius_entry.grid(row=0, column=1)
radius_entry.insert(0, "0")

tk.Label(frame, text="Densidade:").grid(row=1, column=0)
density_entry = tk.Entry(frame, width=5)
density_entry.grid(row=1, column=1)
density_entry.insert(0, "0")

tk.Label(frame, text="Temperatura:").grid(row=2, column=0)
temp_entry = tk.Entry(frame, width=5)
temp_entry.grid(row=2, column=1)
temp_entry.insert(0, "0")

tk.Button(root, text="Calcular ESI", command=run_calculation, bg="lightblue").pack(pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.pack()

table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("Nome", "ESI")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.heading("Nome", text="Nome do Exoplaneta")
table.heading("ESI", text="ESI")
table.pack()

root.mainloop()