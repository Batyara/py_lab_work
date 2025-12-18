import os

def load_data(path):
    """Зчитує дані з файлу та повертає список очищених рядків."""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    # 1. Завантаження даних із файлів
    try:
        names = load_data('student_names.txt')
        math = [int(x) for x in load_data('math.txt')]
        physics = [int(x) for x in load_data('physics.txt')]
        statistics = [int(x) for x in load_data('statistics.txt')]
    except (ValueError, FileNotFoundError) as e:
        print(f"Помилка при обробці файлів: {e}")
        return

    # Визначення мінімальної кількості записів для коректної обробки
    limit = min(len(names), len(math), len(physics), len(statistics))
    if limit == 0:
        print("Помилка: Один або кілька вхідних файлів порожні.")
        return

    # 2. Формування структури даних
    student_records = []
    for i in range(limit):
        scores = {
            'Mathematics': math[i],
            'Physics': physics[i],
            'Statistics': statistics[i]
        }
        average = sum(scores.values()) / len(scores)
        student_records.append({
            'name': names[i],
            'scores': scores,
            'average': average
        })

    print("-" * 50)
    print("ЗВІТ ПРО УСПІШНІСТЬ СТУДЕНТІВ")
    print("-" * 50)

    # 3. Визначення ТОП-3 студентів
    print("\n--- Рейтинг найкращих студентів ---")
    top_performers = sorted(student_records, key=lambda x: x['average'], reverse=True)[:3]
    for pos, student in enumerate(top_performers, 1):
        print(f"{pos}. {student['name']} | Середній бал: {student['average']:.2f}")

    # 4. Статистичний аналіз по дисциплінах
    print("\n--- Загальна статистика за предметами ---")
    subjects_map = {
        'Mathematics': math[:limit],
        'Physics': physics[:limit],
        'Statistics': statistics[:limit]
    }

    for subj, scores in subjects_map.items():
        avg_subj = sum(scores) / len(scores)
        max_subj = max(scores)
        min_subj = min(scores)
        
        # Пошук лідера в конкретній дисципліні
        leader = next(s['name'] for s in student_records if s['scores'][subj] == max_subj)
        
        print(f"Предмет: {subj:12} | Сер: {avg_subj:.1f} | Min: {min_subj} | Max: {max_subj} (Best: {leader})")

    # 5. Студенти з незадовільним результатом (нижче 50)
    print("\n--- Студенти з балом нижче 50 ---")
    at_risk = [s['name'] for s in student_records if s['average'] < 50]
    
    if at_risk:
        print(f"Кількість: {len(at_risk)}")
        print("Список: " + ", ".join(at_risk))
    else:
        print("Студентів із середнім балом нижче 50 не виявлено.")

if __name__ == "__main__":
    main()
