# -*- coding: utf-8 -*-
import sqlite3
import sys
import time

import pandas
from pathlib import Path

def dict_factory(cursor, row):
    dict_obj = {}
    for idx, col in enumerate(cursor.description):
        dict_obj[col[0]] = row[idx]
    return dict_obj

# init data
db_path = Path(sys.argv[0]).parent.joinpath('test_task_python', 'test.db')

# connecting to db
with sqlite3.connect(str(db_path)) as conn:
    conn.row_factory = dict_factory
    curs = conn.cursor()
    query = """
        SELECT factor, year, country, res FROM `testidprod`
        WHERE partner IS NULL
            AND state IS NULL
            AND bs = 0
            AND factor IN (1, 2)
    """
    curs.execute(query)
    sql_result = curs.fetchall()
    new_dict = {
        factor: {
            year: None for year in set(d['year'] for d in sql_result if d['factor'] == factor)
        } for factor in set(d['factor'] for d in sql_result)
    }
    print(new_dict)

    # for item in result:
    #     try:
    #         new_dict[item['factor']]
    #     except KeyError:
    #         new_dict[item['factor']] = {}
    #     a = new_dict[item['factor']]

    # df = pandas.DataFrame(result)
    # print(df)