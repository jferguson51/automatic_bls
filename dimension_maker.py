import csv

from sqlalchemy import create_engine
import pandas as pd

def dim_maker(df, engine, output_table):

    pd.DataFrame.to_sql(df, con=engine, name=output_table, 
        if_exists='append', index=False)

    #dd_statement = "CREATE TABLE dedupe as SELECT * FROM %(opt)s WHERE 1 "
    #" GROUP BY %(col_zero)s, %(col_one)s;" % {"opt": output_table, "col_zero":\
    # df.columns[0], "col_one": df.columns[1]}
    #drop_statement = "DROP TABLE %(opt)s;" % {"opt": output_table}
    #rename_statement = "RENAME TABLE dedupe TO %(opt)s;" % {"opt": output_table}

    engine.execute("CREATE TABLE dedupe as SELECT * FROM %(opt)s WHERE 1 "
    " GROUP BY %(col_zero)s, %(col_one)s;" % {"opt": output_table, "col_zero":\
     df.columns[0], "col_one": df.columns[1]})
    engine.execute("DROP TABLE %(opt)s;" % {"opt": output_table})
    engine.execute("RENAME TABLE dedupe TO %(opt)s;" % {"opt": output_table})
    return

print "Welcome to the Atlas Dimension Populator 3000"

with open ('sql_engine.txt', 'r') as f:
    engine_address = f.read()
engine = create_engine(engine_address)

pre_df = pd.read_csv("prefix.csv")
dim_maker(pre_df, engine, "dim_prefix")

for x in range(0, len(pre_df.index), 1):
    p = pre_df['prefix'].iloc[0]
    geo_df = pd.read_csv(p + "/geo_codes.csv")
    mc_df = pd.read_csv(p + "/measure_codes.csv",
        converters={'measure_code': lambda x: str(x)})
    geo_df['db_prefix'] = p
    mc_df['db_prefix'] = p
    dim_maker(geo_df, engine, "dim_geo")
    dim_maker(mc_df, engine, "dim_mc")

print "to the moon!"
