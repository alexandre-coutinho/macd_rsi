import config as k
import pandas as pd
import ccxt
import pandas_ta as ta
import telegramBot
from datetime import datetime, time
import time as time_module


def get_binance_client():
    """Inicializa e retorna cliente da Binance."""
    return ccxt.binance({
        'enableRateLimit': True,
        'apiKey': k.binancekey,
        'secret': k.binancesecret,
        'adjustForTimeDifference': True,
        'options': {
            'defaultType': 'future',
            'recvWindow': 50000,
        },
    })


def calculate_indicators(df):
    """Calcula EMAs e RSI no dataframe."""
    for ema_length in [9, 21, 50]:
        df[f'EMA_{ema_length}'] = ta.ema(df['fechamento'], length=ema_length)
    
    df['RSI'] = ta.rsi(df['fechamento'], length=14)
    df.ta.macd(close='fechamento', fast=34, slow=48, signal=30, append=True)
    return df


def check_trend_btc(df):
    """Verifica tendência geral no BTC."""
    fechamento = df.iloc[-1]['fechamento']
    ema_50 = df.iloc[-1]['EMA_50']
    ema_9 = df.iloc[-1]['EMA_9']
    ema_21 = df.iloc[-1]['EMA_21']
    
    if fechamento >= ema_50 and ema_9 >= ema_21:
        return 'alta'
    elif fechamento <= ema_50 and ema_9 <= ema_21:
        return 'baixa'
    return None


def get_last_values(df):
    """Extrai últimos valores do dataframe."""
    return {
        'fechamento': df['fechamento'].iloc[-1],
        'rsi': df['RSI'].iloc[-1],
        'ema_9': df['EMA_9'].iloc[-1],
        'ema_21': df['EMA_21'].iloc[-1],
        'ema_50': df['EMA_50'].iloc[-1],
        'macd': df['MACD_34_48_30'].iloc[-1],
        'macd_signal': df['MACDs_34_48_30'].iloc[-1],
        'macd_prev': df['MACD_34_48_30'].iloc[-2],
        'macd_signal_prev': df['MACDs_34_48_30'].iloc[-2],
    }


def send_message(msg, telegram=False):
    """Envia mensagem ao prompt e opcionalmente ao Telegram."""
    print(msg)
    if telegram:
        telegramBot.envia_msg(msg)


def analyze_symbol(binance, symbol, timeframe, trend):
    """Analisa um símbolo específico."""
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    df = pd.DataFrame(bars, columns=['time', 'abertura', 'max', 'min', 'fechamento', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms', utc=True).map(lambda x: x.tz_convert('America/Sao_Paulo'))
    
    df = calculate_indicators(df)
    values = get_last_values(df)
    
    macd_cruza_acima = values['macd'] >= values['macd_signal'] and values['macd_prev'] <= values['macd_signal_prev']
    macd_cruza_abaixo = values['macd'] <= values['macd_signal'] and values['macd_prev'] >= values['macd_signal_prev']
    
    acao = "SEM TENDENCIA"
    
    if trend == 'alta' and 50 <= values['rsi'] <= 70 and macd_cruza_acima:
        acao = "COMPRA"
    
    elif trend == 'baixa' and 30 <= values['rsi'] <= 50 and macd_cruza_abaixo:
        acao = "VENDA"
    
    trend_msg = f"Tendencia BTC: {trend.upper()}" if trend else "Tendencia BTC: INDEFINIDA"
    return f"{symbol} - {acao} (RSI: {values['rsi']:.2f} | MACD: {values['macd']:.4f}) | {trend_msg}"


def run_bot():
    """Função principal do bot."""
    send_message("=== INICIANDO BOT - Pressione Ctrl+C para parar ===")
    
    symbols = ['ADA/USDT', 'AVAX/USDT', 'BCH/USDT', 'BTC/USDT', 'DOT/USDT', 
               'ETH/USDT', 'LINK/USDT', 'LTC/USDT', 'SOL/USDT', 'SUI/USDT', 
               'TRUMP/USDT', 'XLM/USDT', 'XRP/USDT']
    timeframe = '2h'
    
    while True:
        binance = get_binance_client()
        
        send_message(f"\n{'='*50}")
        send_message(f"BOT MACD - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        send_message(f"{'='*50}")
        
        regras = """
CRITERIOS DE ANALISE:
- COMPRA: Tendencia alta no BTC + RSI 50-70 + MACD cruza acima
- VENDA: Tendencia baixa no BTC + RSI 30-50 + MACD cruza abaixo
- SEM TENDENCIA: Nao atende aos criterios acima
"""
        send_message(regras)
        
        bars = binance.fetch_ohlcv('BTC/USDT', timeframe='5m', limit=75)
        df_btc = pd.DataFrame(bars, columns=['time', 'abertura', 'max', 'min', 'fechamento', 'volume'])
        df_btc = calculate_indicators(df_btc)
        trend = check_trend_btc(df_btc)
        
        send_message(f"Tendência geral: {trend.upper()}" if trend else "Tendencia BTC: INDEFINIDA")
        
        for idx, symbol in enumerate(symbols, 1):
            send_message(f"\nAnalisando {idx}/{len(symbols)} - {symbol}")
            result = analyze_symbol(binance, symbol, timeframe, trend)
            
            if "COMPRA" in result or "VENDA" in result:
                send_message(result, telegram=True)
            else:
                send_message(result)
        
        send_message(f"\n=== FIM DO CICLO - Aguardando 5 minutos ===")
        time_module.sleep(300)


if __name__ == '__main__':
    run_bot()
        