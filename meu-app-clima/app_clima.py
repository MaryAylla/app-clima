import tkinter as tk
from tkinter import messagebox
import requests
import os
from PIL import Image, ImageTk
import io
import json

API_KEY = "74c585d34fe876914327f6125afc7ecc" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


current_weather_icon = None
search_history = []
MAX_HISTORY_SIZE = 5
HISTORY_FILE = "search_history.json"

def get_weather_data(city):
    """
    Busca dados do clima para uma cidade específica usando a API da OpenWeatherMap.

    Args:
        city (str): O nome da cidade para a qual buscar os dados do clima.

    Returns:
        dict or None: Um dicionário contendo os dados do clima (temperatura, descrição, etc.)
                      se a requisição for bem-sucedida, caso contrário, None.
    """

    unit_param = current_unit.get() 
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit_param,
        "lang": "pt_br"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get("cod") == "404":
            return None
        
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather_info

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            messagebox.showerror("Erro de API", "Chave de API inválida ou não ativada. Verifique sua chave!")
        elif response.status_code == 404:
            pass 
        else:
            messagebox.showerror("Erro de Requisição", f"Erro HTTP: {http_err} - Código: {response.status_code}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor. Verifique sua conexão com a internet: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        messagebox.showerror("Erro de Tempo Limite", f"A requisição excedeu o tempo limite: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        messagebox.showerror("Erro de Requisição", f"Ocorreu um erro inesperado na requisição: {req_err}")
        return None
    except KeyError as key_err:
        messagebox.showerror("Erro de Dados", f"Estrutura de dados da API inesperada. Chave ausente: {key_err}")
        return None
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado: {e}")
        return None

def load_and_display_icon(icon_code):
    global current_weather_icon

    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    try:
        icon_response = requests.get(icon_url)
        icon_response.raise_for_status()

        image_data = io.BytesIO(icon_response.content)
        pil_image = Image.open(image_data)

        pil_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)

        current_weather_icon = ImageTk.PhotoImage(pil_image)

        icon_label.config(image=current_weather_icon)
        icon_label.image = current_weather_icon 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar ícone: {e}")
        icon_label.config(image='')
        icon_label.image = None
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        icon_label.config(image='')
        icon_label.image = None


def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for city in search_history:
        history_listbox.insert(tk.END, city)


def on_history_select(event):
    selected_indices = history_listbox.curselection()
    if selected_indices:
        index = selected_indices[0]
        selected_city = history_listbox.get(index)
        city_entry.delete(0, tk.END)
        city_entry.insert(0, selected_city)
        city_entry.config(fg=COLOR_TEXT_PRIMARY)
        update_weather_display()


def on_entry_focus_in(event):
    if city_entry.get() == "Digite o nome da cidade...":
        city_entry.delete(0, tk.END)
        city_entry.config(fg=COLOR_TEXT_PRIMARY)

def on_entry_focus_out(event):
    if not city_entry.get():
        city_entry.insert(0, "Digite o nome da cidade...")
        city_entry.config(fg=COLOR_TEXT_SECONDARY)


def update_weather_display():
    """
    Obtém a cidade do campo de entrada, busca os dados do clima e atualiza a interface gráfica.
    """
    global search_history

    city = city_entry.get().strip()
    if not city or city == "Digite o nome da cidade...": 
        messagebox.showwarning("Entrada Inválida", "Por favor, digite o nome de uma cidade.")
        return

    weather_data = get_weather_data(city)

    if weather_data:
        temp_symbol = "°C" if current_unit.get() == "metric" else "°F"

        city_label.config(text=f"{weather_data['city']}, {weather_data['country']}")
        temperature_label.config(text=f"{weather_data['temperature']:.1f}{temp_symbol}")
        description_label.config(text=weather_data['description'])
        
        load_and_display_icon(weather_data['icon'])

        feels_like_label.config(text=f"Sensação: {weather_data['feels_like']:.1f}{temp_symbol}")
        humidity_label.config(text=f"Umidade: {weather_data['humidity']}%")
        pressure_label.config(text=f"Pressão: {weather_data['pressure']} hPa")
        wind_speed_label.config(text=f"Vento: {weather_data['wind_speed']:.1f} m/s")

        city_normalized = weather_data['city'].capitalize()
        if city_normalized in search_history:
            search_history.remove(city_normalized)
        search_history.insert(0, city_normalized)

        if len(search_history) > MAX_HISTORY_SIZE:
            search_history = search_history[:MAX_HISTORY_SIZE]

        update_history_listbox()
        save_history()
    else:
        city_label.config(text="Cidade: ---")
        temperature_label.config(text="--°C")
        description_label.config(text="Condição: ---")
        icon_label.config(image='') 
        icon_label.image = None 
        feels_like_label.config(text="Sensação: ---")
        humidity_label.config(text="Umidade: ---")
        pressure_label.config(text="Pressão: ---")
        wind_speed_label.config(text="Vento: ---")

        if "Erro" not in city_label.cget("text"):
             messagebox.showerror("Erro", "Não foi possível obter os dados do clima para esta cidade.")


def save_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(search_history, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Erro ao salvar histórico: {e}")


def load_history():
    global search_history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                loaded_history = json.load(f)
                if isinstance(loaded_history, list):
                    search_history = loaded_history[:MAX_HISTORY_SIZE]
                else:
                    search_history = []
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar histórico: {e}")
            search_history = []
    else:
        search_history = []
    update_history_listbox()

def on_closing():
    save_history()
    root.destroy()



root = tk.Tk()
root.title("App de Clima")
root.state('zoomed') 

current_unit = tk.StringVar(value="metric") 


COLOR_BG_LIGHT = "#E0F7FA"       
COLOR_BG_CARD = "#FFFFFF"       
COLOR_SHADOW = "#B0BEC5"        
COLOR_TEXT_PRIMARY = "#263238"   
COLOR_TEXT_SECONDARY = "#78909C" 
COLOR_ACCENT_PRIMARY = "#00BCD4" 
COLOR_ACCENT_HOVER = "#00838F"   


FONT_FAMILY = "Verdana"
FONT_TITLE = (FONT_FAMILY, 28, "bold")      
FONT_SUBTITLE = (FONT_FAMILY, 16, "bold")   
FONT_NORMAL = (FONT_FAMILY, 12)             
FONT_TEMP = (FONT_FAMILY, 56, "bold")       
FONT_DESC = (FONT_FAMILY, 18)               
FONT_DETAILS = (FONT_FAMILY, 12)            
FONT_HISTORY = (FONT_FAMILY, 11)            

root.configure(bg=COLOR_BG_LIGHT)


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


main_frame = tk.Frame(root, bg=COLOR_BG_LIGHT, padx=25, pady=25)
main_frame.grid(row=0, column=0, sticky="nsew")


main_frame.grid_rowconfigure(0, weight=0) 
main_frame.grid_rowconfigure(1, weight=0) 
main_frame.grid_rowconfigure(2, weight=1) 
main_frame.grid_rowconfigure(3, weight=1) 
main_frame.grid_columnconfigure(0, weight=1) 


app_title = tk.Label(main_frame, text="App de Clima", font=FONT_TITLE, bg=COLOR_BG_LIGHT, fg=COLOR_TEXT_PRIMARY)
app_title.grid(row=0, column=0, pady=(20, 30))

def create_shadow_card(parent_frame, grid_row, grid_column, pady_val):
    shadow_container = tk.Frame(parent_frame, bg=COLOR_SHADOW)
    shadow_container.grid(row=grid_row, column=grid_column, pady=pady_val, sticky="ew", padx=10) 

    content_frame = tk.Frame(shadow_container, bg=COLOR_BG_CARD, padx=20, pady=20, bd=1, relief="flat", highlightbackground=COLOR_SHADOW, highlightthickness=1)
    content_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    content_frame.grid_columnconfigure(0, weight=1)
    return content_frame

search_card_frame = create_shadow_card(main_frame, 1, 0, (0, 25))

city_entry = tk.Entry(search_card_frame, font=FONT_NORMAL, bd=0, relief="flat", bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY, insertbackground=COLOR_TEXT_PRIMARY)
city_entry.insert(0, "Digite o nome da cidade...") 
city_entry.bind("<FocusIn>", on_entry_focus_in)
city_entry.bind("<FocusOut>", on_entry_focus_out)
city_entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew") 

search_button = tk.Button(search_card_frame, text="Buscar", command=update_weather_display,
                          font=FONT_NORMAL, bg=COLOR_ACCENT_PRIMARY, fg="white",
                          activebackground=COLOR_ACCENT_HOVER, activeforeground="white",
                          bd=0, relief="flat", padx=15, pady=8, cursor="hand2")
search_button.grid(row=0, column=1, pady=5)

unit_selection_frame = tk.Frame(search_card_frame, bg=COLOR_BG_CARD)
unit_selection_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

unit_label = tk.Label(unit_selection_frame, text="Unidade:", font=FONT_NORMAL, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY)
unit_label.pack(side=tk.LEFT, padx=(0, 10))

celsius_radio = tk.Radiobutton(unit_selection_frame, text="Celsius (°C)", variable=current_unit, value="metric",
                               font=FONT_NORMAL, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY,
                               selectcolor=COLOR_BG_CARD, activebackground=COLOR_BG_CARD,
                               command=lambda: update_weather_display() if city_entry.get() != "Digite o nome da cidade..." and city_entry.get() else None)
celsius_radio.pack(side=tk.LEFT, padx=5)

fahrenheit_radio = tk.Radiobutton(unit_selection_frame, text="Fahrenheit (°F)", variable=current_unit, value="imperial",
                                  font=FONT_NORMAL, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY,
                                  selectcolor=COLOR_BG_CARD, activebackground=COLOR_BG_CARD,
                                  command=lambda: update_weather_display() if city_entry.get() != "Digite o nome da cidade..." and city_entry.get() else None)
fahrenheit_radio.pack(side=tk.LEFT, padx=5)


weather_card_frame = create_shadow_card(main_frame, 2, 0, (0, 25))

icon_label = tk.Label(weather_card_frame, bg=COLOR_BG_CARD)
icon_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

city_label = tk.Label(weather_card_frame, text="Cidade: ---", font=FONT_SUBTITLE, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY)
city_label.grid(row=1, column=0, columnspan=2, pady=(0, 5))

temperature_label = tk.Label(weather_card_frame, text="--°C", font=FONT_TEMP, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY)
temperature_label.grid(row=2, column=0, columnspan=2, pady=(0, 5))

description_label = tk.Label(weather_card_frame, text="Condição: ---", font=FONT_DESC, bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY)
description_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))


feels_like_label = tk.Label(weather_card_frame, text="Sensação: ---", font=FONT_DETAILS, bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY)
feels_like_label.grid(row=4, column=0, sticky="w", padx=(0, 10), pady=(5, 2))

humidity_label = tk.Label(weather_card_frame, text="Umidade: ---", font=FONT_DETAILS, bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY)
humidity_label.grid(row=4, column=1, sticky="w", pady=(5, 2))

pressure_label = tk.Label(weather_card_frame, text="Pressão: ---", font=FONT_DETAILS, bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY)
pressure_label.grid(row=5, column=0, sticky="w", padx=(0, 10), pady=(2, 5))

wind_speed_label = tk.Label(weather_card_frame, text="Vento: ---", font=FONT_DETAILS, bg=COLOR_BG_CARD, fg=COLOR_TEXT_SECONDARY)
wind_speed_label.grid(row=5, column=1, sticky="w", pady=(2, 5))


weather_card_frame.grid_columnconfigure(0, weight=1)
weather_card_frame.grid_columnconfigure(1, weight=1)

weather_card_frame.grid_rowconfigure(0, weight=1) 
weather_card_frame.grid_rowconfigure(1, weight=1) 
weather_card_frame.grid_rowconfigure(2, weight=1) 
weather_card_frame.grid_rowconfigure(3, weight=1) 
weather_card_frame.grid_rowconfigure(4, weight=1) 
weather_card_frame.grid_rowconfigure(5, weight=1) 


history_card_frame = create_shadow_card(main_frame, 3, 0, (0, 0)) 

history_title_label = tk.Label(history_card_frame, text="Histórico de Buscas", font=FONT_SUBTITLE, bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY)
history_title_label.pack(pady=(0, 10))

history_listbox = tk.Listbox(history_card_frame, height=MAX_HISTORY_SIZE, font=FONT_HISTORY, bd=0, relief="flat", bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY, selectbackground=COLOR_ACCENT_PRIMARY, selectforeground="white", highlightbackground=COLOR_SHADOW, highlightthickness=1)
history_listbox.pack(pady=(0, 5), fill="both", expand=True) 
history_listbox.bind("<<ListboxSelect>>", on_history_select)


load_history()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
