
from views import *

class LibraryController: #図書システム
    def __init__(self):
        self.lib_view = LibraryView()

    def run(self):
        self.lib_view.run()

class LoginController: #ログイン機能
    def __init__(self):
        self.login_view = LoginView()

    def run(self):
        return self.login_view.run()

if __name__ == '__main__':
    while True:
        login_c=LoginController()
        check=login_c.run() #ログイン
        if check==True: #ログイン成功の場合
            lib_controller = LibraryController()
            lib_controller.run() #図書システム スタート
        else:
            print("終了")
            break