import mysql.connector as mydb
from LibraryDao import *


class UsersDao:
    def __init__(self):

        self.db = Database()

    def get_user(self, user_id):
        query = "SELECT * FROM users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,))
        return result
    
    def get_all_user(self):
        query = "SELECT * FROM users "
        result = self.db.execute_query(query, data=None)
        return result
      
    # def get_user_from_users(self, user_id): #利用者リストでの利用者ID検索用
    #     query = "SELECT * FROM users WHERE user_id = ?"
    #     result = self.db.execute_query(query, (user_id,))
    #     return result

    #利用者削除
    def user_delete_function(self):
        try:
            user_id=input("1:user_idを入力")
            # s2=input("2:user_nameを入力")
            # self.lib_dao.execute("select * from users where user_id=?",(user_id,))

            rows = self.get_user(user_id)
            for row in rows:
                pass
        
            user_name = row[1]
            count_books = row[2]#count_booksの表示方法
            # s3=count_books

            if count_books == 0:
                cmd = input(f"利用者ID:{user_id} 利用者:{user_name} のデータを削除しますか？(y/n):")
                # cur.execute("delete from users where user_id =?,user_name=?,count_books=?",(user_id,user_name,count_books))

                if cmd == "y":
                    self.db.cursor.execute("delete from users where user_id =?",(user_id,))
                    # print(f"利用者「{user_name}」を削除しました")
                
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
        

        conn = mydb.connect(
            host="localhost",
            port="3306",
            user="user",
            password="pass",
            database="lib_sys",
        )

        #カーソルの作成
        cur = conn.cursor(prepared=True)

        
        try:
            
                user_id=input("1:user_id:")
                user_name=(input("2:user_name:"))
                count_books=0
                data1=(user_id, user_name, count_books)

                if len(user_id) ==0 or len(user_name)==0 :
                    # print(user_id, user_name)
                    raise ValueError
                
                # elif s1 is not int:
                #     raise Exception
                
                elif len(user_name) >=20:
                    raise Exception

                #登録するか否かの判断を行う
                else:
                    cmd = input(f"{user_id} {user_name}のデータを登録しますか？(y/n):")
                    if cmd == "y":
                        cur.execute("insert into users values(?,?,?)",data1)
                        print(data1)
                        print(cur.rowcount,"件、インサートしました")
                    
                    elif cmd=="n":
                        print("キャンセルしました")
                        return
                    
                    
        except ValueError:
                conn.rollback()
                print("Error: 利用者名なし")    
            
        except Exception:
                conn.rollback()
                print("Error: 利用者名の長さが20文字を超えています/不正な入力です")

        #print(data1)
        #print(cur.rowcount,"件、インサートしました")
            
        conn.commit()

        # cur.close()

        # conn.close()


    #利用者CSV出力
    def users_display_csv(self):

        

        conn = mydb.connect(
            host="localhost",
            port="3306",
            user="user",
            password="pass",
            database="lib_sys",
        )

        #カーソルの作成
        cur = conn.cursor(prepared=True)


        cur.execute("select * from users" )

        rows=cur.fetchall()

        #実行結果を取得
        #for row in rows:
            #print(row)

        #CSVに変更する手順
        with open("userslines.csv","w") as f:
            data2=[]
            for row in rows:
                s=str(row[0])+","
                
                
                s+=str(row[1])+","
                
                
                s+=str(row[2])+"\n"
                data2.append(s)

        
            f.writelines(data2)

        print("CSV出力完了")

    #利用者表示
    def user_list_display(self):
        

        conn = mydb.connect(
            host="localhost",
            port="3306",
            user="user",
            password="pass",
            database="lib_sys",
        )

        #カーソルの作成
        cur = conn.cursor(prepared=True)

        cur.execute("select * from users" )

        rows=cur.fetchall()

        #実行結果を取得
        for row in rows:
            print(row)

        print(cur.rowcount,"件取得しました")

        # cur.close()

        # conn.close()




                
            
