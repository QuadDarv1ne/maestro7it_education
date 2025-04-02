class Calculator {
    public double add(double a, double b) {
        return a + b;
    }

    public double subtract(double a, double b) {
        return a - b;
    }

    public double multiply(double a, double b) {
        return a * b;
    }

    public double divide(double a, double b) {
        if (b == 0) {
            return Double.POSITIVE_INFINITY; // Возвращаем бесконечность при делении на ноль
        }
        return a / b;
    }
}
