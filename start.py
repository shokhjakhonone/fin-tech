from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objects as go
from io import BytesIO
import base64
import pandas as pd

app = Flask(__name__)

# Функция для получения данных компании (заглушка)
def get_company_data(ticker):
    # Здесь можно использовать API или базу данных для получения данных компании
    # Пример заглушки:
    data = {
        'revenue_growth': 0.15,
        'profit_margin': 0.25
    }
    return data

# Функция для анализа данных и создания графики
def analyze_data(ticker, start_date, end_date):
    # Получение данных о ценах акций
    sberbank_data = yf.download(ticker, start=start_date, end=end_date)

    # Создание колонки с ежедневными доходностями
    sberbank_data['Daily Returns'] = sberbank_data['Close'].pct_change()

    # График цен закрытия в стиле "trade futuristic"
    fig = go.Figure(data=[go.Candlestick(x=sberbank_data.index,
                open=sberbank_data['Open'],
                high=sberbank_data['High'],
                low=sberbank_data['Low'],
                close=sberbank_data['Close'])])
    fig.update_xaxes(title_text='Дата')
    fig.update_yaxes(title_text='Цена')
    fig.update_layout(template="plotly_dark")

    # Сохранение графика в HTML
    plot_div = fig.to_html(full_html=False)

    # Получение данных компании
    company_data = get_company_data(ticker)

    # Функция для анализа данных компании и выдачи рекомендаций
    def analyze_company_performance(data):
        recommendations = []

        if data['revenue_growth'] > 0.1:
            recommendations.append("У компании хороший рост выручки.")
        else:
            recommendations.append("Рост выручки компании может быть улучшен.")

        if data['profit_margin'] > 0.2:
            recommendations.append("Компания имеет высокую рентабельность.")
        else:
            recommendations.append("Рентабельность компании может быть улучшена.")

        return recommendations

    recommendations = analyze_company_performance(company_data)

    # Добавление информации о продуктах и их процентах
    products_data = [
        {'product': 'Кредитные карты', 'percent': 15},
        {'product': 'Дебетовые карты', 'percent': 10},
        {'product': 'Ипотека', 'percent': 5},
        # Другие продукты и проценты
    ]

    return plot_div, recommendations, products_data

@app.route('/')
def home():
    # Получение параметров из запроса GET
    ticker = request.args.get('ticker', 'SBER.ME')
    start_date = request.args.get('start_date', '2022-01-01')
    end_date = request.args.get('end_date', '2022-12-31')

    plot_div, recommendations, products_data = analyze_data(ticker, start_date, end_date)
    return render_template('index.html', plot_div=plot_div, recommendations=recommendations, products_data=products_data, ticker=ticker, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    app.run(port=8080)
