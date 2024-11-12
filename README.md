# UnconvBench
Benchmark for property prediction of unconventional crystal materials. For a comprehensive evaluation, we collected 
various datasets with 2D materials, MOFs, defected crystals and curated sets of bulk crystals.

## Get started
Installation:
```sh
git clone https://github.com/howardwang1997/unconvbench
cd unconvbench
python setup.py install
```
Required packages can be found in `requirements.txt`

## Datasets
Please find the datasets required on Figshare: https://figshare.com/articles/dataset/UnconvBench/26657428 and download 
them to directory `datasets`.

## Run the benchmark
For easy usage, the workflow of this benchmark mostly complies with another benchmark for crystals named `matbench`.
The usage of this benchmark and the API are similar with `matbench`. Example script to run this benchmark is shown in the
file `example_script.py`.

## Submit the result
Please include your model, the `YourModel_result.json.gz` in a subdirectory under `benchmarks`. You are encouraged to
include a json file to introduce your model and the hyperparameters. The benchmark results will be shown in 
`benchmarks/README.md`.
