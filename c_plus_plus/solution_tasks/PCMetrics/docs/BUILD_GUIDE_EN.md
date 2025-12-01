# PCMetrics Build and Run Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Project Structure](#project-structure)
3. [Building with CMake (Recommended)](#building-with-cmake-recommended)
4. [Manual Compilation](#manual-compilation)
5. [Running the Application](#running-the-application)
6. [Running Tests](#running-tests)
7. [Troubleshooting](#troubleshooting)

## System Requirements

- **Operating System**: Windows 7 or higher (64-bit)
- **Compiler**: MinGW-w64 or Visual Studio with C++11 support
- **Build System**: CMake 3.10 or higher
- **Libraries**: 
  - Windows PDH (Performance Data Helper) - included with Windows
  - Optional: NVIDIA NVML, AMD ADL, Intel GPA (for GPU monitoring)

## Project Structure

```
PCMetrics/
├── include/              # Header files (.h)
├── src/                  # Source files (.cpp)
├── libs/                 # External libraries (NVML, ADL, Intel GPA)
├── tests/                # Test files
├── docs/                 # Documentation
├── CMakeLists.txt        # CMake build configuration
├── BUILD_GUIDE.md        # Russian build guide
├── BUILD_GUIDE_EN.md     # This file
├── README.md             # Main documentation
└── .gitignore            # Git ignored files
```

## Building with CMake (Recommended)

### Step 1: Prepare the build environment

1. Open command prompt or PowerShell
2. Navigate to the project root directory:
   ```cmd
   cd path\to\PCMetrics
   ```

### Step 2: Create build directory

```cmd
mkdir build
cd build
```

### Step 3: Generate build files

For MinGW:
```cmd
cmake .. -G "MinGW Makefiles"
```

For Visual Studio (if installed):
```cmd
cmake .. -G "Visual Studio 16 2019"
```

### Step 4: Compile the project

```cmd
cmake --build .
```

After successful build, you will find executables:
- `pcmetrics.exe` - main application
- `pcmetrics_test.exe` - test application (in bin/ subdirectory)

## Manual Compilation

If you prefer to build the project manually without CMake:

### Using g++ (MinGW)

```cmd
g++ -I include src/main.cpp src/cpu_monitor.cpp src/disk_monitor.cpp src/gpu_monitor.cpp src/logger.cpp src/memory_monitor.cpp src/metrics_exporter.cpp -o pcmetrics.exe -lpdh -std=c++11
```

### Using Visual Studio Compiler

```cmd
cl /I include src/main.cpp src/cpu_monitor.cpp src/disk_monitor.cpp src/gpu_monitor.cpp src/logger.cpp src/memory_monitor.cpp src/metrics_exporter.cpp pdh.lib /std:c++11 /out:pcmetrics.exe
```

## Running the Application

### From build directory (CMake)

```cmd
# To run the main application
./pcmetrics.exe

# Or if using Windows Command Prompt
pcmetrics.exe
```

### From project root directory (manual compilation)

```cmd
# To run the main application
./pcmetrics.exe
```

### Launch Options

The application doesn't require special launch parameters. All settings are configured internally during execution.

## Running Tests

### From build directory (CMake)

```cmd
./bin/pcmetrics_test.exe
```

Tests verify:
- Logging system functionality
- Correct memory information retrieval
- Overall monitoring functionality

## Troubleshooting

### Compilation Issues

1. **"Undefined reference" errors**
   - Cause: Not all .cpp files were included in the compilation command
   - Solution: Ensure all .cpp files from the src directory are included in the compilation command

2. **"pdh.h: No such file or directory" error**
   - Cause: Missing Windows PDH header files
   - Solution: Ensure Windows SDK is installed

3. **Linking error with pdh library**
   - Cause: Compiler cannot find pdh.lib library
   - Solution: Ensure you specified the -lpdh flag in the compilation command

### Execution Issues

1. **PDH errors at startup**
   - Cause: Issues accessing Windows performance counters
   - Solution: 
     - Run the application as administrator
     - Check that the Windows performance counters service is running
     - Execute: `lodctr /R` as administrator

2. **Missing GPU information**
   - Cause: Additional GPU libraries not installed
   - Solution: 
     - Place corresponding libraries in libs/nvml, libs/adl, libs/intel directories
     - Rebuild the project with flags:
       ```cmd
       cmake .. -DENABLE_NVML=ON -DENABLE_ADL=ON -DENABLE_INTEL_GPA=ON
       ```

### CMake Issues

1. **"No such file or directory" error when running cmake**
   - Cause: CMake cannot find the compiler
   - Solution: Ensure the compiler (gcc/g++ or cl) is in PATH

2. **Warnings about GPU libraries not found**
   - Cause: Libraries not found in libs/* directories
   - Solution: This is normal behavior if you don't plan to use GPU monitoring

## Additional Information

### Building with GPU Support

To enable GPU monitoring support, you need to:

1. Download the corresponding libraries:
   - NVIDIA NVML: [Download link]
   - AMD ADL SDK: [Download link]
   - Intel GPA: [Download link]

2. Place libraries in the appropriate directories:
   - NVML: libs/nvml/
   - ADL: libs/adl/
   - Intel GPA: libs/intel/

3. Rebuild the project with flags:
   ```cmd
   cmake .. -DENABLE_NVML=ON -DENABLE_ADL=ON -DENABLE_INTEL_GPA=ON
   cmake --build .
   ```

### Logging Configuration

Logging is configured automatically when starting the application. By default:
- Logs are saved to `pcmetrics.log` file
- Log level: INFO
- Console output: enabled

These parameters can be changed in the code in `src/main.cpp` file.

### Data Export

The application supports data export in formats:
- CSV (Comma-Separated Values)
- JSON (JavaScript Object Notation)

Export function is activated at the end of the program upon user request.