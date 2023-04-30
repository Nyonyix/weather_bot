import datetime

class LatAndLongNotFound(Exception):
    def __init__(self) -> None:
        self.message = "Lat and Long coordinates were not found in source file."
        super().__init__(self.message)

class WarningHazardNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The warned hazard has not been found within the source file."
        super().__init__(self.message)

class WarningTimeNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The warning time string has not been found within the source file."
        super().__init__(self.message)

class WarningCountiesNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The affected areas has not been found within the source file."
        super().__init__(self.message)

class WarningSourceNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The source has not been found within the source file."
        super().__init__(self.message)

class WarningIdNotFound(Exception):
    def __init__(self) -> None:
        self.message = "The ID has not been found within the source file."
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
        
        self.keywords = ["source...", "lat...", "hazard...", "time...", "/o."]

        self.file_dir = file_dir

        self.file_parse_out = self.parse_file()
        self.raw_lines = self.file_parse_out[0]
        self.counties = self.file_parse_out[1]

        if file_dir.split(".")[1] == "SVR":
            self.type = "Severe Thunder Storm Warning"
        elif file_dir.split(".")[1] == "TOR":
            self.type = "Tornado Warning"
        else:
            self.type = "Unknown"

        try:
            lat_long_is_there = False
            for line in self.raw_lines:

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
            for line in self.raw_lines:

                if "hazard..." in line:
                    self.hazard = self.parse_hazard(line)
                    hazard_is_there = True

            if not hazard_is_there:
                raise WarningHazardNotFound
        except WarningHazardNotFound as e:
            self.hazard = "Unknown, See Logs"
            exit(e)

        try:
            time_is_there = False
            for line in self.raw_lines:

                if "/o." in line:
                    self.time_issued = self.parse_time(line, True)
                    time_is_there = True

            if not time_is_there:
                raise WarningTimeNotFound
        except WarningTimeNotFound as e:
            self.time_issued = "Unknown, See Logs"
            exit(e)

        try:
            time_is_there = False
            for line in self.raw_lines:

                if "/o." in line:
                    self.time_expire = self.parse_time(line, False)
                    time_is_there = True

            if not time_is_there:
                raise WarningTimeNotFound
        except WarningTimeNotFound as e:
            self.time_expire = "Unknown, See Logs"
            exit(e)

        try:
            source_is_there = False
            for line in self.raw_lines:

                if "source..." in line:
                    self.source = self.parse_source(line)
                    source_is_there = True

            if not source_is_there:
                raise WarningSourceNotFound
        except WarningSourceNotFound as e:
            self.source = "Unknown, See Logs"
            exit(e)

        try:
            id_is_there = False
            for line in self.raw_lines:

                if "/o." in line:
                    self.id = line
                    id_is_there = True

            if not id_is_there:
                raise WarningIdNotFound
        except WarningIdNotFound as e:
            self.id = "Unknown, See Logs"
            exit(e)

    def parse_file(self) -> list[list[str], list[str]]:
        """Function that returns usable data from raw NWS warning files.

        :param file_dir: Directory of the warning file.
        :type file_dir: str
        :param keywords: List of keywords that determines the usable data
        :type keywords: list[str]
        :return: Returns lines of the warning file based on keywords provided.
        :rtype: list[str]
        """
        
        lines_out = []
        counties = []

        with open(self.file_dir, 'r') as f:
            lines = [line[:-1].casefold() for line in f.readlines() if line[:-1] != ""]
            f.close()

        for line in lines:
            for word in self.keywords:

                if word.casefold() in line:
                    lines_out.append(line)

        is_counties = False
        for line in lines:
            if "for..." in line:
                is_counties = True
                continue

            if "* until" in line:
                is_counties = False
                break

            if is_counties:
                counties.append(line.strip()[:-3].title())

        file_out = [lines_out, counties]
        return file_out

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

    def parse_time(self, raw_str: str, issue_time: bool) -> datetime:

        if issue_time:
            datetime_str = raw_str.split(".")[-1].split("-")[0][:-1]
        else:
            datetime_str = raw_str.split(".")[-1].split("-")[1][:-2]

        date_str, time_str = datetime_str.split("t")

        year = int("20" + date_str[:2])
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        hour = int(time_str[:2])
        minute = int(time_str[2:4])

        return datetime.datetime(year, month, day, hour, minute, tzinfo=datetime.timezone.utc)

    def parse_hazard(self, raw_str: str) -> str:
        """Takes the line with the hazard, Removes unnecessary text and capitalises.

        :param raw_str: Raw string containg the hazard
        :type raw_str: str
        :return: Returns capitalised hazard
        :rtype: str
        """

        return raw_str.split("...")[-1][:-1].capitalize()

    def parse_source(self, raw_str: str) -> str:
        """Takes the line with the source, Removes unnecessary text and capitalises.

        :param raw_str: Raw string containg the source
        :type raw_str: str
        :return: Returns capitalised source
        :rtype: str
        """

        return raw_str.split("...")[-1][:-1].capitalize()
