import mysql.connector as mydb
from LibraryDao import *
import pandas
from common import *
from LibraryDao import Database

class UsersDao():
    def __init__(self):

        self.db = Database()
        self.users_title = ["利用者ID", "利用者名", "貸出回数" ]

    def get_user(self, user_id):
        self.db.database_connection()
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,))
        self.db.closing()

        return result
    
    def get_all_user(self):
        self.db.database_connection()
        query = "SELECT * FROM users "
        result = self.db.execute_query(query, data=None)
        self.db.closing()
        return result
    
    def user_list_display(self): #利用者の表示用リスト作成
        user_list = self.get_all_user()
        return user_list

    def show_user_list_by_pandas(self): #pandasを使って一覧表示 >-----------------
        user_list=self.user_list_display()#利用者情報を表示用に加工してリストを作成
        
        pandas.set_option('display.unicode.east_asian_width', True)
        display = pandas.DataFrame(user_list,columns=self.users_title)    
        print(display.to_string(index=False))

    def user_list_display_for_csv(self): #ユーザーのCSV用リスト作成
        
        user_list=self.user_list_display()
        user_list.insert(0,self.users_title)
        return user_list
    
    #利用者削除
    def user_delete_function(self):
        try:
            
            user_id=input("1:user_idを入力")
            # s2=input("2:user_nameを入力")
            # self.lib_dao.execute("select * from users where user_id=?",(user_id,))

            rows = self.get_user(user_id)
            for row in rows:
                pass
            user_id=row[0]
            user_name = row[1]
            count_books = row[2]#count_booksの表示方法
            # s3=count_books

            if count_books == 0:
                cmd = input(f"利用者ID:{user_id} 利用者:{user_name} のデータを削除しますか？(y/n):")
                # cur.execute("delete from users where user_id =?,user_name=?,count_books=?",(user_id,user_name,count_books))

                if cmd == "y":
                    self.db.database_connection()
                    self.db.cursor.execute("delete from users where user_id =?",(user_id,))
                    print(f"利用者「{user_name}」を削除しました")
                
                elif cmd=="n":
                     print("キャンセルしました")
                     return
            
            else:
                print("図書借用中の利用者を削除できません。") 
                raise Exception
           

            if self.db.cursor.rowcount == 0:
                raise Exception
            #更新確定　※トランザクション処理
            self.db.conn.commit()
        

            print(f"利用者ID:{user_id} 利用者:{user_name} のデータを削除しました。")

            return True
        
        except:
            self.db.conn.rollback() 
            print("登録に失敗しました。")
            return False    
        finally:
            self.db.closing()
        

#########################################
    # #利用者削除
    # def user_delete_function(self):
    #     conn = mydb.connect(
    #         host="localhost",
    #         port="3306",
    #         user="user",
    #         password="pass",
    #         database="lib_sys",
    #     )

    #     #カーソルの作成
    #     cur = conn.cursor(prepared=True)
        
    #     try:
            
    #         user_id=input("1:user_idを入力")
    #         # s2=input("2:user_nameを入力")
    #         cur.execute("select * from users where user_id=?",(user_id,))

    #         rows=cur.fetchall()

    #         for row in rows:
    #             pass
        
    #         user_name = row[1]
    #         count_books = row[2]#count_booksの表示方法
    #         # s3=count_books
            
    #         if count_books > 1:
    #             raise Exception 

    #         else:
    #             cmd = input(f"{user_id} {user_name}のデータを削除しますか？(y/n):")
    #             # cur.execute("delete from users where user_id =?,user_name=?,count_books=?",(user_id,user_name,count_books))

    #             if cmd == "y":
    #                 cur.execute("delete from users where user_id =?",(user_id,))
    #                 print(f"{user_id} {user_name}のデータを削除しました。")
    #                 # print(cur.rowcount,"件、削除しました")
        

    #     except Exception as e:
    #         print(e)
    #         conn.rollback()
    #         print("利用者が図書を借用中です")

    #     conn.commit()

    #     cur.close()

    #     conn.close()
##################################

    #利用者登録
    def user_register_function(self):
        

        # conn = mydb.connect(
        #     host="localhost",
        #     port="3306",
        #     user="user",
        #     password="pass",
        #     database="lib_sys",
        # )

        # #カーソルの作成
        # cur = conn.cursor(prepared=True)

        
        try:
            
            user_id=input("1:user_id:")
            user_name=(input("2:user_name:"))
            count_books=0
            data1=(user_id, user_name, count_books)
            user_name_char_len=get_east_asian_width_count(user_name) 
            user_list=self.get_user(user_id)
            if(len(user_list)!=0):
                print("user_idはすでに登録されています。")
                return   
            
            if(str.isdecimal(user_id)==False):
                print("user_idは数字を入力してください。")
                return   

            elif len(user_id) ==0 or len(user_name)==0 :
                # print(user_id, user_name)
                raise ValueError
            
            # elif s1 is not int:
            #     raise Exception

            # elif len(user_name) >=20:
                # raise Exception
            elif user_name_char_len >20: 
                raise Exception
            #登録するか否かの判断を行う
            else:
                cmd = input(f"{user_id} {user_name}のデータを登録しますか？(y/n):")
                if cmd == "y":
                    self.db.database_connection()
                    self.db.cursor.execute("insert into users values(?,?,?)",data1)
                    self.db.conn.commit()
                    self.db.database_closing()
                    # print(data1)
                    print(f"利用者ID:{user_id}  利用者名:{user_name} を登録しました。")
                    # print(self.db.cursor.rowcount,"件、インサートしました")
                    
                elif cmd=="n":
                    print("キャンセルしました")
                    return
                    
                    
        except ValueError:
                self.db.conn.rollback()
                print("Error: 利用者名なし")    
            
        except Exception:
                self.db.conn.rollback()
                print("Error: 利用者名の長さが20文字を超えています/不正な入力です")

        #print(data1)
        #print(cur.rowcount,"件、インサートしました")
        # finally:
            # self.db.conn.commit()
            # self.db.database_closing()
        
        # cur.close()
        # conn.close()


    #利用者CSV出力
    def users_display_csv(self):
        
        #self.db.database_connection()
        rows=self.user_list_display_for_csv()
        #self.db.cursor.execute("select * from users" )
        #rows=self.db.cursor.fetchall()

        #CSVに変更する手順
        #users_title = ("利用者ID", "利用者名", "貸出回数" )
        with open("userslines.csv","w",encoding='utf-8') as f:
            data2=[]
            for row in rows:
                s=str(row[0])+","
                s+=str(row[1])+","
                s+=str(row[2])+"\n"
                data2.append(s)
                #data2.insert(0,users_title)
        
            f.writelines(data2)
            f.flush()
            #self.db.database_closing()

        print("全件CSV出力完了")

#=====================================================================   
    # def users_display_csv(self):

    #     conn = mydb.connect(
    #         host="localhost",
    #         port="3306",
    #         user="user",
    #         password="pass",
    #         database="lib_sys",
    #     )

    #     #カーソルの作成
    #     cur = conn.cursor(prepared=True)


    #     cur.execute("select * from users" )

    #     rows=cur.fetchall()
    #     self.db.database_closing()

    #     #実行結果を取得
    #     #for row in rows:
    #         #print(row)

    #     #CSVに変更する手順
    #     users_title = ["利用者ID", "利用者名", "貸出回数" ]
    #     with open("userslines.csv","w") as f:
    #         data2=[]
    #         for row in rows:
    #             s=str(row[0])+","
    #             s+=str(row[1])+","
    #             s+=str(row[2])+"\n"
    #             data2.append(s)
    #             data2.insert(0,users_title)
        
    #         f.writelines(data2)

    #     print("CSV出力完了")
#========================================================================

    #利用者表示
    # def user_list_display(self):
        
    #     self.db.database_connection()

    #     # conn = mydb.connect(
    #     #     host="localhost",
    #     #     port="3306",
    #     #     user="user",
    #     #     password="pass",
    #     #     database="lib_sys",
    #     # )

    #     # #カーソルの作成
    #     # cur = conn.cursor(prepared=True)

    #     self.db.cursor.execute("select * from users" )

    #     rows=self.db.cursor.fetchall()

    #     #実行結果を取得
    #     for row in rows:
    #         print(row)

    #     print(self.db.cursor.rowcount,"件取得しました")
    #     self.db.database_closing()

        # cur.close()

        # conn.close()

    def search_user(self):
        keyword = input("検索する名前を入力してください:")
        query = "SELECT * FROM users WHERE user_name LIKE ?"
        self.db.database_connection()
        results=self.db.execute_query(query,(f'%{keyword}%',))
        self.db.closing()
        for result in results:
            print(result)


                
            
