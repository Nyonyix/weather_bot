import datetime

class LatAndLongNotFound(Exception):
    def __init__(self) -> None:
        self.message = "Lat and Long coordinates were not found in source file."
        super().__init__(self.message)

class WarningHazardNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The warned hazard has not been found within the source file."
        super().__init__(self.message)

class Warning(object):
    """Warning Object that contains various things related to warnings.

    This object contains various things that pertain to the specific warning that it is built on, Such as:
        - Hazard Type
        - Time
        - Source of warning
        - Latitude and longitude of the warning area

        :param file_dir: Directory to the file containing the warning text.
        :type file_dir: str
    """

    def __init__(self, file_dir: str) -> None:
        
        self.keywords = ["source...", "lat...", "hazard...", "time..."]

        self.file_dir = file_dir

        raw_lines = self.parse_file()
        self.time = 1
        self.source = ""
        self.counties = []

        try:
            lat_long_is_there = False
            for line in raw_lines:

                if "lat..." in line:
                    self.coords = self.parse_coords(line)
                    lat_long_is_there = True

            if not lat_long_is_there:
                raise LatAndLongNotFound
        except LatAndLongNotFound as e:
            self.coords = [["Unknown, See Logs"]]
            exit(e)

        try:
            hazard_is_there = False
            for line in raw_lines:

                if "hazard..." in line:
                    self.hazard = self.parse_hazard(line)
                    hazard_is_there = True

            if not hazard_is_there:
                raise WarningHazardNotFound
        except WarningHazardNotFound as e:
            self.hazard = "Unknown, See Logs"
            exit(e)

    def parse_file(self) -> list[str]:
        """Function that returns usable data from raw NWS warning files.

        :param file_dir: Directory of the warning file.
        :type file_dir: str
        :param keywords: List of keywords that determines the usable data
        :type keywords: list[str]
        :return: Returns lines of the warning file based on keywords provided.
        :rtype: list[str]
        """
        
        lines_out = []

        with open(self.file_dir, 'r') as f:
            lines = [line[:-1].casefold() for line in f.readlines() if line[:-1] != ""]
            f.close()

        for line in lines:
            for word in self.keywords:

                if word.casefold() in line:
                    lines_out.append(line)

        return lines_out

    def parse_coords(self, raw_str: str) -> list[list[str]]:
        """Takes the line of lat long coords from warning and converts to usable format.

        :param raw_str: Raw string containing the coords.
        :type raw_str: str
        :return: Returns a list of lat and long coords.
        :rtype: list[list[str]]
        """

        split_str = raw_str.split(" ")
        split_str = split_str[1:]

        out_coords = []

        for i in range(len(split_str)):

            if i%2 != 0:
                continue
            out_coords.append([split_str[i], f"-{split_str[i+1]}"])

        return out_coords

    def parse_time(self, raw_str: str) -> datetime.datetime:

        raw_str = raw_str[:-1]

        hours = raw_str[:2]
        minutes = raw_str[2:]

        full_time_str = f"{hours}:{minutes}:00.0"

    def parse_hazard(self, raw_str: str) -> str:
        """Takes the line with the hazard, Removes unnecessary text and capitalises.

        :param raw_str: Raw string containg the hazard
        :type raw_str: str
        :return: Returns capitalised hazard
        :rtype: str
        """

        return raw_str.split("...")[-1][:-1].capitalize()
