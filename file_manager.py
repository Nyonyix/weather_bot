import requests
from bs4 import BeautifulSoup
import datetime
import pytz

class FileManager():

    def __init__(self) -> None:

        self.run()

    def run(self) -> None:

        self.__get_files()


    def __get_files(self) -> None:

        url = 'http://warnings.cod.edu/?C=M;O=D'
        utc = pytz.UTC
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[2:-1]

        for row in rows:

            filename = row.find('a').text
            date_str = row.find_next('td', align='right').text.strip().split()[0]
            time_str = row.find_next('td', align='right').text.strip().split()[1]
            
            date_time = datetime.datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            date_time_utc = utc.localize(date_time)
            time_difference = utc.localize(datetime.datetime.utcnow()) - date_time_utc
            
            if time_difference < datetime.timedelta(hours=1):

                file_url = url + filename
                r = requests.get(file_url, stream=True)

                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

    def check_files(self) -> None:

        pass

    def delete_files(self) -> None:

        pass

    
