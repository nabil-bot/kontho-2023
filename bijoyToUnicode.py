# -*- coding:utf-8 -*-
import io

with io.open("CN.txt", 'r', encoding="utf-8") as f:
    country_name_str = f.read()
c_english = country_name_str.split(",")

with io.open("CB.txt", 'r', encoding="utf-8") as f:
    country_name_str = f.read()
c_Bangla = country_name_str.split(",")

print(len(c_english))
print(len(c_Bangla))

