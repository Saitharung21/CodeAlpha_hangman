
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 135.00,
    "MSFT": 375.00,
    "AMZN": 145.00,
    "NVDA": 450.00,
    "META": 320.00,
    "JPM": 155.00,
    "V": 235.00,
    "WMT": 160.00
}

def display_available_stocks():
    """Display available stocks and their prices"""
    print("\n" + "="*50)
    print("AVAILABLE STOCKS")
    print("="*50)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol}: ${price:.2f}")
    print("="*50)

def get_user_portfolio():
    """Get stock holdings from user input"""
    portfolio = {}
    print("\nEnter your stock holdings (type 'done' when finished):")
    
    while True:
        symbol = input("\nEnter stock symbol: ").strip().upper()
        
        if symbol == 'DONE':
            break
            
        if symbol not in STOCK_PRICES:
            print(f"Error: '{symbol}' not found in available stocks.")
            continue
            
        try:
            quantity = int(input(f"Enter quantity for {symbol}: "))
            if quantity <= 0:
                print("Quantity must be a positive number.")
                continue
                
            portfolio[symbol] = portfolio.get(symbol, 0) + quantity
            print(f"Added {quantity} shares of {symbol}")
            
        except ValueError:
            print("Please enter a valid number for quantity.")
            continue
            
    return portfolio

def calculate_total_investment(portfolio):
    """Calculate total investment value"""
    total_value = 0.0
    holdings = []
    
    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        value = price * quantity
        total_value += value
        holdings.append({
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'value': value
        })
    
    return total_value, holdings

def display_results(portfolio, total_value, holdings):
    """Display investment results"""
    print("\n" + "="*60)
    print("INVESTMENT SUMMARY")
    print("="*60)
    
    for holding in holdings:
        print(f"{holding['symbol']}: {holding['quantity']} shares "
              f"@ ${holding['price']:.2f} = ${holding['value']:.2f}")
    
    print("-" * 60)
    print(f"TOTAL INVESTMENT VALUE: ${total_value:.2f}")
    print(f"NUMBER OF HOLDINGS: {len(portfolio)}")
    print("="*60)

def save_to_file(portfolio, total_value, holdings, filename):
    """Save results to a file"""
    try:
        if filename.endswith('.csv'):
            # Save as CSV
            with open(filename, 'w') as f:
                f.write("Stock Symbol,Quantity,Price Per Share,Total Value\n")
                for holding in holdings:
                    f.write(f"{holding['symbol']},{holding['quantity']},"
                           f"{holding['price']:.2f},{holding['value']:.2f}\n")
                f.write(f"\nTotal,,,{total_value:.2f}")
        else:
            # Save as text file
            with open(filename, 'w') as f:
                f.write("STOCK PORTFOLIO REPORT\n")
                f.write("=" * 40 + "\n\n")
                for holding in holdings:
                    f.write(f"{holding['symbol']}: {holding['quantity']} shares "
                           f"@ ${holding['price']:.2f} = ${holding['value']:.2f}\n")
                f.write("\n" + "-" * 40 + "\n")
                f.write(f"TOTAL INVESTMENT: ${total_value:.2f}\n")
                f.write(f"NUMBER OF HOLDINGS: {len(portfolio)}\n")
        
        print(f"\nResults saved successfully to {filename}")
        
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    """Main function to run the stock tracker"""
    print("💰 SIMPLE STOCK TRACKER")
    print("=" * 30)
    
    # Display available stocks
    display_available_stocks()
    
    # Get user portfolio
    portfolio = get_user_portfolio()
    
    if not portfolio:
        print("\nNo stocks were added. Exiting...")
        return
    
    # Calculate total investment
    total_value, holdings = calculate_total_investment(portfolio)
    
    # Display results
    display_results(portfolio, total_value, holdings)
    
    # Ask if user wants to save results
    save_choice = input("\nWould you like to save these results to a file? (y/n): ").lower()
    
    if save_choice in ['y', 'yes']:
        filename = input("Enter filename (with .txt or .csv extension): ").strip()
        if not filename:
            filename = "stock_portfolio.txt"
        save_to_file(portfolio, total_value, holdings, filename)
    
    print("\nThank you for using the Simple Stock Tracker!")

if __name__ == "__main__":
    main()

