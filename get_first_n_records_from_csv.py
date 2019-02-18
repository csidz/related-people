import csv
from utils.customLogger import custom_logger as cl
import logging


# Reads data from a persons_raw_data.csv file
class GetFirstNRecordsFromCSVFile:
    """
    Class to read Persons raw data from a csv file and return the output as a list
    """

    log = cl(log_level=logging.INFO)

    # Decorator
    def read_data_from_csv(self) -> list:
        """
        Decorator function to read lines in a given csv file
        Stops reading if there is blank or EOF

        :return: list of strings
        """
        try:
            with open("./persons_raw_data.csv") as test_data:
                csv_reader = csv.reader(test_data)
                next(csv_reader)  # Filters header line
                for line in csv_reader:
                    if line:
                        yield line
                    else:
                        break
            test_data.close()
        except IOError:
            self.log.error(msg='Unable to access input data file')

    def get_first_n_records(self, count: int) -> list:
        """
        Gets the first 'count' records or all records if less than 'count' from input file

        :param count: int  number of person records
        :return: list of maximum 'count' items. Each item is a list i.e. each person details
        """
        person_details = []
        counter = 0
        record = self.read_data_from_csv()
        for row in record:
            if counter < count:
                person_details.append(row)
                counter += 1
        self.log.info(msg=f'Collected {len(person_details)} records')
        return person_details
