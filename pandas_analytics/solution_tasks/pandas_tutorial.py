import pandas as pd
import logging
import matplotlib.pyplot as plt

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_dataframe():
    """
    Создает и возвращает DataFrame с примерными данными.

    Returns:
        pd.DataFrame: DataFrame с примерными данными.
    """
    data = {
        'Имя': ['Анна', 'Борис', 'Виктор', 'Галина'],
        'Возраст': [28, 34, 25, 42],
        'Город': ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск']
    }
    df = pd.DataFrame(data)
    return df

def print_dataframe(name, df):
    """
    Выводит DataFrame с заданным именем.

    Args:
        name (str): Имя DataFrame.
        df (pd.DataFrame): DataFrame для вывода.
    """
    logging.info(f"{name}:\n{df}\n")

def basic_operations(df):
    """
    Выполняет базовые операции с DataFrame.

    Args:
        df (pd.DataFrame): DataFrame для операций.
    """
    try:
        # Добавление нового столбца
        df['Возраст + 2'] = df['Возраст'] + 2
        logging.info("DataFrame после добавления нового столбца:\n%s", df)

        # Фильтрация данных
        filtered_df = df[df['Возраст'] > 30]
        logging.info("Отфильтрованный DataFrame (возраст > 30):\n%s", filtered_df)

        # Группировка данных
        grouped_df = df.groupby('Город')['Возраст'].mean()
        logging.info("Средний возраст по городам:\n%s", grouped_df)
    except KeyError as e:
        logging.error(f"Ошибка при выполнении базовых операций: {e}")

def visualize_data(df):
    """
    Визуализирует данные из DataFrame.

    Args:
        df (pd.DataFrame): DataFrame для визуализации.
    """
    try:
        df.plot(kind='bar', x='Имя', y='Возраст', legend=False)
        plt.title('Возраст участников')
        plt.xlabel('Имя')
        plt.ylabel('Возраст')
        plt.show()
    except KeyError as e:
        logging.error(f"Ошибка при визуализации данных: {e}")

def test_operations():
    """
    Проводит тестирование функций.
    """
    df = create_dataframe()

    # Тестирование базовых операций
    basic_operations(df)

    # Тестирование визуализации данных
    visualize_data(df)

def main():
    df = create_dataframe()
    print_dataframe("Исходный DataFrame", df)

    test_operations()

if __name__ == "__main__":
    main()
