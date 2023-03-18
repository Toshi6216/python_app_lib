import mysql.connector
import datetime

class database:
    def __init__(self):
        self.conn = mysql.connector.connect(user='user', password='pass', database='lib_sys')
        self.cursor = self.conn.cursor(prepared=True)

    def execute_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def execute_query_login(self, query, staff_id, s_pass):
        self.cursor.execute(query,(staff_id, s_pass))
        result = self.cursor.fetchall()
        return result

    def execute_insert_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        

class LibraryDAO:
    def __init__(self):
        self.db = database()

    def get_book(self, book_id):
        query = "SELECT * FROM books WHERE book_id = '{}'".format(book_id)
        result = self.db.execute_query(query)
        return result
    
    def get_all(self):
        query = "SELECT * FROM books "
        result = self.db.execute_query(query)
        return result
    
    def get_user_from_books(self, user_id):
        query = "SELECT * FROM books WHERE user_id = '{}'".format(user_id)
        result = self.db.execute_query(query)
        return result
    
    def get_user_from_users(self, user_id):
        query = "SELECT * FROM users WHERE user_id = '{}'".format(user_id)
        result = self.db.execute_query(query)
        return result
    
    

#
# 図書返却処理
#   input   1)book_id  図書ID
#           2)user_id   利用者ID
#           3)count_books 貸出数
#   output  1)book_id  図書ID
#           2)user_id   利用者ID
#           3)count_books 貸出数
#       2023.3.15 K.Ishihara
#
    def return_book(self, book_id,user_id,count_books):

        query = "UPDATE books SET is_borrowed=0, borrowed_date=NULL, return_date =NULL, user_id =NULL WHERE book_id = '{}'".format(book_id)
        self.db.execute_insert_query(query)

        query = "UPDATE users SET count_books={} WHERE user_id = '{}'".format(count_books,user_id)
        self.db.execute_insert_query(query)

    def borrow_book(self, book_id, user_id, count_books):
        t_delta = datetime.timedelta(hours=9)  # 9時間
        JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
        today = datetime.datetime.now(JST)
        borrowed_date= today.strftime('%Y/%m/%d')  # タイムゾーン付きでローカルな日付と時刻を取得
        return_date =(today + datetime.timedelta(days=4)).strftime('%Y/%m/%d') #5日間の貸出期間（返却期限は4日後）

        print("borrowed_date",borrowed_date)
        print("return_date",return_date)


        query = "UPDATE books SET is_borrowed=1, borrowed_date='{}', return_date ='{}', user_id ='{}' WHERE book_id = '{}'".format(borrowed_date, return_date, user_id, book_id)
        self.db.execute_insert_query(query)

        query = "UPDATE users SET count_books={} WHERE user_id = '{}'".format(count_books,user_id)
        self.db.execute_insert_query(query)


    def get_staff(self, staff_id,s_pass):
        # query = "SELECT * FROM staff WHERE staff_id = ? and s_pass = ?".format(staff_id, s_pass)
        query = "SELECT * FROM staff WHERE staff_id = ? and s_pass = ?"

        result = self.db.execute_query_login(query,staff_id, s_pass)
        return result
  