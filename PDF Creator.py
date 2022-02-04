import PyPDF2
import os
import tkinter
import sqlite3
import shutil
import csv
import math
from datetime import datetime
from datetime import timedelta
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw()

global inputpdf


class assign:
    def time(self):
        current_time = datetime.now()
        print(current_time)
        print(type(current_time))
        modified_time = current_time.replace(microsecond=0)
        print(modified_time)
        added_current_time = modified_time + timedelta(minutes=330)
        print(added_current_time)
        my_time_format = "%Y_%m_%d_%H_%M_%S"
        converted_format_time = datetime.strftime(added_current_time, my_time_format)
        print(type(converted_format_time))
        print(converted_format_time)
        print()

    def pdf(self):
        pdf_folder = r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\Pdf " \
                     r"Encrypted files"
        for x, y, z in os.walk(pdf_folder):
            print(x)
            print(y)
            print(z)

    def user_pass(self):
        file_name = filedialog.askopenfilename()
        pdf_in_file = open(file_name, 'rb')
        inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
        pages_no = inputpdf.numPages
        output = PyPDF2.PdfFileWriter()
        try:
            for i in range(pages_no):
                inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                output.addPage(inputpdf.getPage(i))
                output.encrypt('password')
        except Exception as ex:
            print(ex)
        with open("two4.pdf", "wb") as outputstream:
            output.write(outputstream)
class csvdata:
    def csv(inputpdf, file_size):
        current_time = datetime.now()
        modified_time = current_time.replace(microsecond=0)
        added_current_time = modified_time + timedelta(minutes=0)
        print(added_current_time)
        my_time_format = "%Y_%m_%d_%H_%M_%S"
        converted_format_time = datetime.strftime(added_current_time, my_time_format)
        old_name = r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\Pdf " \
                   r"Encrypted files"
        new_name = r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\Pdf" \
                   r" Encrypted files" + converted_format_time + ".pdf"
        os.rename(old_name, new_name)
        source = r'C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\Pdf ' \
                 r'Encrypted files'
        dest = r'C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\Pdf ' \
               r'Encrypted files'
        for fname in os.listdir(source):
            if fname.lower().endswith('.pdf'):
                shutil.move(os.path.join(source, fname), dest)
        f = open(r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf_Encryption\file.txt", 'r+')
        w = csv.writer(f)
        for path, dirs, files in os.walk(r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject\Pdf"
                                         r"_Encryption"):
            for filename in files:
                w.writerow(filename)
                file_size = os.path.getsize(r"C:\Users\Shreyas V Shetty\PycharmProjects\pythonProject\pythonProject"
                                            r"\Pdf_Encryption")
                with open("file1.csv", "w") as file_obj:
                    csv_file_obj = csv.writer(file_obj)
                    csv_file_obj.writerow(["filename", file_size])
                    csv_file_obj.writerows(["filename", file_size])


class datadb:

    def database(self):
        connection = sqlite3.connect("PDF_Protection.db")
        query = """CREATE TABLE Detail ("filename" text, "file_size in KB" integer)"""
        execution = connection.execute(query)
        db_data = execution.fetchall()
        print(db_data)
        connection.commit()
        connection.close()

    def my_db_exe(db="PDF_Protection.db"):
        connection = sqlite3.connect(db)
        query = """SELECT * FROM Detail"""
        execution = connection.execute(query)
        db_data = execution.fetchall()
        print(db_data)
        connection.commit()
        connection.close()

    def database_update(inputpdf, my_time_format,password = 'password'):
        file_size = os.path.getsize(inputpdf + ".pdf") / 1024
        file_size = math.trunc(file_size)
        if os.path.isfile("PDF_Protection.db") is True:
            data = (inputpdf, file_size, my_time_format,password)
            db = "PDF_Protection.db"
            #query = """insert into Details values ("filename", "file_size in KB") VALUES ("two4.pdf",file_size) """
            datadb.my_db_exe(query, db,data)
            csvdata.csv(inputpdf, file_size)
        else:
            datadb.database()
            data = (inputpdf, file_size, my_time_format, password)
            db = "PDF_Protection.db"
            query = """insert into detail values (?,?,?,?);"""
            datadb.my_db_exe(query, db, data)
            csvdata.csv(inputpdf, file_size)


my_obj = assign()
my_obj.pdf()
my_obj.user_pass()
my_obj1 = datadb()
my_obj1.database()
my_obj1.my_db_exe()
my_obj1.database_update()

