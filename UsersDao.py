import mysql.connector as mydb
from LibraryDao import *
import pandas
from common import *
from LibraryDao import Database

class UsersDao():
    def __init__(self):

        self.db = Database()
        self.users_title = ["利用者ID", "利用者名", "利用者(かな)","貸出回数" ]

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

    def show_user_list_by_pandas(self,user_list): #pandasを使って一覧表示 >-----------------
        # user_list=self.user_list_display()#利用者情報を表示用に加工してリストを作成
        
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

            rows = self.get_user(user_id)
            for row in rows:
                pass
            user_id=row[0]
            user_name = row[1]
            user_kana=row[2]
            count_books = row[3]#count_booksの表示方法
            # s3=count_books

            if count_books == 0:
                cmd = input(f"利用者ID:{user_id} 利用者:{user_name} 利用者カナ{user_kana}のデータを削除しますか？(y/n):")

                if cmd == "y":
                    self.db.database_connection()
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
        
            print(f"利用者「{user_name}」を削除しました")
            # print(f"利用者ID:{user_id} 利用者:{user_name} のデータを削除しました。")

            return True
        
        except:
            self.db.conn.rollback() 
            print("登録に失敗しました。")
            return False    
        finally:
            self.db.closing()
        


    #利用者登録
    def user_register_function(self):
 
        
            
            user_id=input("1:user_id:")
            user_name=input("2:user_name:")
            user_kana=input("3:user_kana:")
            count_books=0
            data1=(user_id, user_name, user_kana, count_books)
            user_name_char_len=get_east_asian_width_count(user_name) 
            #user_kana_char_len=get_east_asian_width_count(user_kana) 
            user_list=self.get_user(user_id)
            
            if(len(user_list)!=0):
                print("user_idはすでに登録されています")
                return   
            
            elif len(user_id) ==0 or len(user_name)==0 or len(user_kana)==0 :
                print("Error: 利用者名が入力されていません")
                return
            
            #elif ("%" in user_name) or ("_" in user_name) or ("%" in user_kana) or ("_" in user_kana):
                #print("使用できない記号です")

            elif (str.isdecimal(user_id)==False):
                print("user_idは数字を入力してください")
                return   

            #elif len(user_id) ==0 or len(user_name)==0 or len(user_kana)==0 :
                #print("Error: 利用者名なし")
                
            
            elif user_name_char_len >20: 
                print("Error: 利用者名の長さが最大値を超えています")
                return
        
            #登録するか否かの判断を行う
            
            else:
                cmd = input(f"{user_id} {user_name} {user_kana}のデータを登録しますか？(y/n):")
                if cmd == "y":
                    self.db.database_connection()
                    self.db.cursor.execute("insert into users values(?,?,?,?)",data1)
                    self.db.conn.commit()
                    # self.db.database_closing()
                    print(f"利用者ID:{user_id}  利用者名:{user_name} 利用者カナ{user_kana}を登録しました。")
 
                    
                elif cmd=="n":
                    print("キャンセルしました")
                    return
                    
                    
    #利用者CSV出力
    def users_display_csv(self):
     
        rows=self.user_list_display_for_csv()
        
        #CSVに変更する手順
        #users_title = ("利用者ID", "利用者名", "貸出回数" )
        with open("userslines.csv","w",encoding='utf-8') as f:
            data2=[]
            for row in rows:
                s=str(row[0])+","
                s+=str(row[1])+","
                s+=str(row[2])+","
                s+=str(row[3])+"\n"
                data2.append(s)
                #data2.insert(0,users_title)
        
            f.writelines(data2)
            f.flush()
            #self.db.database_closing()

        print("全件CSV出力完了")

    #利用者検索
    def search_user(self):
        keyword = input("検索する名前を入力してください:")
        keyword=keyword.replace("%","\\%")
        keyword=keyword.replace("_","\\_")
        if len(keyword.rstrip())!=0 :
            query1 = "SELECT * FROM users WHERE user_name LIKE %s or user_kana LIKE %s"
            # query2 = "SELECT * FROM users WHERE user_kana LIKE ?"
            
            self.db.database_connection()
            #results1=r"%","_","\\'"
            results1=self.db.execute_query(query1,('%'+keyword+'%','%'+keyword+'%'))
            

            # results1=r"%"
            # results1=r"_"
            #results1=results1.replace( "%","_","\\'")
            
            # results2=self.db.execute_query(query2,(f'%{keyword}%',))
            self.db.closing()
            
            # if results1("%") or results1("_"):
            #     print("使用できない記号です")
            
            if len(results1)!=0:
                results=[]
                for result in results1:
                    # print(result)
                    results.append(result)
                
                # for result in results2:
                #     # print(result)
                #     results.append(result)
                return results
            
        else:
            pass



                
            
