# AugmentedNet
A Roman Numeral Analysis Network with Synthetic Training Examples and Additional Tonal Tasks

## Introduction

### The neural network architecture

The architecture is a CRNN (Convolutional Recurrent Neural Network) with an alternative representation of pitch spelling at the input.

More information about the neural network architecture can be found in the paper.

![AugmentedNet Architecture](img/AugmentedNetArchitecture.png)


### Organization of the repo

The code is organized in the following way
```
.
├── AugmentedNet
├── img
├── misc
├── notebooks
└── test
```

- [AugmentedNet](AugmentedNet) has all the source code of the network
- [img](img) the image diagrams of the network and code organization
- [misc](misc) useful, but non-essential, stand-alone scripts that I wrote while developing this project
- [notebooks](notebooks) Jupyter notebook *playgrounds* used throughout the project (e.g., data exploration)
- [test](test) unit tests for all relevant modules of the network

### The AugmentedNet source code

The general organization of the code is summarized by the following diagram.

![AugmentedNet](img/AugmentedNetCode.png)

Each of the blue rectangles roughly corresponds to a Python module.

The inputs of the network are pairs of (score, annotation) files.

The inputs pairs are transformed into pandas DataFrame objects, stored as `.tsv` files.

Later on, these are encoded in a representation that can be dispatched to the neural network.


## Experiments

### Visualizing the results with [mlflow](https://mlflow.org/)

All the experiments presented in the paper were monitored using `mlflow`.

If you want to visualize the experiments with the [mlflow ui](https://www.mlflow.org/docs/latest/quickstart.html#viewing-the-tracking-ui): 

1. `pip install mlflow`
2. Download the [mlruns.zip](https://github.com/napulen/AugmentedNet/releases/download/untagged-142cdf7f106874032f7e/mlruns.zip) file with the AugmentedNet experiments
3. Unzip (any folder should work)
4. Run `mlflow ui` from the terminal, making sure that `./mlruns/` is reachable from your current working directory
5. Visit `localhost:5000` (default host and port values)
6. That's it! The experiments should be available in your browser

For extra convenience, I also uploaded the logs to [TensorBoard.dev](https://tensorboard.dev/).

Here are the tables of the paper and a link to see the runs of each model in Tensorboard.dev.

### Paper results and tensorboard visualizations

#### AugmentedNet configurations

These are the results for the four different configurations of the AugmentedNet.

| Model                      | Key           | Deg.          | Qual.         | Inv.          | Root          | RN            |
|----------------------------|---------------|---------------|---------------|---------------|---------------|---------------|
| AugmentedNet6              | 82.7          | 64.4          | 76.6          | 77.4          | 82.5          | 43.3          |
| AugmentedNet6+             | 83.0          | 65.1          | 77.5          | **78.6**      | 83.0          | 44.6          |
| AugmentedNet11             | 81.3          | 64.2          | 77.2          | 76.1          | 82.9          | 43.1          |
| AugmentedNet11+            | **83.7**      | **66.0**      | **77.6**      | 77.2          | **83.2**      | **45.0**      |

**[Watch experiments in TensorBoard.dev!](https://tensorboard.dev/experiment/l6CPJ7TdSdOjxCbibzQJwA/#scalars)**

`6` and `11` indicate the number of tasks in the multitask learning layout.

`+` indicates the use of synthetic training data.




#### AugmentedNet vs. other models

These are the results for the best AugmentedNet configuration (11+) against other models.

| Test set                | Training set | Model        | Key                            | Degree                | Quality               | Inversion               | Root                  | ComRN                 | RN*conv*                       | RN*alt*               |
|-------------------------|--------------|--------------|--------------------------------|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|--------------------------------|-----------------------|
| Full test set           | Full dataset | AugN         | 82.9                           | 67.0                  | 79.7                  | 78.8                  | 83.0                  | 65.6                  | 46.4                           | 51.5                  |
| WiR                     | Full dataset | AugN         | 81.8                           | 69.2                  | 85.9                  | 90.3                  | 90.3                  | 70.2                  | 56.4                           | 62.4                  |
| HaydnSun                | Full dataset | AugN         | 81.2                           | 62.9                  | 80.2                  | 82.7                  | 86.5                  | 60.4                  | 48.6                           | 52.1                  |
| ABC                     | Full dataset | AugN         | 83.6                           | 65.6                  | 78.0                  | 76.9                  | 78.9                  | 62.6                  | 44.5                           | 48.4                  |
| TAVERN                  | Full dataset | AugN         | 88.7                           | 60.0                  | 77.4                  | 78.8                  | 81.5                  | 66.3                  | 42.6                           | 52.9                  |
| WTC                     | Full dataset | AugN         | 77.2                           | 69.7                  | 75.0                  | 74.4                  | 82.7                  | 61.7                  | **46.2**                       | 47.9                  |
| WTC*crossval*           | BPS+WTC      | AugN         | **85.1(4.0)**                  | 62.9(5.5)             | 69.1(1.9)             | 70.1(3.7)             | 79.2(1.8)             | 59.9(3.4)             | **42.9(4.2)**                  | 46.9(4.7)             |
| WTC*crossval*           | BPS+WTC      | CS21         | 56.3(2.5)                      | -                     | -                     | -                     | -                     | -                     | 26.0(1.7)                      | -                     |
| BPS                     | Full dataset | AugN         | **85.0**                       | **73.4**              | **79.0**              | **73.4**              | 84.4                  | 68.3                  | **45.4**                       | 49.3                  |
| BPS                     | All data     | Mi20         | 82.9                           | 68.3                  | 76.6                  | 72.0                  | -                     | -                     | 42.8                           | -                     |
| BPS                     | BPS+WTC      | AugN         | **82.9**                       | 70.9                  | 80.7                  | 72.0                  | 85.3                  | 67.6                  | **44.1**                       | 47.5                  |
| BPS                     | BPS+WTC      | CS21         | 79.0                           | -                     | -                     | -                     | -                     | -                     | 41.7                           | -                     |
| BPS                     | BPS          | AugN         | **83.0**                       | **71.2**              | **80.3**              | **71.1**              | 84.1                  | 68.5                  | **44.0**                       | 47.4                  |
| BPS                     | BPS          | Mi20         | 80.6                           | 66.5                  | 76.3                  | 68.1                  | -                     | -                     | 39.1                           | -                     |
| BPS                     | BPS          | CS19         | 78.4                           | 65.1                  | 74.6                  | 62.1                  | -                     | -                     | -                              | -                     |
| BPS                     | BPS          | CS18         | 66.7                           | 51.8                  | 60.6                  | 59.1                  | -                     | -                     | 25.7                           | -                     |

**[Watch experiments in TensorBoard.dev!](https://tensorboard.dev/experiment/fXVA71nWTkSZh6CqTXCeCw/#scalars)**
