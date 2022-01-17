from datetime import date, datetime

dateformat = "%b %d %Y %H:%M:%S"

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.strftime(dateformat)
    raise TypeError ("Type %s not serializable" % type(obj))