import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import os

class CNCCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор кода ЧПУ Harper_IDS")
        self.root.geometry("900x700")
        
        # Установка иконки (если есть)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Переменные для параметров
        self.step_var = tk.DoubleVar(value=40.0)
        self.width_var = tk.DoubleVar(value=200.0)
        self.height_var = tk.DoubleVar(value=200.0)
        self.length_var = tk.DoubleVar(value=4.0)
        self.speed_var = tk.DoubleVar(value=300.0)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка шаблона
        self.load_template()
        
        # Информация об авторстве
        self.show_credits()
    
    def create_widgets(self):
        # Создание основных фреймов
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Панель параметров
        params_frame = ttk.LabelFrame(top_frame, text="Параметры")
        params_frame.pack(fill=tk.X, pady=5)
        
        # Параметр шага (Y)
        ttk.Label(params_frame, text="Шаг (Y):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(params_frame, textvariable=self.step_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        # Параметр ширины (X)
        ttk.Label(params_frame, text="Ширина (X):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(params_frame, textvariable=self.width_var, width=10).grid(row=0, column=3, padx=5, pady=2)
        
        # Параметр высоты (максимальное значение Y)
        ttk.Label(params_frame, text="Высота (Y max):").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(params_frame, textvariable=self.height_var, width=10).grid(row=0, column=5, padx=5, pady=2)
        
        # Параметр глубины (Z)
        ttk.Label(params_frame, text="Глубина (Z):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(params_frame, textvariable=self.length_var, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Параметр скорости (F)
        ttk.Label(params_frame, text="Скорость (F):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        ttk.Entry(params_frame, textvariable=self.speed_var, width=10).grid(row=1, column=3, padx=5, pady=2)
        
        # Кнопки управления
        button_frame = ttk.Frame(params_frame)
        button_frame.grid(row=0, column=6, rowspan=2, padx=20)
        
        ttk.Button(button_frame, text="Загрузить .nc файл", command=self.load_file).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Сгенерировать код", command=self.generate_code).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Сохранить", command=self.save_file).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Сохранить как", command=self.save_file_as).pack(fill=tk.X, pady=2)
        
        # Текстовое поле для редактирования кода
        text_frame = ttk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Добавление прокрутки
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.code_text = tk.Text(text_frame, wrap=tk.NONE, yscrollcommand=text_scrollbar.set)
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        text_scrollbar.config(command=self.code_text.yview)
        
        # Справка
        help_frame = ttk.LabelFrame(self.root, text="Справка")
        help_frame.pack(fill=tk.X, padx=10, pady=5)
        
        help_text = tk.Text(help_frame, height=4, wrap=tk.WORD)
        help_text.pack(fill=tk.X, padx=5, pady=5)
        help_text.insert(tk.END, "Справочник по контроллеру RichAuto A11: https://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf")
        help_text.config(state=tk.DISABLED)
    
    def load_template(self):
        """Загрузка шаблона кода"""
        template_code = """G54
G00X0.000Y000Z4.000
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y40
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y80
Z4.000
G01Z0.000
X200.000F300
G00Z20.000
X0.000Y120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y1960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2320
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2360
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2400
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2440
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2480
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2520
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2560
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2600
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2640
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2680
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2720
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2760
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2800
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2840
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2880
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2920
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y2960
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3000
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3040
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3080
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3120
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3160
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3200
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3240
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3280
Z4.000
G01Z0.000
X200.000
G00Z20.000
X0.000Y3320
Z4.000"""
        
        self.code_text.insert(tk.END, template_code)
    
    def show_credits(self):
        """Показать информацию об авторстве"""
        messagebox.showinfo("Информация", 
            "Разработано Harper_IDS\nДля организации КД-Групп\nПортативная программа для редактирования кода ЧПУ")
    
    def load_file(self):
        """Загрузить файл .nc"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл .nc",
            filetypes=[("Файлы ЧПУ", "*.nc"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def generate_code(self):
        """Сгенерировать код на основе параметров"""
        step = self.step_var.get()
        width = self.width_var.get()
        height = self.height_var.get()
        length = self.length_var.get()
        speed = self.speed_var.get()
        
        # Генерация кода
        code_lines = ["G54"]
        
        y_pos = 0
        while y_pos <= height:
            # Подход к рабочей позиции
            code_lines.append(f"G00X0.000Y{y_pos:.3f}Z{length:.3f}")
            code_lines.append(f"Z{length:.3f}")
            code_lines.append(f"G01Z0.000")
            code_lines.append(f"X{width:.3f}F{speed}")
            code_lines.append(f"G00Z20.000")
            
            y_pos += step
        
        # Удалить последнюю строку G00Z20.000 если она лишняя
        if code_lines[-1] == "G00Z20.000":
            code_lines.pop()
        
        # Обновить текстовое поле
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, "\n".join(code_lines))
    
    def save_file(self):
        """Сохранить файл с именем в формате y{шаг}x{ширина}.nc"""
        step = int(self.step_var.get())
        width = int(self.width_var.get())
        
        # Создать имя файла
        filename = f"y{step}x{width}.nc"
        
        # Проверить, открыт ли файл, если нет - использовать save_as
        try:
            # Пробуем получить текущий путь файла, если он был открыт
            current_file = getattr(self, 'current_file', None)
            if current_file:
                with open(current_file, 'w', encoding='utf-8') as file:
                    file.write(self.code_text.get(1.0, tk.END).rstrip())
            else:
                self.save_file_as()
        except:
            self.save_file_as()
    
    def save_file_as(self):
        """Сохранить файл как с именем в формате y{шаг}x{ширина}.nc"""
        step = int(self.step_var.get())
        width = int(self.width_var.get())
        
        # Создать имя файла по умолчанию
        default_filename = f"y{step}x{width}.nc"
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл .nc",
            defaultextension=".nc",
            initialfile=default_filename,
            filetypes=[("Файлы ЧПУ", "*.nc"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.code_text.get(1.0, tk.END).rstrip())
                self.current_file = file_path
                messagebox.showinfo("Сохранено", f"Файл сохранен как {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

def main():
    root = tk.Tk()
    app = CNCCodeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()