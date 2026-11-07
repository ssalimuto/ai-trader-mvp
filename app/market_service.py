async def get_mock_market_snapshot(symbol: str):
    symbol = symbol.upper()
    prices = {
        "BTCUSD": 67234.15,
        "ETHUSD": 3510.44,
        "AAPL": 214.87,
        "EURUSD": 1.09
    }
    return {"symbol": symbol, "price": prices.get(symbol, 100.0)}
