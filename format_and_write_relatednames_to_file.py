from utils.customLogger import custom_logger as cl
import logging
from get_related_persons import GetRelatedPersons


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
        related_names_data = GetRelatedPersons().get_related_names_data()
        matches = FormatAndWriteRelatedNamesToAFile.build_format_for_related_names(related_names_data)
        try:
            with open('related_persons_info.txt', 'w') as output_file:
                for match in matches:
                    try:
                        output_file.write(match)
                    except OSError:
                        self.log.error(msg="Error while writing to the Output text file")
            output_file.close()
        except IOError:
            self.log.error(msg='Unable to access output txt file')
        self.log.info(msg="Check out the output file for Related Persons details")


if __name__ == "__main__":
    """
    Calls the function that initiates the operation of finding related persons
    """
    FormatAndWriteRelatedNamesToAFile().write_related_names_data_to_text_file()
