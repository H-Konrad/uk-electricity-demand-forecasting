def months_to_seasons(month):
    if 3 <= month < 6:
        return "Spring"
    elif 6 <= month < 9:
        return "Summer"
    elif 9 <= month < 12:
        return "Autumn"
    else:
        return "Winter"