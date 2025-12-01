# NVIDIA Management Library (NVML)

This directory should contain the NVIDIA Management Library (NVML) files for GPU monitoring.

## Required Files:
- `nvml.h` - Header file for NVML API
- `nvml.lib` - Static library for linking (Windows)
- `nvml.dll` - Dynamic library (Windows)

## Installation:
1. Download NVIDIA GPU Driver or CUDA Toolkit
2. Extract NVML files to this directory
3. Enable NVML support in CMake with `-DENABLE_NVML=ON`

## Documentation:
- [NVIDIA Management Library Documentation](https://docs.nvidia.com/deploy/nvml-api/)