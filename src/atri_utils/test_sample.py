from .decodeCharts import parse_charts
from .uploaded_files import parse_uploaded_file
import pandas as pd
import os
import requests
import numpy as np


def test_1_parse_charts():
    st = ",price,sales,kids\n0,10,230,2\n1,20,130,0\n2,30,300,4\n3,40,340,7\n4,50,110,1\n5,60,30,12\n6,70,900,4"
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'test1.csv'
    with open(file_path, 'w') as f:
        f.write(st)
    df = pd.read_csv(file_path, index_col=0)
    os.remove(file_path)
    assert parse_charts(df, 'bar', x='price') == [{'x': 10, 'sales': 230, 'kids': 2}, {'x': 20, 'sales': 130, 'kids': 0}, {'x': 30, 'sales': 300, 'kids': 4}, {'x': 40, 'sales': 340, 'kids': 7}, {'x': 50, 'sales': 110, 'kids': 1}, {'x': 60, 'sales': 30, 'kids': 12}, {'x': 70, 'sales': 900, 'kids': 4}]


def test_2_parse_upload():
    response = requests.get("https://i.imgur.com/ExdKOOz.png")
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'test2.png'
    with open(file_path, "wb") as file:
        file.write(response.content)
    assert type(parse_uploaded_file('test2.png')) == np.ndarray
    os.remove(file_path)

