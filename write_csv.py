import csv, os

def write_csv(file_path, stock_data):
    """
    Write data to csv file.

    Parameters:
    stock_data (dict): symbol (str), datetime (str), price (str) as keys. 
    """

    # Check the file exists.
    if os.path.exists(file_path):
        # If exists, append to the file.
        with open(file_path, "a", newline="") as file:
            fieldnames = ['date', 'price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'date': stock_data["date"], 'price': stock_data["price"]})
    else:
        # Does not exist, create a new file.
        with open(file_path, "x", newline="") as file:
            fieldnames = ['date', 'price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'date': stock_data["date"], 'price': stock_data["price"]})


if __name__ == "__main__":

    # Test write to csv file
    stock_data = {
        "symbol": "MDX",
        "date": "13 Jun 2025",
        "price": str(1.26),
    }
    # file_path = f"csv/{stock_data["symbol"]}.csv"
    file_path = os.path.join("data_csv", stock_data["symbol"] + ".csv")


    write_csv(file_path, stock_data)