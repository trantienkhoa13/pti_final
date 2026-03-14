import json
import os
import sys
import webbrowser

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Tra ve duong dan day du cua file trong thu muc du an.
def get_path(file_name):
    return os.path.join(BASE_DIR, file_name)


# Doc du lieu contest tu file JSON.
def load_contests():
    file_path = get_path("contest.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if type(data) == dict and "contests" in data and type(data["contests"]) == list:
        return data["contests"]

    if type(data) == list:
        return data

    return []


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        # Nap giao dien tu file .ui da tao bang Qt Designer.
        uic.loadUi(get_path("login.ui"), self)
        self.signup_button.clicked.connect(self.show_register)
        self.login_button.clicked.connect(self.check_login)
        self.msg_box = QMessageBox()

    def check_login(self):
        # Lay du lieu nguoi dung nhap vao o input.
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        print(f"Email: '{email}' | Password: '{password}'")

        if email == "admin" and password == "admin":
            print("Login successful!")
            main.show()
            self.close()
        else:
            print("Login failed!")
            self.msg_box.warning(
                self,
                "Error",
                f"Invalid email or password!\nYou entered:\nEmail: '{email}'\nPassword: '{password}'",
            )

    def show_register(self):
        register.show()
        self.close()


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path("sign_in.ui"), self)
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
        uic.loadUi(get_path("main.ui"), self)

        # Gan su kien click cho cac nut dieu huong.
        self.account_button.clicked.connect(self.show_account)
        self.contest_button.clicked.connect(self.show_contest)
        self.top10_button.clicked.connect(self.show_top10)
        self.friend_button.clicked.connect(self.show_friend)
        self.gym_button.clicked.connect(self.show_gym)

    def show_account(self):
        account.show()
        self.close()

    def show_contest(self):
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
        uic.loadUi(get_path("account.ui"), self)

        self.logout_button.clicked.connect(self.logout)
        self.goout_button.clicked.connect(self.back_to_main)

    def logout(self):
        login.show()
        self.close()

    def back_to_main(self):
        main.show()
        self.close()


class Contest(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path("contest.ui"), self)

        # Cac nut menu tren man contest.
        self.account_button.clicked.connect(self.show_account)

        if hasattr(self, "main_button"):
            self.main_button.clicked.connect(self.show_main)
        if hasattr(self, "main_button_2"):
            self.main_button_2.clicked.connect(self.show_main)

        self.top10_button.clicked.connect(self.show_top10)
        self.friend_button.clicked.connect(self.show_friend)
        self.gym_button.clicked.connect(self.show_gym)
        self.history_button.clicked.connect(self.show_main)

        # Tao khu vuc rong de do danh sach contest.
        self.create_contest_area()
        self.load_contests_to_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_contests_to_ui()

    def create_contest_area(self):
        # An 2 contest mau cu trong file .ui vi du lieu se duoc tao dong bang code.
        if hasattr(self, "horizontalLayoutWidget"):
            self.horizontalLayoutWidget.hide()
        if hasattr(self, "horizontalLayoutWidget_2"):
            self.horizontalLayoutWidget_2.hide()

        # ScrollArea giup hien thi duoc nhieu contest va co thanh cuon.
        self.scroll_area = QScrollArea(self.centralwidget)
        self.scroll_area.setGeometry(30, 150, 520, 360)
        self.scroll_area.setWidgetResizable(True)

        # scroll_layout la noi se them tung contest widget vao.
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(10)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

    def load_contests_to_ui(self):
        # Moi lan load lai thi xoa danh sach cu truoc.
        self.clear_layout(self.scroll_layout)

        try:
            contests = load_contests()
        except Exception as error:
            self.scroll_layout.addWidget(self.create_message_widget(str(error)))
            self.scroll_layout.addStretch()
            return

        if len(contests) == 0:
            self.scroll_layout.addWidget(
                self.create_message_widget("Khong co contest trong file contest.json")
            )
            self.scroll_layout.addStretch()
            return

        # Tao 1 widget rieng cho moi contest trong JSON.
        for contest_data in contests:
            if type(contest_data) == dict:
                contest_widget = self.create_contest_widget(contest_data)
                self.scroll_layout.addWidget(contest_widget)

        self.scroll_layout.addStretch()

    def clear_layout(self, layout):
        # Xoa cac widget cu trong layout de tranh bi lap lai du lieu.
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def create_message_widget(self, text):
        # Widget don gian de hien thong bao loi hoac thong bao rong.
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout()
        label = QLabel(text)
        label.setWordWrap(True)

        layout.addWidget(label)
        frame.setLayout(layout)
        return frame

    def create_contest_widget(self, contest_data):
        # Moi contest se duoc dong goi trong 1 frame rieng.
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)

        main_layout = QHBoxLayout()
        info_layout = QVBoxLayout()

        # Lay thong tin tu dict. Neu thieu truong thi dung gia tri mac dinh.
        name = contest_data.get("name", "Untitled Contest")
        date = contest_data.get("date", "N/A")
        difficulty = contest_data.get("difficulty", contest_data.get("difficult", "N/A"))
        participants = contest_data.get("participants", "N/A")
        status = contest_data.get("status", "")
        link = contest_data.get("link", "")

        name_label = QLabel(name)
        name_label.setWordWrap(True)

        # Noi cac thong tin contest thanh 1 doan text de hien thi.
        info_text = "Date: " + str(date) + "\n"
        info_text += "Difficulty: " + str(difficulty) + "\n"
        info_text += "Participants: " + str(participants)

        if status != "":
            info_text += "\nStatus: " + str(status)

        info_label = QLabel(info_text)
        info_label.setWordWrap(True)

        join_button = QPushButton("Join")
        join_button.setFixedWidth(100)

        # Dung lambda de nho dung link cua tung contest.
        if link != "":
            join_button.clicked.connect(
                lambda checked, url=link: self.open_link(url)
            )
        else:
            join_button.setEnabled(False)

        info_layout.addWidget(name_label)
        info_layout.addWidget(info_label)

        main_layout.addLayout(info_layout)
        main_layout.addWidget(join_button)

        frame.setLayout(main_layout)
        return frame

    def open_link(self, link):
        # Mo contest bang trinh duyet mac dinh cua may.
        if link == "":
            QMessageBox.warning(self, "Error", "Contest nay chua co link")
            return

        webbrowser.open(link)

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


class Top10(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(get_path("top10.ui"), self)

        self.account_button.clicked.connect(self.show_account)
        self.contest_button.clicked.connect(self.show_contest)
        self.history_button.clicked.connect(self.show_main)
        self.friend_button.clicked.connect(self.show_friend)
        self.gym_button.clicked.connect(self.show_gym)

    def show_account(self):
        account.show()
        self.close()

    def show_contest(self):
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
        uic.loadUi(get_path("friend.ui"), self)

        self.account_button.clicked.connect(self.show_account)
        self.main_button.clicked.connect(self.show_main)
        self.contest_button.clicked.connect(self.show_contest)
        self.top10_button.clicked.connect(self.show_top10)
        self.history_button.clicked.connect(self.show_main)
        self.gym_button.clicked.connect(self.show_gym)

    def show_account(self):
        account.show()
        self.close()

    def show_contest(self):
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
        uic.loadUi(get_path("gym.ui"), self)

        self.account_button.clicked.connect(self.show_account)
        self.pushButton_9.clicked.connect(self.show_main)
        self.top10_button.clicked.connect(self.show_top10)
        self.contest_button.clicked.connect(self.show_contest)
        self.history_button.clicked.connect(self.show_main)
        self.friend_button.clicked.connect(self.show_friend)

    def show_account(self):
        account.show()
        self.close()

    def show_contest(self):
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
    contest = Contest()

    login.show()

    app.exec()
