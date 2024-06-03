import tkinter as tk
from tkinter import filedialog
import os
import json
from tkinter import messagebox

transparent_window = None


config_file_path = ''

def select_config_folder():
    global config_file_path
    folder_selected = filedialog.askdirectory(title="Select Configuration Folder")
    if folder_selected:
        config_file_path = os.path.join(folder_selected, 'window_positions.json')
        if not os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'w') as file:
                    json.dump({}, file)
            except PermissionError:
                messagebox.showerror("Permission Error", "Не удалось создать файл конфигурации из-за ограничений доступа.")
                exit()
            except Exception as e:
                messagebox.showerror("Unexpected Error", f"Произошла ошибка при создании файла конфигурации: {e}")
                exit()
    else:
        exit() 

def save_window_position(window, position, size):
    """Сохраняет позицию и размер окна в файл конфигурации."""
    try:
        with open(config_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    

    data[window.title()] = {'coords': position, 'size': size}
    with open(config_file_path, 'w') as file:
        json.dump(data, file)

def restore_window_position(window_title, window):
    """Восстанавливает позицию и размер окна из файла конфигурации."""
    try:
        with open(config_file_path, 'r') as file:
            data = json.load(file)
        saved_data = data.get(window_title, {'coords': [100, 100], 'size': '300x200'})

        x, y = saved_data['coords']

        if 'size' in saved_data:
            size_str = saved_data['size'].split('+')[0]  
            size_parts = size_str.split('x')
            if len(size_parts)!= 2:
                raise ValueError("Неверный формат размера окна")
            width, height = map(int, size_parts)

            window.geometry(f"{width}x{height}+{x}+{y}")
    except FileNotFoundError:
        print("Файл конфигурации не найден. Используется стандартное положение.")
        window.geometry("300x200+100+100")

def create_or_close_transparent_window():
    global transparent_window
    if check_var.get():  
        if transparent_window is not None:
            transparent_window.destroy()  
        transparent_window = tk.Toplevel()
        transparent_window.title("EVEScan")
        

        restore_window_position(transparent_window.title(), transparent_window)
        
        transparent_window.attributes('-topmost', True)  
        transparent_color = '#abcdef'
        transparent_window.attributes('-transparentcolor', transparent_color)
        
        label = tk.Label(transparent_window, text="EVEScan test,\ntest.", bg=transparent_color)
        label.config(foreground='white')  
        label.pack(fill=tk.BOTH, expand=True)
    else:
        if transparent_window is not None:
            transparent_window.destroy()  
            if transparent_window.winfo_exists():
                save_window_position(transparent_window, [transparent_window.winfo_x(), transparent_window.winfo_y()], transparent_window.geometry())

select_config_folder()


root = tk.Tk()
root.title("EVEScan")


menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)


file_menu.add_command(label="Select Config Folder", command=select_config_folder)


save_button = tk.Button(root, text="Сохранить конфиг", 
                        command=lambda: save_window_position(transparent_window, 
                                                            [transparent_window.winfo_x(), transparent_window.winfo_y()],
                                                            transparent_window.geometry()))
save_button.pack(pady=20)

check_var = tk.BooleanVar()
check_box = tk.Checkbutton(root, text="Открыть прозрачное окно", variable=check_var, command=create_or_close_transparent_window)
check_box.pack(pady=20)

root.mainloop()