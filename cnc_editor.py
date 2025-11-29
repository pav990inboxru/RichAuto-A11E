#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC Code Editor для контроллера RichAuto A11
Разработано Harper_IDS для КД-Групп
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re
import os
import webbrowser
from typing import Optional


class CNCCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Code Editor - RichAuto A11")
        self.root.geometry("1200x800")
        
        # Установка темной темы
        self.setup_dark_theme()
        
        # Переменные для параметров
        self.step_y = tk.StringVar(value="40")
        self.width_x = tk.StringVar(value="200")
        self.raise_z = tk.StringVar(value="4.000")
        self.cut_depth_z = tk.StringVar(value="0.000")
        self.feed_rate = tk.StringVar(value="300")
        
        # Текущий файл
        self.current_file = None
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка горячих клавиш
        self.bind_shortcuts()
        
        # Установка фокуса на редактор
        self.text_area.focus_set()
        
    def setup_dark_theme(self):
        """Настройка темной темы"""
        self.root.configure(bg='#2b2b2b')
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка стилей для виджетов
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Dark.TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('Dark.TButton', background='#3c3c3c', foreground='#ffffff')
        style.configure('Dark.TEntry', fieldbackground='#3c3c3c', foreground='#ffffff', insertcolor='white')
        style.map('Dark.TButton', background=[('active', '#4a4a4a')])
        
        # Цвета для кнопок
        self.btn_colors = {
            'blue': '#1e88e5',
            'green': '#43a047',
            'orange': '#fb8c00',
            'red': '#e53935'
        }
    
    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Боковая панель параметров
        params_frame = ttk.LabelFrame(main_frame, text="Параметры", style='Dark.TFrame', width=300)
        params_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        params_frame.pack_propagate(False)
        
        # Поля ввода параметров
        self.create_param_field(params_frame, "Шаг (Y, мм):", self.step_y, 0)
        self.create_param_field(params_frame, "Ширина (X, мм):", self.width_x, 1)
        self.create_param_field(params_frame, "Высота подъёма (Z, мм):", self.raise_z, 2)
        self.create_param_field(params_frame, "Глубина реза (Z, мм):", self.cut_depth_z, 3)
        self.create_param_field(params_frame, "Скорость подачи (F):", self.feed_rate, 4)
        
        # Кнопки
        button_frame = ttk.Frame(params_frame, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.create_colored_button(button_frame, "Загрузить", self.load_file, self.btn_colors['blue'], 0)
        self.create_colored_button(button_frame, "Сгенерировать", self.generate_code, self.btn_colors['green'], 1)
        self.create_colored_button(button_frame, "Сохранить", self.save_file, self.btn_colors['orange'], 2)
        self.create_colored_button(button_frame, "Сохранить как", self.save_as_file, self.btn_colors['red'], 3)
        
        # Кнопка справки
        help_btn = tk.Button(
            params_frame, 
            text="Справка по RichAuto A11", 
            command=self.open_manual,
            bg='#7b1fa2', 
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        help_btn.pack(fill=tk.X, pady=(10, 5))
        
        # Информация об авторстве
        author_label = tk.Label(
            params_frame, 
            text="Harper_IDS\nдля КД-Групп", 
            bg='#2b2b2b', 
            fg='#aaaaaa',
            font=('Arial', 9),
            justify=tk.CENTER
        )
        author_label.pack(pady=(20, 0))
        
        # Основная область редактирования
        editor_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Заголовок области редактирования
        editor_title = tk.Label(
            editor_frame, 
            text="Код программы (.nc)", 
            bg='#2b2b2b', 
            fg='#ffffff',
            font=('Arial', 12, 'bold')
        )
        editor_title.pack(anchor=tk.W, pady=(0, 5))
        
        # Текстовая область с прокруткой
        self.text_area = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.NONE,
            width=80,
            height=30,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#dcdcdc',
            insertbackground='white',
            selectbackground='#264f78',
            borderwidth=2,
            relief='solid'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Статусная строка
        self.status_var = tk.StringVar(value="Готово")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#3c3c3c',
            fg='#ffffff'
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_param_field(self, parent, label_text, variable, row):
        """Создание поля ввода параметра"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=label_text, bg='#2b2b2b', fg='#ffffff')
        label.pack(anchor=tk.W)
        
        entry = tk.Entry(
            frame, 
            textvariable=variable, 
            bg='#3c3c3c', 
            fg='#ffffff', 
            insertbackground='white',
            relief='solid',
            borderwidth=1
        )
        entry.pack(fill=tk.X, pady=(2, 0))
    
    def create_colored_button(self, parent, text, command, color, row):
        """Создание цветной кнопки"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=5,
            pady=3
        )
        btn.pack(fill=tk.X, pady=2)
    
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_as_file())  # Shift+Ctrl+S
        self.root.bind('<F5>', lambda e: self.generate_code())
        
        # Обработка клавиш табуляции для навигации
        self.root.bind('<Tab>', self.focus_next_widget)
        self.root.bind('<Shift-Tab>', self.focus_prev_widget)
    
    def focus_next_widget(self, event):
        """Переход к следующему виджету при нажатии Tab"""
        event.widget.tk_focusNext().focus()
        return "break"
    
    def focus_prev_widget(self, event):
        """Переход к предыдущему виджету при нажатии Shift+Tab"""
        event.widget.tk_focusPrev().focus()
        return "break"
    
    def load_file(self):
        """Загрузка файла .nc"""
        file_path = filedialog.askopenfilename(
            title="Открыть файл .nc",
            filetypes=[("CNC файлы", "*.nc"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                
                self.current_file = file_path
                self.extract_parameters_from_code(content)
                self.status_var.set(f"Файл загружен: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
    
    def extract_parameters_from_code(self, code: str):
        """Извлечение параметров из кода"""
        try:
            # Извлечение высоты подъёма (Z после G00 или отдельно стоящее Z)
            # Сначала ищем Z после G00
            raise_match = re.search(r'G00[^\n]*Z([0-9.]+)', code)
            if raise_match:
                # Берём первое значение подъёма как высоту (это начальная высота)
                self.raise_z.set(raise_match.group(1))
            else:
                # Если нет G00Z, ищем просто Z после G00 в начальной позиции
                initial_z_match = re.search(r'G00X[0-9.]+Y[0-9.]+Z([0-9.]+)', code)
                if initial_z_match:
                    self.raise_z.set(initial_z_match.group(1))
            
            # Извлечение глубины реза (Z после G01)
            depth_match = re.search(r'G01[^\n]*Z([0-9.]+)', code)
            if depth_match:
                self.cut_depth_z.set(depth_match.group(1))
            
            # Извлечение скорости подачи
            feed_match = re.search(r'F([0-9.]+)', code)
            if feed_match:
                self.feed_rate.set(feed_match.group(1))
            
            # Извлечение ширины (X в строках с движением)
            x_values = re.findall(r'X([0-9.]+(?:\.[0-9]+)?)F?', code)
            if x_values:
                # Берём максимальное значение как ширину
                max_x = max(float(x) for x in x_values)
                self.width_x.set(str(int(max_x)))
            
            # Извлечение шага (Y в строках с движением)
            y_values = re.findall(r'Y([0-9.]+(?:\.[0-9]+)?)', code)
            if len(y_values) > 1:
                # Вычисляем шаг между значениями Y
                y_nums = [float(y) for y in y_values]
                y_nums = list(set(y_nums))  # Убираем дубликаты
                y_nums.sort()
                if len(y_nums) > 1:
                    steps = [y_nums[i+1] - y_nums[i] for i in range(len(y_nums)-1) if y_nums[i+1] != y_nums[i]]
                    if steps:
                        # Берём модальное значение или среднее
                        from collections import Counter
                        step_counts = Counter(steps)
                        # Находим наиболее часто встречающийся шаг
                        most_common_step = step_counts.most_common(1)[0][0]
                        self.step_y.set(str(int(most_common_step)))
        
        except Exception as e:
            print(f"Ошибка при извлечении параметров: {e}")
    
    def generate_code(self):
        """Генерация кода на основе параметров"""
        try:
            step_y = float(self.step_y.get())
            width_x = float(self.width_x.get())
            raise_z = float(self.raise_z.get())
            cut_depth_z = float(self.cut_depth_z.get())
            feed_rate = float(self.feed_rate.get())
            
            # Генерация кода по шаблону
            code_lines = []
            code_lines.append("G54")  # Начальная команда
            
            y_pos = 0.0
            # Первый проход - начальная позиция
            code_lines.append(f"G00X0.000Y{y_pos:.0f}Z0.000")  # Фиксированное значение Z0.000
            code_lines.append(f"Z0.000")  # Дублируем Z как в шаблоне - всегда 0.000
            code_lines.append(f"G01Z{cut_depth_z:.3f}")
            code_lines.append(f"X{width_x:.3f}F{feed_rate:.0f}")
            code_lines.append(f"G00Z20.000")  # Подъём на 20.000 как в шаблоне (фиксированное значение)
            
            y_pos += step_y
            line_num = 1
            
            # Ограничиваем количество строк для предотвращения бесконечного цикла
            max_lines = 1000
            
            # Последующие проходы
            while y_pos <= 3200 and line_num < max_lines:  # Ограничение по Y
                # Перемещение к следующей Y позиции
                code_lines.append(f"X0.000Y{y_pos:.0f}")
                # Устанавливаем Z=0.000 перед резом
                code_lines.append(f"Z0.000")  # Фиксированное значение Z0.000 перед каждым резом
                code_lines.append(f"G01Z{cut_depth_z:.3f}")
                # Режем по оси X
                code_lines.append(f"X{width_x:.3f}F{feed_rate:.0f}")
                # Поднимаемся вверх
                code_lines.append(f"G00Z20.000")  # Подъём на 20.000 как в шаблоне (фиксированное значение)
                
                y_pos += step_y
                line_num += 1
            
            # Обновление текстовой области
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, '\n'.join(code_lines))
            
            self.status_var.set(f"Код сгенерирован: Шаг={step_y}, Ширина={width_x}")
        
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения параметров. Пожалуйста, проверьте ввод.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации кода:\n{str(e)}")
    
    def save_file(self):
        """Сохранение файла"""
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                
                self.status_var.set(f"Файл сохранён: {os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Сохранение файла как"""
        try:
            step_y = int(float(self.step_y.get()))
            width_x = int(float(self.width_x.get()))
            
            default_name = f"y{step_y}x{width_x}.nc"
            
            file_path = filedialog.asksaveasfilename(
                title="Сохранить файл .nc",
                defaultextension=".nc",
                initialfile=default_name,
                filetypes=[("CNC файлы", "*.nc"), ("Все файлы", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                
                self.current_file = file_path
                self.status_var.set(f"Файл сохранён: {os.path.basename(file_path)}")
        
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные значения параметров для имени файла.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def open_manual(self):
        """Открытие справки по RichAuto A11"""
        try:
            webbrowser.open("https://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf")
        except Exception:
            messagebox.showinfo("Информация", "Не удалось открыть ссылку. Пожалуйста, посетите:\nhttps://cnczavod.ru/uploads/docs/kontroller-richauto-dsp-a11e-manual-rus.pdf")


def main():
    root = tk.Tk()
    app = CNCCodeEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()