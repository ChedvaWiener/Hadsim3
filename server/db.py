import sqlite3
import logging
from threading import Lock
import time
from dataclasses import dataclass
from typing import Dict


ERROR = 400
OK = 201


@dataclass
class Image:
    """ Represents an Image in the database. """
    client_id: int
    img_name: str
    img: bytes


@dataclass
class Client:
    """ Represents a client in the database. """
    client_id: int
    first_name: str
    last_name: str
    city: str
    street: str
    house_number: str
    phone_number: str
    cellular: str
    born_date: str


@dataclass
class Covid19:
    """ Represents a Covid19 in the database. """
    client_id: int
    positive_date: str
    recovery_date: str


@dataclass
class Vaccination:
    """ Represents a Vaccination in the database. """
    client_id: int
    manufacturer: str
    date: str
    vaccine_number: int = 0


class Database:
    """
    This class handles all the database operations.
    """
    LOCAL_DB_FILE_NAME = "HMO.db"

    # SQL Scripts for table creation.
    CREATE_CLIENT_SQL = """
    CREATE TABLE IF NOT EXISTS Client (
    ID int NOT NULL PRIMARY KEY,
    FirstName text,
    LastName text,
    City text,
    Street text,
    HouseNumber text,
    PhoneNumber varchar(9),
    Cellular varchar(10),
    BornDate text
);
    """

    CREATE_COVID19_SQL = """ 
CREATE TABLE IF NOT EXISTS Covid19 (
    ID int NOT NULL,
    PositiveDate text,
    RecoveryDate text
);
    """

    CREATE_VACCINATION_SQL = """
        CREATE TABLE IF NOT EXISTS Vaccination (
    ID int NOT NULL,
    Manufacturer text,
    Date text,
    VaccineNumber INT
    );
        """

    CREATE_IMAGES_SQL = """
           CREATE TABLE IF NOT EXISTS Image (
           ID int NOT NULL,
           ImgName text,
           Img BLOB
       );
           """

    def __init__(self):
        self.logger = logging.getLogger("Server.DataAccess")
        self.covid19: Dict[int, Covid19] = {}
        self.clients: Dict[int, Client] = {}
        self.images: Dict[int, Image] = {}
        self.vaccinations: Dict[int, list] = {}
        self._conn = None
        self.__create_or_open_database()
        self.__create_tables()
        self.__load_data()

        # Thread saftey is important - This is a shared object!
        self.lock = Lock()

    def __create_or_open_database(self):
        """Open the DB"""
        self._conn = sqlite3.connect(self.LOCAL_DB_FILE_NAME, check_same_thread=False)

    def __create_tables(self):
        """Create tables if not exists"""
        self.logger.info("Making sure all tables exist.")
        cursor = self._conn.cursor()
        cursor.execute(self.CREATE_CLIENT_SQL)
        cursor.execute(self.CREATE_COVID19_SQL)
        cursor.execute(self.CREATE_VACCINATION_SQL)
        cursor.execute(self.CREATE_IMAGES_SQL)
        cursor.close()
        self._conn.commit()

    def __load_data(self):
        """ This method loads all the persistant SQLite3 DB data into the memory. """
        cursor = self._conn.cursor()
        all_clients = cursor.execute("SELECT * FROM Client").fetchall()
        all_covid19 = cursor.execute("SELECT * FROM Covid19").fetchall()
        all_vaccinations = cursor.execute("SELECT * FROM Vaccination").fetchall()
        all_images = cursor.execute("SELECT * FROM Image").fetchall()

        for img_row in all_images:
            client_id = img_row[0]
            self.images[client_id] = Image(client_id, *img_row[1:])

        for client_row in all_clients:
            client_id = client_row[0]
            self.clients[client_id] = Client(client_id, *client_row[1:])

        for covid19_row in all_covid19:
            client_id = covid19_row[0]
            self.covid19[client_id] = Covid19(client_id, *covid19_row[1:])

        for vaccine_row in all_vaccinations:
            client_id = vaccine_row[0]
            vaccine = Vaccination(client_id, *vaccine_row[1:])
            if client_id in self.vaccinations.keys():
                self.vaccinations[client_id].insert(0, vaccine)
            else:
                self.vaccinations[client_id] = [vaccine]

    def add_client(self, client: Client):
        """Add client"""
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO Client (ID, FirstName, LastName,City,Street,HouseNumber,PhoneNumber,Cellular,BornDate) VALUES (?,?,?,?, ?,?,?,?,?)",
            [client.client_id, client.first_name, client.last_name,client.city,client.street,client.house_number, client.phone_number,
             client.cellular,
             client.born_date])
        self.clients[client.client_id] = client
        self._conn.commit()
        cursor.close()
        self._conn.commit()

    def get_client_by_id(self, client_id):
        """Get client object by ID"""
        try:
            self.lock.acquire()
            if client_id in self.clients.keys():
                return self.clients[client_id]
            return None
        finally:
            self.lock.release()

    def client_exists(self, client_id):
        """Check if client exists"""
        cursor = self._conn.cursor()
        matches = cursor.execute("SELECT * FROM Client WHERE ID=?", [client_id]).fetchall()
        return len(matches) > 0

    def get_vaccines_list_by_id(self, client_id):
        """Get the client vaccination list by ID"""
        if client_id in self.vaccinations.keys():
            return self.vaccinations[client_id]
        else:
            return []

    def get_covid_info_by_id(self, client_id) -> Covid19:
        """Get the client Covid19 information by ID"""
        try:
            self.lock.acquire()
            if client_id in self.covid19.keys():
                return self.covid19[client_id]
            return None
        finally:
            self.lock.release()

    def add_vaccine(self, client_id, manufacturer, date):
        """Add vaccine to the client vaccination list"""
        try:
            self.lock.acquire()
            vaccine = None
            if not (client_id in self.vaccinations.keys()):
                vaccine: Vaccination = Vaccination(client_id, manufacturer, date, 1)
                self.vaccinations[client_id] = [vaccine]
            else:
                count = len(self.vaccinations[client_id])
                if count >= 4:
                    return ERROR
                else:
                    vaccine: Vaccination = Vaccination(client_id, manufacturer, date, ++count)
                    self.vaccinations[client_id].insert(0, vaccine)
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO Vaccination (ID, Manufacturer, Date,VaccineNumber) VALUES (?, ?, ?,?)",
                [client_id, manufacturer, date, vaccine.vaccine_number])
            self._conn.commit()
            cursor.close()
            return OK
        except Exception as error:
           return -1
        finally:
            self.lock.release()

    def add_covid(self, covid: Covid19):
        """Add Covi19 information to client"""
        try:
            self.lock.acquire()
            if covid.client_id in self.covid19.keys():
                return ERROR
            self.covid19[covid.client_id] = covid
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO Covid19 (ID, PositiveDate, RecoveryDate) VALUES (?, ?, ?)",
                [covid.client_id, covid.positive_date, covid.recovery_date])
            self._conn.commit()
            cursor.close()
            return OK
        except Exception as error:
           return ERROR
        finally:
            self.lock.release()

    def close(self):
        self._conn.close()

    def add_image(self, img: Image):
        try:
            self.lock.acquire()
            if img.client_id in self.images.keys():
                return ERROR
            self.images[img.client_id] = img
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO Image (ID, ImgName, Img) VALUES (?, ?, ?)",
                [img.client_id, img.img_name, img.img])
            self._conn.commit()
            cursor.close()
            return OK
        except Exception as error:
           return ERROR
        finally:
            self.lock.release()

    def vaccine_info(self):
        """Get the HMO vaccination information"""
        try:
            self.lock.acquire()
            vaccine_1 = len([1 for c in self.vaccinations.values() if len(c) == 1])
            vaccine_2 = len([1 for c in self.vaccinations.values() if len(c) == 2])
            vaccine_3 = len([1 for c in self.vaccinations.values() if len(c) == 3])
            vaccine_4 = len([1 for c in self.vaccinations.values() if len(c) == 4])
            vaccine_0 = len(self.clients.keys()) - vaccine_1 - vaccine_2 - vaccine_3 - vaccine_4
            info = {
                'labels': ['0', '1', '2', '3', '4'],
                'values': [vaccine_0, vaccine_1, vaccine_2, vaccine_3, vaccine_4],
                'colors': ['#66cc00', '#00f280', '#66b2ff', '#0066cc', '#004c99']
            }
            return info
        finally:
            self.lock.release()
