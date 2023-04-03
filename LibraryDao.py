import mysql.connector
import datetime
import views
import pandas as pd
import matplotlib.pyplot as plt
#conda install matplotlib

# import japanize_matplotlib
#pip install japanize-matplotlib

class Database: #データベースの基本操作

    def database_connection(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', port='3306', user='user', password='pass', database='lib_sys')
            self.cursor = self.conn.cursor(prepared=True)
        except (mysql.connector.errors.ProgrammingError) as e:
            print(e)
        # print("end:__init__")

    def database_closing(self):
        try:
            self.conn.close()
        except (mysql.connector.errors.ProgrammingError) as e:
            print(e)
        # print("end:__del__")


    def execute_query(self, query, data): #データベース読込
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        return result


    def execute_insert_query(self, query, data): #データ更新
        self.cursor.execute(query, data)
        # self.conn.commit() #ここではコミットせず、トランザクション処理の為、まとめておこなうこと

    def closing(self):
        #カーソル切断
            self.cursor.close()
            # print("カーソル切断")
            #コネクション切断
            self.conn.close()
            # print("コネクション切断")
  

class LibraryDao:
    def __init__(self):
        self.db = Database()

    def get_book(self, book_id):
        self.db.database_connection()
        query = "SELECT * FROM books WHERE book_id = ?"
        result = self.db.execute_query(query, (book_id,))
        self.db.database_closing()
        return result
    
    def get_all(self):
        self.db.database_connection()
        query = "SELECT * FROM books "
        result = self.db.execute_query(query, data=None)
        self.db.database_closing()
        return result
    
    def get_user_from_books(self, user_id): #図書の利用者検索用
        self.db.database_connection()
        query = "SELECT * FROM books WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,))
        self.db.database_closing()
        return result
    
    def get_user_from_users(self, user_id): #利用者リストでの利用者ID検索用
        self.db.database_connection()
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,))
        self.db.database_closing()
        return result

    def get_user_from_borrowed_books(self, is_borrowed): #図書リストでの貸出中の検索
        self.db.database_connection()
        query = "SELECT * FROM books WHERE is_borrowed = ?"
        result = self.db.execute_query(query, (is_borrowed,))
        self.db.database_closing()
        return result
    
    def get_user(self, user_id):
        self.db.database_connection()
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,))
        self.db.database_closing()
        return result

    def get_ranking_book(self):
        self.db.database_connection()
        query = "SELECT isbn,book_title,sum(count_borrowed) as 貸出合計 FROM books GROUP BY isbn,book_title order by sum(count_borrowed) desc"
        result = self.db.execute_query(query, data=None)
        self.db.database_closing()
        return result
    
    #図書検索
    def search_book(self):
       

        keyword = input("検索する図書名を入力してください:")
        keyword = keyword.replace('%', '\\%')
        keyword = keyword.replace('_', '\\_')
        # keyword = keyword.replace('\\', '\\\\')

        if len(keyword.rstrip())!=0 :
            query1 = "SELECT * FROM books WHERE book_title LIKE %s or book_kana LIKE %s"
            # query2 = "SELECT * FROM books WHERE book_kana LIKE ?"
            
            self.db.database_connection()
            results1=self.db.execute_query(query1,('%'+keyword+'%','%'+keyword+'%'))
            # results1=self.db.execute_query(query1,(f'%{keyword}%',f'%{keyword}%'))

            # results2=self.db.execute_query(query2,(f'%{keyword}%',))

            self.db.closing()
            if len(results1)!=0:
                results=[]
                for result in results1:
                    # print(result)
                    results.append(result)
                # for result in results2:
                #     # print(result)
                #     results.append(result)
                    
                return results
        
    #ランキング
    def show_ranking_graph(self):
   
        plt.rcParams['font.family']= ['MS Gothic']
    #     # ランキングデータを取得
        ranking_list = self.get_ranking_book()
   

        # # データの整形
        x_values = []
        y_values = []
        for data in ranking_list:
            # print(data)
            x_values.append(data[1])
            y_values.append(data[2])

        # # グラフの設定
        plt.figure(figsize=(10, 8))  # グラフのサイズを指定
        plt.barh(x_values, y_values)  # 水平棒グラフを描画
        plt.title('Library Ranking')  # グラフのタイトルを設定
        plt.xlabel('Number of Loans')  # x軸のラベルを設定
        plt.ylabel('Book Title')  # y軸のラベルを設定
        plt.gca().invert_yaxis()  # y軸を逆転して、上から下に描画

        plt.tight_layout()
        # グラフを表示
        plt.show()



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
    def return_book_dao(self, book_id,user_id,count_books):
        try:
            self.db.database_connection()
            query = "UPDATE books SET is_borrowed=0, borrowed_date=NULL, return_date =NULL, user_id =NULL WHERE book_id = ?"
            self.db.execute_insert_query(query, (book_id,))
            # print("self.db.cursor.rowcount",self.db.cursor.rowcount)

            if self.db.cursor.rowcount == 0:
                raise Exception

            query = "UPDATE users SET count_books=? WHERE user_id = ?"
            data=(count_books,user_id)
            self.db.execute_insert_query(query, data)
            # print("self.db.cursor.rowcount",self.db.cursor.rowcount)

            if self.db.cursor.rowcount == 0:
                raise Exception
            #更新確定　※トランザクション処理
            self.db.conn.commit()
            # self.db.database_closing()
            self.db.closing()
            return True
        except:
            self.db.conn.rollback() 
            print("登録に失敗しました。")
            return False

    #貸出処理
    def borrow_book_dao(self, book_id, user_id, count_books, count_borrowed):
        t_delta = datetime.timedelta(hours=9)  # 9時間
        JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
        today = datetime.datetime.now(JST)
        borrowed_date= today.strftime('%Y/%m/%d')  # タイムゾーン付きでローカルな日付と時刻を取得
        return_date =(today + datetime.timedelta(days=4)).strftime('%Y/%m/%d') #5日間の貸出期間（返却期限は4日後）


        try:
            self.db.database_connection()
            query = "UPDATE books SET is_borrowed=1, borrowed_date=?, return_date =?, user_id =?, count_borrowed =? WHERE book_id = ?"
            data=(borrowed_date, return_date, user_id, count_borrowed, book_id)
            self.db.execute_insert_query(query, data)
            if self.db.cursor.rowcount == 0:
                raise Exception

            query = "UPDATE users SET count_books=? WHERE user_id = ?"
            data=(count_books,user_id)
            self.db.execute_insert_query(query, data)

            if self.db.cursor.rowcount == 0:
                raise Exception

            #更新確定　※トランザクション処理
            self.db.conn.commit()
            self.db.closing()

            return True
        
        except:
            self.db.conn.rollback() 
            print("登録に失敗しました。")
            return False

    def get_staff(self, data):
        self.db.database_connection()
        query = "SELECT * FROM staff WHERE staff_id = ? and s_pass = ?"
        result = self.db.execute_query(query,data)
        self.db.closing()
        
        return result

#
# 図書登録処理
#   input   1)book_id  図書ID
#           2)book_title 図書名
#           3)book_kana 図書名（かな）
#   output  1)book_id  図書ID
#           2)book_title 図書名
#       2023.3.20 K.Ishihara
#
    def lib_register_dao(self, book_id,isbn,book_title,book_kana): ###
        try:
            self.db.database_connection()
            query = "insert into books values(?,?,?,?,0,NULL,NULL,NULL,0)" ###
            self.db.execute_insert_query(query, (book_id,isbn,book_title,book_kana)) ###

            if self.db.cursor.rowcount == 0:
                raise Exception

            #更新確定　※トランザクション処理
            self.db.conn.commit()
            self.db.closing()

            return True
        except:
            self.db.conn.rollback() 
            print("登録に失敗しました。")
            return False

#
# 図書削除処理
#   input   1)book_id  図書ID
#   output  1)book_id  図書ID
#       2023.3.20 K.Ishihara
#
    def lib_delete_dao(self, book_id):
        try:
            self.db.database_connection()
            query = "delete from books where book_id =?"
            self.db.execute_insert_query(query, (book_id,))
            if self.db.cursor.rowcount == 0:
                raise Exception

            #更新確定　※トランザクション処理
            self.db.conn.commit()
            self.db.closing()

            return True
        except:
            self.db.conn.rollback() 
            print("削除に失敗しました。")
            return False
        

        