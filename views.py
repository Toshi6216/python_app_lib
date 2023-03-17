from LibraryDAO import *

class LibraryView:
    def __init__(self):
        self.lib_dao = LibraryDAO()

    # def show_menu(self):

    #     print("1:本を表示 2:全ての本を表示 3:貸出処理 4:返却処理 5:終了")  ###


    def get_input(self, message):
        return input(message)
    
    def book_data_display(self, book):
        ctx={
        # book情報を各変数に保存する
        "book_id":book[0],
        "book_title":book[1],
        "is_borrowed":book[2],
        "borrowed_date":book[3],
        "return_date":book[4],
        "borrow_user":book[5],
        }
        


    def run(self):
        while True:

            print("1:利用者メニュー  2:図書メニュー  3:csv出力  5:ログアウト")
            choice = int(self.get_input("Enter your choice: "))

            if choice == 1:
                pass

            elif choice == 2:
                books = self.lib_dao.get_all()
                for book in books:
                    print(book)
                book_id = self.get_input("Enter borrow book id: ")

                print("1:貸出処理 2:返却処理 5:もどる")  ###
                choice2 = int(self.get_input("Enter your choice: "))

                if choice2 == 1:
                    books = self.lib_dao.get_book(book_id)
                    
                    for book_row in books:
                        pass
                    print(book)

                    book_id=book_row[0]
                    book_title=book_row[1]
                    is_borrowed=book_row[2]

                    if is_borrowed == False:
                        print(f"{book[0]} {book[1]}の貸出処理をします")

                        user_id = self.get_input("Enter borrow user id: ")
                        books = self.borrow_book(book_id,user_id)
                    else:
                        print(f"{book[0]} {book[1]}は貸出中です。")

                elif choice2 == 2:     #返却
                    # book_id = self.get_input("Enter retrun book id: ")
                    print(f"{book[0]} {book[1]}の返却処理します")
                    books = self.return_book(book_id)

                elif choice2 == 5:

                # elif choice2 == 3:
                #     choice = self.get_input("CSV出力しますか？(y/n):")
                #     if choice == 'y':
                #         books_display_csv()
                #     else:
                #         break

            elif choice == 3:
                choice = self.get_input("CSV出力しますか？(y/n):")
                if choice == 'y':
                    books_display_csv()
                else:
                    break

            elif choice == 5:
                print("ログアウト")
                break

                # elif choice2 == '3':     #貸出
                #     book_id = self.get_input("Enter borrow book id: ")
                #     user_id = self.get_input("Enter borrow user id: ")

                #     books = self.borrow_book(book_id,user_id)

                # elif choice2 == 2:     #返却
                #     # book_id = self.get_input("Enter retrun book id: ")
                #     print(f"{book[0]} {book[1]}の返却処理します")
                #     books = self.return_book(book_id)

                # elif choice2 == '5':
                #     break
                # else:
                #     print("Invalid choice")

            # if choice == '1':
            #     book_id = self.get_input("Enter book id: ")
            #     book = self.lib_dao.get_book(book_id)
            #     print(book)
            # elif choice == '2':
               
            #     books = self.lib_dao.get_all()
                
            #     for book in books:
            #         print(book)

            # elif choice == '3':     #貸出
            #     book_id = self.get_input("Enter borrow book id: ")
            #     user_id = self.get_input("Enter borrow user id: ")

            #     books = self.borrow_book(book_id,user_id)

            # elif choice == '4':     #返却
            #     book_id = self.get_input("Enter retrun book id: ")
            #     books = self.return_book(book_id)

            # elif choice == '5':
            #     break
            # else:
            #     print("Invalid choice")


#
# 図書貸出確認処理
#   input   1)book_id  図書ID
#           2)books情報
#           3)users情報
#   output  1)book_id  図書ID
#           2)user_id   利用者ID
#           3)count_books 貸出数
#       2023.3.16 T.Hotta
#
    def borrow_book(self,book_id,user_id):
        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)

        # 入力したIDの本が存在しているか？
        if len(book_rows)==0:
            print("不正な図書ＩＤが入力されました。")
        else:
            user_rows=self.lib_dao.get_user_from_users(user_id) #user情報取得
            for user_row in user_rows:
                count_books = user_row[2]
                       
            if len(user_rows)==0: #user_idが存在しない場合
                print("不正な利用者ＩＤが入力されました。")
            elif count_books == 3:
                print("利用者はすでに３冊の図書を借りています。")
            else:
                for book_row in book_rows:
                    pass
                    # print(row)
                    # print(row[0],row[1],row[2],row[3],row[4],row[5])

                # book情報を各変数に保存する
                book_id=book_row[0]
                book_title=book_row[1]
                is_borrowed=book_row[2]
                # borrowed_date=book_row[3]
                # return_date=book_row[4]

                user_id=user_id

                if(book_row[2]==0):
                    
 
                    print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n")   
                    while True:
                        key=input("貸出処理しますか。y/n：")
                        #貸出確認
                        if(key=="y"):

                            # # book情報を各変数に保存する
                            # count_books=user_row[2]
                            # 貸出数を加算する
                            count_books+=1
                            
                            # 貸出処理
                            self.lib_dao.borrow_book(book_id,user_id,count_books)
                            print(f"{book_title}の貸出処理をしました。")
                            
                            book = self.lib_dao.get_book(book_id)
                            print(book)
                            break

                        elif(key=="n"):
                            break
                        else:
                            print("正しく入力してください")

                else:
                    print("図書はすでに貸出中です。")



#
# 図書返却確認処理
#   input   1)book_id  図書ID
#           2)books情報
#           3)users情報
#   output  1)book_id  図書ID
#           2)user_id   利用者ID
#           3)count_books 貸出数
#       2023.3.15 K.Ishihara
#
    def return_book(self,book_id):
        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)
        # print(rows)
        
        # 登録されていないか？
        if len(book_rows)==0:
            print("不正な図書ＩＤが入力されました。")
        else:
            
            for book_row in book_rows:
                pass
            # book情報を各変数に保存する
            book_id=book_row[0]
            book_title=book_row[1]
            is_borrowed=book_row[2]
            borrowed_date=book_row[3]
            return_date=book_row[4]
            user_id=book_row[5]

            user_rows=self.lib_dao.get_user_from_users(user_id)
            if user_rows:
                print(user_rows)
                for user_row in user_rows:
                    pass
                print(user_row)
                # count_books=user_row[2]
            else:
                print("貸し出されていません。")
                

            if(is_borrowed==0):
                print("図書は貸出されていません")
            else:
                print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n利用者ID：{user_id}\n返却日：{return_date}\n")   
                while True:
                    key=input("返却しますか。y/n：")
                    #返却確認
                    if(key=="y"):

                        # for book_row in book_rows:
                        #     pass

                        # book情報を各変数に保存する
                        # user_id=row[0]
                        # count_books=row[2]

                        # 貸出数を減算する
                        count_books-=1
                        # 0未満にならないように防止
                        if count_books<0:
                            count_books=0
                        # 返却処理
                        self.lib_dao.return_book(book_id,user_id,count_books)
                        print(f"図書 {book_title}を返却しました。")
                        break

                    elif(key=="n"):
                        break
                    else:
                        print("正しく入力してください")

    def all_books_display(self):
        books = self.lib_dao.get_all()
        for book in books:
            print(book)
        

# class LoginView:
#     def __init__(self):
#         self.login_dao = LoginDAO()

#     def show_menu(self):
#         # print("1. Add User")
#         # print("2. Update User")
#         # print("3. Delete User")
#         # print("4. View User")
#         # print("5. Exit")
#         print("1:login 5:終了")

#     def get_input(self, id, passw):
#         return input(message)

class LoginView:
    def __init__(self):
        self.lib_dao = LibraryDAO()

    def show_menu(self):
        print("1:ログイン 2:終了")  ###

    def get_input(self, message):
        return input(message)

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_input("Enter your choice: ")
            if choice == '1':

                staff_id = self.get_input("Enter staff id: ")

                s_pass = self.get_input("Enter staff pass: ")
                result = self.check_login(staff_id,s_pass)
                if result == True:
                    return result
                # break
	            
            elif choice == '2':
                result = False
                return result
                # break

            else:
                print("Invalid choice")

    def check_login(self,staff_id,s_pass):
        rows = self.lib_dao.get_staff(staff_id,s_pass)
    
        if len(rows) == 0:
           print("ログインIDまたはパスワードが違います。")
           return False

        else:
             return True


def books_display_csv():
    import mysql.connector as mydb
    

    conn = mydb.connect(
        host="localhost",
        port="3306",
        user="user",
        password="pass",
        database="lib_sys",
    )

    #カーソルの作成
    cur = conn.cursor(prepared=True)


    cur.execute("select * from books" )

    rows=cur.fetchall()
    #CSVに変更する手順
    with open("books.table","w") as f:

        #実行結果を取得
        # for row in rows:
        #     print(row)

            data2=[]
            for i in rows:
                print(i)
                s=""
                s+=str(i[0])+","
                s+=str(i[1])+","
                s+=str(i[2])+","
                s+=str(i[3])+","
                s+=str(i[4])+","
                s+=str(i[5])+"\n"
                data2.append(s)
            print(data2)
            print()

    with open("books.table","w") as f:
        print(f.writelines(data2))

    print("CSV出力完了")

