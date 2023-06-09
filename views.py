from LibraryDao import *
import pandas
from UsersDao import *
from common import *


class LibraryView:
    def __init__(self):
        self.lib_dao = LibraryDao()
        self.users_dao = UsersDao()
        self.title = ["図書ID", "ISBN", "タイトル", "タイトル(かな)", "貸出状況", "貸出日", "返却日", "利用者ID", "貸出回数" ] ###
        #self.users_title = ["利用者ID", "利用者名", "貸出回数" ]
        self.books_ranking_title = ["ランキング","ISBN", "タイトル", "貸出回数" ]
    

        
    def book_cell_format_change(self, books): #図書情報の内容を表示用に変換してリストで渡す
        book_list=[]
         #*** bookテーブルのフィールド構成 ***    
        # book_id=book_row[0]
        # book_title=book_row[1]
        # is_borrowed=book_row[2]
        # borrowed_date=book_row[3]
        # return_date=book_row[4]
        # borrow_id=book_row[5]
    #************************************
        for book in books:
            book = list(book)
            if book[4]: #is_borrowed
                book[4]="貸出中"
                book[5]=book[5].strftime('%Y/%m/%d')
                book[6]=book[6].strftime('%Y/%m/%d')
            else:
                book[4]="貸出可能"
                book[5]="-"
                book[6]="-"
                book[7]="-"
            book_list.append(book)
        return book_list


    def book_list_display(self): #図書の表示用リスト作成
        books = self.lib_dao.get_all()
        book_list=self.book_cell_format_change(books)
        return book_list

    #     book_list=[]

    # #*** bookテーブルのフィールド構成 ***    
    #     # book_id=book_row[0]
    #     # book_title=book_row[1]
    #     # is_borrowed=book_row[2]
    #     # borrowed_date=book_row[3]
    #     # return_date=book_row[4]
    #     # borrow_id=book_row[5]
    # #************************************
    #     for book in books:
    #         book = list(book)
    #         if book[2]: #is_borrowed
    #             book[2]="貸出中"
    #             book[3]=book[3].strftime('%Y/%m/%d')
    #             book[4]=book[4].strftime('%Y/%m/%d')
    #         else:
    #             book[2]="貸出可能"
    #             book[3]="-"
    #             book[4]="-"
    #             book[5]="-"
    #         book_list.append(book)

    
    def book_list_display_for_csv(self): #図書のCSV用リスト作成
        
        book_list=self.book_list_display()
        book_list.insert(0,self.title)
        return book_list
    
    def borrowed_books_list_display_for_csv(self): #貸出中図書のCSV用リスト作成
        
        borrowed_books=self.lib_dao.get_user_from_borrowed_books(is_borrowed = True)
        borrowed_books_list=self.book_cell_format_change(borrowed_books)

        borrowed_books_list.insert(0,self.title) #一覧の項目名を１行目に挿入
        return borrowed_books_list
    
    
    def book_exist(self, book_id):
        book_rows=self.lib_dao.get_book(book_id)
        # 入力したIDの本が存在しているか？
        if len(book_rows)==0:
            print("不正な図書ＩＤが入力されました。")
            return
        return book_rows
    
    def show_book_list_by_pandas(self, book_list): #pandasを使って一覧表示 >-----------------
        # book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成→引数で受け取るように変更

        pandas.set_option('display.unicode.east_asian_width', True)
        display = pandas.DataFrame(book_list,columns=self.title)    
        print(display.to_string(index=False))

    def show_book_ranking_by_pandas(self, book_list): #pandasを使って一覧表示 >-----------------
        # book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成→引数で受け取るように変更
        # pandas.options.display.max_colwidth=10
        pandas.set_option('display.unicode.east_asian_width', True)
        display = pandas.DataFrame(book_list,columns=self.title)    
        display['rank']=display['貸出回数'].rank(ascending=False, method='min').astype('int')
        print(display.to_string(index=False))


    
    def book_ranking_list_display(self): #bookランキングの表示用リスト作成
        rannking_list = self.lib_dao.get_ranking_book()
        return rannking_list

    def show_book_ranking_list_by_pandas(self, ranking_list): #pandasを使って一覧表示 >-----------------
        # ranking_list=self.book_ranking_list_display()#bookランキング情報を表示用に加工してリストを作成
        count=1
        old_num=-1
        rank=1
        ranking_list2=[]
        for row in ranking_list:
            # row[2]=int(row[2])
            num=row[2]
            # print("num:",num) #
            row2=list(row)
            if(num<old_num):
                rank=count
            row2.insert(0,rank)
            ranking_list2.append(tuple(row2))
            old_num=num
            count+=1
        # ranking_num=list(range(1,1+len(ranking_list)))
        pandas.set_option('display.unicode.east_asian_width', True)
        # pandas.index('ranking')
        # display = pandas.DataFrame(ranking_list,columns=self.books_ranking_title,index=ranking_num)    
        display = pandas.DataFrame(ranking_list2,columns=self.books_ranking_title)    
        print(display.to_string(index=False))
        # return display


    def run(self):
        while True:
            try:
                print("1:利用者メニュー  2:図書貸出・返却  3:図書データCSV出力  4:図書登録・削除  5:ランキング   6:図書検索  0:ログアウト")

                choice = int(input("Enter your choice: "))

                if choice == 1: #利用者メニュー
                    user_list=self.users_dao.user_list_display()#利用者情報を表示用に加工してリストを作成
                    self.users_dao.show_user_list_by_pandas(user_list) #pandasを使ってuserリスト一覧表示
                    # users_view=UsersView()
                    print("1:利用者登録  2:利用者一覧  3:利用者一覧CSV出力  4:利用者削除  5:利用者検索  0:もどる")

                    choice1 = int(input("Enter your choice: "))

                    if choice1 == 1: #利用者登録
                        self.users_dao.user_register_function()


                    elif choice1 == 2: #利用者一覧
                        # self.users_dao.user_list_display()
                        user_list=self.users_dao.user_list_display()#利用者情報を表示用に加工してリストを作成
                        self.users_dao.show_user_list_by_pandas(user_list) #pandasを使ってuserリスト一覧表示


                    elif choice1 == 3: #利用者一覧CSV出力
                        self.users_dao.users_display_csv()

                    elif choice1 == 4: #利用者削除

                        self.users_dao.user_delete_function()

                    elif choice1 == 5: #利用者検索
                        search_data=self.users_dao.search_user()
                        if search_data!=None:
                            self.users_dao.show_user_list_by_pandas(search_data) #pandasを使ってuserリスト一覧表示
                        else:
                            print("該当する名前がありません")


                    elif choice1 == 0: #もどる
                        pass


                elif choice == 2: #図書貸出返却
                    book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成
                    # self.show_book_ranking_by_pandas(book_list) #pandasを使ってbookリスト一覧表示(ランキング)
                    self.show_book_list_by_pandas(book_list) #pandasを使ってbookリスト一覧表示

                    book_id = input("Enter book id: ") #処理する図書のIDを入力

                    #book存在チェック
                    book_rows=self.book_exist(book_id)

                    if book_rows: #入力した図書IDが存在した場合処理を選ばせる
                            
                        for book_row in book_rows:
                            pass
                        # book情報を各変数に保存する
                        book_id=book_row[0]
                        isbn=book_row[1]
                        book_title=book_row[2]
                        book_kana=book_row[3]
                        is_borrowed=book_row[4]
                        borrowed_date=book_row[5]
                        return_date=book_row[6]
                        borrow_user=book_row[7]

                        
                        print("1:貸出処理 2:返却処理 0:もどる")  ###
                        choice2 = int(input("Enter your choice: "))

                        if choice2 == 1: #貸出処理

                            if is_borrowed == False: #貸出中でなければ貸出処理
                                print(f"{book_id} {book_title}の貸出処理をします")

                                user_id = input("Enter borrow user id: ")
                                self.borrow_book(book_id,user_id)
                            
                            else: #貸出中の場合
                                print(f"{book_id} {book_title}、図書はすでに貸出中です。")  #文言訂正 2023/03/23 石井
                                

                        elif choice2 == 2:     #返却
                            if is_borrowed: #貸出中なら返却処理
                                print(f"{book_id} {book_title}の返却処理をします")
                                self.return_book(book_id)
                            else:
                                print(f"{book_title}、図書は貸出されていません。")  #文言訂正 2023/03/23 石井
                        

                        elif choice2 == 0: #最初のメニューにもどる
                            pass #なにもせず図書メニューから抜ける
                    else: #入力した図書IDが存在しない場合は何もせずメニューにもどる
                        pass
                    

                elif choice == 3: #CSV出力
                    print("1:全図書CSV 2:貸出中CSV 0:もどる")  ###
                    choice3 = int(input("Enter your choice: "))


                    if choice3 == 1: #全図書CSV表示
                        choice3_1 = input("CSV出力しますか？(y/n):")
                        if choice3_1 == 'y':
                            self.books_display_csv() #図書一覧のCSV出力を実行
                        else:
                            pass
                        
                    elif choice3 == 2: #貸出中図書のCSV出力を実行
                        choice3_2 = input("CSV出力しますか？(y/n):")
                        if choice3_2 == 'y':
                            self.borrowed_books_display_csv() #図書一覧のCSV出力を実行
                        else:
                            pass
                    
                elif choice == 4: #図書登録・削除
                    # users_view=UsersView()
                    book_list=self.book_list_display()#図書情報を表示用に加工してリストを作成

                    self.show_book_list_by_pandas(book_list) #pandasを使ってbookリスト一覧表示
                    print("1:図書登録  2:図書削除  0:もどる")
                    choice1 = int(input("Enter your choice: "))

                    if choice1 == 1: #図書登録
                        
                        book_id=input("Enter book id: ")
                        isbn=input("Enter book isbn: ")
                        book_title=input("Enter book title: ")
                        book_kana=input("Enter book title(kana)")
                        self.lib_register(book_id,isbn,book_title,book_kana)


                    elif choice1 == 2: #図書削除
                        book_id=input("Enter book id: ")
                        self.lib_delete(book_id)

                    elif choice1 == 0: #もどる
                        pass

                elif choice == 5: #ランキング
                    # self.lib_dao.ranking_list()
                    book_list=self.book_ranking_list_display()#図書情報を表示用に加工してリストを作成

                    self.show_book_ranking_list_by_pandas(book_list) #pandasを使ってbookランキングリスト一覧表示

                    self.lib_dao.show_ranking_graph() #グラフ表示
                    
                elif choice == 6: #図書検索
                    # self.lib_dao.search_book()
                    results=self.lib_dao.search_book()
                    if results!=None:
                        book_list=self.book_cell_format_change(results)
                        self.show_book_list_by_pandas(book_list)
                    else:
                        print("該当する図書がありません")


                elif choice == 0:
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
#
    def borrow_book(self,book_id,user_id): #貸出処理メイン
        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)

        # 入力したIDの本が存在しているか？
        if len(book_rows)==0:
            print("不正な図書ＩＤが入力されました。")
            return
        else:
            user_rows=self.lib_dao.get_user_from_users(user_id) #userリストからuser情報取得
            for user_row in user_rows:
                count_books = user_row[3]
                       
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
                # isbn=book_row[1]
                book_title=book_row[2] #book_titleセット
                # book_kana=book_row[3]
                is_borrowed=book_row[4] #貸出状態をセット
                # borrowed_date=book_row[5]
                # return_date=book_row[6]
                # borrow_user=book_row[7]
                count_borrowed=book_row[8]

                user_id=user_id #本のデータにuser_idにセット

                if is_borrowed == False:
                    
                    print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n")   
                    while True:
                        key=input("貸出処理しますか。y/n：")
                        #貸出確認
                        if(key=="y"):

                            # 貸出数を加算する
                            count_books+=1
                            count_borrowed+=1
                            
                            # 貸出処理   2023.03.24 修正　石井
                            borrow_success=self.lib_dao.borrow_book_dao(book_id,user_id,count_books,count_borrowed)
                            if borrow_success:
                                print(f"{book_title}の貸出処理をしました。")
                                books = self.lib_dao.get_book(book_id)
                                for book in books:
                                    book = list(book)
                                    book[6]=book[6].strftime('%Y/%m/%d')
                                # print(book)
                                print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n利用者ID：{user_id}\n返却日：{book[6]}\n")
                                break

                            else:
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
#
    def return_book(self,book_id): #返却処理メイン
        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)
            
        for book_row in book_rows:
            pass
        # book情報を各変数に保存する
        book_id=book_row[0]
        # isbn=book_row[1]
        book_title=book_row[2]
        # book_kana=book_row[3]
        is_borrowed=book_row[4]
        # borrowed_date=book_row[5]
        return_date=book_row[6]
        borrow_id=book_row[7]
        count_borrowed=book_row[8]


        #user情報取得
        user_rows=self.lib_dao.get_user_from_users(borrow_id) 
        if user_rows: #利用者が存在していたら返却
            # print(user_rows)
            for user_row in user_rows:
                pass
            # print(user_row)
            count_books=user_row[3]

        
            print(f"図書ID：{book_id}\n図書タイトル：{book_title}\n利用者ID：{borrow_id}\n返却日：{return_date.strftime('%Y/%m/%d')}\n")   
            while True:
                key=input("返却しますか。y/n：")
                #返却確認
                if(key=="y"):

                    # 貸出数を減算する
                    count_books-=1

                    # 返却処理
                    return_success=self.lib_dao.return_book_dao(book_id,borrow_id,count_books)
                    if return_success:
                        print(f"図書 {book_title}を返却しました。")
                        break
                    else:
                        break

                elif(key=="n"):
                    break
                else:
                    print("正しく入力してください")
        else:
            print("図書は貸出されていません。") #文言訂正 2023/03/23 石井


    def books_display_csv(self): #図書一覧CSV出力
        rows=self.book_list_display_for_csv()
        # print(rows)
        #CSVに変更する手順
        with open("books.csv","w", encoding='utf-8') as f:
            data2=[]
            for row in rows:
                # print(row)
                s=""
                s+=str(row[0])+","
                s+=str(row[1])+","
                s+=str(row[2])+","
                s+=str(row[3])+","
                s+=str(row[4])+","
                s+=str(row[5])+","
                s+=str(row[6])+","
                s+=str(row[7])+","
                s+=str(row[8])+"\n"
                data2.append(s)
            f.writelines(data2)
            f.flush()

        print("全件CSV出力完了")     

    def borrowed_books_display_csv(self): #図書一覧CSV出力
        rows=self.borrowed_books_list_display_for_csv()
        # print(rows)
        #CSVに変更する手順
        with open("borrowed_books.csv","w", encoding='utf-8') as f:
            data2=[]
            for row in rows:
                # print(row)
                s=""
                s+=str(row[0])+","
                s+=str(row[1])+","
                s+=str(row[2])+","
                s+=str(row[3])+","
                s+=str(row[4])+","
                s+=str(row[5])+","
                s+=str(row[6])+","
                s+=str(row[7])+","
                s+=str(row[8])+"\n"
                data2.append(s)
            f.writelines(data2)
            f.flush()

        print("CSV出力完了")     

#
# 図書登録入力処理
#   input   1)book_id  図書ID
#           2)book_title 図書名
#   output  1)book_id  図書ID
#           2)book_title 図書名
#
    def lib_register(self,book_id,isbn,book_title,book_kana): #図書登録入力処理メイン
        if(str.isdecimal(book_id)==False):
            print("図書IDは数字のみです。")
            return       

        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)
            
        if len(book_rows)!=0:
            print("図書IDが重複しています。")
            return

        char_len=get_east_asian_width_count(book_title)     
        if char_len<=0:
            print("図書名が入力されていません。")
            return
        if char_len>40:
            print("図書名の長さが最大値を超えています。")
            return
        char_kana_len=get_east_asian_width_count(book_kana)     
        if char_kana_len<=0:
            print("図書名(かな)が入力されていません。")
            return

        # 図書登録処理
        return_success=self.lib_dao.lib_register_dao(book_id,isbn,book_title,book_kana)
        if return_success:
            print(f"図書ID：{book_id}\t図書名： {book_title}を登録しました。")
        else:
            pass
#
# 図書削除確認処理
#   input   1)book_id  図書ID
#   output  1)book_id  図書ID
#
    def lib_delete(self,book_id): #図書削除確認処理メイン

        # 該当book情報を取得
        book_rows=self.lib_dao.get_book(book_id)
            
        if len(book_rows)==0:
            print("図書が登録されていません。")
            return

        for book_row in book_rows:
            pass
        # book情報を各変数に保存する
        book_id=book_row[0]
        # isbn=book_row[1]
        book_title=book_row[2]
        # book_title_kana=book_row[3]
        is_borrowed=book_row[4]
        borrowed_date=book_row[5]
        return_date=book_row[6]
        borrow_id=book_row[7]

        if is_borrowed!=0:
            print("貸出中の図書を削除できません。")
            return

        # 図書削除処理
        return_success=self.lib_dao.lib_delete_dao(book_id)
        if return_success:
            print(f"図書{book_title}を削除しました。")
        else:
            pass


class LoginView:
    def __init__(self):
        self.lib_dao = LibraryDao()

    def run(self):
        while True:
            try:
                print("1:ログイン 0:終了")
                choice = int(input("Enter your choice: "))
                if choice == 1:

                    staff_id = input("Enter staff id: ") #ログインID入力
                    s_pass = input("Enter staff pass: ") #パスワード入力
                    staff_id_pass = (staff_id, s_pass)
                    result = self.check_login(staff_id_pass) #ログイン可能かチェック
                    if result == True:
                        return result
                    # break
                    
                elif choice == 0:
                    result = False
                    return result

                else:
                    print("Invalid choice")
            except:
                print("不正な値です。")

    def check_login(self,staff_id_pass):
        rows = self.lib_dao.get_staff(staff_id_pass)
        # rows = self.lib_dao.get_staff(staff_id_pass)
    
        if len(rows) == 0:
           print("ログインIDまたはパスワードが違います。")
           return False

        else: #ログイン成功
             return True
