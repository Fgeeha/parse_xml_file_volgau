# main.py
from creathtml import create_html
import os
from zipfile import ZipFile
import gzip
import shutil
from datetime import datetime


def check_dir(dir_name: str) -> None:
    if not os.path.exists(f'{dir_name}'):
        os.mkdir(f'{dir_name}')


def add_file_to_archive(archive_name, file_path):
    # Проверяем, существует ли архив
    archive_exists = os.path.exists(archive_name)
    
    # Открываем архив для добавления файлов
    with ZipFile(archive_name, 'a' if archive_exists else 'w') as archive:
        # Добавляем файл в архив
        archive.write(file_path, os.path.basename(file_path))


def main():
    debug_mode = False
    """
    False - transferring files to a folder dump
    True - zip archives remain in the root folder
    """

    if not debug_mode:
        # Настройки Даты и Время
        data_time_now = datetime.now()
        data_time_format = "%d%m%Y %H-%M-%S"
        time1 = data_time_now.strftime(data_time_format)
        dt_now = str(time1)

    # Название файлов для высшего приоритета
    file_name_enr_recommended_bak = 'enr_recommended_enrollment_list_1780165749254516989.zip'
    file_name_enr_recommended_mag = 'enr_recommended_enrollment_list_1780165823923613949.zip'
    # Название директории где будет высший приоритет
    dir_name_file_priority = 'file_priority'
    # словарь ( краткое название ПК : названия файла до расширения)
    
    name_pk = {'bak': 'enr_rating_1780165749254516989',
               'mag': 'enr_rating_1780165823923613949',
               'spo': 'enr_rating_1790248022834278653',
               'asp': 'enr_rating_1780891192879345917'
               }

    if not debug_mode:
        check_dir('dump')
        os.mkdir(f'dump/{dt_now}')
        
    
    for _ in name_pk:
        if _ == 'mag' or _ == 'bak':
            file_name_enr_recommended = ''
            if os.path.exists(dir_name_file_priority):
                shutil.rmtree(dir_name_file_priority)
            os.mkdir(dir_name_file_priority)
            if _ == 'mag':
                file_name_enr_recommended = file_name_enr_recommended_mag
            elif _ == 'bak':
                file_name_enr_recommended = file_name_enr_recommended_bak
            if os.path.exists(file_name_enr_recommended):
                with ZipFile(file_name_enr_recommended, "r") as myzip:
                    myzip.extractall(path=dir_name_file_priority)
                    myzip.close()
                if not debug_mode:
                    shutil.move(file_name_enr_recommended, f'dump/{dt_now}/{file_name_enr_recommended}')

        if os.path.exists(f'{name_pk[_]}.xml.zip'):
            if os.path.exists(f'{name_pk[_]}.xml'):
                try:
                    os.remove(f'{name_pk[_]}.xml')
                except OSError as e:
                    print(f"Error: {e.filename} - {e.strerror}.")

            with gzip.open(f"{name_pk[_]}.xml.zip", 'rb') as f_in:
                with open(f"{name_pk[_]}.xml", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            create_html(pk_name=_, file_xml_name=f'{name_pk[_]}', dir_name_for_priority=dir_name_file_priority)
            if _ == 'mag' or _ == 'bak' or _ == 'spo':
                add_file_to_archive('lists_2024.zip', f'lists_{_}_2024.html')
                check_dir(f'dump/{dt_now}/html')
                shutil.move(f'lists_{_}_2024.html',f'dump/{dt_now}/html/lists_{_}_2024.html')
            os.remove(f'{name_pk[_]}.xml')
            

            if os.path.exists(dir_name_file_priority):
                shutil.rmtree(dir_name_file_priority)

            if not debug_mode:
                shutil.move(f'{name_pk[_]}.xml.zip', f'dump/{dt_now}/{name_pk[_]}.xml.zip')

    if not debug_mode:
        if os.path.exists(dir_name_file_priority):
            shutil.rmtree(dir_name_file_priority)


if __name__ == '__main__':
    main()
