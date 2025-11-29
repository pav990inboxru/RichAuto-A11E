#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование логики генерации кода
"""
import re

def generate_code(step_y, width_x, raise_z, cut_depth_z, feed_rate):
    """Генерация кода на основе параметров"""
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
    
    return '\n'.join(code_lines)

def extract_parameters_from_code(code):
    """Извлечение параметров из кода"""
    # Извлечение высоты подъёма (Z после G00 или отдельно стоящее Z)
    # Сначала ищем Z после G00
    raise_match = re.search(r'G00[^\n]*Z([0-9.]+)', code)
    if raise_match:
        # Берём первое значение подъёма как высоту (это начальная высота)
        raise_z = raise_match.group(1)
    else:
        # Если нет G00Z, ищем просто Z после G00 в начальной позиции
        initial_z_match = re.search(r'G00X[0-9.]+Y[0-9.]+Z([0-9.]+)', code)
        if initial_z_match:
            raise_z = initial_z_match.group(1)
        else:
            raise_z = "4.000"  # значение по умолчанию
    
    # Извлечение глубины реза (Z после G01)
    depth_match = re.search(r'G01[^\n]*Z([0-9.]+)', code)
    if depth_match:
        cut_depth_z = depth_match.group(1)
    else:
        cut_depth_z = "0.000"  # значение по умолчанию
    
    # Извлечение скорости подачи
    feed_match = re.search(r'F([0-9.]+)', code)
    if feed_match:
        feed_rate = feed_match.group(1)
    else:
        feed_rate = "300"  # значение по умолчанию
    
    # Извлечение ширины (X в строках с движением)
    x_values = re.findall(r'X([0-9.]+(?:\.[0-9]+)?)F?', code)
    if x_values:
        # Берём максимальное значение как ширину
        max_x = max(float(x) for x in x_values)
        width_x = int(max_x)
    else:
        width_x = 200  # значение по умолчанию
    
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
                step_y = int(most_common_step)
            else:
                step_y = 40  # значение по умолчанию
        else:
            step_y = 40  # значение по умолчанию
    else:
        step_y = 40  # значение по умолчанию
    
    return {
        'step_y': step_y,
        'width_x': width_x,
        'raise_z': float(raise_z),
        'cut_depth_z': float(cut_depth_z),
        'feed_rate': float(feed_rate)
    }

# Тестируем логику
print("Тестирование новой логики генерации кода...")
print()

# Проверим извлечение параметров из существующего файла
with open('/workspace/test.nc', 'r', encoding='utf-8') as f:
    original_code = f.read()

print("Оригинальный код:")
print(original_code)
print()

params = extract_parameters_from_code(original_code)
print("Извлеченные параметры:")
for key, value in params.items():
    print(f"  {key}: {value}")
print()

# Генерируем новый код с извлеченными параметрами
new_code = generate_code(
    params['step_y'], 
    params['width_x'], 
    params['raise_z'], 
    params['cut_depth_z'], 
    params['feed_rate']
)

print("Сгенерированный код с новыми требованиями:")
print(new_code)
print()

# Проверим, что все значения Z перед резом равны 0.000 и все подъемы равны 20.000
lines = new_code.split('\n')
z_before_cut = []
z_raise = []

for i, line in enumerate(lines):
    if line.startswith('Z') or 'Z' in line.split() or 'Z' in line:
        if 'Z0.000' in line and not 'G00' in line:
            z_before_cut.append(line)
        elif 'G00Z20.000' in line:
            z_raise.append(line)

print(f"Количество Z0.000 перед резом: {len(z_before_cut)}")
print(f"Количество G00Z20.000 подъемов: {len(z_raise)}")
print()

print("Примеры Z0.000 перед резом:")
for line in z_before_cut[:5]:  # Показываем первые 5
    print(f"  {line}")
print()

print("Примеры G00Z20.000 подъемов:")
for line in z_raise[:5]:  # Показываем первые 5
    print(f"  {line}")