# How many Thursdays were there between 1990 - 2000?

from datetime import date

start_date = date(1990, 1, 1)
# StartDate
end_date = date(2000, 12, 31)
# EndDate
days_middle = end_date - start_date

print(int(days_middle.days / 7 + 1))
#Adding 1 for remainder value, if not properly divisible
