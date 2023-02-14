from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
import customtkinter

gpa = 0.0


# function to delete login elements and create gpa elements
def delete_login():
    username_entry.destroy()
    password_entry.destroy()
    login_button.destroy()


# function to display current letter grades and corresponding gpa
def display_gpa(class_names, letter_grades, gpa_points):
    global gpa

    # make number of rows that is equal to the number of classes
    for i in range(len(class_names) + 1):
        frame.grid_rowconfigure(i, weight=1)

    # make 4 columns
    for i in range(4):
        frame.grid_columnconfigure(i, weight=1)

    # make column labels
    class_label = customtkinter.CTkLabel(
        master=frame, text="Class:", font=("Arial", 20)
    )
    class_label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

    letter_grade_label = customtkinter.CTkLabel(
        master=frame, text="Letter Grade:", font=("Arial", 20)
    )
    letter_grade_label.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")

    gpa_label = customtkinter.CTkLabel(
        master=frame, text="Class GPA:", font=("Arial", 20)
    )
    gpa_label.grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

    end_gpa_label = customtkinter.CTkLabel(
        master=frame, text="Final GPA:", font=("Arial", 20)
    )
    end_gpa_label.grid(row=0, column=3, pady=10, padx=10, sticky="nsew")

    # create class name labels
    for i in range(len(class_names)):
        class_name_label = customtkinter.CTkLabel(
            master=frame, text=class_names[i], font=("Arial", 20)
        )
        class_name_label.grid(row=i + 1, column=0, pady=10, padx=10, sticky="nsew")

    # create letter grade labels
    for i in range(len(letter_grades)):
        letter_grade_label = customtkinter.CTkLabel(
            master=frame, text=letter_grades[i], font=("Arial", 20)
        )
        letter_grade_label.grid(row=i + 1, column=1, pady=10, padx=10, sticky="nsew")

    # create gpa labels
    for i in range(len(gpa_points)):
        gpa_label = customtkinter.CTkLabel(
            master=frame, text=gpa_points[i], font=("Arial", 20)
        )
        gpa_label.grid(row=i + 1, column=2, pady=10, padx=10, sticky="nsew")

    # make gpa label
    gpa_label = customtkinter.CTkLabel(
        master=frame, text=f"GPA: {gpa}", font=("Arial", 20)
    )
    gpa_label.grid(row=1, column=3, pady=10, padx=10, sticky="nsew")

    app.update()


# function to get gpa from oncourseconnect
def get_gpa():
    global gpa

    username = username_entry.get()
    password = password_entry.get()

    delete_login()

    # create loading label
    loading_label = customtkinter.CTkLabel(
        master=frame, text="Loading...", font=("Arial", 20)
    )
    loading_label.pack(pady=10, padx=10, anchor="center")

    # update window
    app.update()

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.set_window_size(1920, 1080)

    driver.get("https://oncourseconnect.com/login")

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, """//*[@id=":r0:"]"""))
    )

    username_input = driver.find_element(By.XPATH, """//*[@id=":r0:"]""")
    password_input = driver.find_element(By.XPATH, """//*[@id="passwordField"]""")

    username_input.send_keys(username)
    password_input.send_keys(password)

    driver.find_element(By.XPATH, """//*[@id=":r2:"]""").click()

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, """//*[@id="root"]/div/div/div/div/ul[2]/li[4]/a""")
        )
    )

    driver.find_element(
        By.XPATH, """//*[@id="root"]/div/div/div/div/ul[2]/li[4]/a"""
    ).click()

    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                """//*[@id="main"]/div[2]/div[3]/section/div/table/tbody/tr[1]/td[9]""",
            )
        )
    )

    class_names = []

    # make loop to generate xpath for each class
    for i in range(1, 10):
        class_names.append(
            driver.find_element(By.XPATH, f"""//*[@id="main"]/div[2]/div[3]/section/div/table/tbody/tr[{i}]/td[1]/p"""
                                ).text)

    gpa_points = []
    grade_letters = []

    for i in range(1, 10):
        try:
            grade = driver.find_element(By.XPATH, f"""//*[@id="main"]/div[2]/div[3]/section/div/table/tbody/tr[{i}]/td[9]""").text
        except:
            continue

        # if grade is a number, convert to letter grade
        if grade.isnumeric():
            grade = int(grade)

            if grade >= 93:
                grade = "A+"
            elif grade >= 90:
                grade = "A"
            elif grade >= 87:
                grade = "A-"
            elif grade >= 83:
                grade = "B+"
            elif grade >= 80:
                grade = "B"
            elif grade >= 77:
                grade = "B-"
            elif grade >= 73:
                grade = "C+"
            elif grade >= 70:
                grade = "C"
            elif grade >= 67:
                grade = "C-"
            elif grade >= 63:
                grade = "D+"
            elif grade >= 60:
                grade = "D"
            elif grade >= 57:
                grade = "D-"
            elif grade < 57:
                grade = "F"

        grade_letters.append(grade)

        # convert letter grade to grade point
        if grade == "A+":
            grade = 4.0
        elif grade == "A":
            grade = 4.0
        elif grade == "A-":
            grade = 3.67
        elif grade == "B+":
            grade = 3.33
        elif grade == "B":
            grade = 3.0
        elif grade == "B-":
            grade = 2.67
        elif grade == "C+":
            grade = 2.33
        elif grade == "C":
            grade = 2.0
        elif grade == "C-":
            grade = 1.67
        elif grade == "D+":
            grade = 1.33
        elif grade == "D":
            grade = 1.0
        elif grade == "D-":
            grade = 0.67
        elif grade == "F":
            grade = 0.0

        gpa_points.append(grade)

    driver.quit()

    number_of_grades = len(gpa_points)
    total = sum(gpa_points)

    gpa = round(total / number_of_grades, 2)

    # delete loading label
    loading_label.destroy()

    app.update()

    display_gpa(class_names, grade_letters, gpa_points)


app = customtkinter.CTk()
app.geometry("1000x700")
app.title("GPA Calculator")
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# make frame that fills top 1/4 of the window
top_frame = customtkinter.CTkFrame(app, height=100)
top_frame.pack(fill="x", padx=10, pady=(10, 0))

# make frame that fills the entire window
frame = customtkinter.CTkFrame(app)
frame.pack(fill="both", expand=True, padx=10, pady=10)

app_text = customtkinter.CTkLabel(top_frame, text="GPA Calculator", font=("Arial", 25))
label_text = customtkinter.CTkLabel(
    top_frame, text="Oncourse Connect Automation Tool", font=("Arial", 15)
)

username_entry = customtkinter.CTkEntry(frame, placeholder_text="Username")
password_entry = customtkinter.CTkEntry(frame, placeholder_text="password", show="*")

# make login button that calls the get_gpa function and passes the username and password
login_button = customtkinter.CTkButton(
    frame,
    text="Login",
    command=get_gpa,
)

label_text.pack(pady=20, padx=20, side="right", anchor="e")
app_text.pack(pady=20, padx=20, side="left", anchor="w")

username_entry.place(relx=0.5, rely=0.5, anchor="center")
password_entry.place(relx=0.5, rely=0.545, anchor="center")
login_button.place(relx=0.5, rely=0.593, anchor="center")

app.mainloop()
