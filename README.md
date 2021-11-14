# Converter

In this project I wrote class with two methods. First method is converting database file to csv file. And second method is reading data from csv file and converting to database file. I putted two converting files. One of them converts data to SQLITE3 and another one converts data to Oracle database server. They have small differences, on the contrary there are more similarities.


## Getting started

Let's firsty descripe script which converts data to <b> Oracle database server</b>. Firstly we need to install ORACLE database, Oracle sql developer and connect it with each other. After that we need to create new connection in Oracle sql developer or we can use existing connection. In this project I used created connection. It is important for converting, because without connection we can't convert it to Oracle.

# First install modules and import them

`
import csv, cx_Oracle, datetime
`

## Create connection 

`conn = cx_Oracle.connect("User_name/password@//localhost:1521/xe") `

You can see connections details in Oracle sql developer.

![img](https://github.com/nurbolatkz/Converter/blob/main/static/connection_details.png)

If we use connection details from image above we should write `conn = cx_Oracle.connect("User2/password@//localhost:1521/xe")`

### Describe Converter Class

Class converter contains two main methods and one additional method.

` def find_type(self, elem)` -> this additional method helps to us find type of each elemnt in csv file. Return type string. For example returns -> <b>REAL, NULL, VARCHAR2, DATE,  NUMBER(25) </b>

`def convert_csv_to_sql(self, conn, csv_file)` ->  this method will convert data from csv to sql.

<b>How this method works: </b>

1. Read data from csv file and save it as list.
2. Find table name(for table name I used basename of file.)
3. Find colunm names(First row of csv file will be column names)
4. Find data type of each colunms
5. Create new table
6. Insert all data from list to table
7. Commit all changes

`def converter_to_csv(self, conn, csv_name)` - > this method will convert data from sql tables to csv file.

<b>How this method works: </b>

1. Find table name (I find table as `SELECT table_name FROM user_tables`)
2. Find column names
3. Open new csv file and write all data to it.









