import argparse


class ArgumentParser:
    """
    Taking care for creating argument parser object, handling passed arguments
    and returning them in the needed format for later use.
    """
    genres_choices = ['Travel', 'Mystery', 'Classics']
    sort_by_choices = ['rating', 'available', 'title', 'price']
    sorting_choices = ['ascending', 'descending']

    filter_choices = ['available', 'rating', 'price']
    filter_operators = ['<', '>', '=']

    def __init__(self):
        self.__parser = argparse.ArgumentParser(description='''
        This is tool to scrape books from http://books.toscrape.com/index.html.
        You have different options for filtering and manipulating the books.
        For more info type main.py -h
        ''')
        self.__exclusive_args_group = self.__parser.add_mutually_exclusive_group()
        self.__create_arguments()

    def return_parsed_arguments(self):
        args = self.__parser.parse_args()
        for el in args.__dict__:
            if args.__dict__[el]:
                return args
        raise self.__parser.error('You must use at least one flag')

    @staticmethod
    def __custom_sorting_dict(argument):
        """
        Parsing and validating argument. Creating dict from it.
        :param value: Single argument that we are taking from the command line
        :return: dict
        """

        try:
            value = str(argument)
        except ValueError:
            raise argparse.ArgumentTypeError(f'Expected string, got {argument!r}')
        split_data = value.split(' ')

        if len(split_data) > 2 or len(split_data) < 2:
            raise argparse.ArgumentTypeError(
                f'You must provide sort-by criteria {ArgumentParser.sort_by_choices} and way of sorting {ArgumentParser.sorting_choices}, got {argument}')
        sort_by, sorting = split_data

        if sort_by not in ArgumentParser.sort_by_choices:
            raise argparse.ArgumentTypeError(f'Sort by must be between {ArgumentParser.sort_by_choices}, got {sort_by}')
        if sorting not in ArgumentParser.sorting_choices:
            raise argparse.ArgumentTypeError(
                f'Sorting choices must be between {ArgumentParser.sorting_choices}, got {sorting}')

        return {sort_by: sorting}

    @staticmethod
    def __custom_filtering_list(argument):
        """
        Parsing and validating argument. Creating dict from it.
        :param value: Single argument that we are taking from the command line
        :return: list of dictionaries that contain the info for every filter.
        """
        try:
            value = str(argument)
        except ValueError:
            raise argparse.ArgumentTypeError(f'Expected string, got {argument!r}')

        first_filters_split = value.split(', ')
        result = []
        for cur_filter in first_filters_split:
            split_data = cur_filter.split(' ')

            if len(split_data) != 3:
                raise argparse.ArgumentTypeError(
                    f'''One filter must consist of 3 elements:
                     filter choice {ArgumentParser.filter_choices},
                     filter operator {ArgumentParser.filter_operators},
                     number by your choice, separated by space.
                     Format: <choice> <operator> <value>
                    ''')

            filter_choice, filter_operator, filter_value = split_data
            if filter_choice not in ArgumentParser.filter_choices:
                raise argparse.ArgumentTypeError(
                    f'Filter choice must be between {ArgumentParser.filter_choices}, got {filter_choice}')
            if filter_operator not in ArgumentParser.filter_operators:
                raise argparse.ArgumentTypeError(
                    f'Filter operator must be between {ArgumentParser.filter_operators}, got {filter_operator}')
            try:
                price = int(filter_value)
            except ValueError:
                raise argparse.ArgumentTypeError(f'Filter value must be integer, got {filter_value!r}')
            if price < 0:
                raise argparse.ArgumentTypeError(f'Filter value must be bigger than 0, got {filter_value}')
            result.append({'filter_choice': filter_choice,
                           'filter_operator': filter_operator,
                           'filter_value': filter_value,
                           })
        return result

    def __create_arguments(self):
        """
        Template code from argparse library to create and set the arguments that are taken from the command line.
        :return: None
        """
        self.__parser.add_argument(
            '-b',
            '-books',
            type=int,
            default=0,
            help='Get given number of books'
        )

        self.__parser.add_argument(
            '-g',
            '--genres',
            type=str,
            nargs='+',
            choices=ArgumentParser.genres_choices,
            default='',
            help='Search only in given genres'
        )

        self.__parser.add_argument(
            '-s',
            '--sorting',
            type=self.__custom_sorting_dict,
            default={},
            help='Sort the books by some stats'
        )

        self.__parser.add_argument(
            '-f',
            '--filters',
            type=self.__custom_filtering_list,
            default=[],
            help='Filter books by given filters'
        )

        self.__parser.add_argument(
            '-d',
            '--description',
            type=str,
            nargs='+',
            default=[],
            help='Search books by given keywords found in the description'
        )

        self.__exclusive_args_group.add_argument(
            '-t',
            '--title',
            type=str,
            nargs=1,
            help='Search for a book by its name'
        )

        self.__exclusive_args_group.add_argument(
            '-w',
            '--wanted',
        )
