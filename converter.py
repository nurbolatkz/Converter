import csv
import cx_Oracle
import datetime


class Converter:
          #Converter function csv ---> sql
          def find_type(self, elem):
                    return_type = ''
                    
                    try:
                              int_d = float(elem)
                              if '.' in str(elem):
                                        return_type = " REAL,"
                              else:
                                        return_type = " NUMBER(25) ,"
                                                  
                    except ValueError as ex:
                              if '-'  in elem or "/" in elem:
                                        return_type = " DATE ,"
                              else:
                                        if elem == 'null':
                                                  #print('worked')
                                                  return_type = 'NULL'
                                        else:
                                                  return_type = " VARCHAR2(50),"
                    return return_type
                    
                    
          def convert_csv_to_sql(self, conn, csv_file):
                    #read  csv file
                    with open(csv_file,'r') as f:
                              reader =  csv.reader(f)
                              data_lst = [ each for each in reader if len(each) > 0]
                    types = []
                    for i in data_lst[1]:
                              types.append(self.find_type(i))

                              
                    for i in range(1,len(data_lst)):
                              for j in range(len(data_lst[i])):
                                        if self.find_type(data_lst[i][j]) == " REAL,":
                                                  data_lst[i][j] = float(data_lst[i][j])
                                        elif self.find_type(data_lst[i][j]) == " DATE ,":
                                                  data = data_lst[i][j]
                                                  data = ''.join(data.split('-')[::-1])
                                                  data = datetime.datetime.strptime(data, "%d%m%Y").date()
                                                  data_lst[i][j] = data
                                                            
                                        elif self.find_type(data_lst[i][j]) == " NUMBER(25) ,":
                                                  data_lst[i][j] = float(data_lst[i][j])
                                        elif self.find_type(data_lst[i][j]) == 'NULL':
                                                  data_lst[i][j] = None
                                        
                    
                                        
                                        
                    tableName = csv_file[:-4]
                    tableName = tableName.upper()

                    query = f"""BEGIN EXECUTE IMMEDIATE 'DROP TABLE {tableName}'; EXCEPTION WHEN OTHERS THEN NULL; END;"""

                    cur = conn.cursor()
                    cur.execute(query)
                    conn.commit()

                    colNameType = ['"' + data_lst[0][i] + '"' + types[i] for i in range(len(types))]

                    query = "CREATE TABLE " + tableName + " ("

                    for each in colNameType:
                              if each == colNameType[-1]:
                                        query += " " + each[:-1]+ ")"
                              else:
                                        query += each
                                        
                    print(query, "\n\n")
                    
                    cur.execute(query)
                    conn.commit()


                    ColNamesList = ['"' + i  + '"' for i in data_lst[0]]
                    colNames =  ' (' + ', '.join(ColNamesList) + ')'
                    ValuesList = [':' + str(i) for i in range(1, len(ColNamesList) + 1)]

                 
                                                  
                    restQuery = " VALUES( " + ', '.join(ValuesList) + ')'
                    insertQuery = "INSERT INTO  " + tableName + colNames + restQuery
                                
                    try:
                              cur.executemany(insertQuery , data_lst[1:])
                    except cx_Oracle.DatabaseError as e:
                              print("has error", e)
                    conn.commit()

                    print("converted :)")
          def converter_to_csv(self, conn, csv_name):
                    
                    cur =  conn.cursor()
                    cur.execute("SELECT table_name FROM user_tables")
                    tableName = str(cur.fetchone())[2:-3]

                    cur.execute("SELECT * FROM "  + tableName)
                    desc = cur.description
                    print(desc, "\n\n")
                    
                    colNames = [ each[0] for each in desc]
                    print(colNames)

                    cur.execute("""SELECT * FROM """ + tableName )

                    with open(csv_name, 'w', encoding='utf-8') as csv_file:
                              csv_writer = csv.writer(csv_file)
                              csv_writer.writerow(colNames)
                              for each in cur:
                                        
                                        csv_writer.writerow(list(each)[:-1])
                    print("Converted sql to csv :)") 
                    

newConverter =  Converter()

conn = cx_Oracle.connect("User2/oracle@//localhost:1521/xe")
print(conn.version)

newConverter.convert_csv_to_sql(conn, "mInfo.csv")
newConverter.convert_csv_to_sql(conn, "mydata.csv")
newConverter.convert_csv_to_sql(conn, "myprocess.csv")

print("Finished")
                    
