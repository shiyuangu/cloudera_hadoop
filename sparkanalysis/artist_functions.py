def fix_year(line):
    # This function fixes two digit and negative years
    (id, name, year) = line.strip().split('\t')
    year = int(year)
    # If the year is negative, return the absolute value
    if year < 0:
        year = abs(year)
    # If the year is two digits, add 1900
    if year < 100:
        year += 1900

    return "%s\t%s\t%s" % (id, name, str(year))
