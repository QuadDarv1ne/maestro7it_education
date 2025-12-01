# Intel Graphics Performance Analyzers

This directory should contain Intel Graphics performance analysis libraries for Intel GPU monitoring.

## Required Files:
- `igpa.h` - Header file for Intel GPA API
- `igpa.lib` - Static library for linking (Windows)
- `igpa.dll` - Dynamic library (Windows)

## Installation:
1. Download Intel Graphics Performance Analyzers from Intel website
2. Extract Intel GPA files to this directory
3. Enable Intel GPA support in CMake with `-DENABLE_INTEL_GPA=ON`

## Documentation:
- [Intel Graphics Performance Analyzers Documentation](https://software.intel.com/content/www/us/en/develop/tools/graphics-performance-analyzers.html)