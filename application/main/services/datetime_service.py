from datetime import datetime

def dt(dt_str):
    return datetime.strptime(dt_str, "%Y/%m/%d %H:%M:%S:%f")

def string(dt):
    return dt.strftime("%Y/%m/%d %H:%M:%S:%f")[:-3]