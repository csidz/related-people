import re
from validate_email import validate_email
from utils.customLogger import custom_logger as cl
import logging
from toolz import functoolz
from get_first_n_records_from_csv import GetFirstNRecordsFromCSVFile


# Applies all Validation Rules on fields and returns filtered data
class FilterFields:
    """
    FilterFields class performs all the required user validations defined in requirements document
    and returns list items where each item is a list consisting of a person's first_name and last_name
    """

    log = cl(log_level=logging.INFO)

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
            temp = [row[0], row[1], row[9]]
            data_with_required_fields_only.append(temp)
        self.log.info(msg='Filtered all fields keeping first_name, last_name and email only')
        return data_with_required_fields_only

    def get_fields_with_valid_email_format(self, data: list) -> list:
        """
        Filters the person records consisting of invalid formatted emails
        Uses 'validate_email' library
        Checks whole email address is in valid format or not using validate_email library
        Checks Local part of email length is less than 65 chars

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

    def get_names_containing_atleast_one_alpha(self, data: list) -> list:
        """
        Filters the person record if it does not contain atleast one alpha character in first_name or last_name

        :param data: list (received from function 'get_first_last_name_email_notblank_combination')
        :return: list of items
        Each item is a person details with first_name, last_name, email where first_name and last_name
        contain atleast one alpha character
        Example: it filters any first_name or last_name with only '--' or '  '
        """
        data_with_atleast_one_alpha = []
        for row in data:
            field_with_atleast_one_alpha = True
            for field in row:
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
            for field in row:
                if not re.fullmatch('^[a-zA-Z- ]*$',  field):
                    field_with_alpha_space_hyphen = False
                    break
            if field_with_alpha_space_hyphen is True:
                data_with_alpha_or_space_hypen.append(row)
        self.log.info(f"""{len(data_with_alpha_or_space_hypen)} out of {len(
            data)} records do not chars other than alpha or space or hyphen""")
        return data_with_alpha_or_space_hypen

    # All filter actions methods calling
    def get_filtered_first_lastname_details(self) -> list:
        """
        This function calls all the user validation functions above in an order and return persons details with
        last_name and first_name
        Uses fancy functoolz.compose from toolz library

        :return:list of items
        Each item is a person details which have gone through all user validations as per requirements
        Each item is a list consisting of first_name, last_name only
        """
        data = GetFirstNRecordsFromCSVFile().get_first_n_records(count=1000)
        name_details_after_fields_filtering = functoolz.compose(self.get_names_containing_alpha_or_space_hyphen_only,
                                                                self.get_names_containing_atleast_one_alpha,
                                                                self.get_first_and_lastname_details_and_remove_email,
                                                                self.get_fields_with_valid_email_format,
                                                                self.get_first_last_name_email_notblank_combination,
                                                                self.get_data_with_only_first_lastname_email,
                                                                self.get_data_with_fields_length_less_than_257)(data)
        self.log.info(msg=f'{len(name_details_after_fields_filtering)} records passed filtering')
        return name_details_after_fields_filtering
