def format_currency(value, factor=100):
    return '{:.2f} €'.format(value / factor).replace('.', ',')
