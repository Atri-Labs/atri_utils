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

    def helper_parse_charts_2(df: pd.DataFrame):
        if 'name' not in set(df.columns):
            df.rename(columns={args['name']: 'name'}, inplace=True)
        if 'value' not in set(df.columns):
            df.rename(columns={args['value']: 'value'}, inplace=True)
        return df[['name', 'value']].to_dict(orient='records')

    if type_chart == 'bar' or type_chart == 'line' or type_chart == 'area':
        if args['x'] in set(data.columns):
            data.rename(columns={args['x']: 'x'}, inplace=True)
        data_processed = data.to_dict(orient='records')
        return data_processed
    elif type_chart == 'scatter':
        data_processed = []
        if type(data) == list:
            for d in data:
                data_processed.append(helper_parse_charts(d))
        else:
            data_processed.append(helper_parse_charts(data))
        return data_processed
    elif type_chart == 'histogram':
        if 'x' not in set(data.columns):
            data.rename(columns={args['x']: 'x'}, inplace=True)
        if 'y' not in set(data.columns):
            data.rename(columns={args['y']: 'y'}, inplace=True)
        return data[['x', 'y']].to_dict(orient='records')
    elif type_chart == 'candlestick':
        data_processed = []
        for i in data.columns:
            dic = {}
            data_curr = data[i]
            dic['name'] = i
            dic['median'] = int(data_curr.median())
            dic['average'] = int(data_curr.mean())
            dic['min'] = int(data_curr.min())
            dic['max'] = int(data_curr.max())
            dic['lowerQuartile'] = int(data_curr.quantile(q=0.25))
            dic['upperQuartile'] = int(data_curr.quantile(q=0.75))
            data_processed.append(dic)
        return data_processed
    elif type_chart == 'pie':
        data_processed = []
        data_processed.append(helper_parse_charts_2(data))
        if 'data2' in set(args.keys()):
            data_processed.append(helper_parse_charts_2(args['data2']))
        return data_processed



