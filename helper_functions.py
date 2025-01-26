def calculate_total_value(units, price, action):
    if action == 'sell':
        total_value = units*price*-1
    else:
        total_value = units*price
    
    return total_value