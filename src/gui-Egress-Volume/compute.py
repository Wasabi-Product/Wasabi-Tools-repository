import datetime


class Compute:
    size_table = None

    def __init__(self):
        # Generate a table for SI units symbol table.
        self.size_table = {0: 'Bs', 1: 'KBs', 2: 'MBs', 3: 'GBs', 4: 'TBs', 5: 'PBs', 6: 'EBs'}

    @staticmethod
    def calculate_size(size, _size_table):
        """
        This function dynamically calculates the right base unit symbol for size of the object.
        :param size: integer to be dynamically calculated.
        :param _size_table: dictionary of size in Bytes. Created in wasabi-automation.
        :return: string of converted size.
        """
        count = 0
        while size // 1024 > 0:
            size = size / 1024
            count += 1
        return str(round(size, 2)) + ' ' + _size_table[count]

    def get_egress(self, json_data, days):
        # get json data for billing

        # initialize a dict for adding up numbers
        result = 0

        # get the initial time and check date only for this day.
        initial_time = datetime.datetime.now()

        # for each bucket add the the data to the dict
        for bucket in json_data:
            # check the time from the last day.
            time = datetime.datetime.strptime(bucket['StartTime'], '%Y-%m-%dT%H:%M:%SZ')
            # summing logic.
            diff = initial_time - time
            if diff.days <= days:
                result += bucket['DownloadBytes']
            else:
                break
        return self.calculate_size(result, self.size_table), diff.days - 1
