import PyPDF2
import tkinter
import sqlite3
import os
import csv
import math
from datetime import datetime
from tkinter import filedialog
root = tkinter.Tk()
root.withdraw()


class Project:

    def pdf(self):
        pdf_folder = r"C:\Users\Shreyas V Shetty\PycharmProjects\Database\Pdf"
        for x, y, z in os.walk(pdf_folder):
            print(x)
            print(y)
            print(z)

    def datetimestamp(self):
        current_time = datetime.now()
        modified_time = current_time.replace(microsecond=0)
        my_time_format = "%d %h %Y %H:%M:%S"
        converted_format_time = datetime.strftime(modified_time, my_time_format)
        return converted_format_time

    def pdf_creator(self):
        file_name = filedialog.askopenfilename()
        pdf_in_file = open(file_name, 'rb')
        inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
        pages_no = inputpdf.numPages
        pdfname = "Default.pdf"
        output = PyPDF2.PdfFileWriter()
        try:
            for i in range(pages_no):
                inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                output.addPage(inputpdf.getPage(i))
                output.encrypt('password')
        except Exception as ex:
            print(ex)
        with open(r"C:\Users\Shreyas V Shetty\PycharmProjects\Database"
                  r"\Pdf_Encrypted\Default.pdf", "wb") as outputstream:
            output.write(outputstream)
        with open(pdfname, "wb") as outputstream:
            output.write(outputstream)
            self.datetimestamp()

    def filesizedata(self):
        pdfname = "Default"
        file_size = os.path.getsize(pdfname + ".pdf") / 1024
        file_size = math.trunc(file_size)
        return pdfname, file_size, self.datetimestamp()

    def database(self):
        connection = sqlite3.connect("PDF_Protection.db")
        cur = connection.cursor()
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Detail' ''')
        if cur.fetchone()[0] == 1:
            data = self.filesizedata()
            query = """INSERT INTO Detail ("filename", "file size", "Time of encryption") VALUES (?,?,?)"""
            execution = connection.execute(query, data)
            db_data = execution.fetchall()
            print(db_data)
        else:
            query = """CREATE TABLE Detail ("filename" text, "file size" integer, "Time of encryption" text)"""
            execution = connection.execute(query)
            db_data = execution.fetchall()
            print(db_data)
        connection.commit()
        connection.close()

    def db_display(self):
        connection = sqlite3.connect("PDF_Protection.db")
        query = """SELECT * FROM Detail"""
        execution = connection.execute(query)
        db_data = execution.fetchall()
        print(db_data)
        connection.commit()
        connection.close()

    def file_csv(self):
        pdfname = "Default"
        file_size = os.path.getsize(pdfname + ".pdf") / 1024
        file_size = math.trunc(file_size)
        if os.path.isfile("Pdf_data.csv") is False:
            with open("Pdf_data.csv", "a", newline="") as file_obj:
                obj = csv.writer(file_obj)
                obj.writerow(["FileName", "File Size", "Time of encryption", "Email id", "Password"])
                email = input("Enter your email ID: ")
                password = input("Enter your email password: ")
                obj.writerow(["filename", file_size, self.datetimestamp(), email, password])
        else:
            with open("Pdf_data.csv", "a", newline="") as file_obj:
                obj = csv.writer(file_obj)
                email = input("Enter your email ID: ")
                password = input("Enter your email password: ")
                obj.writerow([pdfname, file_size, self.datetimestamp(), email, password])
        print("CSV file updated successfully")


my_obj = Project()
my_obj.pdf()
my_obj.pdf_creator()
my_obj.database()
my_obj.db_display()
my_obj.file_csv()
