from datetime import datetime, date, time
from PyQt5.QtCore import qInfo
import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QCheckBox, QInputDialog, QLineEdit, QSpinBox, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QMainWindow)


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.datetime()
        self._connect_to_db()
        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()


    def datetime(self):
        self.row_max = 4
        self.day_name = ['Monday', 'Tuesday', 'Wednesday']
        start = date(2021, 9, 1)
        d = datetime.now()
        self.week = d.isocalendar()[1] - start.isocalendar()[1] + 1
        if self.week % 2 == 1:
            self.top_week = 'ODD'
        else:
            self.top_week = 'EVEN'


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="telegramschedule",
                                     user="postgres",
                                     password="1",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()


    def _create_schedule_tab(self):

        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Schedule")


        self.dof = int(input("1 - Понедельник, 2 - Вторник, 3 - Среда)\n"))
        if self.dof == 1:
            self.day_of_week = 'Понедельник'
        if self.dof == 2:
            self.day_of_week = 'Вторник'
        if self.dof == 3:
            self.day_of_week = 'Среда'
 
        self.day_gbox = QGroupBox(f"{self.day_name[self.dof - 1]}")
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)
        self.shbox1.addWidget(self.day_gbox)

        self._create_monday_table()

        self.update_schedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_day_table)

        self.saveButton = QPushButton("Save all")
        self.shbox2.addWidget(self.saveButton)
        self.saveButton.clicked.connect(lambda: self._change_day_from_table(self.row_max))
        self.saveButton.clicked.connect(self._update_day_table)

        self.schedule_tab.setLayout(self.svbox)


    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.monday_table.setColumnCount(5)
        self.monday_table.setHorizontalHeaderLabels(["Start time", "Subject", "Week", "Room", "Delete"])

        self._update_day_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.day_gbox.setLayout(self.mvbox)


    def _update_day_table(self):
        self.records = []
        self._connect_to_db()
        self.cursor.execute(f"Select * from timetable where timetable.day='{self.day_of_week}' and week in ('{self.top_week}', 'ALWAYS')")
        self.records = list(self.cursor.fetchall())
        self.cursor.execute(f"select * from subject")
        recors_subj = list(self.cursor.fetchall())
        self.names = {rname:rpublicname for (rname,rpublicname) in recors_subj}
        self.publicnames = {rpublicname:rname for (rname,rpublicname) in recors_subj}
        print(self.names)
        self.monday_table.setRowCount(self.row_max)
        for i, r in enumerate(self.records):
            r = list(r)
            drop_button1 = QPushButton("Delete")
            drop_button2 = QPushButton("Delete")
            drop_button3 = QPushButton("Delete")
            drop_button4 = QPushButton("Delete")
            drop_button5 = QPushButton("Delete")
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[3]))) #Time
            self.monday_table.setItem(i, 1, QTableWidgetItem(self.names[r[2]] if (self.names[r[2]] != None ) else r[2])) #Subject
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[4]))) #Week
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[5]))) #Room
            self.monday_table.setCellWidget(0, 4, drop_button1)
            self.monday_table.setCellWidget(1, 4, drop_button2)
            self.monday_table.setCellWidget(2, 4, drop_button3)
            self.monday_table.setCellWidget(3, 4, drop_button4)
            self.monday_table.setCellWidget(4, 4, drop_button5)
            drop_button1.clicked.connect(lambda: self._delete_row(0))
            drop_button2.clicked.connect(lambda: self._delete_row(1))
            drop_button3.clicked.connect(lambda: self._delete_row(2))
            drop_button4.clicked.connect(lambda: self._delete_row(3))
            drop_button5.clicked.connect(lambda: self._delete_row(4))
        self.monday_table.resizeRowsToContents()

        for j in range(len(self.records), self.row_max):
            self.monday_table.setItem(j, 0, QTableWidgetItem(None))  #Time
            self.monday_table.setItem(j, 1, QTableWidgetItem(None))  #Subject
            self.monday_table.setItem(j, 2, QTableWidgetItem(None))  #Week
            self.monday_table.setItem(j, 3, QTableWidgetItem(None))  #Room


    def _delete_row(self, rowNum):
        try:
            self.cursor.execute(f"DELETE FROM timetable WHERE id = {self.records[rowNum][0]};")
            self.conn.commit()

        except:
            QMessageBox.about(self, "Error", f"Can't delete row = {rowNum + 1}")
        self._update_day_table()


    def _change_day_from_table(self, rowNum):      
        for j in range(len(self.records)):
            row = list()
            for i in range(self.monday_table.columnCount()):
                try:
                    row.append(self.monday_table.item(j, i).text())
                except:
                    row.append(None)
         
            self.cursor.execute(f"UPDATE timetable SET start_time = '{row[0]}' WHERE id = {self.records[j][0]}")
            self.cursor.execute(f"UPDATE subject SET subject_name = '{row[1]}' WHERE id = {self.records[j][2]}")
            self.cursor.execute(f"UPDATE timetable SET room_numb = '{row[3]}' WHERE id = {self.records[j][0]}")

            self.conn.commit() 

        for j in range(len(self.records), self.row_max):
            row = list()
            for i in range(self.monday_table.columnCount() - 1):
                try:
                    row.append(self.monday_table.item(j, i).text())
                except:
                    row.append(None)


            if any([(e == '' or e == ' ') for e in row]):
                continue
           

            if not(row[1] in self.publicnames):
                self.cursor.execute(f"insert into subject (subject_name) values ('{row[1]}')")
                self.conn.commit()
                self.cursor.execute(f"select subject.id from subject where subject.subject_name = '{row[1]}'")
                id=list(self.cursor.fetchall())[0][0]
            else: 
                id=self.publicnames[row[1]]
            self.cursor.execute(f"insert into timetable (fk_subject_id,start_time,day,week,room_numb) values ({id},'{row[0]}','{self.day_of_week}','{row[2]}','{row[3]}')")
            self.conn.commit()
            

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())