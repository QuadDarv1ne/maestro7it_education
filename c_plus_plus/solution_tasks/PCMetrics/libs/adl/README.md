# AMD Display Library (ADL)

This directory should contain the AMD Display Library (ADL) files for AMD GPU monitoring.

## Required Files:
- `adl_sdk.h` - Header file for ADL API
- `ADL.lib` - Static library for linking (Windows)
- `ADL.dll` - Dynamic library (Windows)

## Installation:
1. Download AMD Display Library SDK from AMD website
2. Extract ADL files to this directory
3. Enable ADL support in CMake with `-DENABLE_ADL=ON`

## Documentation:
- [AMD Display Library Documentation](https://developer.amd.com/resources/graphics-development/display-library-adl-sdk/)