import os
import CONSTANT
import datetime



class usmlogging(object):
    def __init__(self,inputtext):
        self.log_file_dir = CONSTANT.LOG_FILE_DIR
        self.log_file_name = CONSTANT.LOG_FILE_NAME
        self.log_last_number = CONSTANT.LOG_LAST_NUMBER
        self.log_file_maxsize = CONSTANT.LOG_MAX_SIZE
        self.default_log_file_path = '{}/{}'.format(self.log_file_dir,self.log_file_name)
        self.write_log(inputtext)


    def get_next_file_name(self):
        new_file_path = ''
        work_file = self.default_log_file_path

        for i in range(1, int(self.log_last_number) + 1):
            file_path = work_file + '.{}'.format(i)
            if os.path.exists(file_path) == False:
                new_file_path = file_path
                break
            elif os.path.exists(file_path) == True and os.path.getsize(file_path) < self.log_file_maxsize:
                new_file_path = file_path
                break
        if new_file_path:
            return new_file_path
        else:
            self.rename_files()
            return work_file

    def write_text_to_log(self, text:str, filepath:str):
        now = datetime.datetime.now()
        if os.path.exists(filepath) == False:
            f = open(r'{}'.format(filepath), 'a')
            f.close()
        try:
            my_file = open(filepath, "a")
            my_file.write('{}-{}-{} {}:{} '.format(now.day, now.month, now.year, now.hour, now.minute) + text + '\n')
            my_file.close()
        except Exception as err:
            print(err)
    def rename_files(self):
        work_file = self.default_log_file_path
        old_file = self.default_log_file_path + '.' + self.log_last_number
        if os.path.exists(old_file) == True:
            os.remove(old_file)
            # print('Удалил:', old_file)
        i = int(self.log_last_number) - 1
        while i != 0:
            file_name = work_file + '.{}'.format(i)
            new_file_name = work_file + '.{}'.format(i + 1)
            os.rename(file_name,new_file_name)
            # print('Переименовал:', file_name,'в', new_file_name)
            i = i - 1
        if os.path.exists(work_file) == True:
            new_file_name = work_file + '.{}'.format(1)
            os.rename(work_file, new_file_name)
            # print('Переименовал:', work_file, 'в', new_file_name)
            f = open(r'{}'.format(work_file), 'a')
            f.close()
            # print('Создал файл:', work_file)



    def write_log(self,inputtext:str):

        work_file = self.default_log_file_path
        try:
            log_file_size = os.path.getsize(work_file)
        except Exception:
            log_file_size = 0

        if log_file_size > self.log_file_maxsize:
            log_file = self.get_next_file_name()
            self.write_text_to_log(inputtext, log_file)
        else:
            self.write_text_to_log(inputtext, work_file)










