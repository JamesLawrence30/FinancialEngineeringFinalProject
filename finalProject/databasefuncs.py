import requests, json, sqlite3, copy

def get_stock_data(stock_symbols):
    iex_uri = 'https://api.iextrading.com/1.0/tops?symbols=' + ",".join(stock_symbols)
    # print("Retrieving from {}".format(iex_uri))
    response = requests.get(iex_uri)
    return response.json()


def insert_into_TransactionHistory(connection, StockType, Quantity, BuyOrSell, Price, Value):
    c = connection.cursor()
    c.execute("insert into TransactionHistory values ('{}', {}, '{}', {}, {})".format(TypeOfStock, userquantity, BuyOrSell, stockprice, value))
    connection.commit()

def get_portfolio(connection):
    c = connection.cursor()
    c.execute("select Ticker, Quantity from portfolio")
    Records = c.fetchall()
    TickerQuantities = {}
    for x in Records:
        TickerQuantities[x[0]] = x[1]BuyOrSell
    return TickerQuantities

def update_portfolio(connection, Ticker, Quantity):
    c = connection.cursor()
    c.execute("update portfolio set Quantity = {} where Ticker = '{}'".format(new_quantity, TypeOfStock))
    connection.commit()


if __name__ == '__main__':
    symbols = ['AAPL', 'FB', 'SNAP']
    content = get_stock_data(symbols)
    value = 0
    conn = sqlite3.connect('database')

    # get_stock_data returns an array of dicts, where each dict contains data for a given stock. Format is displayed
    # by the following print statement
    #print(json.dumps(content, indent=1) + "\n")

    while True:
        BuyOrSell = input("Please select B if you would like to buy stock, S if you would like to sell Stock, or P if you would like to view your portfolio: ")

        if BuyOrSell == 'B' or BuyOrSell == 'S':
            TypeOfStock = input("Select from the following AAPL, FB, SNAP: ")

            # Data can be extracted in the following way:
            #if symbols['symbol'] == TypeOfStock
            for stock_data in content:
                #print(stock_data['symbol'] + ": " + str(stock_data['askPrice']))
                if stock_data['symbol'] == TypeOfStock and BuyOrSell == 'B':
                    stockprice = (stock_data['askPrice'])
                if stock_data['symbol'] == TypeOfStock and BuyOrSell == 'S':
                    stockprice = (stock_data['bidPrice'])
            #print(stockprice)

            userquantity = input("Enter a quantity: ")
            userquantity = int(userquantity)
            portfolio = get_portfolio(conn)
            current_quantity = portfolio[TypeOfStock]

            if BuyOrSell == 'S':
                if userquantity > current_quantity:
                    print("You can't sell more socks than you have, you currently have " + str(current_quantity) + " stocks")
                    input("Press any key to continue")
                    continue

            if BuyOrSell == 'B':
                value = int(userquantity)*stockprice
                pnL = int(userquantity)*stockprice*(-1)
            elif BuyOrSell == 'S':
                value = int(userquantity)*stockprice*(-1)
                pnL = int(userquantity)*stockprice
            else:
                print('Invalid input')
            #print(value)

            insert_into_TransactionHistory(conn, TypeOfStock, userquantity, BuyOrSell, stockprice, value)

            new_quantity = portfolio[TypeOfStock]
            if BuyOrSell == 'B':
                new_quantity += userquantity
            elif BuyOrSell == 'S':
                new_quantity -= userquantity

            update_portfolio(conn, TypeOfStock, userquantity)

        elif BuyOrSell == 'P':
            portfolio = get_portfolio(conn)
            portfolio_quantity = copy.copy(portfolio)
            for stock_data in content:
                portfolio[stock_data['symbol']]*= stock_data['bidPrice']
            print("This is your portfolio: ")
            print("Stock quantities: " + str(portfolio_quantity))
            print("Current Value: " + str(sum(portfolio.values())))

        else:
            print("You did not select a valid ticker")


