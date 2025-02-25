# Cats vs. Dogs Image Classification

This project implements a Convolutional Neural Network (CNN) to classify images of cats and dogs using TensorFlow and Keras. The model achieved an accuracy of **98.3%** on the validation set after 10 epochs.

## Table of Contents

- [Project Description](#project-description)
- [Dataset Structure](#dataset-structure)
- [Dependencies](#dependencies)
- [Training Performance](#training-performance)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

## Project Description

This project utilizes a CNN built with TensorFlow and Keras to classify images of cats and dogs. The dataset is loaded and preprocessed using `keras.utils.image_dataset_from_directory` for efficient data handling. The model is trained for 10 epochs, achieving a high accuracy of 98.3% on the validation set.






Ensure that the `train` and `test` folders contain subfolders named `cats` and `dogs`, each containing the respective images.

## Dependencies

-   Python 3.x
-   TensorFlow (>= 2.x)
-   Keras
-   NumPy
-   Pandas
-   Matplotlib

You can install the dependencies using pip:

```bash
pip install tensorflow numpy pandas matplotlib
Training Performance
The model achieved an accuracy of 98.3% on the validation set after 10 epochs. The training process utilized keras.utils.image_dataset_from_directory for efficient data loading and preprocessing, and the model was built using keras.models and keras.layers.

The following libraries were used:

Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import models, layers
```

## Future Improvements
-**Data Augmentation:** Implement more extensive data augmentation techniques to improve model generalization.
-**Hyperparameter Tuning:** Fine-tune the model's hyperparameters to potentially achieve even higher accuracy.

-**Deployment:** Deploy the trained model for real-time image classification.
-**Larger Dataset:** Test the model on a much larger dataset.

## Author
**Pratham Mohan**
```bash 
[prathammohan3@gmail.com]
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.


Remember to create a `LICENSE` file (if you choose to use the MIT license) and replace `[Your 
