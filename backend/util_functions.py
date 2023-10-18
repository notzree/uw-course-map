def generate_term_code(year_month_tuple):
    year, month = year_month_tuple
    a = 0 if year < 2000 else 1
    yy = str(year)[-2:]
    m = str(month).zfill(2)
    return f"{a}{yy}{m}"
