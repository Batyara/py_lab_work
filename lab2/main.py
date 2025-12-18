import os

class CastIterator:
    """
    Окремий клас-ітератор для завдання 4.
    Проходить по рядках і повертає склад акторів, якщо він довший за 50 символів.
    """
    def __init__(self, dataset, col_idx):
        self.dataset = dataset
        self.col_idx = col_idx
        self._cursor = 0
        self._limit = len(dataset)

    def __iter__(self):
        return self

    def __next__(self):
        while self._cursor < self._limit:
            row = self.dataset[self._cursor]
            self._cursor += 1
            
            # Перевірка наявності колонки та довжини тексту
            if len(row) > self.col_idx:
                cast_data = row[self.col_idx]
                if len(cast_data) > 50:
                    return cast_data
        
        raise StopIteration


class NetflixAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.columns = []
        self.data = []
        self._load_data()

    def _load_data(self):
        """Завдання 1: Зчитування та парсинг через split(',')"""
        if not os.path.exists(self.file_path):
            print(f"Error: File '{self.file_path}' not found.")
            return

        with open(self.file_path, 'r', encoding='utf-8') as f:
            # Читаємо всі рядки і одразу стріпаємо
            raw_lines = [line.strip() for line in f.readlines() if line.strip()]

        # Парсинг першого рядка як заголовка
        if raw_lines:
            self.columns = raw_lines[0].split(',')
            # Парсинг решти рядків
            self.data = [line.split(',') for line in raw_lines[1:]]

    def _get_idx(self, col_name):
        """Безпечний пошук індексу колонки"""
        try:
            return self.columns.index(col_name)
        except ValueError:
            return -1

    def task_filter_high_rated(self):
        """Завдання 2: List Comprehension (Rating > 7.5)"""
        idx_rate = self._get_idx('rating')
        if idx_rate == -1: return

        print(f"\n[Task 2] Фільми з рейтингом > 7.5 (перші 5 колонок):")
        
        # Comprehension
        results = [
            row[:5] for row in self.data
            if len(row) > idx_rate 
            and row[idx_rate].replace('.', '', 1).isdigit() 
            and float(row[idx_rate]) > 7.5
        ]

        # Демонстрація (перші 3)
        for res in results[:3]:
            print(res)

    def task_generator_english_recent(self):
        """Завдання 3: Генератор (English + >2015)"""
        idx_lang = self._get_idx('language')
        idx_end = self._get_idx('endYear')

        def _generator():
            for row in self.data:
                if len(row) <= max(idx_lang, idx_end): continue
                
                # Логіка фільтрації
                is_english = (row[idx_lang] == 'English')
                is_recent = (row[idx_end].isdigit() and int(row[idx_end]) > 2015)

                if is_english and is_recent:
                    yield row

        print(f"\n[Task 3] Генератор: English контент після 2015 року:")
        gen = _generator()
        
        # Виводимо декілька результатів
        try:
            for _ in range(3):
                print(next(gen))
        except StopIteration:
            pass

    def task_custom_iterator(self):
        """Завдання 4: Використання класу CastIterator"""
        idx_cast = self._get_idx('cast')
        if idx_cast == -1: return

        print(f"\n[Task 4] Ітератор: довгий список акторів (>50 символів):")
        walker = CastIterator(self.data, idx_cast)
        
        counter = 0
        for cast_info in walker:
            if counter >= 10: break
            print(f" -> {cast_info[:60]}...")
            counter += 1

    def task_statistics(self):
        """Завдання 5: Статистика (Adult count, Avg Rating)"""
        idx_adult = self._get_idx('isAdult')
        idx_votes = self._get_idx('numVotes')
        idx_rate = self._get_idx('rating')

        adult_counter = 0
        valid_ratings = []

        for row in self.data:
            if len(row) <= max(idx_adult, idx_votes, idx_rate): continue

            # a) Підрахунок Adult
            if row[idx_adult] == '1':
                adult_counter += 1

            # b) Рейтинг де голосів > 1000
            if row[idx_votes].isdigit() and int(row[idx_votes]) > 1000:
                r_val = row[idx_rate]
                if r_val.replace('.', '', 1).isdigit():
                    valid_ratings.append(float(r_val))

        avg_val = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0
        
        print(f"\n[Task 5] Статистика:")
        print(f" - Кількість Adult відео: {adult_counter}")
        print(f" - Середній рейтинг (популярних): {avg_val:.2f}")
        
        return avg_val

    def task_advanced_filter(self, threshold_rating):
        """Завдання 6: Генератор + Comprehension (Episodes > 10 & High Rating)"""
        idx_ep = self._get_idx('episodes') 
        # Фоллбек, якщо назва колонки інша
        if idx_ep == -1: idx_ep = self._get_idx('episode')
        
        idx_rate = self._get_idx('rating')
        idx_title = self._get_idx('title')

        print(f"\n[Task 6] Серіали (>10 епізодів) з рейтингом вище {threshold_rating:.2f}:")

        # Внутрішній генератор
        def show_gen():
            for row in self.data:
                if len(row) <= max(idx_ep, idx_rate, idx_title): continue
                
                ep_str = row[idx_ep]
                rate_str = row[idx_rate]

                if ep_str.isdigit() and int(ep_str) > 10:
                    if rate_str.replace('.', '', 1).isdigit() and float(rate_str) > threshold_rating:
                        yield row[idx_title]

        # Comprehension для збору даних з генератора
        final_list = [name for name in show_gen()]

        for item in final_list[:5]:
            print(f" * {item}")


def main():
    # Точка входу
    file_name = 'netflix_list.csv'
    
    app = NetflixAnalyzer(file_name)
    
    if not app.data:
        print("Дані не завантажено. Перевірте файл.")
        return

    # Послідовне виконання завдань
    app.task_filter_high_rated()
    app.task_generator_english_recent()
    app.task_custom_iterator()
    
    # Отримуємо середній рейтинг для наступного кроку
    avg_rating = app.task_statistics()
    
    app.task_advanced_filter(avg_rating)

if __name__ == '__main__':
    main()
