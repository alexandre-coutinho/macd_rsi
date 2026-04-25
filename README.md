# Bot MACD RSI

Bot de análise técnica para trading de criptomoedas na Binance Futures.

## Descrição

Este bot analisa mercados de criptomoedas utilizando os indicadores técnicos MACD e RSI para identificar sinais de compra e venda.

## Indicadores Utilizados

- **EMA**: Médias móveis exponenciais (9, 21, 50)
- **RSI**: Relative Strength Index (período 14)
- **MACD**: (34, 48, 30)

## Critérios de Análise

- **COMPRA**: Tendência de alta no BTC + RSI entre 50-70 + MACD cruzando acima do signal
- **VENDA**: Tendência de baixa no BTC + RSI entre 30-50 + MACD cruzando abaixo do signal
- **SEM TENDENCIA**: Não atende aos critérios acima

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Edite o arquivo `config.py` com suas credenciais da API da Binance:

```python
binancekey = 'sua_api_key'
binancesecret = 'seu_api_secret'
```

## Usage

```bash
python MacdRsi.py
```

O bot analisa os seguintes símbolos cada ciclo:
ADA/USDT, AVAX/USDT, BCH/USDT, BTC/USDT, DOT/USDT, ETH/USDT, LINK/USDT, LTC/USDT, SOL/USDT, SUI/USDT, TRUMP/USDT, XLM/USDT, XRP/USDT

Timeframe: 2h
Ciclo: A cada 5 minutos

## Arquivos

- `MacdRsi.py`: Main do bot
- `config.py`: Configurações de API
- `telegramBot.py`: Módulo de notificação Telegram

## Aviso

Este bot é apenas para fins educacionais. Use por sua conta e risco.