There is my code which I wrote for employers.\
Some information may be hidden in description, but code is untouched.

<h1>Task_1</h1>

deeds.py\
deeds.json\
**Taske description:**\
It is necessary to obtain data from the website: \
http://www.???.com/ \
Specifically, for this task, you need to collect data from the page (Land Court section): \
http://www.???.com/Searches/ImageSearch.aspx \
Get data on all DEED documents for the current year (2020).
It is enough to parse only the data from the "preview" (what appears when you click on the button
view, no need to parse)
Output data in json format to output (you can output one at a time, no need
accumulate everything).

List of required fields and their format: \
date: datetime \
type: str \
book: str \
page_num: str \
doc_num: str \
city: str \
description: str \
cost: float \
street_address: str \
state: str \
zip: str 

There are no separate columns for some fields, but all the information is in others.
columns, the values of which will have to be resolved. Some field values may
be absent, so you need to use None.

This application should be written in Python (version> = 3.4) using
Scrapy.
All other packages at your discretion (however, do not get involved in this, for example,
install Java to parse text)
