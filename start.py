from scraper import Parser


def menu():
    input_name = input('Specify the item to search for: \n')
    file_name = input('Specify the filename to save the data: \n')

    Parser(item_name=input_name, file_name=file_name).save_to_csv()


if __name__ == "__main__":
    menu()
