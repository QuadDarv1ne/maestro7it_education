import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_arrays():
    """
    Создает и возвращает одномерный и двумерный массивы.

    Returns:
        tuple: Одномерный и двумерный массивы.
    """
    array_1d = np.array([1, 2, 3, 4, 5])
    array_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    return array_1d, array_2d

def print_array(name, array):
    """
    Выводит массив с заданным именем.

    Args:
        name (str): Имя массива.
        array (np.ndarray): Массив для вывода.
    """
    logging.info(f"{name}:\n{array}\n")

def basic_operations(array_1d):
    """
    Выполняет базовые операции с одномерным массивом.

    Args:
        array_1d (np.ndarray): Одномерный массив.
    """
    try:
        if array_1d.ndim != 1:
            raise ValueError("Ожидался одномерный массив.")

        sum_arrays = array_1d + np.array([10, 20, 30, 40, 50])
        scalar_multiplication = array_1d * 2
        logging.info(f"Сложение массивов: {sum_arrays}")
        logging.info(f"Умножение массива на скаляр: {scalar_multiplication}\n")
    except ValueError as e:
        logging.error(f"Ошибка при выполнении базовых операций: {e}")

def matrix_operations(array_2d):
    """
    Выполняет операции с матрицей.

    Args:
        array_2d (np.ndarray): Двумерный массив (матрица).
    """
    try:
        if array_2d.ndim != 2:
            raise ValueError("Ожидался двумерный массив.")

        transposed_matrix = array_2d.T
        matrix_product = np.dot(array_2d, transposed_matrix)
        logging.info("Транспонированная матрица:\n%s", transposed_matrix)
        logging.info("Произведение матриц:\n%s\n", matrix_product)
    except ValueError as e:
        logging.error(f"Ошибка при выполнении операций с матрицей: {e}")

def statistical_operations(array_1d):
    """
    Выполняет статистические операции с массивом.

    Args:
        array_1d (np.ndarray): Одномерный массив.
    """
    mean_value = np.mean(array_1d)
    sum_value = np.sum(array_1d)
    std_deviation = np.std(array_1d)
    max_value = np.max(array_1d)
    min_value = np.min(array_1d)
    logging.info(f"Среднее значение массива: {mean_value}")
    logging.info(f"Сумма элементов массива: {sum_value}")
    logging.info(f"Стандартное отклонение массива: {std_deviation}")
    logging.info(f"Максимальное значение массива: {max_value}")
    logging.info(f"Минимальное значение массива: {min_value}")

def test_operations():
    """
    Проводит тестирование функций.
    """
    array_1d, array_2d = create_arrays()

    # Тестирование базовых операций
    basic_operations(array_1d)

    # Тестирование операций с матрицей
    matrix_operations(array_2d)

    # Тестирование статистических операций
    statistical_operations(array_1d)

def main():
    array_1d, array_2d = create_arrays()
    print_array("Одномерный массив", array_1d)
    print_array("Двумерный массив (матрица)", array_2d)

    array_range = np.arange(0, 10, 2)
    array_linspace = np.linspace(0, 1, 5)
    print_array("Массив с использованием arange", array_range)
    print_array("Массив с использованием linspace", array_linspace)

    test_operations()

if __name__ == "__main__":
    main()
