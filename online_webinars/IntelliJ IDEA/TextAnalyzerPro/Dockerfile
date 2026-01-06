# Use OpenJDK 11 as base image
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /app

# Copy the JAR file
COPY target/TextAnalyzerPro-1.0.0.jar app.jar

# Create directories for input/output
RUN mkdir -p input output

# Set entrypoint
ENTRYPOINT ["java", "-jar", "app.jar"]

# Default command
CMD ["--help"]