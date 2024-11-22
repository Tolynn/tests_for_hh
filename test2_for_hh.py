import requests
from bs4 import BeautifulSoup


def get_animal_names(url: str):
    """
    Парсит список названий животных с указанной страницы Википедии.
    Возвращает Список названий животных или None в случае ошибки.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Поднимает исключение для кодов ошибок (4xx или 5xx)

        soup = BeautifulSoup(response.content, "html.parser")

        animal_names = []
        animal_links = soup.select("div[class*=mw-category] li a")

        for link in animal_links:
            title = link.get("title")
            if title and not title.startswith("Категория:"):
                animal_names.append(title)

        # Получаем ссылку на следующую страницу
        next_page_link = soup.find('a', title="Категория:Животные по алфавиту", string="Следующая страница")

        return animal_names, next_page_link

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к странице: {e}")
        return None, None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None, None


def scrape_all_animals(initial_url: str):
    """
    Парсит все страницы животных, собирая ссылки на следующую страницу.
    Возвращает список всех животных
    """
    current_url = initial_url
    all_animal_names = []

    # x = 0
    # while x < 9:
    while current_url:
        animal_names, next_page_link = get_animal_names(current_url)
        if animal_names:
            all_animal_names.extend(animal_names)  # Добавляем собранные имена
        current_url = f'https://ru.wikipedia.org{next_page_link.get("href")}' if next_page_link else None
        # x += 1
    return all_animal_names


if __name__ == "__main__":
    initial_url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"
    all_names = scrape_all_animals(initial_url)

    animal_dict = dict()

    if all_names:
        # записываем всех животных, построчно, в блокнот, для наглядности. Формируем словарь animal_dict
        with open("animal_names.txt", "w", encoding="utf-8") as f:
            for name in all_names:
                f.write(name + "\n")
                if name == 'Служебная:RandomInCategory/Животные по алфавиту':
                    continue
                elif name[0].strip() == 'A':  # игнорируем латинский алфавит. нужна только кириллица
                    break
                elif name[0].strip() in animal_dict:
                    animal_dict[name.strip()[0]] += 1
                else:
                    animal_dict[name[0].strip()] = 1
        print("Список животных сохранен в animal_names.txt")
        print(animal_dict)

        sorted_animal_dict = {k: animal_dict[k] for k in sorted(animal_dict)}

        with open("beasts.csv", "w", encoding="utf-8") as f:
            for k, v in sorted_animal_dict.items():
                f.write(f"{k},{v}\n")

    else:
        print("Список животных не получен.")
