import pandas as pd
import statistics
import math
import csv


def get_approximately_right_dates_for_price_data(income_data, shareprices_file):

    """ 
    Create unique dates for each ticker
    """

    TICKER_PRICE_DATES = {}

    for tick in income_data.Ticker.unique():
        q_dates = income_data.loc[income_data['Ticker'] == tick].Publish_Date.unique()
        TICKER_PRICE_DATES[tick] = q_dates

    with open(shareprices_file) as csv_file, open('edited-prices.csv', 'w') as out:
        reader = csv.reader(csv_file, delimiter=';')
        writer = csv.writer(out, delimiter=';')
        for line in reader:
            if line[2] in TICKER_PRICE_DATES.get(line[0], []):
                writer.writerow(line)

    price_data = price_data[~price_data['Close'].isin(q_dates)]

def main():
    income_data = pd.read_csv('us-income-quarterly.csv', sep=';')
    income_data.columns = [c.replace(' ', '_') for c in income_data.columns]

    price_data = pd.read_csv('edited-prices.csv', sep=';')
    price_data.columns = [c.replace(' ', '_') for c in price_data.columns]

    correlations = {}

    for tick in income_data.Ticker.unique():

        data_length = income_data.loc[income_data['Ticker'] == tick].index

        if len(data_length) < 10:
            continue

        merged_data = pd.merge(left=income_data.loc[income_data['Ticker'] == tick], right=price_data.loc[price_data['Ticker'] == tick], left_on='Publish_Date', right_on='Date')

        column_1 = merged_data["Operating_Income_(Loss)"]
        column_2 = merged_data["Close"]

        correlation = column_2.corr(column_1)
        correlations[tick] = correlation if (correlation and not math.isnan(correlation)) else None

        fixed_corrs = [corr for corr in correlations.values() if (corr and not math.isnan(corr))]

    print(statistics.mean(fixed_corrs))
    print(correlations)


if __name__ == "__main__":
    main()