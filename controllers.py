from views import *

class LibraryController:
    def __init__(self):
        self.lib_view = LibraryView()

    def run(self):
        self.lib_view.run()

class LoginController:
    def __init__(self):
        self.login_view = LoginView()

    def run(self):
        return self.login_view.run()

if __name__ == '__main__':
    while True:
        login_c=LoginController()
        check=login_c.run()
        if check==True:
            
            lib_controller = LibraryController()
            lib_controller.run()
        else:
            print("終了")
            break