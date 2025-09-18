# Компилятор и флаги
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Wpedantic -g
INCLUDES = -I./include
LIBS = -L./lib

# Исходные файлы и целевые объекты
SRC_DIR = src
BUILD_DIR = build
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)
TARGET = myapp

# Правила сборки
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $^ $(LIBS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<

# Очистка
clean:
	rm -rf $(BUILD_DIR) $(TARGET)

# Пересборка
rebuild: clean $(TARGET)

# Запуск
run: $(TARGET)
	./$(TARGET)

.PHONY: clean rebuild run