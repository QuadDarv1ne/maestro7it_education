# Multi-stage build: compile with Maven, run with JRE
FROM openjdk:11-jdk AS build

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN apt-get update && apt-get install -y maven && mvn dependency:go-offline

# Copy source code
COPY src ./src

# Compile and package
RUN mvn clean package -DskipTests

# Runtime stage
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /app

# Copy the JAR from build stage
COPY --from=build /app/target/textanalyzerpro-1.0.0.jar app.jar

# Create directories for input/output
RUN mkdir -p input output

# Set entrypoint
ENTRYPOINT ["java", "-jar", "app.jar"]

# Default command
CMD ["--help"]