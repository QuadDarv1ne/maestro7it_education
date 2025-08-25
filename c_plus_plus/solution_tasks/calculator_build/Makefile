# Makefile - компиляция в build/, бинарник в текущей папке

CXX := g++
CXXFLAGS := -g -Wall -std=c++11

BUILD_DIR := build
SRC_DIR := .
HEADERS := $(SRC_DIR)/calculator.h

ifeq ($(OS),Windows_NT)
	TARGET := calculator.exe
	CXXFLAGS += -D_WIN32
else
	TARGET := calculator
	CXXFLAGS += -DLINUX
endif

TARGET_PATH := $(CURDIR)/$(TARGET)
SRCS := $(SRC_DIR)/main.cpp $(SRC_DIR)/calculator.cpp
OBJECTS := $(BUILD_DIR)/main.o $(BUILD_DIR)/calculator.o

.PHONY: all clean run debug

all: $(TARGET)

# Линковка: объектные файлы -> бинарник (в текущей папке)
$(TARGET): $(OBJECTS) | $(BUILD_DIR)
	@echo Linking $@ ...
	$(CXX) $(CXXFLAGS) $(OBJECTS) -o $(TARGET_PATH)

# Правило для сборки .o из соответствующего .cpp (в корне проекта)
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp $(HEADERS) | $(BUILD_DIR)
	@echo Compiling $< ...
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Создание папки build
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Быстрая цель для запуска (учитывает Windows)
run: $(TARGET)
ifeq ($(OS),Windows_NT)
	@echo Running $(TARGET) ...
	@chcp 65001 >nul && "$(TARGET_PATH)"
else
	@echo Running $(TARGET) ...
	@./$(TARGET_PATH)
endif

# Цель для отладки (пересобирает с debug-флагами)
debug: CXXFLAGS += -O0 -g3 -DDEBUG
debug: clean all

# Очистка (Linux/WSL и Windows(cmd) варианты)
clean:
ifeq ($(OS),Windows_NT)
	-@if exist "$(BUILD_DIR)\*" ( del /Q "$(BUILD_DIR)\*" ) 
	-@if exist "$(TARGET_PATH)" ( del /Q "$(TARGET_PATH)" )
	-@if exist "$(BUILD_DIR)" ( rmdir /S /Q "$(BUILD_DIR)" )
else
	@rm -rf $(BUILD_DIR) $(TARGET_PATH)
endif
