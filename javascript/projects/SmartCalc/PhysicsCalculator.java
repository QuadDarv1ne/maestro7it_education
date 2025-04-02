class PhysicsCalculator extends Calculator {
    public double force(double mass, double acceleration) {
        return mass * acceleration;
    }

    public double energy(double mass, double velocity) {
        return 0.5 * mass * Math.pow(velocity, 2);
    }
}
