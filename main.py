#pip3 install psycopg2-binary
import datetime
import psycopg2
from db_config import db_host, db_user, db_password, db_name

#create table
# CREATE TABLE IF NOT EXISTS public.train
# (
#     destination text COLLATE pg_catalog."default" NOT NULL,
#     train_number integer NOT NULL,
#     "time" time without time zone NOT NULL,
#     id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
#     CONSTRAINT train_pkey PRIMARY KEY (id)
# )

# позволяет вводить информацию,
# хранить её в файле (БД),
# осуществлять поиск,
# модификацию,
# сортировку и
# удаление данных


#what to make better:
# check table exist on start and create if not exist
# move db connect/disconnect code to seporated func
# render db results in main()



def id_exist(request_id):
    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        db_connection.autocommit = True

        request_id = str(request_id)

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM train where id = %s;""",
                [request_id]
            )
            #print('print fetchall: ', cursor.fetchall())
            if not cursor.fetchall():
                result = -1
            else:
                result = 1

    except Exception as _ex:
        print("[INFO id exist] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO id exist] PostgreSQL connection closed")

    return result

def show_on_screen_db_data(result):
    print('\nDestination, Train number, Time, id')
    # loop through the rows
    for i in result:
        j = 0
        while j < len(i):
            print(i[j], end=' ')
            j += 1
        print('')

def render_database():
    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_name)
        db_connection.autocommit = True

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM train;"""
            )

            # fetch all the matching rows
            result = cursor.fetchall()
            # loop through the rows
            show_on_screen_db_data(result)
            print('')

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO] PostgreSQL connection closed")

def add_data_to_db(destination, train_number, time):
    if len(destination) >= 200:
        print('Destination name length is out of limit (limit = 200)')
        return -1
    #проверка, что номер поезда -- номер
    if not train_number.isnumeric():
        print('Train number incorrect')
        return -1
    #проверка, что введенная дата -- дата
    try:
        time = datetime.datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        print('Time is incorrect')
        return -1

    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_name)
        db_connection.autocommit = True

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO train 
                (destination, train_number, time)
                VALUES (%s, %s, %s);""",
                (destination, train_number, time))
        print('[INFO] Data added to database')



    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO] PostgreSQL connection closed")

def delete_data_from_db(request_id):
    if id_exist(request_id) == -1:
        #thre is no such id in db
        print('Such id not found')
    else:
        #id detected
        #delete row
        try:
            # connect to exist database
            db_connection = psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name)
            db_connection.autocommit = True

            request_id = str(request_id)

            # get data from a table
            with db_connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM train WHERE id = %s;""",
                    [request_id]
                )
                #print('print fetchall: ', cursor.fetchall())

        except Exception as _ex:
            print("[INFO delete_data_from_db] Error while working with PostgreSQL", _ex)
        finally:
            if db_connection:
                db_connection.close()
                print("[INFO delete_data_from_db] PostgreSQL connection closed")

def sort_data_base(sort_type):
    if sort_type == 1:
        sort_cmd = 'asc'
    elif sort_type == 2:
        sort_cmd = 'desc'

    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        db_connection.autocommit = True

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """select * from train order by train_number %s;""" %
                sort_cmd
            )
            result = cursor.fetchall()
            show_on_screen_db_data(result)
            print('')

    except Exception as _ex:
        print("[INFO sort_data_base] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO sort_data_base] PostgreSQL connection closed")

def search_data_db(search_data):
    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host,user=db_user,password=db_password,database=db_name)
        db_connection.autocommit = True

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """select * from train where train_number = %s;""",
                [search_data]
            )

            # fetch all the matching rows
            result = cursor.fetchall()
            # loop through the rows
            show_on_screen_db_data(result)
            print('')

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO] PostgreSQL connection closed")

def edit_data_in_db(row_id_to_edit,destination,train_number,time):
    try:
        # connect to exist database
        db_connection = psycopg2.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        db_connection.autocommit = True

        # get data from a table
        with db_connection.cursor() as cursor:
            cursor.execute(
                """UPDATE train
                    SET destination = %s, train_number = %s, time = %s
                    WHERE id = %s;""",
                (destination,train_number,time,row_id_to_edit))

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if db_connection:
            db_connection.close()
            print("[INFO] PostgreSQL connection closed")




def main():
    print('Welcom to course project\n'
          'Discipline:\tbasics of programming\n'
          'Variant\t\t#8\n'
          'Student:\tAndreev Nikolay Nikolayevich\n'
          'Group:\t\tz0431\n'
          'Ver.:\t\t 0.1 pre-alpha')
    while True:
        print('-'*40 + '\n' +
              ' '*15 + 'MAIN MENU\n' +
              '-' * 40 + '\n' +
                '[0]\tRender database\n'
                '[1]\tAdd data\n'
                '[2]\tSearch data\t[by train number]\n'
                '[3]\tEdit data\t[by id]\n'
                '[4]\tSort data\t[by train number]\n'
                '[5]\tDelete data\t[by id]\n'
                '[6]\tExit')

        #check users choose from menu
        while True:
            choose_action = input('[INPUT]\tSelect select number of operation (only number): ')
            if choose_action.isnumeric(): #if user inpputed numeric
                choose_action = int(choose_action)  #make users input integer
                if choose_action > -1 and choose_action < 7: #user input digit from 0 to 6
                    break
                else:
                    print('[ERROR]\tInput Correct digit')
            else: # user's input is  not numeric
                print('[ERROR]\tIncorrect input, please input only digit')

        # render database
        if choose_action == 0: render_database()

        # Add data
        elif choose_action == 1:
            while True: #circle to input data
                if add_data_to_db(input('[INPUT]\tInsert destination (maximum length 200): '),
                               input('[INPUT]\tInsert train number (only integer): '),
                               input('[INPUT]\tInsert time (format HH:MM:SS): ')) != -1:
                    break #if user inputed correct data, break while

        # search by train
        elif choose_action == 2:
            while True:
                train_number = input('Please enter train number (only digits): ')
                if train_number.isnumeric():
                    search_data_db(train_number)
                    break
                else:
                    print('[INPUT]\tEnter correct train number (only digits is available)')

        # edit data
        elif choose_action == 3:
            while True:
                #input id and check it
                row_id_to_edit = input('[INPUT]\tEnter id of row to edit (only digit):')
                if row_id_to_edit.isnumeric():
                    row_id_to_edit = int(row_id_to_edit)
                else:
                    print('[ERROR]\tPlease enter only digit')
                    continue

                #input destination and check it
                destination = input('[INPUT]\tEnter new destination (maximum length 200): '),
                if len(destination) >= 200:
                    print('[ERROR]\tDestination name length is out of limit (limit = 200)')
                    continue

                # input and check train nmbr
                train_number = input('[INPUT]\tEnter new train number (only integer): ')
                if not train_number.isnumeric():
                    print('[ERROR]\tTrain number incorrect')
                    continue

                # input and check date
                time = input('[INPUT]\t Input new time (format HH:MM:SS): ')
                try:
                    time = datetime.datetime.strptime(time, "%H:%M:%S")
                except ValueError:
                    print('[ERROR]\tTime is incorrect')
                    continue

                #call func
                edit_data_in_db(row_id_to_edit,destination,train_number,time)

                # break when done
                break




        # sort data
        elif choose_action == 4:
            while True:
                sort_type = input('[INFO]\tSort database by TRAIN NUMBER:\n'
                                  '[INFO]\tPlease choose sort type (enter only digit):\n'
                                  '[1]\tasc;\n'
                                  '[2]\tdesc\n'
                                  '[INPUT]\tMake ur choose: ')
                if sort_type.isnumeric(): #check if digit
                    sort_type = int(sort_type) #if data isnumeric covert it to int
                    if sort_type == 1 or sort_type == 2: #check if sort type == 1 or == 2
                        sort_data_base(sort_type)
                        break
                    else:
                        print('[ERROR]\tEnter only 1 or 2')
                else:
                    print('[ERROR]\tEnter only digit!')

        # delete data
        elif choose_action == 5:
            while True:
                request_id = input('[INPUT]\tPlease enter ID to delete: ')
                if request_id.isnumeric(): #check data is numeric
                    delete_data_from_db(request_id) #request func to delete data
                    break
                else:
                    print('[ERROR]\tIncorrect input, please input only digit')

        # exit software
        elif choose_action == 6:
            break


if __name__ == "__main__":
    main()
