"""
Format sample feature data as Parquet for bulk ingestion into Feast
"""
import datetime
import pandas as pd


DATES = [
    datetime.datetime.now() + datetime.timedelta(hours=-1),
    datetime.datetime.now() + datetime.timedelta(hours=-2),
    datetime.datetime.now() + datetime.timedelta(hours=-3),
    datetime.datetime.now() + datetime.timedelta(hours=-4),
]
# user_name, age, purchases, visit_frequency, active_cart
USER_DATA = [
    ('janet',   34, 108, 1.33, 0),
    ('oscar',   65,  41, 4.72, 1),
    ('rodolfo', 21, 323, 8.59, 1),
    ('marilyn', 55,  12, 0.17, 0),
]

if __name__ == '__main__':
    #
    cols = list(zip(*USER_DATA))
    #
    user_data = pd.DataFrame.from_dict({
        'event_timestamp': DATES,
        'user_name': cols[0],
        'age': cols[1],
        'purchases': cols[2],
        'visit_frequency': cols[3],
    })
    userDataFileName = 'user_data.parquet'
    user_data.to_parquet(userDataFileName, compression='None')
    print('created "%s"' % userDataFileName)
    #
    active_cart = pd.DataFrame.from_dict({
        'event_timestamp': DATES,
        'user_name': cols[0],
        'active_cart': cols[4],
    })
    activeCartFileName = 'active_cart.parquet'
    active_cart.to_parquet(activeCartFileName, compression='None')
    print('created "%s"' % activeCartFileName)
