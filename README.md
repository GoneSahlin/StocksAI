## StocksAI

#### How to collect data
make collect

#### How to train model
1. [install tensorflow](https://www.tensorflow.org/install/pip)
2. python model/src/train.py

#### How to run app
make run-app

### Results
![Accuracy Plot](./plots/accuracy_chart.png)

None of the models were able to predict with more accuracy than the model predicting zero change.

### Potential Problems
* Inconsistencies in the stock market over the last two years of data. Previous ten years showed steady increase, but over the last two years stock prices decreased.
* Lack of data. Might be improved with more stocks, a longer time period, and more attributes.
