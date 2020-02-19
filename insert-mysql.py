import pymysql
conn = pymysql.connect(host='localhost', user='root', passwd='python', db='mydb',
                       port=3306, charset='utf8')   #连接数据库
cursor = conn.cursor()  #光标对象
cursor.execute("insert into students (name,sex,grade) values(%s,%s,%s)",
               ('张三','女',87))   #插入数据
conn.commit()