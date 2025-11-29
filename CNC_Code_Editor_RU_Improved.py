import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re

class CNCCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор кода ЧПУ Harper_IDS")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Установка стиля
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Создание основных фреймов
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Редактор кода ЧПУ Harper_IDS", 
                              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Параметры слева
        params_frame = tk.LabelFrame(main_frame, text="Параметры", font=("Arial", 12, "bold"), 
                                    bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
        params_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Поля ввода параметров
        tk.Label(params_frame, text="Шаг (Y):", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.step_entry = tk.Entry(params_frame, font=("Arial", 10), width=15, relief="solid", bd=1)
        self.step_entry.grid(row=0, column=1, pady=5, padx=(5, 0))
        self.step_entry.insert(0, "40")
        
        tk.Label(params_frame, text="Ширина (X):", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.width_entry = tk.Entry(params_frame, font=("Arial", 10), width=15, relief="solid", bd=1)
        self.width_entry.grid(row=1, column=1, pady=5, padx=(5, 0))
        self.width_entry.insert(0, "200")
        
        tk.Label(params_frame, text="Высота (Y max):", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.height_entry = tk.Entry(params_frame, font=("Arial", 10), width=15, relief="solid", bd=1)
        self.height_entry.grid(row=2, column=1, pady=5, padx=(5, 0))
        self.height_entry.insert(0, "2000")
        
        tk.Label(params_frame, text="Глубина (Z):", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.depth_entry = tk.Entry(params_frame, font=("Arial", 10), width=15, relief="solid", bd=1)
        self.depth_entry.grid(row=3, column=1, pady=5, padx=(5, 0))
        self.depth_entry.insert(0, "4.000")
        
        tk.Label(params_frame, text="Скорость (F):", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.speed_entry = tk.Entry(params_frame, font=("Arial", 10), width=15, relief="solid", bd=1)
        self.speed_entry.grid(row=4, column=1, pady=5, padx=(5, 0))
        self.speed_entry.insert(0, "300")
        
        # Кнопки управления
        buttons_frame = tk.Frame(params_frame, bg="#f0f0f0")
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        self.load_button = tk.Button(buttons_frame, text="Загрузить .nc файл", command=self.load_file, 
                                    bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                                    relief="flat", padx=10, pady=5)
        self.load_button.pack(fill=tk.X, pady=5)
        
        self.generate_button = tk.Button(buttons_frame, text="Сгенерировать код", command=self.generate_code, 
                                        bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), 
                                        relief="flat", padx=10, pady=5)
        self.generate_button.pack(fill=tk.X, pady=5)
        
        self.save_button = tk.Button(buttons_frame, text="Сохранить", command=self.save_file, 
                                    bg="#f39c12", fg="white", font=("Arial", 10, "bold"), 
                                    relief="flat", padx=10, pady=5)
        self.save_button.pack(fill=tk.X, pady=5)
        
        self.save_as_button = tk.Button(buttons_frame, text="Сохранить как", command=self.save_as_file, 
                                       bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
                                       relief="flat", padx=10, pady=5)
        self.save_as_button.pack(fill=tk.X, pady=5)
        
        # Текстовый редактор
        editor_frame = tk.Frame(main_frame, bg="#f0f0f0")
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Метка редактора
        editor_label = tk.Label(editor_frame, text="Код программы:", font=("Arial", 12, "bold"), 
                               bg="#f0f0f0", fg="#2c3e50")
        editor_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Текстовая область с прокруткой
        text_frame = tk.Frame(editor_frame, relief="solid", bd=1, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = tk.Text(text_frame, wrap=tk.NONE, font=("Courier New", 10), 
                                bg="white", fg="black", insertbackground="black",
                                selectbackground="#3498db", selectforeground="white")
        v_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        h_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        
        self.text_area.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Меню
        self.create_menu()
        
        # Загрузка начального шаблона
        self.load_template()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить", command=self.load_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=lambda: self.text_area.edit_undo())
        edit_menu.add_command(label="Повторить", command=lambda: self.text_area.edit_redo())
        edit_menu.add_separator()
        edit_menu.add_command(label="Копировать", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставить", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Вырезать", command=lambda: self.text_area.event_generate("<<Cut>>"))
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Руководство по контроллеру", command=self.show_manual)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Привязка клавиш
        self.root.bind('<Control-o>', lambda event: self.load_file())
        self.root.bind('<Control-s>', lambda event: self.save_file())
        
    def load_template(self):
        template = """G54
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
        
        self.text_area.insert(tk.END, template)
        self.text_area.edit_modified(False)
        
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл .nc",
            filetypes=[("CNC файлы", "*.nc"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.text_area.edit_modified(False)
                    
                    # Попытка извлечь параметры из файла
                    self.extract_params_from_code(content)
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
    
    def extract_params_from_code(self, code):
        # Попытка извлечь параметры из существующего кода
        lines = code.split('\n')
        
        for line in lines:
            if 'X' in line and 'Y' in line and 'F' in line:
                # Извлечение ширины (X)
                x_match = re.search(r'X([\d.]+)', line)
                if x_match:
                    self.width_entry.delete(0, tk.END)
                    self.width_entry.insert(0, x_match.group(1))
                
                # Извлечение шага (Y) - только для первой строки с Y
                y_match = re.search(r'Y([\d.]+)', line)
                if y_match:
                    self.step_entry.delete(0, tk.END)
                    self.step_entry.insert(0, y_match.group(1))
                
                # Извлечение скорости (F)
                f_match = re.search(r'F([\d.]+)', line)
                if f_match:
                    self.speed_entry.delete(0, tk.END)
                    self.speed_entry.insert(0, f_match.group(1))
    
    def generate_code(self):
        try:
            step = float(self.step_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            depth = float(self.depth_entry.get())
            speed = int(self.speed_entry.get())
            
            # Проверка значений
            if step <= 0 or width <= 0 or height <= 0 or depth < 0 or speed <= 0:
                raise ValueError("Все параметры должны быть положительными")
            
            # Генерация кода
            code_lines = []
            code_lines.append("G54")
            code_lines.append(f"G00X0.000Y000Z{depth}")
            y_pos = 0
            
            while y_pos <= height:
                code_lines.append(f"Z{depth}")
                code_lines.append("G01Z0.000")
                code_lines.append(f"X{width}F{speed}")
                code_lines.append("G00Z20.000")
                
                y_pos += step
                if y_pos <= height:
                    code_lines.append(f"X0.000Y{y_pos}")
            
            # Вставка сгенерированного кода
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, '\n'.join(code_lines))
            self.text_area.edit_modified(False)
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверные параметры:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка генерации кода:\n{str(e)}")
    
    def save_file(self):
        if not hasattr(self, 'current_file') or not self.current_file:
            self.save_as_file()
        else:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    self.text_area.edit_modified(False)
                    messagebox.showinfo("Сохранено", f"Файл сохранен:\n{self.current_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def save_as_file(self):
        try:
            # Получение значений параметров для имени файла
            step = self.step_entry.get().replace('.', '')
            width = self.width_entry.get().replace('.', '')
            
            file_path = filedialog.asksaveasfilename(
                title="Сохранить файл .nc",
                initialfile=f"y{step}x{width}.nc",
                defaultextension=".nc",
                filetypes=[("CNC файлы", "*.nc"), ("Все файлы", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    self.current_file = file_path
                    self.text_area.edit_modified(False)
                    messagebox.showinfo("Сохранено", f"Файл сохранен:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def show_manual(self):
        manual_text = """Руководство по контроллеру RichAuto A11:
https://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf

Данное руководство содержит полную информацию о программировании и эксплуатации контроллера RichAuto A11."""
        
        messagebox.showinfo("Руководство по контроллеру", manual_text)
    
    def show_about(self):
        about_text = """Редактор кода ЧПУ Harper_IDS
Разработано для Организации КД-Групп

Версия: 1.0
Автор: Harper_IDS

Программа для редактирования кода станка ЧПУ в формате .nc
для контроллера ЧПУ RichAuto A11"""
        
        messagebox.showinfo("О программе", about_text)

def main():
    root = tk.Tk()
    app = CNCCodeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()