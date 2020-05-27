# -*- coding: utf-8 -*-
from DBService import *

class User (object):
    @classmethod
    def get_balance(cls,message):
        db = DBService()
        balance = db.select('user','points','tg_id = {}'.format(message.from_user.id))
        db.close()
        for i in balance:
            return i['points']

    @classmethod
    def inc_balance(cls,message,points):
        db= DBService()
        db.select(
            'user',
            query='update user set points = points + {} where tg_id = {}'.format(points, message.from_user.id)
        )
        db.close()

    @classmethod
    def get_tasks_status(cls,message):
        db = DBService()
        status = db.select('user','tasks_status','tg_id = {}'.format(message.from_user.id))
        db.close()
        for i in status:
            return i['tasks_status']

    @classmethod
    def finish_task(cls,message,task):
        db = DBService()
        tasks_status = cls.get_tasks_status(message)
        tasks_status = tasks_status[:task - 1]+'1'+tasks_status[task:]
        data = {'tasks_status':tasks_status}
        db.update('user',data,'tg_id = {}'.format(message.from_user.id))
        db.close()

    @classmethod
    def is_task_finished(cls, message, task):
        """
        :param message: - отправитель
        :param task: - номер задания
        :return True: - выполнено
        :return False: - не выполнено
        """

        db = DBService()
 
        if task <= 6:
            tasks = db.select(
                'user', 
                query="select tasks_status from user where tg_id={}".format(message.from_user.id)
            )

            db.close()

            for t in tasks:
                user_task = t['tasks_status']

            return (user_task[task - 1] == '1')

        else:
            tasks = db.select(
                'user', 
                query="select tasks_status, t_6  from user where tg_id={}".format(message.from_user.id)
            )
            
            db.close()

            for t in tasks:
                user_task = t

            return (user_task['tasks_status'][5] == '1' and str(user_task['t_6']) == '2')

    @classmethod
    def add_user(cls, message):
        """
        Добавляет пользователя, отправившего сообщение в бд как участника
        :param message:     - данные о сообщении
        """
        db = DBService()

        data = {
            'tg_id'     : message.from_user.id, 
            'marathon_chat_id'   : 0, 
            'bot_chat_id' : message.chat.id, 
            'f_name'    : message.from_user.first_name, 
            'role'      : 'user', 
        }

        db.insert('user', data)

        db.close()

    @classmethod
    def add_admin(cls, message):
        """
        Добавляет пользователя, отправившего сообщение в бд как админа
        :param message:     - данные о сообщении
        """
        db = DBService()

        data = {
            'tg_id'     : message.from_user.id, 
            'marathon_chat_id'   : message.chat.id, 
            'bot_chat_id' : 0, 
            'f_name'    : message.from_user.first_name, 
            'role'      : 'admin', 
        }

        db.insert('user', data)

        db.close()

    @classmethod
    def is_admin(cls, message):
        """
        Является ли отправитель сообщения админом
        :param message: - данные о сообщении
        :return True: - админ
        :return False: - не админ
        """
        db = DBService()

        role_res = db.select(
            'user',
            'role', 
            'tg_id = {}'.format(message.from_user.id)
        )

        db.close()

        for i in role_res:
            role = i

        if list(role.values())[0] == 'user':
            return False
        else:
            return True

    @classmethod
    def get_chat_link(cls):
        """
        :return link:   - str
        :return None:   - ссылки нету.
        """
        db = DBService()

        id_ = db.select(
            'chat',
            query='select link from chat order by id desc limit 0, 1'
        )

        if id_.rowcount == 0:
            return None

        for i in id_:
            link = i
        
        db.close()

        return link['link']


    @classmethod 
    def update_marathon_info(cls, message, role='user'):
        """
        :param message:     - данные сообщения
        :param role:        - роль пользователя
        """
        db = DBService()

        data = {
            'marathon_chat_id' : message.chat.id, 
            'role'    : role,
        }

        db.update(
            'user', 
            data, 
            'tg_id = %s' % message.from_user.id
        )

        db.close()

    @classmethod
    def already_exists(cls, message):
        """
        Проверяем, существует или нет
        :return True:   - существует
        :return False:  - не существует
        """
        db = DBService()

        exists = db.select(
            'user',
            query ='SELECT EXISTS(SELECT * FROM user WHERE tg_id = {})'.format(message.from_user.id)
        )

        db.close()

        for i in exists:
            is_exist = i

        if list(is_exist.values())[0] == 0:
            return False
        else:
            return True


class Chat (object):
    @classmethod
    def next_task(cls, message, task):
        db = DBService()
        
        db.update(
            'chat',
            {'available_tasks':task},
            'chat_id = {}'.format(message.chat.id)
        )

        db.close() 

    @classmethod
    def get_task_text(cls,id):
        db = DBService()
        text = db.select('chat', query='select task_{}_text from chat order by id desc limit 0, 1'.format(id))
        db.close()

        for i in text:
            return i['task_{}_text'.format(id)]

    @classmethod
    def get_available_task(cls, message=None):
        """
        Получаем номер задание до которого(включительно) можно
        отвечать на задания
        """
        if message is not None:
            db = DBService()

            tasks = db.select(
                'chat',
                'available_tasks',
                'chat_id = {}'.format(message.chat.id)
            )
            
            db.close()

            for i in tasks:
                return i['available_tasks']

        else: 
            db = DBService()  
            
            tasks = db.select (
                'chat', 
                query='select available_tasks from chat order by id desc limit 0, 1'
            )

            db.close()

            for i in tasks:
                return i['available_tasks']

    @classmethod
    def add(cls, message, link=None):
        """
        Добавляет чат в бд
        :param message:     - данные о сообщении
        :param link:        - ссылка на беседу
        :return Chat:       - объект класса Chat
        """
        db = DBService()

        data = {
            'chat_id' : message.chat.id, 
            'link'    : link, 
            'admin_id': message.from_user.id  
        }

        db.insert('chat', data)

        db.close()

    @classmethod
    def already_exists(cls, message):
        """
        Проверяем, существует или нет
        :return True:   - существует
        :return False:  - не существует
        """
        db = DBService()
        exists = db.select(
            'chat',
            query ='SELECT EXISTS(SELECT * FROM chat WHERE chat_id = {})'.format(message.chat.id)
        )
        db.close()
        
        for i in exists:
            is_exist = i

        if list(is_exist.values())[0] == 0:
            return False
        else:
            return True

    @classmethod
    def set_task(cls, message, id, text):
        db = DBService()
        data = {'task_{}_text'.format(id):text}
        db.update('chat',data,'chat_id ={}'.format(message.chat.id))
        db.close()
        

    