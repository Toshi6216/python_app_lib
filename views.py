from LibraryDAO import *
import pandas


class LibraryView:
    def __init__(self):
        self.lib_dao = LibraryDAO()
        
    def book_list_display(self): #図書の表示用リスト作成
        books = self.lib_dao.get_all()

        book_list=[]
        for book in books:
            book = list(book)
            if book[2]: #is_borrowed
                book[2]="貸出中"
                book[3]=book[3].strftime('%Y/%m/%d')
                book[4]=book[4].strftime('%Y/%m/%d')
            else:
                book[2]="貸出可能"
                book[3]="-"
                book[4]="-"
                book[5]="-"
            book_list.append(book)

        return book_list
    
    def book_list_display_for_csv(self): #図書のCSV用リスト作成
        title = ["図書ID", "タイトル", "貸出状況", "貸出日", "返却日", "利用者ID" ]
        book_list=self.book_list_display()

        book_list.insert(0,title)
        return book_list
    
    def book_exist(self, book_id):
        book_rows=self.lib_dao.get_book(book_id)
        # 入力したIDの本が存在しているか？
        if len(book_rows)==0:
            print("不正な図書ＩＤが入力されました。")
            return
        return book_rows
    
    def show_book_list_by_pandas(self):
        #pandasを使って一覧表示 >-----------------
        book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成
        title = ["図書ID", "タイトル", "貸出状況", "貸出日", "返却日", "利用者ID"]
        # pandas.options.display.max_colwidth=10
        pandas.set_option('display.unicode.east_asian_width', True)
        display = pandas.DataFrame(book_list,columns=title)
       
        print(display.to_string(index=False, justify='left'))
        #pandasを使って一覧表示 >-----------------

    def run(self):
        while True:
            try:
                print("1:利用者メニュー  2:図書メニュー  3:csv出力  5:ログアウト")
        
                choice = int(input("Enter your choice: "))


                if choice == 1: #利用者メニュー
                    pass

                elif choice == 2: #図書メニュー
                    self.show_book_list_by_pandas() #pandasを使ってbookリスト一覧表示
                    book_id = input("Enter borrow book id: ") #処理する図書のIDを入力

                    #book存在チェック
                    book_rows=self.book_exist(book_id)

                    if book_rows: #入力した図書IDが存在した場合処理を選ばせる
                            
                        for book_row in book_rows:
                            pass
                        # book情報を各変数に保存する
                        book_id=book_row[0]
                        book_title=book_row[1]
                        is_borrowed=book_row[2]
                        borrowed_date=book_row[3]
                        return_date=book_row[4]
                        borrow_id=book_row[5]

                        
                        print("1:貸出処理 2:返却処理 5:もどる")  ###
                        choice2 = int(input("Enter your choice: "))

                        if choice2 == 1: #貸出処理

                            if is_borrowed == False: #貸出中でなければ貸出処理
                                print(f"{book_row[0]} {book_row[1]}の貸出処理をします")

                                user_id = input("Enter borrow user id: ")
                                self.borrow_book(book_id,user_id)
                            else: #貸出中の場合
                                print(f"{book_id} {book_title}は貸出中です。")
                                

                        elif choice2 == 2:     #返却
                            if is_borrowed: #貸出中なら返却処理
                                print(f"{book_id} {book_title}の返却処理をします")
                                self.return_book(book_id)
                            else:
                                print("貸出中ではありません")
                                

                        elif choice2 == 5: #最初のメニューにもどる
                            pass #なにもせず図書メニューから抜ける
                    else:
                        pass
                    

                elif choice == 3: #CSV出力
                    choice = input("CSV出力しますか？(y/n):")
                    if choice == 'y':
                        self.books_display_csv()
                    else:
                        pass

                elif choice ==9: #お試し　book情報表示
                    #pandasを使って一覧表示
                    book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成
                    title = ["図書ID", "タイトル", "貸出状況", "貸出日", "返却日", "利用者ID", ]
                    # pandas.options.display.max_colwidth=10
                    pandas.set_option('display.unicode.east_asian_width', True)
                    display = pandas.DataFrame(book_list,columns=title)
                    
                    print(display.to_string(index=False, justify='left'))   
                    

                elif choice == 5:
                    print("ログアウト")
                    return
            except:
                print("不正な値です。")
                


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
            return
        else:
            user_rows=self.lib_dao.get_user_from_users(user_id) #userリストからuser情報取得
            for user_row in user_rows:
                count_books = user_row[2]
                       
            if len(user_rows)==0: #user_idが存在しない場合
                print("不正な利用者ＩＤが入力されました。")
                return
            elif count_books == 3: #user_idが存在しているがすでに3冊借りている
                print("利用者はすでに３冊の図書を借りています。")
                return
            else:
                for book_row in book_rows: #展開
                    pass


                # book情報を各変数に保存する
                book_id=book_row[0] #book_idセット
                book_title=book_row[1] #book_titleセット
                is_borrowed=book_row[2] #貸出状態をセット
                # borrowed_date=book_row[3]
                # return_date=book_row[4]

                user_id=user_id #本のデータにuser_idにセット

                if is_borrowed == False:
                    
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
                            return

                else:
                    print("図書はすでに貸出中です。")
                    return


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
            
        for book_row in book_rows:
            pass
        # book情報を各変数に保存する
        book_id=book_row[0]
        book_title=book_row[1]
        is_borrowed=book_row[2]
        borrowed_date=book_row[3]
        return_date=book_row[4]
        borrow_id=book_row[5]

        #user情報取得
        user_rows=self.lib_dao.get_user_from_users(borrow_id) 
        if user_rows: #利用者が存在していたら返却
            print(user_rows)
            for user_row in user_rows:
                pass
            print(user_row)
            count_books=user_row[2]

        
            print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n利用者ID：{borrow_id}\n返却日：{return_date}\n")   
            while True:
                key=input("返却しますか。y/n：")
                #返却確認
                if(key=="y"):

                    # 貸出数を減算する
                    count_books-=1

                    # 返却処理
                    self.lib_dao.return_book(book_id,borrow_id,count_books)
                    print(f"図書 {book_title}を返却しました。")
                    break

                elif(key=="n"):
                    break
                else:
                    print("正しく入力してください")
        else:
            print("貸し出されていません。")

    def books_display_csv(self): #図書一覧CSV出力

        
        rows=self.book_list_display_for_csv()
        print(rows)
        #CSVに変更する手順
        with open("books.csv","w") as f:
            data2=[]
            for row in rows:
                # print(row)
                s=""
                s+=str(row[0])+","
                s+=str(row[1])+","
                s+=str(row[2])+","
                s+=str(row[3])+","
                s+=str(row[4])+","
                s+=str(row[5])+"\n"
                data2.append(s)
            f.writelines(data2)
            f.flush()

        # with open("books.csv","w") as f:
            # print(f.writelines(data2))


        print("CSV出力完了")        


class LoginView:
    def __init__(self):
        self.lib_dao = LibraryDAO()

    def show_menu(self):
        print("1:ログイン 5:終了")  ###

    def run(self):
        while True:
            try:
                self.show_menu()
                choice = int(input("Enter your choice: "))
                if choice == 1:

                    staff_id = input("Enter staff id: ")

                    s_pass = input("Enter staff pass: ")
                    result = self.check_login(staff_id,s_pass)
                    if result == True:
                        return result
                    # break
                    
                elif choice == 5:
                    result = False
                    return result
                    # break

                else:
                    print("Invalid choice")
            except:
                print("不正な値です。")

    def check_login(self,staff_id,s_pass):
        rows = self.lib_dao.get_staff(staff_id,s_pass)
    
        if len(rows) == 0:
           print("ログインIDまたはパスワードが違います。")
           return False

        else:
             return True



