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
        
        if data.empty:
            messagebox.showerror("Erro", "Nenhum dado foi retornado pela NASA.")
            return None
        
        return data
    except requests.exceptions.Timeout:
        messagebox.showerror("Erro", "Tempo limite excedido ao tentar baixar os dados.")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Erro", f"Erro ao conectar-se à API da NASA: {err}")
    except pd.errors.ParserError:
        messagebox.showerror("Erro", "Erro ao processar os dados. O formato pode ter mudado.")
    
    return None

# Função para calcular o ESI
def calculate_esi(row, weights):
    earth_values = {'radius': 1.0, 'density': 1.0, 'temp': 288.0}
    planet_values = {
        'radius': row.get('pl_rade'),
        'density': row.get('pl_dens'),
        'temp': row.get('pl_eqt')
    }
    
    if any(pd.isna(v) or v is None for v in planet_values.values()):
        return None  
    
    esi_components = []
    
    for key, weight in weights.items():
        if weight > 0 and planet_values[key] + earth_values[key] != 0:
            factor = 1 - abs((planet_values[key] - earth_values[key]) / (planet_values[key] + earth_values[key]))
            esi_components.append(factor ** weight)
    
    if not esi_components:
        return None

    return (sum(esi_components) / len(esi_components))  

# Função chamada ao pressionar o botão
def run_calculation():
    try:
        # Pegando os pesos informados na interface
        radius_weight = float(radius_entry.get())
        density_weight = float(density_entry.get())
        temp_weight = float(temp_entry.get())
        
        weights = {'radius': radius_weight, 'density': density_weight, 'temp': temp_weight}
        
        if any(w < 0 or w > 1 for w in weights.values()):
            messagebox.showerror("Erro", "Os pesos devem estar entre 0 e 1.")
            return

        if round(sum(weights.values()), 2) != 1.0:
            messagebox.showerror("Erro", "A soma dos pesos deve ser exatamente 1.")
            return
        
        # Baixando os dados
        status_label.config(text="Baixando dados...", fg="blue")
        root.update_idletasks()
        exoplanet_data = fetch_exoplanet_data()
        
        if exoplanet_data is not None:
            # Calculando o ESI
            status_label.config(text="Calculando ESI...", fg="blue")
            root.update_idletasks()
            exoplanet_data['ESI'] = exoplanet_data.apply(calculate_esi, axis=1, weights=weights)
            exoplanet_data = exoplanet_data.dropna(subset=['ESI'])
            ranked_exoplanets = exoplanet_data.sort_values(by='ESI', ascending=False)
            
            if not ranked_exoplanets.empty:
                status_label.config(text="Top 10 exoplanetas encontrados!", fg="green")
                
                # Limpando a tabela
                for row in table.get_children():
                    table.delete(row)
                
                # Inserindo os dados na tabela
                for _, row in ranked_exoplanets[['pl_name', 'ESI']].head(10).iterrows():
                    table.insert("", "end", values=(row['pl_name'], round(row['ESI'], 5)))
            else:
                status_label.config(text="Nenhum exoplaneta válido encontrado.", fg="red")
        else:
            status_label.config(text="Erro ao baixar os dados.", fg="red")
    
    except ValueError:
        messagebox.showerror("Erro", "Digite valores numéricos válidos para os pesos.")

root = tk.Tk()
root.title("Cálculo de ESI de Exoplanetas")
root.geometry("500x500")

tk.Label(root, text="Defina os pesos para cada parâmetro (soma deve ser 1):").pack(pady=10)
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Raio:").grid(row=0, column=0)
radius_entry = tk.Entry(frame, width=5)
radius_entry.grid(row=0, column=1)
radius_entry.insert(0, "0.33")  

tk.Label(frame, text="Densidade:").grid(row=1, column=0)
density_entry = tk.Entry(frame, width=5)
density_entry.grid(row=1, column=1)
density_entry.insert(0, "0.33")  

tk.Label(frame, text="Temperatura:").grid(row=2, column=0)
temp_entry = tk.Entry(frame, width=5)
temp_entry.grid(row=2, column=1)
temp_entry.insert(0, "0.34")  

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
