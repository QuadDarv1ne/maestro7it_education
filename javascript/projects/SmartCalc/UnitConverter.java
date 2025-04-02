class UnitConverter extends AdvancedCalculator {
    public double metersToFeet(double meters) {
        return meters * 3.28084;
    }

    public double celsiusToFahrenheit(double celsius) {
        return (celsius * 9 / 5) + 32;
    }
}
