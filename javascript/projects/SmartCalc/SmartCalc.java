public class SmartCalc {
    public static void main(String[] args) {
        UnitConverter calc = new UnitConverter();

        System.out.println("Арифметические операции:");
        System.out.println("Сложение: 5 + 3 = " + calc.add(5, 3));
        System.out.println("Вычитание: 10 - 4 = " + calc.subtract(10, 4));
        System.out.println("Умножение: 7 * 6 = " + calc.multiply(7, 6));
        System.out.println("Деление: 8 / 2 = " + calc.divide(8, 2));

        System.out.println("\nФизические вычисления:");
        System.out.println("Сила: масса 10 кг, ускорение 9.8 м/с² = " + calc.force(10, 9.8) + " Н");
        System.out.println("Энергия: масса 5 кг, скорость 10 м/с = " + calc.energy(5, 10) + " Дж");

        System.out.println("\nТригонометрические функции:");
        System.out.println("Синус 90° = " + calc.sine(90));
        System.out.println("Косинус 0° = " + calc.cosine(0));

        System.out.println("\nКонвертация единиц:");
        System.out.println("10 метров в футах = " + calc.metersToFeet(10));
        System.out.println("100°C в Фаренгейтах = " + calc.celsiusToFahrenheit(100));

        System.out.println("\nЧисла Фибоначчи:");
        System.out.println("Первые 10 чисел Фибоначчи: " + java.util.Arrays.toString(calc.fibonacci(10)));

        System.out.println("\nПростые числа (решето Эратосфена):");
        System.out.println("Простые числа до 50: " + java.util.Arrays.toString(calc.sieveOfEratosthenes(50)));
    }
}
