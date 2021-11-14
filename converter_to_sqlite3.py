import sqlite3
import csv

conn = sqlite3.connect('list_volcanos.db')
cur = conn.cursor()

                
class Converter:
          
          def convert_csv_to_sql(self, conn, csv_file):
                    def find_type(row_values):
                              rslt = []
                              for i in range(len(row_values)):
                                        try:
                                                  int_d = float(row_values[i])
                                                  digit_type = ''
                                                  if '.' in row_values[i]:
                                                            rslt.append(" REAL,\n")
                                                  else:
                                                            rslt.append(" INT,\n")
                                        except ValueError as ex:
                                                  rslt.append(" TEXT,\n")
                              return rslt
                  
                    cur = conn.cursor()
                    with open(csv_file,'r') as f:
                              reader =  csv.reader(f)
                              data_lst = [ each for each in reader if len(each) > 0]

                    table_name = "volcanos"
                    types = find_type(data_lst[2])

                    cur.execute('DROP TABLE IF EXISTS ' + table_name)
                    col_name_type = ["'" + data_lst[0][i] + "'" + types[i] for i in range(len(types))]

                    query = "CREATE TABLE IF NOT EXISTS " + table_name + "("

                    for each in col_name_type:
                              if each == col_name_type[-1]:
                                        each_ =  each.split("\n")
                                        query += " " + each_[0][:-1]+ ");"
                              else:
                                        query += each
                    cur.execute(query)
                    for each in range(1,len(data_lst)):
                              insert_query = "INSERT INTO " + table_name + " VALUES(?,?,?,?,?,?)"
                              if len(data_lst[each]) != 6:
                                        for j in range(6 - len(data_lst[each])):
                                                  data_lst[each].append(None)
                              cur.execute(insert_query, data_lst[each])

                    conn.commit()
                    print("converted")
          def converter_csv(self, conn, csv_name):
                    cur =  conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    table_name = str(cur.fetchone())[2:-3]

                    cur.execute("SELECT * FROM "  + table_name)
                    desc = cur.description

                    colnames = [ i for each in desc for i in each if i != None ]

                    cur.execute("""SELECT * FROM """ + table_name )

                    with open(csv_name, 'w', encoding='utf-8') as csv_file:
                              csv_writer = csv.writer(csv_file)
                              csv_writer.writerow(colnames)
                              for each in cur:
                                        csv_writer.writerow(list(each)[:-1])
                    print("converted")



conn = sqlite3.connect('all_fault_line.db')
new_con = sqlite3.connect('my_db_file.db')

Converter().convert_csv_to_sql(new_con,'list_volcano_inf.csv')
Converter().converter_csv(conn, "mydata___f.csv")
