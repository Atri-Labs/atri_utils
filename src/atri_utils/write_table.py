import pandas as pd

def write_table(df:pd.DataFrame, id_col='id', col_styles={}):
    """
    Returns a tuple containing rows and columns that can be provided to a Table component.
    Parameters
    ----------
    df : dataframe
        Contains the data that is to be displayed in the table. 
    id_col : string
        Column to be set as id of the table. 
    col_styles : dict, optional
        Additional styling parameters for each column
    Returns
    -------
    all_rows : list
        Array of rows for the Table.
    all_columns : list
        Array of columns for the Table.
    """
    df.rename(columns={id_col:'id'}, 
                        inplace=True)

    all_columns = []
    for i in range(0, len(df.columns.tolist())):
        # finding required params
        if df.columns.tolist()[i] == id_col:
            req_params = {'field': 'id', 'headerName': df.columns.tolist()[i]}
        else:
            req_params = {'field': df.columns.tolist()[i], 'headerName': df.columns.tolist()[i]}

        opt_params = {}
        # finding optional params
        if df.columns.tolist()[i] in col_styles:
            opt_params = col_styles[df.columns.tolist()[i]]

        # concatening required and optional params
        all_columns.append({**req_params, **opt_params})

    all_rows = df.to_dict(orient='records')

    return all_rows, all_columns