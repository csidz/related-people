"""
The following script reads the persons details from './persons_raw_data.csv' file
and creates 'related_persons_info_solution1.txt' file.

The 'related_persons_info_solution1.txt' contains information of related persons based on
defined requirements
"""

import csv
import re
from validate_email import validate_email
from utils.customLogger import custom_logger as cl
import logging


# Reads data from a persons_raw_data.csv file
# raises error when there is a blank row
class GetMax1000RecordsFromCSVFile:
    """
    Class to read Persons raw data from a csv file and return the output as a list
    """

    log = cl(log_level=logging.INFO)

    def read_data_(self) -> list:
        """
        Reads data from csv file. Uses 'csv' library

        :return: list of items. Each item is a list consisting of persons raw data
        :exception raises exception if there is any blank line in the source csv file
        """
        person_details = []
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

    # Decorator
    def read_data_from_csv(self):
        with open("./persons_raw_data.csv") as test_data:
            csv_reader = csv.reader(test_data)
            next(csv_reader)  # Filters header line
            for line in csv_reader:
                if line:
                    yield line
                else:
                    break
        test_data.close()

    def get_first_1000_records_max(self, count: int) -> list:
        """
        Gets the first 1000 records from input file

        :param count: int  number of person records
        :return: list of maximum 1000 items. Each item is a list i.e. each person details
        """
        person_details = []
        counter = 0
        record = self.read_data_from_csv()
        for row in record:
            if counter < count:
                person_details.append(row)
                counter += 1
        return person_details


# Applies all Validation Rules on fields and returns filtered data
class FilterFields:
    """
    FilterFields class performs all the required user validations defined in requirements document
    and returns list items where each item is a list consisting of a person's first_name and last_name
    """

    log = cl(log_level=logging.INFO)

    def get_first_1000_records_max(self, data) -> list:
        """
        Gets the first 1000 items in a list

        :param data: list
        :return: list of maximum 1000 items. Each item is a list i.e. each person details
        """

        len_of_records = len(data)
        if len_of_records <= 1000:
            data = data[1:len_of_records]
            self.log.info(msg=f'Collected all {len_of_records-1} records')
        else:
            data = data[1:1000]
            self.log.info(msg="Collected first 1000 records")
        return data

    def get_data_with_fields_length_less_than_257(self, data: list) -> list:
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
        self.log.info(msg=f"""{len(rows_with_fields_len_257_max)} out of {len(
            data)} records have fields less than the length of 257""")
        return rows_with_fields_len_257_max

    # Helper
    def get_data_with_only_first_lastname_email(self, data: list) -> list:
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
        self.log.info(msg='Filtered all fields keeping first_name, last_name and email only')
        return data_with_required_fields_only

    def get_first_last_name_email_notblank_combination(self, data: list) -> list:
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
        self.log.info(msg=f'{len(data_with_nonblank_fields)} out of {len(data)} records do not have blank emails')
        return data_with_nonblank_fields

    def get_names_containing_atleast_one_alpha(self, data: list) -> list:
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
        self.log.info(msg=f"""{len(data_with_atleast_one_alpha)} out of {len(
            data)} records have atleast one alpha in their first_name and last_name""")
        return data_with_atleast_one_alpha

    def get_names_containing_alpha_or_space_hyphen_only(self, data: list) -> list:
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
        self.log.info(f"""{len(data_with_alpha_or_space_hypen)} out of {len(
            data)} records do not chars other than alpha or space or hyphen""")
        return data_with_alpha_or_space_hypen

    def get_fields_with_valid_email_format(self, data: list) -> list:
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
        self.log.info(f'{len(data_with_valid_email_format)} out of {len(data)} records have valid emails')
        return data_with_valid_email_format

    # Helper
    def get_first_and_lastname_details_and_remove_email(self, data: list) -> list:
        """
        Filters the person record and return only first_name and last_name
        :param data: list (received from function 'get_fields_with_valid_email_format')
        :return: list of items
        Each item is a person details with first_name, last_name only
        """
        data_first_lastname_filtered = []
        for row in data:
            data_first_lastname_filtered.append(row[0:2])
        self.log.info(msg='Filtered email keeping the first_name and last_name only')
        return data_first_lastname_filtered

    # All filter actions methods calling
    def get_filtered_first_lastname_details(self) -> list:
        """
        This function calls all the user validation functions above in an order and return persons details with
        last_name and first_name
        :return:list of items
        Each item is a person details which have gone through all user validations as per requirements
        Each item is a list consisting of first_name, last_name only
        """
        first_1000_records = GetMax1000RecordsFromCSVFile().get_first_1000_records_max(count=1000)
        data_with_fields_less_than_257chars = FilterFields().get_data_with_fields_length_less_than_257(data=first_1000_records)
        data_with_only_first_lastname_email = FilterFields().get_data_with_only_first_lastname_email(data=data_with_fields_less_than_257chars)
        filter_blank_names_emails_records = FilterFields().get_first_last_name_email_notblank_combination(data=data_with_only_first_lastname_email)
        data_with_atleast_one_alphachar = FilterFields().get_names_containing_atleast_one_alpha(data=filter_blank_names_emails_records)
        data_with_names_containing_alpha_or_space_hyphen_only = FilterFields().get_names_containing_alpha_or_space_hyphen_only(data=data_with_atleast_one_alphachar)
        data_with_valid_email_format = FilterFields().get_fields_with_valid_email_format(data=data_with_names_containing_alpha_or_space_hyphen_only)
        filtered_first_lastname_details = FilterFields().get_first_and_lastname_details_and_remove_email(data=data_with_valid_email_format)
        self.log.info(msg=f'{len(filtered_first_lastname_details)} records passed filtering')
        return filtered_first_lastname_details


# Applies the Search criteria for finding related persons and returns related persons data
class RelatedPersons:


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
        :param split_char: any char, in our project it hyphen
        :return: list
        """
        if '-' in last_name:
            last_name_ = last_name.split(split_char)
            # self.log.info(msg=f'"{last_name}" last Name contains {split_char} and splitted to {last_name_}') # enable if needed
            return last_name_
        else:
            # self.log.info(msg=f'"{last_name}" last name does not contain {split_char}') # enable if needed
            last_name = [last_name]
            return last_name

    def filter_keys_with_empty_values(self, names: dict) -> dict:
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


# Formats and writes related people to related_persons_info_solution2.txt file
class FormatAndWriteRelatedNamesToAFile:
    """
        FormatAndWriteRelatedNamesToAFile class gets the Matched names data,
        formats it as mentioned in requirements document and writes into a txt file"
        """

    log = cl(log_level=logging.INFO)

    # Generator
    @staticmethod
    def build_format_for_related_names(related_names_data: dict) -> str:
        """
        Generator function which returns string in the expected output
        :param related_names_data: list (received from get_related_names_data)
        :return: string (formatted)
        """
        for key, value in related_names_data.items():
            matched_names = ', '.join([str(x) for x in value])
            yield f'{key}: {matched_names} \n'

    def write_related_names_data_to_text_file(self):
        """
        Writes the string received from Generator to 'related_persons_info.text' file
        :return: text file
        """
        related_names_data = RelatedPersons().get_related_names_data()
        matches = FormatAndWriteRelatedNamesToAFile.build_format_for_related_names(related_names_data)
        try:
            with open('related_persons_info_solution2.txt', 'w') as output_file:
                for match in matches:
                    try:
                        output_file.write(match)
                    except OSError:
                        self.log.error(msg="Error while writing to the Output text file")
            output_file.close()
        except FileNotFoundError:
            self.log.error(msg="The output txt file does not exist")
        self.log.info(msg="Check out the output for Related Persons")


if __name__ == "__main__":
    """
    Calls the function that initiates the operation of finding related persons
    """
    FormatAndWriteRelatedNamesToAFile().write_related_names_data_to_text_file()
