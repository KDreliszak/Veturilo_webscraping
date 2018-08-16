from data_to_file import get_station_values
import config_data 
#import GPS ??


def main():    
    print('Find station by name or by GPS?')
    option_list = ['Find by name', 'Find by GPS']
    chosen_option = choice(option_list)

    if chosen_option == option_list[0]:
        get_station_name()
    else:
        find_station_by_GPS()


def open_file(file_name):
    try:
        f = open(file_name, 'r')
        temp_list = f.readlines()
        f.close()
        return list(map(lambda line: line.replace('\n', ''), temp_list))

    except FileNotFoundError:
        if file_name == config_data.file_station_names:
            get_station_values(file_name, config_data.station_names_col)
        else:
            get_station_values(file_name, config_data.station_localization_col)
        return open_file(file_name)


def get_station_name():
    print("Write down the name of the station or 0 if u want to see names of all stations ")
    station_name = input("").upper()
    if station_name == "0":
        choice(station_names)
    else:
        autocomplete(station_name, station_names)


def find_station_by_GPS():
    latitude_diff = 0.005
    longitude_diff = 0.004

    nearest_stations = []

    print(station_names, station_localizations)
    coordinates = [52.22983, 20.993996] #--------------pobieranie danych o pol. GPS---------------

    for line in station_localizations:
        latitude = float(line.replace(' ','').split(',')[0])
        longitude = float(line.replace(' ','').split(',')[1])

        if abs(coordinates[0]-latitude) < latitude_diff and abs(coordinates[1]-longitude) < longitude_diff:
            nearest_stations.append(station_names[station_localizations.index(line)])
    
    if nearest_stations:
        choice(nearest_stations)
    else:
        print('No stations nearby')
        main()


def choice(cos):
    if cos[0] != "Find by name" and cos[-1] != 'BACK TO MAIN MENU':
        cos.append('BACK TO MAIN MENU')

    for index, name in enumerate(cos):
        print("{0}: {1}".format(index, name))
    
    index = input("Enter choice number: ")

    try:
        chosen = cos[int(index)]
        if chosen == 'BACK TO MAIN MENU':
            main()
        elif cos[-1] != 'BACK TO MAIN MENU':
            return chosen
        else:
            print('Selected: {0}'.format(chosen))
            find_bikes(chosen, station_names)
    except IndexError:
        print("Wrong index\nWrite the number in range from 0 to %s" % (len(cos)-1))
        return choice(cos)


def autocomplete(station_name, station_names):
    filtered_stations = list(filter(lambda x: x.startswith(station_name), station_names))
    
    if len(station_name) > 2:
        for name in station_names:
            if station_name.upper() in name.upper():
                if name not in filtered_stations:
                    filtered_stations.append(name)
                    
    #Testing if the list: filtered_stations is not empty
    try:
        if len(filtered_stations) > 1:
            # More than one station has been found
            print('There are more than one station starting with "{0}"'.format(station_name))
            print('Select the station from choices: ')
            
            choice(filtered_stations)

        else:
            # One station has been found
            print('Selected station: {0}'.format(filtered_stations[0]))
            station = filtered_stations[0]
            find_bikes(station, station_names)

    except:
        print("There is no station starting with: %s \nTry again" % station_name)
        get_station_name()


def find_bikes(station, station_names):
    if station in station_names:
        right_class = config_data.soup.find(class_=config_data.xml_class_name)
        right_table = right_class.table
        
        for row in right_table.findAll('tr'):
            try:
                if row.findAll('td')[0].text.upper() == station:
                    free_bikes = row.findAll('td')[config_data.free_bikes_col].text
                    free_space = row.findAll('td')[config_data.free_space_col].text
                    break
            except:
                pass  

        print("Free bikes: %s" % free_bikes)
        print("Free space: %s" % free_space)


#get_station_name()

#find_station_by_GPS()

station_names = open_file(config_data.file_station_names)
station_localizations = open_file(config_data.file_station_localizations)

main()
