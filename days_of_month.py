import datetime
from dateutil import relativedelta


def first_day_of_month(date):
    first_day = date.replace(day=1)
    return first_day


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


if __name__ == '__main__':

    # for month in range(1,13):
    #     day = datetime.date(2016, month, 1)
    #     print(first_day_of_month(day))
    #     print(last_day_of_month(day))

    today = datetime.datetime.today()
    longtimeago = datetime.datetime.strptime('2015-01-01', "%Y-%m-%d")
    for m in range(1, 36):
        rd = relativedelta.relativedelta(months=m)
        print(longtimeago + rd)

    print(relativedelta.relativedelta(today, longtimeago))

    longtime = longtimeago
    while (longtime < today):
        longtime += relativedelta.relativedelta(months=1)
        if (longtime < today):
            print(longtime)
