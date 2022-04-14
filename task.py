# -*- coding: utf-8 -*-
import sqlite3
import sys

import numpy
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

    # There is a dict building with dict comprehensions
    df_dict = {
        (factor, year):
            sum(item['res'] if item['res'] is not None else 0 for item in sql_result
                if item['year'] == year and item['factor'] == factor)
            if year in set(item['year'] for item in sql_result if item['factor'] == factor) else numpy.NaN
        for year in range(2006, 2021)
        for factor in set(item['factor'] for item in sql_result)
    }

    # There is a dict building process with traditional "for" loops
    # Result is similar with dict comprehension approach
    # df_dict = {}
    # factors = set(item['factor'] for item in sql_result)
    # for factor in factors:
    #     years = set(item['year'] for item in sql_result if item['factor'] == factor)
    #     for year in range(2006, 2021):
    #         if year in years:
    #             all_res = (
    #                 item['res'] if item['res'] is not None else 0 for item in sql_result
    #                 if item['year'] == year and item['factor'] == factor
    #             )
    #             df_dict[(factor, year)] = sum(all_res)
    #         else:
    #             df_dict[(factor, year)] = numpy.NaN

    df = pandas.DataFrame(df_dict, index=('world',))

