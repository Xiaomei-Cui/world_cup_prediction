介绍：匹配GDP原始数据中国家的ISO3代码与世界杯参赛国家的完整名字，最后将参赛国的GDP数据总结
worldcup country01.py：利用country.CSV文件中国家的ISO3代码，将country_data.csv中的国家名字进行匹配，匹配结果保存为country_out.csv
worldcup country02.py：筛选出在used country.txt但不在匹配结果中的国家
worldcup country03.py：筛选出used country.txt中的国家在GDP.csv中的数据，并保存为GDP in cup.csv
country.CSV：国家的ISO3代码
used country.txt：世界杯参赛国的名字
country_data.csv：原始数据
country_out.csv：匹配国家名后数据
GDP.csv：各国GDP原始数据
GDP in cup.csv：匹配、筛选后数据