from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import sys
import os
import webbrowser

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.signup_button.clicked.connect(self.show_register)
        self.login_button.clicked.connect(self.check_login)
        self.msg_box = QMessageBox()
    
    def check_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Debug
        print(f"Email: '{email}' | Password: '{password}'")
        
        if email == "admin" and password == "admin":
            print("Login successful!")
            main.show()
            self.close()
        else:
            print("Login failed!")
            self.msg_box.warning(self, "Error", f"Invalid email or password!\nYou entered:\nEmail: '{email}'\nPassword: '{password}'")
            
    def show_register(self):
        register.show()
        self.close()


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("sign_in.ui", self)
        self.signup_button.clicked.connect(self.register_user)
        self.signin_button.clicked.connect(self.back_to_login)
        self.msg_box = QMessageBox()
    
    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        cfp = self.cfp_input.text().strip()
        email = self.email_input.text().strip()
        
        if password == cfp and username and email:
            self.msg_box.information(self, "Success", "Registration successful!")
            self.back_to_login()
        else:
            self.msg_box.warning(self, "Error", "Please check your inputs!")
    
    def back_to_login(self):
        login.show()
        self.close()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        
        self.account_button.clicked.connect(self.show_account)
        self.contest_button.clicked.connect(self.show_contest)  # ADDED
        self.top10_button.clicked.connect(self.show_top10)
        self.friend_button.clicked.connect(self.show_friend)
        self.gym_button.clicked.connect(self.show_gym)
        
    def show_account(self):
        account.show()
        self.close()
    
    def show_contest(self):  # ADDED
        contest.show()
        self.close()
        
    def show_top10(self):
        top10.show()
        self.close()
        
    def show_friend(self):
        friend.show()
        self.close()
        
    def show_gym(self):
        gym.show()
        self.close()


class Account(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("account.ui", self)
        
        self.logout_button.clicked.connect(self.logout)
        self.goout_button.clicked.connect(self.back_to_main)
        
    def logout(self):
        login.show()
        self.close()
        
    def back_to_main(self):
        main.show()
        self.close()


class Contest(QMainWindow):  # ADDED NEW CLASS
    def __init__(self):
        super().__init__()
        uic.loadUi("contest.ui", self) 
        
        
        if hasattr(self, 'account_button'):
            self.account_button.clicked.connect(self.show_account)
        if hasattr(self, 'main_button'):
            self.main_button.clicked.connect(self.show_main)
        if hasattr(self, 'top10_button'):
            self.top10_button.clicked.connect(self.show_top10)
        if hasattr(self, 'friend_button'):
            self.friend_button.clicked.connect(self.show_friend)
        if hasattr(self, 'gym_button'):
            self.gym_button.clicked.connect(self.show_gym)
        if hasattr(self, 'history_button'):
            self.history_button.clicked.connect(self.show_main)
        if hasattr(self, 'join1'):
            self.join1.clicked.connect(self.join1)

     
    def show_account(self):
        account.show()
        self.close()
        
    def show_main(self):
        main.show()
        self.close()
        
    def show_top10(self):
        top10.show()
        self.close()
        
    def show_friend(self):
        friend.show()
        self.close()
        
    def show_gym(self):
        gym.show()
        self.close()
    
    def open_link(id):
        for contest in contestData:
            if contest["id"] == id:
                webbrowser.open(contest["link"])
                break


class contestData ():
    def __init__ (self,file_path):
        self.contest_list = []
        self.file_path = file_path
        self.load_data()

    def load_data (self ):
        data = read_json(self.file_path)

        for item in data :
            contest = contest_item(
                id= item.get("id"),
                name=item.get("name"),
                date=item.get("date"),
                participants=item.get ("participants"),
                difficult=item.get ("difficult"),
                link=item.get("link"),
                img=item.get("img")
            )
            self.contest_list.append(contest)

    def save_data (self):
        data = []
        for anime in self.anime_list:
            data.append (anime.to_dict())
        write_json (self.file_path,data)


    



class contest_item ():
    def __init__(self , id , name , date,  difficult , participants = None, link= None, img = None):
        self.id = id
        self.name = name
        self.date = date
        self.difficult = difficult
        self.participants  = float (participants) if participants else 0
        self.link = link
        self.img = img 

    def update (self , newdata):
        if "id" in newdata:
            self.id = newdata ["id"]
        if "name" in newdata:
            self.id = newdata ["name"]
        if "date" in newdata:
            self.id = newdata ["date"]
        if "participants" in newdata:
            try:
                self.id = float(newdata ["participants"])
            except ValueError :
                print("participants not avaible")
        if "link" in newdata:
            self.id = newdata ["link"]
        if "img" in newdata:
            self.id = newdata ["img"]


    def to_dict (self):
        return {
            "id": self.id,
            "name":self.name,
            "date":self.date,
            "difficult":self.difficult,
            "participants":self.participants,
            "link":self.link,
            "img":self.img
        }


class Top10(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("top10.ui", self)
        
        self.account_button.clicked.connect(self.show_account)
        self.contest_button.clicked.connect(self.show_contest)  # UPDATED
        self.history_button.clicked.connect(self.show_main)
        self.friend_button.clicked.connect(self.show_friend)
        self.gym_button.clicked.connect(self.show_gym)
        
    def show_account(self):
        account.show()
        self.close()
    
    def show_contest(self):  # ADDED
        contest.show()
        self.close()
        
    def show_main(self):
        main.show()
        self.close()
        
    def show_friend(self):
        friend.show()
        self.close()
        
    def show_gym(self):
        gym.show()
        self.close()


class Friend(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("friend.ui", self)
        
        self.account_button.clicked.connect(self.show_account)
        self.main_button.clicked.connect(self.show_main)
        self.contest_button.clicked.connect(self.show_contest)  # UPDATED
        self.top10_button.clicked.connect(self.show_top10)
        self.history_button.clicked.connect(self.show_main)
        self.gym_button.clicked.connect(self.show_gym)
        
    def show_account(self):
        account.show()
        self.close()
    
    def show_contest(self):  # ADDED
        contest.show()
        self.close()
        
    def show_main(self):
        main.show()
        self.close()
        
    def show_top10(self):
        top10.show()
        self.close()
        
    def show_gym(self):
        gym.show()
        self.close()


class Gym(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gym.ui", self)
        
        self.account_button.clicked.connect(self.show_account)
        self.pushButton_9.clicked.connect(self.show_main)  
        self.top10_button.clicked.connect(self.show_top10)
        self.contest_button.clicked.connect(self.show_contest)  # UPDATED
        self.history_button.clicked.connect(self.show_main)
        self.friend_button.clicked.connect(self.show_friend)
        
    def show_account(self):
        account.show()
        self.close()
    
    def show_contest(self):  # ADDED
        contest.show()
        self.close()
        
    def show_main(self):
        main.show()
        self.close()
        
    def show_top10(self):
        top10.show()
        self.close()
        
    def show_friend(self):
        friend.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    global login, register, main, account, top10, friend, gym, contest
    
    login = Login()
    register = Register()
    main = Main()
    account = Account()
    top10 = Top10()
    friend = Friend()
    gym = Gym()
    contest = Contest()  # ADDED
    
    login.show()
    
    app.exec()