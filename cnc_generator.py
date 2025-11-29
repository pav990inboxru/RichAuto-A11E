#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор CNC кода для контроллера RichAuto A11
Разработано Harper_IDS для КД-Групп
"""

import re
import os
import sys
from typing import Optional


class CNCCodeGenerator:
    def __init__(self):
        # Параметры по умолчанию
        self.step_y = 40.0
        self.width_x = 200.0
        self.raise_z = 4.000
        self.cut_depth_z = 0.000
        self.feed_rate = 300.0
    
    def generate_code(self, step_y: float = None, width_x: float = None, raise_z: float = None, 
                     cut_depth_z: float = None, feed_rate: float = None) -> str:
        """Генерация кода на основе параметров"""
        # Используем переданные параметры или значения по умолчанию
        step_y = step_y if step_y is not None else self.step_y
        width_x = width_x if width_x is not None else self.width_x
        raise_z = raise_z if raise_z is not None else self.raise_z
        cut_depth_z = cut_depth_z if cut_depth_z is not None else self.cut_depth_z
        feed_rate = feed_rate if feed_rate is not None else self.feed_rate
        
        # Генерация кода
        code_lines = []
        code_lines.append("G54")  # Начальная команда
        
        # Начальная позиция
        y_pos = 0.0
        line_num = 0
        
        # Ограничиваем количество строк для предотвращения бесконечного цикла
        max_lines = 1000
        
        # Генерация кода по шаблону
        y_pos = 0.0
        # Первый проход - начальная позиция
        code_lines.append(f"G00X0.000Y{y_pos:.0f}Z0.000")
        code_lines.append(f"Z0.000")  # Устанавливаем Z в 0 перед резом
        code_lines.append(f"G01Z{cut_depth_z:.3f}")
        code_lines.append(f"X{width_x:.3f}F{feed_rate:.0f}")
        code_lines.append(f"G00Z20.000")  # Подъём на 20.000 как в шаблоне (без зависимости от raise_z)
        
        y_pos += step_y
        line_num = 1
        
        # Последующие проходы
        while y_pos <= 3200 and line_num < max_lines:  # Ограничение по Y
            # Перемещение к следующей Y позиции
            code_lines.append(f"X0.000Y{y_pos:.0f}")
            # Опускаемся до уровня реза
            code_lines.append(f"Z0.000")  # Устанавливаем Z в 0 перед резом
            code_lines.append(f"G01Z{cut_depth_z:.3f}")
            # Режем по оси X
            code_lines.append(f"X{width_x:.3f}F{feed_rate:.0f}")
            # Поднимаемся вверх
            code_lines.append(f"G00Z20.000")  # Подъём на 20.000 как в шаблоне (без зависимости от raise_z)
            
            y_pos += step_y
            line_num += 1
        
        return '\n'.join(code_lines)
    
    def extract_parameters_from_code(self, code: str) -> dict:
        """Извлечение параметров из кода"""
        params = {}
        
        try:
            # Извлечение высоты подъёма после резки (Z после G00 в строках подъёма)
            # В новой логике это фиксированное значение 20.000 мм
            # Ищем G00Z20.000 или подобные команды подъёма после резки
            raise_after_cut_matches = re.findall(r'G00Z([0-9.]+)', code)
            if raise_after_cut_matches:
                # Берём первое найденное значение подъёма после резки
                # В нормальной ситуации это должно быть 20.000
                params['raise_z'] = float(raise_after_cut_matches[0])
            else:
                # Если не найдено, используем значение по умолчанию
                params['raise_z'] = 4.000

            
            # Извлечение глубины реза (Z после G01)
            depth_matches = re.findall(r'G01[^\n]*Z([0-9.]+)', code)
            if depth_matches:
                params['cut_depth_z'] = float(depth_matches[0])
            
            # Извлечение скорости подачи
            feed_matches = re.findall(r'F([0-9.]+)', code)
            if feed_matches:
                params['feed_rate'] = float(feed_matches[0])
            
            # Извлечение ширины (X в строках с движением)
            x_values = re.findall(r'X([0-9.]+(?:\.[0-9]+)?)F?', code)
            if x_values:
                # Берём максимальное значение как ширину
                max_x = max(float(x) for x in x_values)
                params['width_x'] = max_x
            
            # Извлечение шага (Y в строках с движением)
            y_values = re.findall(r'Y([0-9.]+(?:\.[0-9]+)?)', code)
            if len(y_values) > 1:
                # Вычисляем средний шаг между значениями Y
                y_nums = [float(y) for y in y_values]
                y_nums.sort()
                # Убираем дубликаты
                y_nums = list(set(y_nums))
                y_nums.sort()
                if len(y_nums) > 1:
                    steps = [y_nums[i+1] - y_nums[i] for i in range(len(y_nums)-1) if y_nums[i+1] != y_nums[i]]
                    if steps:
                        # Берём модальное значение или среднее
                        from collections import Counter
                        step_counts = Counter(steps)
                        # Находим наиболее часто встречающийся шаг
                        params['step_y'] = step_counts.most_common(1)[0][0]
        
        except Exception as e:
            print(f"Ошибка при извлечении параметров: {e}")
        
        return params
    
    def load_code_from_file(self, file_path: str) -> str:
        """Загрузка кода из файла"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def save_code_to_file(self, code: str, file_path: str) -> bool:
        """Сохранение кода в файл"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def main():
    generator = CNCCodeGenerator()
    
    print("CNC Code Generator для RichAuto A11")
    print("Разработано Harper_IDS для КД-Групп")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Если переданы аргументы командной строки
        if sys.argv[1] == "generate":
            # Генерация кода с параметрами
            if len(sys.argv) >= 6:
                try:
                    step_y = float(sys.argv[2])
                    width_x = float(sys.argv[3])
                    raise_z = float(sys.argv[4])
                    cut_depth_z = float(sys.argv[5])
                    feed_rate = float(sys.argv[6]) if len(sys.argv) > 6 else 300.0
                    
                    code = generator.generate_code(step_y, width_x, raise_z, cut_depth_z, feed_rate)
                    print("Сгенерированный код:")
                    print("-" * 20)
                    print(code)
                    print("-" * 20)
                    
                    # Сохранение в файл
                    filename = f"y{int(step_y)}x{int(width_x)}.nc"
                    generator.save_code_to_file(code, filename)
                    print(f"Код сохранён в файл: {filename}")
                    
                except ValueError:
                    print("Ошибка: Некорректные параметры. Используйте: python cnc_generator.py generate шаг_по_Y ширина_по_X высота_подъёма глубина_реза [скорость_подачи]")
            else:
                print("Использование: python cnc_generator.py generate шаг_по_Y ширина_по_X высота_подъёма глубина_реза [скорость_подачи]")
        
        elif sys.argv[1] == "extract" and len(sys.argv) > 2:
            # Извлечение параметров из существующего файла
            try:
                file_path = sys.argv[2]
                code = generator.load_code_from_file(file_path)
                params = generator.extract_parameters_from_code(code)
                
                print(f"Параметры, извлечённые из файла {file_path}:")
                for param, value in params.items():
                    print(f"  {param}: {value}")
                
                # Обновляем параметры генератора
                for param, value in params.items():
                    setattr(generator, param, value)
                
            except Exception as e:
                print(f"Ошибка при извлечении параметров: {e}")
        
        elif sys.argv[1] == "help":
            print("Доступные команды:")
            print("  python cnc_generator.py generate шаг_по_Y ширина_по_X высота_подъёма глубина_реза [скорость_подачи]")
            print("  python cnc_generator.py extract путь_к_файлу.nc")
            print("  python cnc_generator.py help")
        
        else:
            print("Неизвестная команда. Используйте 'python cnc_generator.py help' для справки.")
    
    else:
        # Интерактивный режим
        while True:
            print("\nВыберите действие:")
            print("1. Генерировать новый код")
            print("2. Извлечь параметры из существующего файла")
            print("3. Выйти")
            
            choice = input("Введите номер действия: ").strip()
            
            if choice == "1":
                try:
                    step_y = float(input(f"Шаг по Y (мм) [{generator.step_y}]: ") or generator.step_y)
                    width_x = float(input(f"Ширина по X (мм) [{generator.width_x}]: ") or generator.width_x)
                    raise_z = float(input(f"Высота подъёма Z (мм) [{generator.raise_z}]: ") or generator.raise_z)
                    cut_depth_z = float(input(f"Глубина реза Z (мм) [{generator.cut_depth_z}]: ") or generator.cut_depth_z)
                    feed_rate = float(input(f"Скорость подачи F [{generator.feed_rate}]: ") or generator.feed_rate)
                    
                    code = generator.generate_code(step_y, width_x, raise_z, cut_depth_z, feed_rate)
                    print("\nСгенерированный код:")
                    print("-" * 20)
                    print(code)
                    print("-" * 20)
                    
                    save = input(f"\nСохранить в файл y{int(step_y)}x{int(width_x)}.nc? (y/n): ").strip().lower()
                    if save == 'y':
                        filename = f"y{int(step_y)}x{int(width_x)}.nc"
                        generator.save_code_to_file(code, filename)
                        print(f"Код сохранён в файл: {filename}")
                
                except ValueError:
                    print("Ошибка: введите числовые значения")
            
            elif choice == "2":
                file_path = input("Введите путь к файлу .nc: ").strip()
                if os.path.exists(file_path):
                    try:
                        code = generator.load_code_from_file(file_path)
                        params = generator.extract_parameters_from_code(code)
                        
                        print("Извлечённые параметры:")
                        for param, value in params.items():
                            print(f"  {param}: {value}")
                        
                        # Обновляем параметры генератора
                        for param, value in params.items():
                            setattr(generator, param, value)
                        
                        regenerate = input("Хотите перегенерировать код с этими параметрами? (y/n): ").strip().lower()
                        if regenerate == 'y':
                            code = generator.generate_code()
                            print("\nПерегенерированный код:")
                            print("-" * 20)
                            print(code)
                            print("-" * 20)
                            
                            save = input(f"Сохранить в файл? (y/n): ").strip().lower()
                            if save == 'y':
                                # Используем текущие параметры для генерации имени файла
                                filename = f"y{int(generator.step_y)}x{int(generator.width_x)}.nc"
                                generator.save_code_to_file(code, filename)
                                print(f"Код сохранён в файл: {filename}")
                    
                    except Exception as e:
                        print(f"Ошибка при обработке файла: {e}")
                else:
                    print("Файл не найден")
            
            elif choice == "3":
                print("До свидания!")
                break
            
            else:
                print("Неверный выбор")


if __name__ == "__main__":
    main()