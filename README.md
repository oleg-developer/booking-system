# HOTEL PRO PROJECT

Сontrol system 

The service is intended for automation of process of the account and service of guests, management of number Fund and tariffs, and also allows to form primary accounting records (receipts, accounts, acts of the performed works, etc.). 

The service has the ability to work with external sites for accommodation (Booking, HotelLook, Ostrovok, etc.), displaying reservations from all sites in one sheet of loading.


### Project apps
  - auth_core - include auth methods (Token authorization)
  - common - include common models (Phone, Country, etc...)
  - dashboard - some additional temlates
  - hotels - managing hotels, rooms, booking
  - users - managing users (Employee, Chief, etc...)

### Installation

Install the dependencies and start the server.

```
$ make venv
$ source venv/bin/activate
$ python src/manage.py migrate
$ python src/manage.py runserver
```

### Additional info

#### Install rabbitmq (celery)
Mac OS:
```
brew install rabbitmq
```
Linux:
```
sudo apt-get install rabbitmq-server
```