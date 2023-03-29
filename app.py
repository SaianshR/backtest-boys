import streamlit as st
import pandas as pd
import numpy as np

# function to calculate sharpe ratio
def sharpe_ratio(returns, risk_free_rate=0.02):
    return (returns.mean() - risk_free_rate) / returns.std()

# function to calculate maximum drawdown
def max_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1
    return drawdown.min()

# function to calculate transaction costs
def transaction_costs(returns, tc=0.01):
    returns_with_tc = returns - tc
    return returns_with_tc

# function to calculate position sizing
def position_sizing(returns, capital, max_risk=0.01):
    returns_with_tc = transaction_costs(returns)
    position_size = capital * max_risk / np.abs(returns_with_tc).mean()
    returns_with_tc_scaled = returns_with_tc * position_size
    return returns_with_tc_scaled


def run_app():
    st.title("Backtesting Tool")
    st.text("Columns in the uploaded data should be - 'Date', 'Open', 'Close', 'Adj Close' ")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            #uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, low_memory=False)
            if all(col in df.columns for col in ['Date', 'Open', 'Close', 'Adj Close']):
                st.write("Your CSV file has been successfully uploaded and has the correct columns.")
                # add calculation for returns
                df['returns'] = df['Adj Close'].pct_change()
                df.set_index('Date', inplace=True)
                # get user inputs for transaction costs, position sizing, and risk management
                tc = st.slider("Transaction Costs", 0.0, 1.0, 0.01)
                capital = st.number_input("Capital", value=100000.0, step=1000.0)
                max_risk = st.slider("Max Risk as Percentage of Capital", 0.01, 1.0, 0.01)

                # calculate returns with transaction costs and position sizing
                returns_with_tc_scaled = position_sizing(df['returns'], capital, max_risk)

                # calculate sharpe ratio and maximum drawdown
                sharpe = sharpe_ratio(returns_with_tc_scaled)
                drawdown = max_drawdown(returns_with_tc_scaled)

                # display results
                st.write("Sharpe Ratio: ", sharpe)
                st.write("Maximum Drawdown: ", drawdown)

                # show a line chart of the returns
                st.line_chart(returns_with_tc_scaled)
                st.write("Cumulative Returns:")
                st.line_chart(returns_with_tc_scaled.cumsum())
            else:
                    st.error("Your CSV file does not have the correct column names (Date, Open, Close, Adj Close).")
        except Exception as e:
            st.error("An error occurred while reading the CSV file.")
            st.write(e)


run_app()