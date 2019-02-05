"""
The following script reads the persons details from './persons_raw_data.csv' file
and creates 'related_persons_info.txt' file.

The 'related_persons_info.txt' contains information of related persons based on
defined requirements
"""

import csv
import re
from validate_email import validate_email
from utils.customLogger import custom_logger as cl
import logging


# Reads data from a persons_raw_data.csv file
# raises error when there is a blank row
class ReadInputData:
    log = cl(log_level=logging.INFO)
    """
    Class to read Persons raw data from a csv file and return the output as a list
    """
    def read_data(self) -> list:
        """
        Reads data from csv file. Uses 'csv' library

        :return: list of items. Each item is a list consisting of persons raw data
        :exception raises exception if there is any blank line in the source csv file
        """
        person_details = []
        input
        try:
            with open("./persons_raw_data.csv") as test_data:
                csv_reader = csv.reader(test_data)
                for row in csv_reader:
                    person_details.extend([row])
            test_data.close()
            self.log.info(msg="Raw data has been successfully read from csv file")
            return person_details

        except FileNotFoundError:
            self.log.error(msg="The input csv file does not exist")


# Applies all Validation Rules on fields and returns filtered data
class FilterFields:
    """
    FilterFields class performs all the required user validations defined in requirements document
    and returns list items where each item is a list consisting of a person's first_name and last_name
    """

    @staticmethod
    def get_first_1000_records_max(data) -> list:
        """
        Gets the first 1000 items in a list

        :param data: list
        :return: list of maximum 1000 items. Each item is a list i.e. each person details
        """
        len_of_records = len(data)
        if len_of_records <= 1000:
            data = data[1:len_of_records]
        else:
            data = data[1:1000]
        return data

    @staticmethod
    def get_data_with_fields_length_less_than_257(data: list) -> list:
        """
        Filters the person record if any of the person field length is more than 256

        :param data: list (received from function 'get_first_1000_records_max')
        :return: list of items. Each item is a person details with each detail length less then 256
        """
        rows_with_fields_len_257_max = []
        for row in data:
            field_len_less_than_257 = True
            for field in row:
                if len(field) > 257:
                    field_len_less_than_257 = False
                    break
            if field_len_less_than_257 is True:
                rows_with_fields_len_257_max.append(row)
        return rows_with_fields_len_257_max

    @staticmethod
    def get_data_with_only_first_lastname_email(data: list) -> list:
        """
        Filters all the fields from Persons details and return only first_name, last_name and email of each person

        :param data: list (received from function 'get_data_with_fields_length_less_than_257')
        :return: list of items. Each item is a person details with only first_name, last_name and email
        """
        data_with_required_fields_only = []
        for row in data:
            temp = []
            temp.extend([row[0]])
            temp.extend([row[1]])
            temp.extend([row[9]])
            data_with_required_fields_only.append(temp)
        return data_with_required_fields_only

    @staticmethod
    def get_first_last_name_email_notblank_combination(data: list) -> list:
        """
        Filters the person record if it contain blank first_name or last_name or email

        :param data: list (received from function 'get_data_with_only_first_lastname_email')
        :return: list of items.
        Each item is a person details with first_name, last_name and email which are not blank
        """
        data_with_nonblank_fields = []
        for row in data:
            is_field_blank = True
            for field in row:
                if not field:
                    is_field_blank = False
                    break
            if is_field_blank is True:
                data_with_nonblank_fields.append(row)
        return data_with_nonblank_fields

    @staticmethod
    def get_names_containing_atleast_one_alpha(data: list) -> list:
        """
        Filters the person record if it does not contain atleast one alpha character in first_name or last_name

        :param data: list (received from function 'get_first_last_name_email_notblank_combination')
        :return: list of items
        Each item is a person details with first_name, last_name, email where first_name and last_name
        contain atleast one alpha character
        """
        data_with_atleast_one_alpha = []
        for row in data:
            field_with_atleast_one_alpha = True
            for field in row[0:2]:
                if not re.search('[a-zA-Z]', field):
                    field_with_atleast_one_alpha = False
                    break
            if field_with_atleast_one_alpha is True:
                data_with_atleast_one_alpha.append(row)
        return data_with_atleast_one_alpha

    @staticmethod
    def get_names_containing_alpha_or_space_hyphen_only(data: list) -> list:
        """
        Filters the person record if it contains any character other than allowed alpha, space, hyphen
        in first_name or last_name

        :param data: list (received from function 'get_names_containing_atleast_one_alpha')
        :return: list of items
        Each item is a person details with first_name, last_name, email where first_name and last_name
        does not contain any character other than allowed
        """
        data_with_alpha_or_space_hypen = []
        for row in data:
            field_with_alpha_space_hyphen = True
            for field in row[0:2]:
                if not re.fullmatch('^[a-zA-Z- ]*$',  field):
                    field_with_alpha_space_hyphen = False
                    break
            if field_with_alpha_space_hyphen is True:
                data_with_alpha_or_space_hypen.append(row)
        return data_with_alpha_or_space_hypen

    @staticmethod
    def get_fields_with_valid_email_format(data: list) -> list:
        """
        Filters the person records consisting of invalid formatted emails
        Uses 'validate_email' library

        :param data: list (received from function 'get_names_containing_alpha_or_space_hyphen_only')
        :return: list of items
        Each item is a person details with first_name, last_name, email where emails are in valid format only

        ..note:: filters following email which are valid as per https://en.wikipedia.org/wiki/Email_address
        " "@example.org,  "john..doe"@example.org
        """
        data_with_valid_email_format = []
        for row in data:
            local_part = row[-1].split('@')[0]
            if (validate_email(row[-1])) and (len(local_part) < 65):
                data_with_valid_email_format.append(row)
        return data_with_valid_email_format

    # Helper
    @staticmethod
    def get_first_and_lastname_details_and_remove_email(data: list) -> list:
        """
        Filters the person record and return only first_name and last_name
        :param data: list (received from function 'get_fields_with_valid_email_format')
        :return: list of items
        Each item is a person details with first_name, last_name only
        """
        data_first_lastname_filtered = []
        for row in data:
            data_first_lastname_filtered.append(row[0:2])
        return data_first_lastname_filtered

    # All filter actions methods calling
    @staticmethod
    def get_filtered_first_lastname_details() -> list:
        """
        This functions calls all the user validation functions above in an order and return persons details with
        last_name and first_name
        :return:list of items
        Each item is a person details which have gone through all user validations as per requirements
        Each item is a list consisting of first_name, last_name only
        """
        raw_input_data = ReadInputData().read_data()
        first_1000_records = FilterFields.get_first_1000_records_max(data=raw_input_data)
        data_with_fields_less_than_257chars = FilterFields.get_data_with_fields_length_less_than_257(data=first_1000_records)
        data_with_only_first_lastname_email = FilterFields.get_data_with_only_first_lastname_email(data=data_with_fields_less_than_257chars)
        filter_blank_names_emails_records = FilterFields.get_first_last_name_email_notblank_combination(data=data_with_only_first_lastname_email)
        data_with_atleast_one_alphachar = FilterFields.get_names_containing_atleast_one_alpha(data=filter_blank_names_emails_records)
        data_with_names_containing_alpha_or_space_hyphen_only = FilterFields.get_names_containing_alpha_or_space_hyphen_only(data=data_with_atleast_one_alphachar)
        data_with_valid_email_format = FilterFields.get_fields_with_valid_email_format(data=data_with_names_containing_alpha_or_space_hyphen_only)
        filtered_first_lastname_details = FilterFields.get_first_and_lastname_details_and_remove_email(data=data_with_valid_email_format)
        return filtered_first_lastname_details


# Applies Search Criteria and writes related people to related_persons_info.txt file
class RelatedPersons:
    """
    RelatedPersons class finds whether a person is related to any another person based on search/match patterns
    defined in requirements document
    """

    @staticmethod
    def get_lastname_that_is_same_as_lastname_of_another(lastname: str, another_lastname: str) -> bool:
        """
        Compares two strings whether they are exactly same
        :param lastname: string
        :param another_lastname: string
        :return: boolean
        True if strings are exactly same
        """
        return lastname == another_lastname

    @staticmethod
    def get_a_part_of_hyphenated_name_that_appears_as_hyphenated_part_of_another(lastname: str, another_lastname: str) -> bool:
        """
        Finds whether a part of hyphenated string matches with any part of another hyphenated string
        :param lastname: string
        :param another_lastname: string
        :return: boolean
        True if matches else False
        """
        if ("-" in lastname) and ("-" in another_lastname):
            hyphenated_lastname = lastname.split("-")
            hyphenated_other_lastname = another_lastname.split("-")
            matches = [x for x in hyphenated_lastname if x in hyphenated_other_lastname]
            return matches
        else:
            return False

    @staticmethod
    def get_lastname_of_one_that_appears_as_part_of_hyphenated_lastname_of_another(lastname: str, another_lastname:str) -> bool:
        """
        Finds whether a string is exactly same as any part of hyphenated string
        :param lastname: string
        :param another_lastname: string
        :return: boolean
        True if same else False
        """
        if "-" in another_lastname:
            hyphenated_other_lastname = another_lastname.split("-")
            if lastname in hyphenated_other_lastname:
                return True
        elif "-" in lastname:
            hyphenated_lastname = lastname.split("-")
            if another_lastname in hyphenated_lastname:
                return True
        else:
            return False

    @staticmethod
    def get_related_names_data() -> list:
        """
        Call the search pattern functions above and returns a list of related persons
        :return: list
        each list contains a dictionary.
        In each dictionary:
            key = person first_name, last_name
            value: list of persons with first_name, last_name whose last_name matches with last_name in the key person
        as per requirements
        """
        data = FilterFields().get_filtered_first_lastname_details()
        related_names = []
        for i in range(0, len(data)):
            row = {}
            matching_lastnames = []
            for j in range(0, len(data)):
                if i != j:
                    record = data[i]
                    another_record = data[j]
                    if RelatedPersons.get_lastname_that_is_same_as_lastname_of_another(lastname=record[1],
                                                                                       another_lastname=another_record[1]):
                        matching_lastnames.append(another_record[0] + " " + another_record[1])
                        row[record[0] + " " + record[1]] = matching_lastnames
                    elif RelatedPersons.get_a_part_of_hyphenated_name_that_appears_as_hyphenated_part_of_another(lastname=record[1],
                                                                                                                 another_lastname=another_record[1]):
                        matching_lastnames.append(another_record[0] + " " + another_record[1])
                        row[record[0] + " " + record[1]] = matching_lastnames
                    elif RelatedPersons.get_lastname_of_one_that_appears_as_part_of_hyphenated_lastname_of_another(lastname=record[1],
                                                                                                                   another_lastname=another_record[1]):
                        matching_lastnames.append(another_record[0] + " " + another_record[1])
                        row[record[0] + " " + record[1]] = matching_lastnames
            if row:
                related_names.append(row)
        return related_names

    # Generator
    @staticmethod
    def build_format_for_related_names(related_names_data: list) -> str:
        """
        Generator function which returns string in the expected output
        :param related_names_data: list (received from get_related_names_data)
        :return: string (formatted)
        """
        for record in related_names_data:
            for key, value in record.items():
                matched_names = ', '.join([str(x) for x in value])
                yield f'{key}: {matched_names} \n'

    @staticmethod
    def write_related_names_data_to_text_file():
        """
        Writes the string received from Generator to 'related_persons_info.text' file
        :return: text file
        """
        related_names_data = RelatedPersons().get_related_names_data()
        matches = RelatedPersons.build_format_for_related_names(related_names_data)
        with open('related_persons_info.txt', 'w') as output_file:
            for match in matches:
                output_file.write(match)
        output_file.close()


if __name__ == "__main__":
    """
    Calls the function that initiates the operation of finding related persons
    """
    RelatedPersons().write_related_names_data_to_text_file()
