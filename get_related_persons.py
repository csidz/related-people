from utils.customLogger import custom_logger as cl
import logging
from filter_fields import FilterFields


# Applies the Search criteria for finding related persons and returns related persons data
class GetRelatedPersons:

    """
    RelatedPersons class finds whether a person is related to any another person based on search/match patterns
    defined in requirements document
    """

    log = cl(log_level=logging.INFO)

    def split_last_name(self, last_name: str, split_char: str) -> list:
        """
        Gets a string as a 1st param, check if the string contains a split char.
        If the string contains a split char, it will be split based on split char otherwise not
        In either way it return string converted to list
        :param last_name: a string normally, ex: "William-Scott" or "William"
        :param split_char: any char, in our project it is hyphen
        :return: list
        """
        if '-' in last_name:
            last_name_ = last_name.split(split_char)
            # enable if needed
            # self.log.info(msg=f'"{last_name}" last Name contains {split_char} and splitted to {last_name_}')
            return last_name_
        else:
            # self.log.info(msg=f'"{last_name}" last name does not contain {split_char}') # enable if needed
            last_name = [last_name]
            return last_name

    def filter_keys_with_empty_values(self, names: dict) -> dict:
        """
        It receives all the persons as keys and value as list of matching persons.
        When a person does not have a matching then that value will be empty list.
        This function filters those dictionary items having empty lists as the values

        :param names: dictionary with a key as a person first_name, last_name and value as list of matching persons.
        :return:
        """
        filtered_names = {k: v for k, v in names.items() if v}
        self.log.info(msg=f'{len(filtered_names)} keys filtered out of {len(names)} keys have values')
        return filtered_names

    def get_related_names_data(self) -> dict:
        """
        Takes one name at a time and compares its last name with the last names next in the order in the list
        The improvement over the solution1 is it compares two names in a list only once
        :return: dict with the values having last name matching with the last name in the respective key
        """
        items = FilterFields().get_filtered_first_lastname_details()
        related_names_dict = {}
        for i in range(0, len(items)):
            k = ' '.join([items[i][0], items[i][1]])
            last_name = []
            if k not in related_names_dict:
                related_names_dict[k] = []
            last_name.extend(self.split_last_name(last_name=items[i][1], split_char='-'))

            for j in range(i + 1, len(items)):
                another_last_name = self.split_last_name(last_name=items[j][1], split_char='-')
                match = [x for x in last_name if x in another_last_name]
                j = ' '.join([items[j][0], items[j][1]])
                if match:
                    related_names_dict[k].append(j)
                    if j not in related_names_dict:
                        related_names_dict[j] = []
                    related_names_dict[j].append(k)
        self.log.info("Completed comparing last names but result dictionary may contain keys with empty values")
        related_names_final_dict = self.filter_keys_with_empty_values(names=related_names_dict)
        self.log.info(f'Found {len(related_names_final_dict)} names in total having last name similar to others')
        return related_names_final_dict
