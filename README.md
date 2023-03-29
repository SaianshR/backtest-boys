# Backtesting Tool

This is a backtesting tool that allows you to simulate the implementation of a trading strategy on historical data. You can upload a CSV file that contains the historical data, set the transaction costs, position sizing, and risk management parameters, and the tool will calculate the Sharpe ratio and maximum drawdown of your strategy.

## Requirements

- Python 3
- Streamlit
- Pandas
- Numpy

## Usage

To use the tool, simply run the following command in your terminal:

```
streamlit run app.py
```

Then, follow the on-screen instructions to upload your CSV file and set the parameters. The results will be displayed in the app.

Note: The columns in the uploaded CSV file should be 'Date', 'Open', 'Close', 'Adj Close'.

