# AlgoEdge Pro

AlgoEdge Pro is an institutional-grade, no-code algorithmic trading platform. Traders can design, backtest, optimize, and deploy automated strategies without writing code.

## Core Capabilities
- No-code strategy builder (drag-and-drop): Indicators, Entry/Exit conditions, Risk rules
- Indicators: EMA, SMA, RSI, MACD, Bollinger Bands, Fibonacci, VWAP, and basic ICT/SMC structures (FVG, BOS, Order Blocks)
- AI-assisted strategy completion and parameter suggestions
- Backtesting and optimization across Forex, Crypto, and Stocks (5–10y) with key metrics: Win Rate, Profit Factor, Max Drawdown, Sharpe
- Live execution with broker integrations: MT4/MT5, Binance, Alpaca, Interactive Brokers (stubs included)
- Strategy marketplace for publishing and copying strategies
- Risk management dashboard with daily limits, equity protection, and news filters
- User profiles and leaderboards

## Monorepo Structure
```
/workspace/algoedge-pro
  apps/
    web/                     # Next.js React app (no-code builder, dashboards)
  python/
    algoedge/                # Shared Python engine
      __init__.py
      strategy_dsl.py       # DSL schema + parsing
      backtester.py         # Backtesting engine + metrics
      optimizer.py          # Parameter search (Optuna-like stub)
      indicators.py         # Technical indicators (pandas/ta wrappers)
      ict.py                # ICT/SMC structure detection (basic stubs)
      data.py               # Data loaders (crypto/forex/stocks) with fallbacks
      connectors/
        __init__.py
        binance.py
        alpaca.py
        ib.py
        mt5.py
  services/
    api/                     # FastAPI service
      main.py
      routers/
        strategies.py
        webhooks.py
        live.py
        leaderboard.py
      core/
        config.py
        database.py
      models/
        base.py
        user.py
        strategy.py
        runs.py
        marketplace.py
      schemas/
        strategy.py
        common.py
      tasks/
        celery_app.py
        jobs.py
      requirements.txt
      Dockerfile
    worker/                  # Celery worker service
      requirements.txt
      Dockerfile
  docker-compose.yml
  .env.example
```

## Quick Start (Docker Compose)
1. Copy env file and set secrets
```
cp .env.example .env
```
2. Build and start
```
docker compose up --build
```
- API: http://localhost:8000/docs
- Web: http://localhost:3000

## Notes
- Data connectors currently include basic implementations; you will need API keys for live data and execution
- Some features ship as stubs to enable rapid iteration (e.g., ICT structures, MT4/5)
- Optimizer uses a simple random/grid search initially; can be upgraded to Optuna/Nevergrad
- Strategy DSL enables versioned, portable strategies between UI and engine

## Monetization
- SaaS subscriptions (tiers by strategy slots & data access)
- Marketplace transaction fees (default 20%)

## Security & Compliance
- API keys and credentials are never stored in code. Use environment variables or a secrets manager
- Respect broker/exchange terms and paper-trade before live trading

## License
Proprietary. All rights reserved.