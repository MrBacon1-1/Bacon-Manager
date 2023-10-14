
#----------------------------------Modules----------------------------------#

import os
import colorama
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import hashlib
import time
import keyboard
from tabulate import tabulate
import pyperclip
import random
import customtkinter
import base64
import tkinter
import ctypes

#----------------------------------Constants----------------------------------#

version = "v1.0"
SW_HIDE = 0
SW_SHOW = 5

MAIN_MENU = f"""                                                        

                                                    ______                            __ _  __
                                                   / ____/___  ____________  ______  / /| |/ /
                                                  / __/ / __ \/ ___/ ___/ / / / __ \/ __/   / 
                                                 / /___/ / / / /__/ /  / /_/ / /_/ / /_/   |  
                                                /_____/_/ /_/\___/_/   \__, / .___/\__/_/|_|  {version}
                                                                      /____/_/                  

                                                                            |
                                                                            |          <Options>
                                ^7YGB#&&&&#BGY7^                            |
                              ~5#&@&&@@@@@@&&@&#5~                          |
                             Y&@&&&&BPYJJYPB&&&&@&Y:                        |           1 ~> View Passwords              
                           :P@&&&&P!        !P&&&&@P:                       |
                           J@&&&&J            J&&&&@J                       |           2 ~> Add Password
                           G&&&&B              B&&&&G                       |
                           B&&&&G              G&&&&B                       |           3 ~> Remove Password
                           B&&&&G              G&&&&G                       |
                           B&&&&G              G&&&&G                       |           4 ~> Password Generator
                           B&&&&G              G&&&&B                       |
                     JGBBBB&&&&&&BBBBBBBBBBBBBB&&&&&&BBBBGJ                 |           5 ~> Switch To GUI
                     &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&                 |           6 ~> Exit
                     &&&&&&&&&&&&&&&&#PYYP#&&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&G^....^G&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&@J .... J@&&&&&&&&&&&&&&                 |          <Key Binds>
                     &&&&&&&&&&&&&&&#J:..:J#&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&&B:..:B&&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&@J....J@&&&&&&&&&&&&&&&                 |           Ctrl + E ~> Exit
                     &&&&&&&&&&&&&&&&~ .. ~&&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&#777777#&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                 |
                     &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&                 |
                     P&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&P                 |
                                                                            |
"""

#----------------------------------Functions----------------------------------#

def generate_key(master_password, salt):
   backend = default_backend()
   iterations = 100000

   master_password_bytes = master_password.encode()
   salt_bytes = salt.encode()

   kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=16,
      salt=salt_bytes,
      iterations=iterations,
      backend=backend
   )

   key = kdf.derive(master_password_bytes)

   return key.hex()


def encryption(key, plaintext):
   backend = default_backend()
   block_size = algorithms.AES.block_size

   padder = padding.PKCS7(block_size).padder()
   padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

   cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=backend)
   encryptor = cipher.encryptor()

   ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

   return ciphertext

def decryption(key, ciphertext):
   backend = default_backend()
   block_size = algorithms.AES.block_size

   cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=backend)
   decryptor = cipher.decryptor()

   padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

   unpadder = padding.PKCS7(block_size).unpadder()
   plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

   return plaintext

def exit_bind():
   pid = os.getpid()
   os.system(f"taskkill /F /PID {pid}")

def get_data():
   global ready_data
   ready_data = []

   if os.path.isfile("Passwords.txt") != True:
      with open("Passwords.txt", "w") as w:
         w.close()
      
   with open("Passwords.txt", "rb") as read:
      split_data = read.read().split(b"\n")
      read.close()

   for data in split_data:
         if data:
            url_or_program, user, password = data.split(b"04n$b3e0R5K*")
            url_or_program, user, password = base64.b64decode(url_or_program), base64.b64decode(user), base64.b64decode(password)
            url_or_program = decryption(key, url_or_program).decode()
            user = decryption(key, user).decode()
            password = decryption(key, password).decode()
            rating = password_rating_check(password)
            ready_data.append([url_or_program, user, password, rating])
            
   for ind, x in enumerate(ready_data):
      x.insert(0, ind) 


def add_password(url_or_program, user, password):
   encrypted_password = encryption(key, password)
   time.sleep(0.2)
   encrypted_username = encryption(key, user)
   time.sleep(0.2)
   encrypted_url_or_program = encryption(key, url_or_program)
   time.sleep(0.2)

   with open("Passwords.txt", "ab") as p:
      p.write(base64.b64encode(encrypted_url_or_program) + b"04n$b3e0R5K*" + base64.b64encode(encrypted_username) + b"04n$b3e0R5K*" + base64.b64encode(encrypted_password) + b"\n")            
       
def remove_password(index):
   with open("Passwords.txt", "rb") as read:
      lines = read.readlines()
      read.close()
   with open("Passwords.txt", "wb") as write:
      for index_of_line, line in enumerate(lines):
         if index_of_line != int(index):
            write.write(line)

   if style == "gui":
      for item in tree.get_children():
         tree.delete(item)

      get_data()
      for line in ready_data:
         tree.insert("", "end", values=(line)) 
      
      

def password_rating_check(password):
    score = 0
    lowercase_characters_present = uppercase_characters_present = special_characters_present = numbers_present = False

    lowercase_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
 
    for char in lowercase_characters:
        if char in password:
         lowercase_characters_present = True
    for char in uppercase_characters:
        if char in password:
         uppercase_characters_present = True
    for char in special_characters:
        if char in password:
         special_characters_present = True
    for char in numbers:
        if char in password:
         numbers_present = True
 
    if lowercase_characters_present == True:
      score +=1

    if uppercase_characters_present == True:
      score +=1

    if special_characters_present == True:
      score +=1

    if numbers_present == True:
      score +=1

    if len(password) >= 8:
      score +=1

    return score

#----------------------------------Main CLI----------------------------------#

def main_cli():
   style = "cli"

   os.system("cls")
   os.system(f"title EncryptX {version} ~ Logged In As {username_} ")
   os.system("mode con:cols=144 lines=41")
   print(colorama.Fore.LIGHTCYAN_EX + MAIN_MENU + colorama.Fore.RESET)
   opt = input(colorama.Fore.LIGHTCYAN_EX + "  EncryptX/Console/.. " + colorama.Fore.RESET)

   if opt == "":
      print(colorama.Fore.RED + "\n" +"  !Invlid Option!" + colorama.Fore.RESET)
      time.sleep(1)
      main_cli()

   elif opt == "1":
      get_data()
      table_to_print = tabulate(ready_data, headers=["Index", "Name", "Username", "Password", "Rating (1-5)"], tablefmt="double_grid")
    
      Length = len(table_to_print.split("\n")[0])
    
      os.system(f"cls && mode con:cols={Length} lines=9999")
      print(colorama.Fore.LIGHTCYAN_EX + table_to_print + colorama.Fore.RESET)
      input()
      main_cli()

   elif opt == "2":
      os.system("cls & mode con:cols=80 lines=16")
      print(colorama.Fore.RED + "\nYour name, username or password can not be longer than 50 characters.\n" + colorama.Fore.RESET)
      url_or_program = input(colorama.Fore.LIGHTCYAN_EX + "\nWebsite Or Program Name ~> " + colorama.Fore.RESET)
      user = input(colorama.Fore.LIGHTCYAN_EX + "Username ~> " + colorama.Fore.RESET)
      password = input(colorama.Fore.LIGHTCYAN_EX + "Password To Store ~> " + colorama.Fore.RESET)

      if len(password) > 50 or len(user) > 50 or len(url_or_program) > 50:
         main_cli()

      add_password(url_or_program, user, password)
      main_cli()

   elif opt == "3":
      os.system("cls & mode con:cols=80 lines=16")
      index = input(colorama.Fore.LIGHTCYAN_EX + "\nIndex Of Password To Remove ~> " + colorama.Fore.RESET)
      remove_password(index)
      main_cli()

   elif opt == "4":
      os.system("cls & mode con:cols=80 lines=16")
      while True:
         length = int(input(colorama.Fore.LIGHTCYAN_EX + "Enter Password Length ~> " + colorama.Fore.RESET))
         characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()"
         generated_password = ""
         for i in range(length):
            generated_password += random.choice(characters)
         print(colorama.Fore.LIGHTCYAN_EX + f"Password ~> {generated_password}" + colorama.Fore.RESET)
         opt = input(colorama.Fore.LIGHTCYAN_EX + "Use this password (Y/N) ~> " + colorama.Fore.RESET)
         if opt.lower() == "y":
            pyperclip.copy(generated_password)
            print(colorama.Fore.LIGHTCYAN_EX + "Password Copied To Your Clip Board!" + colorama.Fore.RESET)
            time.sleep(2)
            break
         else:
            continue
      main_cli()
      
   elif opt == "5":
      hwnd = ctypes.windll.kernel32.GetConsoleWindow()
      if hwnd:
         ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)
      main_gui()

   elif opt == "6":
      exit()
       
   else:
      print(colorama.Fore.RED + "\n" + "  !Invlid Option!" + colorama.Fore.RESET)
      time.sleep(1)
      main_cli()

   main_cli()

#----------------------------------Main GUI----------------------------------#

def switch_to_cli(root):
   time.sleep(0.5)
   root.destroy()
   time.sleep(1)
   hwnd = ctypes.windll.kernel32.GetConsoleWindow()
   if hwnd:
      ctypes.windll.user32.ShowWindow(hwnd, SW_SHOW)
   main_cli()

def refresh_stats(total_passwords):
   get_data()
   global total_passwords_value
   total_passwords_value = len(ready_data)
   total_passwords.configure(text=("Passwords Saved ~> ", total_passwords_value))

def refresh_treeview(tree):
   for item in tree.get_children():
      tree.delete(item)

   get_data()
   for line in ready_data:
      tree.insert("", "end", values=(line)) 

def add_password_gui(root, tree):
   info_window = customtkinter.CTkToplevel(root)
   info_window.geometry("400x200")
   info_window.title("Add Password")
   name_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Name/URL")
   username_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Username")
   password_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Password", show="*")
   name_text_box.pack(padx=10, pady=10)
   username_text_box.pack(padx=10, pady=10)
   password_text_box.pack(padx=10, pady=10)

   def send_info(tree):
      name = name_text_box.get()
      username = username_text_box.get()
      password = password_text_box.get()

      add_password(name, username, password)

      for item in tree.get_children():
         tree.delete(item)

      get_data()
      for line in ready_data:
         tree.insert("", "end", values=(line))

      info_window.destroy()

   save_button = tkinter.Button(info_window, text="Add Password", command=lambda: send_info(tree))
   save_button.pack(pady=5)

def copy_user_or_pass(itemid, copy):
   get_data()
   data = ready_data[int(itemid)]

   if copy == "user":
      user = data[2]
      pyperclip.copy(user)
   elif copy == "pass":
      password = data[3]
      pyperclip.copy(password)
   else:
      pass

def on_right_click(event):
   item = tree.identify_row(event.y)
   if item != "":
      item_id = tree.item(item, "values")[0]

   if item:
      menu = tkinter.Menu(root, tearoff=0)
      menu.add_command(label="Remove Item", command=lambda:remove_password(item_id))
      menu.add_command(label="Copy Username", command=lambda:copy_user_or_pass(item_id, copy="user"))
      menu.add_command(label="Copy Password", command=lambda:copy_user_or_pass(item_id, copy="pass"))
      menu.tk_popup(event.x_root, event.y_root)

def main_gui():

   global tree, root

   root = customtkinter.CTk()
   root.geometry("1400x800")
   root.title(f"EncryptX {version} ~ Logged In As {username_}")

   tabview = customtkinter.CTkTabview(root, width=1400, height=800)
   tabview.pack(pady=5,padx=5)
   tabview.add("Passwords")
   tabview.add("Password Generator") 
   tabview.add("Stats")
   tabview.add("Settings") 

   # Password Page   

   try: 
      get_data()
   except:
      pass  

   tree = tkinter.ttk.Treeview(master=tabview.tab("Passwords"), columns=("ID", "Name/URL", "Username", "Password", "Password_Rating"), show="headings")

   scrollbar = tkinter.ttk.Scrollbar(tree, orient=tkinter.VERTICAL, command=tree.yview)
   tree.configure(yscroll=scrollbar.set) 

   tree.heading("ID", text="ID")
   tree.heading("Name/URL", text="Name/URL")
   tree.heading("Username", text="Username")
   tree.heading("Password", text="Password")
   tree.heading("Password_Rating", text="Password Rating (1-5)")  

   for line in ready_data:
      tree.insert("", "end", values=(line)) 

   tree.column("ID", anchor="center")
   tree.column("Name/URL", anchor="center")
   tree.column("Username", anchor="center")
   tree.column("Password", anchor="center")
   tree.column("Password_Rating", anchor="center") 

   tree.pack(fill="both", expand=True) 

   tree.bind("<Button-3>", on_right_click)

   add_password_button = customtkinter.CTkButton(master=tabview.tab("Passwords"), text="Add Password", font=("Cascadia Code", 12), command=lambda: add_password_gui(root, tree))
   add_password_button.pack(pady=(10,5), padx=5)

   refresh_button = customtkinter.CTkButton(master=tabview.tab("Passwords"), text="Refresh Passwords List", font=("Cascadia Code", 12), command=lambda: refresh_treeview(tree))
   refresh_button.pack() 

   # Stats Page

   title_stats = customtkinter.CTkLabel(master=tabview.tab("Stats"), text="EncryptX Stats", font=("Cascadia Code", 22))
   title_stats.pack(pady=15, padx=10)

   total_passwords_value = len(ready_data)
   total_passwords_label = customtkinter.CTkLabel(master=tabview.tab("Stats"), text=("Passwords Saved ~> ", total_passwords_value), font=("Cascadia Code", 12))
   total_passwords_label.pack(pady=(10,5), padx=5)

   refresh_button_stats = customtkinter.CTkButton(master=tabview.tab("Stats"), text="Refresh Stats", font=("Cascadia Code", 12), command=lambda: refresh_stats(total_passwords_label))
   refresh_button_stats.pack() 

   # Settings Page

   switch_mode_button = customtkinter.CTkButton(master=tabview.tab("Settings"), text="Switch To CLI", font=("Cascadia Code", 12), command=lambda: switch_to_cli(root))
   switch_mode_button.pack(pady=(10,5), padx=5)



   root.mainloop()  

#----------------------------------Login Functions----------------------------------#

def login_check(master_pass, username):
   global username_, key
   username_ = username
   
   if len(master_pass) < 8 or len(username) < 8:
      login.destroy()
      exit

   salt = "UKXcH*=/:PSOF(*8y3Sau8ZVq/b(p1OVLA2gY)R.gbf@gx--48"
   key = generate_key(master_pass, salt)
   encrypted_password = encryption(key, master_pass)

   hash_password = hashlib.md5(encrypted_password).hexdigest()
   with open("UserData.txt", "r") as r:
      userdata = r.read().split("\n")
      r.close()
   
   for user in userdata:
      if user.split("04n$b3e0R5K*")[0] == username and user.split("04n$b3e0R5K*")[1] == hash_password:
         login.destroy()
         main_gui()
      else:
         login.destroy()
         exit()
             
def login_create(master_pass, second_entry, username):
   global username_, key
   username_ = username

   if len(username) < 8:
      login.destroy()
      exit()
   if len(master_pass) < 8 or master_pass != second_entry:
      login.destroy()
      exit()
   if len(master_pass) > 64 or len(username) > 64:
      login.destroy()
      exit()


   salt = "UKXcH*=/:PSOF(*8y3Sau8ZVq/b(p1OVLA2gY)R.gbf@gx--48"
   key = generate_key(master_pass, salt)
   encrypted_password = encryption(key, master_pass)
   hash_password = hashlib.md5(encrypted_password).hexdigest()

   with open("UserData.txt", "w") as w:
      w.write(f"{username}04n$b3e0R5K*{hash_password}")
      w.close()

   login.destroy()
   main_gui()

def login_creation_gui():
   global login

   hwnd = ctypes.windll.kernel32.GetConsoleWindow()
   if hwnd:
      ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

   login = customtkinter.CTk()
   login.geometry("400x300")
   login.resizable(width=0, height=0)
   login.title(f"EncryptX {version} ~ Account Creation")

   title = customtkinter.CTkLabel(master=login, text="EncryptX", font=("Cascadia Code", 32))
   title.pack(pady=20, padx=5)

   username_box = customtkinter.CTkEntry(master=login, placeholder_text="Username", font=("Cascadia Code", 12))
   password_box = customtkinter.CTkEntry(master=login, placeholder_text="Password", font=("Cascadia Code", 12), show="*")
   second_password_box = customtkinter.CTkEntry(master=login, placeholder_text="Re-Enter Password", font=("Cascadia Code", 12), show="*")
   username_box.pack(pady=20, padx=5)
   password_box.pack(pady=5, padx=5)
   second_password_box.pack(pady=5, padx=5)

   button = customtkinter.CTkButton(master=login, text="Create Account", command=lambda:login_create(password_box.get(), second_password_box.get(), username_box.get()))
   button.pack(pady=20, padx=5)

   login.mainloop()

def login_gui():
   global login

   hwnd = ctypes.windll.kernel32.GetConsoleWindow()
   if hwnd:
      ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

   login = customtkinter.CTk()
   login.geometry("400x300")
   login.resizable(width=0, height=0)
   login.title(f"EncryptX {version} ~ Account Login")

   title = customtkinter.CTkLabel(master=login, text="EncryptX", font=("Cascadia Code", 22))
   title.pack(pady=20, padx=5)

   username_box = customtkinter.CTkEntry(master=login, placeholder_text="Username", font=("Cascadia Code", 12))
   password_box = customtkinter.CTkEntry(master=login, placeholder_text="Password", font=("Cascadia Code", 12), show="*")
   username_box.pack(pady=20, padx=5)
   password_box.pack(pady=5, padx=5)

   button = customtkinter.CTkButton(master=login, text="Login", command=lambda:login_check(password_box.get(), username_box.get()))
   button.pack(pady=20, padx=5)

   login.mainloop()

#----------------------------------Boot----------------------------------#

def boot():
   global style
   style = "gui"

   keyboard.add_hotkey('Ctrl+E', exit_bind)

   if os.path.exists("UserData.txt"):
      new_user = False
   else:
      new_user = True

   if new_user == True:
      login_creation_gui()
   elif new_user == False:
      login_gui()

if __name__=="__main__":
   boot()
