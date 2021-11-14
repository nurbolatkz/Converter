# Converter

In this project I wrote class with two methods. First method is converting database file to csv file. And second method is reading data from csv file and converting to database file. I putted two converting files. One of them converts data to SQLITE3 and another one converts data to Oracle database server. They have small differences, on the contrary there are more similarities.


## Getting started

Let's firsty descripe script which converts data to <b> Oracle database server</b>. Firstly we need to install ORACLE database, Oracle sql developer and connect it with each other. After that we need to create new connection in Oracle sql developer or we can use existing connection. In this project I used created connection. It is important for converting, because without connection we can't convert it to Oracle.

# First install modules and import them

`import csv

import cx_Oracle

import datetime`

## Create connection 

`conn = cx_Oracle.connect("User_name/password@//localhost:1521/xe") `

You can see connections details in Oracle sql developer.

[!img](https://github.com/nurbolatkz/Converter/blob/main/static/connection_details.png)

If we use connection details from image above we should write `conn = cx_Oracle.connect("User2/password@//localhost:1521/xe")`







