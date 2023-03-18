
# import unicodedata
import pandas

list = [[1, 100, 0.33, '半角AAA', 'AAA100'], 
            [2, 200, 0.67, 'AAAAAAAAAAAABBB', 'BBB200'], 
            [3, 300, 1, 'CCC', 'CCC300'], 
            [4, 400, 1.33, 'DDD', 'DDD400'], 
            [5, 500, 1.67, 'EEE', 'EEE500'], 
            [6, 600, 2, 'FFF', 'FFF600']
]
title = ['番号','年齢','血圧','肺活量','AAA']
# pandas.options.display.max_colwidth=10
pandas.set_option('display.unicode.east_asian_width', True)

df = pandas.DataFrame(list,columns=title)
# print(df)
print(df.to_string(index=False, justify='left'))

