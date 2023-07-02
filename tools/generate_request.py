from csv import reader as csv_reader


def generate_tu_prefere():
    """Generate the command SQL for insertion

    Returns:
        str: The SQL command to execute later
    """
    with open('./tools/data/tu_prefere.csv', 'r', encoding='utf-8') as file:
        reader = csv_reader(file)
        req = 'INSERT INTO TuPrefere (id, choice1, choice2) VALUES '
        id = 1
        for row in reader:
            req += f'({id},"{row[0]}","{row[1]}"),'
            id += 1

        req = f'{req[:-1]};'

        file.close()
    
    return req

print(generate_tu_prefere())
