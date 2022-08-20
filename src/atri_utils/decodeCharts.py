import pandas as pd
from typing import Union


def parse_charts(data: Union[pd.DataFrame, list], type_chart: str, **args):
    """
    data: It is either a DataFrame(bar) or list of DataFrames(scatter)
    type_chart: It can currently have values 'bar', 'scatter'
    **args : currently can accept x, y, z

    returns based on a type_chart either an array of dict's (bar) or array of array of dict's (scatter)
    """
    def helper_parse_charts(df: pd.DataFrame):
        columns = set(df.columns)
        if args['x'] in columns:
            df.rename(columns={args['x']: 'x'}, inplace=True)
        if args['y'] in columns:
            df.rename(columns={args['y']: 'y'}, inplace=True)
        if args['z'] in columns:
            df.rename(columns={args['z']: 'z'}, inplace=True)
        columns = set(df.columns)
        if 'x' not in columns or 'y' not in columns or 'z' not in columns:
            raise Exception(
                'Either x,y,z values were not passed or the DataFrame passed does not contain columns x,y,z')
        return df.to_dict(orient='records')

    if type_chart == 'bar':
        if args['x'] in set(data.columns):
            data.rename(columns={args['x']: 'x'}, inplace=True)
        data_processed = data.to_dict(orient='records')
        print(data_processed)
        return data_processed
    elif type_chart == 'scatter':
        data_processed = []
        if type(data) == list:
            for d in data:
                data_processed.append(helper_parse_charts(d))
        else:
            data_processed.append(helper_parse_charts(data))
        return data_processed

