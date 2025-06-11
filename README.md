# Simple ES Strategy with NautilusTrader

This project implements a simple trading strategy for E-mini S&P 500 futures (ES) using NautilusTrader and Interactive Brokers.

## Strategy Description

The strategy is very simple and is meant for testing purposes:
- Enters a long position every 10th 1-minute candle
- Exits the position on the 3rd candle after entry

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Interactive Brokers credentials:
   - Open `main.py`
   - Replace `YOUR_IB_USERNAME` with your IB username
   - Replace `YOUR_IB_PASSWORD` with your IB password
   - Replace `YOUR_IB_ACCOUNT` with your IB account ID

3. Make sure you have Docker installed and running on your system (required for the IB Gateway)

## Running the Strategy

1. Start the strategy:
```bash
python main.py
```

## Important Notes

- The strategy is configured to use paper trading by default. To switch to live trading, change `trading_mode="paper"` to `trading_mode="live"` in `main.py`
- The strategy uses the ES March 2024 contract (ESM24). Make sure to update the contract symbol if you want to trade a different expiration
- Always test thoroughly in paper trading mode before using real money
- Monitor the strategy's performance and adjust parameters as needed

## Disclaimer

This is a test strategy and should not be used for real trading without proper testing and risk management. Trading futures involves substantial risk of loss and is not suitable for all investors. 