import pymysql
import re

f = open('dict.txt')
db = pymysql.connect('localhost', 'root', '123456', 'Dictionary')
cursor = db.cursor()

for line in f:
    L = re.split(r'\s+', line)
    sql = "insert into dict(word, translate) values('%s','%s')"\
        % (L[0], ' '.join(L[1:]))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        db.rollback()
f.close()
