from persiantools.jdatetime import JalaliDate

def gregorian_to_numeric_jalali(date):
    if date is None:
        return "نامشخص"
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)


def calculate_deadline(finished, started):
    if finished is None or started is None:
        return 'تاریخ نامشخص'
    diff = JalaliDate(finished) - JalaliDate(started)
    days = diff.days
    if days < 0:
        return None
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))

