PATH_TO_CARS = 'files/'
ALL = 'files/all.txt'
RENTED = 'files/rented.txt'
NOT_RENTED = 'files/not_rented.txt'


def load_file(file):
    '''
    Load content of file. Parameter "file" includes path.
    '''
    with open(file) as f:
        return f.read()


def create_db():
    '''
    Create dictionary of cars.
    '''
    main_db = {}
    cars = load_file(ALL)
    cars_list = list(cars.replace('\n', ''))
    for car_num in cars_list:
        if car_num:
            car = {}
            car_content = load_file(PATH_TO_CARS + car_num + '.txt')
            rows = list(car_content.split('\n'))
            inner_dict_key = ''

            for record in rows:
                if record:
                    key, value = record.split('=')
                    if not value:
                        inner_dict_key = key
                        car[key] = {}
                    elif key[0] == ' ' and inner_dict_key:
                        key = key.strip()
                        car.get(inner_dict_key).update({key: value})
                    else:
                        car[key] = value
                        inner_dict_key = ''

        main_db[car_num] = car
    return main_db


def print_head():
    '''
    Print heading of menu
    '''
    print('*'*75)
    print()
    print('hello !!! this is rent car app'.upper())
    print()
    print('*'*75)


def print_menu(menu):
    '''
    Print menu items
    '''
    print()
    for item in menu:
        print(item, end='   ')
    print()
    print()
    print('*'*75)


def print_selected_cars(main_db, cars_list):
    '''
    Print table with selected cars
    '''
    template = '''{}
| {:^12} | {:^12} | {:^12} | {:^12} | {:^12} |
| {:^12} | {:^12} | {:^12} | {:^12} | {:^12} |'''
    input_for_print = create_selection_for_print(main_db, cars_list)
    star_row = '*'*75
    for row in input_for_print:
        print(template.format(star_row, *row))
    print(star_row)


def create_selection_for_print(main_db, cars_list):
    '''
    Create list of values for each car,
    which serves as a print input
    '''
    input_for_print = []
    row_key = ['ID']
    for car in cars_list:
        row = [car]
        for key, value in main_db[car].items():
            if isinstance(value, dict):
                for key_inner, value_inner in value.items():
                    if not input_for_print:
                        row_key.append(key_inner)
                    row.append(value_inner)
            else:
                if not input_for_print:
                    row_key.append(key)
                row.append(value)
        input_for_print.append(row)
    input_for_print = [row_key] + input_for_print
    return input_for_print


main_db = create_db()
cars_list = list(main_db)
create_selection_for_print(main_db, cars_list)


def choose_car():
    '''
    User choose car ID for rent.
    The car have to be in file of not rented cars.
    If user choose invalid ID, the program prints available cars ID.
    '''
    while True:
        ID = input('Select the car number you want to rent: ')
        print()
        if ID.lower() == 'q':
            return
        elif ID in load_file(NOT_RENTED):
            return ID
        else:
            if ID in load_file(RENTED):
                print('The car is NOT available')
            else:
                print('Wrong choice, try again or press Q to QUIT.')
            not_rented = load_file(NOT_RENTED).strip().replace('\n', ', ')
            print('You can choose this cars: {}\n'.format(not_rented))


def return_car():
    '''
    User choose car ID for return.
    The car have to be in file of rented cars.
    If user choose invalid ID, the program prints list of rented cars.
    '''
    while True:
        ID = input('Select the car number you want to return: ')
        print()
        if ID.lower() == 'q':
            return
        elif ID in load_file(RENTED):
            return ID
        else:
            print('Wrong choice, try again or press Q to QUIT.')
            rented = load_file(RENTED).strip().replace('\n', ', ')
            print('You can choose this cars: {}\n'.format(rented))


def write_car_to_file(ID, file):
    '''
    Write car ID to file.
    '''
    with open(file) as f:
        content = f.read()
    content = list(content.strip().replace('\n', ''))
    content.append(ID)
    content.sort()
    content = '\n'.join(content)
    with open(file, 'w') as f:
        f.write(content)


def del_car_from_file(ID, file):
    '''
    Delete car ID from file
    '''
    with open(file) as f:
        content = f.read()
    content = content.replace(ID, '').replace('\n\n', '\n')
    with open(file, 'w') as f:
        f.write(content)


def conditions(cond_list):
    '''
    Collection of conditions from the user.
    Return list od conditions = tuples.
    '''
    parametr = input('''Enter parameter you search:
--> ''').strip()
    if not parametr:
        return cond_list
    value = input('''Enter value you search:
--> ''').strip()
    if not value:
        return cond_list
    comp_sing = input('''Enter comparison sing you search. Use:
=   is equal         >   is bigger             <   is smaller
!=  is not equal     >=  is bigger or equal    <=  is smaller or equal
--> ''').strip()
    if not comp_sing:
        return cond_list
    condition = (parametr, value, comp_sing)
    cond_list.append(condition)
    return cond_list


def compare_cond(value1, comp_sing, value2):
    '''
    Compare value1 with value2 using comp_sing.
    Example:
    value 1 = 5, value 2 = 6, comp_sing = '=='
    5 == 6   -->   False
    '''
    if value1.isdigit() and value2.isdigit():
        value1, value2 = float(value1), float(value2)

    if comp_sing == '=':
        return value1 == value2
    elif comp_sing == '!=':
        return value1 != value2
    elif comp_sing == '>':
        return value1 > value2
    elif comp_sing == '>=':
        return value1 >= value2
    elif comp_sing == '<':
        return value1 < value2
    elif comp_sing == '<=':
        return value1 <= value2
    else:
        return False


def search_conditions(cond_list, main_db):
    '''
    Searches for a car according to the specified conditions.
    Returns a list of cars that meet all conditions.
    '''
    results = []
    for condition in cond_list:
        result = []
        cond_key, cond_value, cond_comp_sing = condition
        for ID, car_values in main_db.items():
            for key, value in car_values.items():
                if isinstance(value, dict):
                    for key2, value2 in value.items():
                        if key2 == cond_key:
                            if compare_cond(value2, cond_comp_sing, cond_value):
                                result.append(ID)
                if key == cond_key:
                    if compare_cond(value, cond_comp_sing, cond_value):
                        result.append(ID)
        result = set(result)
        results.append(result)
    if not results:
        return []
    return list(set.intersection(*results))


def add_condition():
    '''
    After searching user can add additional condition.
    '''
    while True:
        answer = input('Do you want add new condition? Yes or No?: ')
        if answer.lower() in ['n', 'no']:
            return False
        if answer.lower() in ['y', 'yes']:
            return True


def main():
    print_head()
    main_db = create_db()

    while True:
        menu = ['1 - Show all', '2 - Search car',
                '3 - Rent car', '4 - Return car', '5 - Quit app']
        print_menu(menu)
        choice = input('Choose your option: '.upper())
        print()

        # SHOW ALL
        if choice == '1':
            print('summary of all cars:'.upper())
            cars_list = list(main_db)
            print_selected_cars(main_db, cars_list)
            print()

        # SEARCH CAR
        elif choice == '2':
            print('Search your dream car'.upper())
            cond_list = []
            while True:
                cond_list = conditions(cond_list)
                if cond_list:
                    print('Searching...')
                    print()
                    results = search_conditions(cond_list, main_db)
                    if results:
                        print_selected_cars(main_db, results)
                    else:
                        del cond_list[-1]
                        print('No valid results')
                answer = add_condition()
                if not answer:
                    break
            print()

        # RENT CAR
        elif choice == '3':
            ID = choose_car()
            if ID:
                write_car_to_file(ID, RENTED)
                del_car_from_file(ID, NOT_RENTED)
                print('congratulation, you choose car {}'.upper().format(ID))
            print()

        # RETURN CAR
        elif choice == '4':
            ID = return_car()
            if ID:
                write_car_to_file(ID, NOT_RENTED)
                del_car_from_file(ID, RENTED)
                print('thank you for returning car {}'.upper().format(ID))
            print()

        # QUIT
        elif choice == '5':
            print('Thanks for using rent car app. Bye.'.upper())
            break
            print()

        # WRONG CHOICE
        else:
            print('your choice is unknown'.upper())
            print()


main()
