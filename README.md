# rdec
The Roller Derby Event Coordinator (**RDEC**) is a Web application designed for Roller Derby leagues to help them
monitor and manage the attendence of their members to events. It aims to provide answers to the questions that plague event organisers:
* *How many officials are coming to this event?*
* *How many skaters are coming?*
* *How we can we avoid people opting out because they think an event will have low attendance?*
* *Do we have any third-party visitors coming?*

### Installation
A Python virtual environment - either virtualenv or conda - is recommended.

````conda create -n rdecenv python=3.6.0
source activate rdecenv
pip install --use-wheel -r requirements.txt
````

### Configuration
Major configuration is via environment variables.

````DATABASE_URL='sqlite:///rdec.db'
DATABASE_URL='postgres://rdecuser:rdecpass@localhost:5432/rdecdb'
RDEC_ALLOWED_HOSTS='.roller-derby.rocks rdec.herokuapp.com'
RDEC_DEBUG=False
RDEC_LEAGUE_NAME='Hellfire Harlots'
RDEC_MAIL_FROM_ADDRESS='harlots-rdec@roller-derby.rocks'
RDEC_RECENT_EVENT_CUTOFF_DAYS=7
````

### Initial Setup
````python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
````

### Running
A Python WSGI server is required - gunicorn is recommended.

````
gunicorn rdecsite.wsgi
````

### Completing Setup
Browse to http://*host*:*port*, log in with the administrative superuser and whack 'Admin' in the navigation bar.
Add Event Roles using the Admin interface. Examples of roles are:
* NSO
* Skater
* Referee
* Bench
* Line-up
* Event Staff

Add events using the Events admin page.
