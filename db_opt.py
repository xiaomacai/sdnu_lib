# coding: utf-8
"""
数据库建表及操作处理
数据库表：
表1： 座位表（desk）包括编号（id)、座位名(name)，主键为编号
表2： 学生表(student) 包括编号(id)、姓名(name)、学号(card_id)，主键为编号
表3： 占座表(occupy) 包含编号(id)、座位编号(desk_id)、学生编号(student_id)、占座开始时间(start_time)、占座结束时间(end_time)、
    真实开始时间（real_start_time)、真实结束时间(real_end_time)；其中座位编号和学生编号为外键，编号为主键.
"""
import sqlite3
from datetime import datetime


class DateOpt(object):
    def __init__(self):
        self.conn = sqlite3.connect('occupy_desk.sqlite')
        self.cursor = self.conn.cursor()

    @staticmethod
    def create_tables():
        """
        静态函数，用于创建数据库表(座位表、学生表、占座表)
        :return:
        """
        conn = sqlite3.connect('occupy_desk.sqlite')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS desk(id INTEGER PRIMARY KEY, name TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS student(id INTEGER PRIMARY KEY, name TEXT, card_id INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS occupy(id INTEGER PRIMARY KEY, desk_id INTEGER, student_id INTEGER, start_time
                        DATETIME, end_time DATETIME, real_start_time DATETIME, real_end_time DATETIME, current_d DATE,
                        FOREIGN KEY(desk_id) REFERENCES desk(id), FOREIGN KEY (student_id) REFERENCES student(id))''')

        conn.commit()
        conn.close()

    def select_id_from_desk(self, name):
        """
        根据课桌名选出课桌id， 如果课桌不存在数据库当中则先进行插入操作，后选出id
        :param name: 课桌名
        :return: 课桌id
        """
        self.cursor.execute('SELECT id FROM desk WHERE name={}}'.format(name))
        res = self.cursor.fetchone()
        if not res:
            self.insert_into_desk(name)
            self.conn.commit()
            self.select_id_from_desk(name)
        else:
            return res

    def insert_into_desk(self, name):
        """
        向课桌表中插入数据
        :param name: 课桌名
        :return:
        """
        self.cursor.execute('INSERT INTO desk (name) VALUES ({})'.format(name))
        return True

    def select_id_from_student(self, name, card_id):
        """
        通过学生学号从表中选出学生id，如果该学生不在数据表中则将其插入表中后再选出id
        :param name: 学生姓名
        :param card_id: 学生学号
        :return: 学生编号
        """
        self.cursor.execute('SELECT id FROM student WHERE card_id={}'.format(card_id))
        res = self.cursor.fetchone()
        if not res:
            self.insert_into_student(name, card_id)
            self.conn.commit()
            self.select_id_from_student(name, card_id)
        else:
            return res

    def insert_into_student(self, name, card_id):
        """
        向学生表中插入数据
        :param name: 学生名
        :param card_id: 学生学号
        :return:
        """
        self.cursor.execute('INSERT INTO student (name, card_id) VALUES ({}, {}})'.format(name, card_id))
        self.conn.commit()
        return True

    def insert_into_occupy(self, desk_id, student_id, start_time, end_time):
        """
        向占座表中插入数据, 表中‘真实开始时间’及‘真实结束时间’均为当前时间
        :param desk_id: 课桌编号
        :param student_id: 学生编号
        :param start_time: 占座开始时间
        :param end_time: 占座结束时间
        :return:
        """
        self.cursor.execute('''INSERT INTO occupy (desk_id, student_id, start_time, end_time, read_start_time, \
                real_end_time, current_d) VALUES ({}, {}, {}, {}, {}, {}, {}})'''.format(
            desk_id, student_id, start_time, end_time, datetime.now().strftime('%H:%M'), datetime.now().strftime("%H:%M"),\
            datetime.now().strftime("%d")
        ))
        self.conn.commit()

    def update_occupy(self, desk_id, student_id, start_time, end_time):
        """
        更新占座表操作,当座位为当天切学生为换时更新学生真实结束时间
        :param desk_id: 课桌id
        :param student_id: 学生id
        :param start_time: 占座开始时间
        :param end_time:占座结束时间
        :return:
        """
        self.cursor.execute('''
              select real_end_time from occupy where desk_id = {} and student_id = {} and start_time={} and current_d = {}
              '''.format(desk_id, student_id, start_time, datetime.now().strftime('%d')))
        res = self.cursor.fetchone()
        if res and res < datetime.now().strftime('%H:%M'):
            self.cursor.execute('''
              update occupy set real_end_time = {} where desk_id = {} and student_id = {} and start_time={} and current_d = {}
              '''.format(datetime.now().strftime('%H:%M'), desk_id, student_id, start_time, datetime.now().strftime('%d')))
            self.conn.commit()
        else:
            self.insert_into_occupy(desk_id, student_id, start_time, end_time)