import pandas as pd
from typing import Union


def parse_charts_data(data: Union[pd.DataFrame, list], type_chart: str, **args):
    """
    data: It is either a DataFrame(bar) or list of DataFrames(scatter)
    type_chart: It can currently have values 'bar', 'scatter', 'line', 'area', 'histogram', 'candlestick', 'pie'
    **args : currently can accept x, y, z, name, value, OuterData
    x value is to be specified for type_chart == 'bar' if the column you want to see on th x-axis is not named x
    x, y, z values are to be specified when type_chart == 'scatter' if the DataFrame does not already contain these columns
    name, value are to specified only when type_chart == 'pie' giving information about column containing the name and the respective value
    OuterData is to specified only when type_chart == 'pie' and you want an Outer pie chart surroeding the inner Chart OuterData is of type pd.DataFrame

    returns based on a type_chart either an array of dict's (bar) or array of array of dict's (scatter)
    """
    def scatter_charts_helper(df: pd.DataFrame):
        """
        It's a helper function to parse a DataFrame and rename columns specified to x, y, z
        To easily return the Data required by the Scatter Chart instance
        """
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

    def pie_charts_helper(df: pd.DataFrame):
        """
        It's a helper function to parse a DataFrame and rename columns specified to name, value
        To easily return the Data required by the Pie Chart instance
        """
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
                data_processed.append(scatter_charts_helper(d))
        else:
            data_processed.append(scatter_charts_helper(data))
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
        data_processed = [pie_charts_helper(data)]
        if 'outerData' in set(args.keys()):
            data_processed.append(pie_charts_helper(args['outerData']))
        return data_processed


def parse_charts_options(**args):
    pass


def draw_charts(chart, data: Union[pd.DataFrame, list], type_chart: str, **kwargs):
    chart.custom.data = parse_charts_data(data=data, type_chart=type_chart, **kwargs)
    if type_chart == 'pie' and 'outerData' in set(kwargs.keys()):
        chart.custom.options = [
                    # options for first circle
                    {
                        "cx": "50%",            # center of the circle's x
                        "cy": "50%",            # center of the circle's y
                        "outerRadius": "40%",   # radius of the circle
                        "showLabel": True,
                        "animate": False,
                    },
                    # options for second circle
                    {
                        "cx": "50%",
                        "cy": "50%",
                        "innerRadius": "65%",
                        "showLabel": True,
                        "animate": False,
                    },
                    ]





