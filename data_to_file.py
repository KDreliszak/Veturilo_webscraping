import config_data


def get_station_values(file_name, col):
    station_attrib = []

    right_class = config_data.soup.find(class_=config_data.xml_class_name)
    right_table = right_class.table

    for row in right_table.findAll('tr'):
        try:
            station_attrib.append(row.findAll('td')[col].text.upper())
        except:
            pass
    
    f = open(file_name, 'w')
    f.writelines(map(lambda line: line + '\n', station_attrib))
    f.close()
    