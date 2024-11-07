![StandardRL Components Logo](https://assets.standardrl.com/general/components/icon-full.png)
# JetsonMeasure

Simple Python script to measure and record the performance of a an application on a Jetson Nano in one line. Measures power consumption (in mW), memory usage in MB, CPU utilisation across all four cores (in %) and CPU and GPU temperatures (in C).

## Usage

`python3 measure.py`

Press Control+C to stop execution. While the script is running, measurements are made continuously. When finished, results are output to `results.csv`.