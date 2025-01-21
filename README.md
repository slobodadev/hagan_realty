# Hagen Realty Internal Tool

## Project Overview

This is an internal tool built for Hagen Realty to facilitate interaction with the BrightLMS (https://brightmls.com/) OData-based resource (https://brightmls.portal.swaggerhub.com/brightreso/default/). BrightLMS provides a comprehensive database of real estate properties, historical data, and metadata about those properties, enabling Hagen Realty to efficiently access, view, and manage essential property information.

Key Features

-	**Data Retrieval**: Connects to BrightLMS OData endpoints to fetch property details, historical data, and associated metadata.
-	**Data Management**: Provides options to truncate data within the application as required, ensuring smooth and efficient data operations.
-	**Django Admin Panel**: Allows users to view and manage the retrieved data directly through Django’s intuitive admin interface.
-	**Local Use Only**: Designed as a monolithic Django application to run on a local PC with no deployment or testing for web-based environments required.

### BrightLMS Integration

The tool is tightly integrated with the BrightLMS OData resource, relying on its API to fetch and process data. For more information about the OData endpoints and configurations, refer to the BrightLMS API documentation: BrightLMS API Documentation.

Use Case

This application empowers Hagen Realty with the ability to:
1.	Fetch and store data from BrightLMS on demand.
2.	Quickly view and analyze property information within a user-friendly admin interface.
3.	Manage local data efficiently with built-in truncation and cleanup tools.


## Deployment

The system can be deployed using Docker or on a bare-metal Windows server.

### Common Requirements

The following steps are common for all deployment methods:

1. Clone the https://github.com/slobodadev/hagan_realty repository from the main branch.
2. Review your BrightLMS API credentials and ensure they are up-to-date.
3. Copy .env.example to .env and fill in the variables:
   - BRIGHT_MLS_CLIENT_ID - BrightMLS client ID.
   - BRIGHT_MLS_CLIENT_SECRET - BrightMLS client secret.

Next steps will be different depending on the deployment method. If you are linux/macos user, you can use Docker. If you are a Windows user, you can deploy the application using virtual environment setup.


### Using Docker (for linux/macos users only)

You need to have installed Docker and Docker-compose on your machine.

After installing Docker and Docker-compose, you need to change some Docker settings:
1. Open Docker Desktop
2. Go to Settings
3. Go to Resources
4. Set CPU, Memory and Swap to the values you need (it totaly depends on your machine)
5. Disable ResourceSaver
6. Apply and restart Docker Desktop

#### Run

Local development is done with docker-compose.
1. Run `docker-compose up -d --build`
2. Run `docker-compose exec web python manage.py migrate`
3. To access adminpanel, run `docker-compose exec web python manage.py createsuperuser` and fill in the required fields
4. Open http://localhost:8000 in your browser

#### Stop

To stop the project, run `docker-compose down`

#### Start if stopped

To start the project after it was already build once and just stopped, run `docker-compose up -d`

#### Run commands

To run any command in the container, you need to run the following command:
`docker-compose exec web python manage.py <command>`

For example, to run the `python manage.py migrate` command, you need to run the following command:
`docker-compose exec web python manage.py migrate`


### Using Virtual Environment (for Windows users)

There are some limitations to running Docker on Windows. It is an issue with docker-volumes and file permissions for PostgreSQL data. Therefore, it is recommended to use a virtual environment for Windows users.

To run the application on Windows, you need to install software:
1. Python 3.8 or higher
2. PostgreSQL 13 or higher

After installing the required software, follow these steps (from the root of the project):
1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment: `.venv\Scripts\activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser` and fill in the required fields
6. Run the local server: `python manage.py runserver` to access the application at http://localhost:8000

If you need to access local server and run some commands at the same time, you can open a new terminal and run the following command:
1. Go to the root of the project
2. Activate the virtual environment: `.venv\Scripts\activate`
3. Run the command: `python manage.py <command>`

                              
## Usage

### Populating the DB

For populating the DB the `mls_grab` command is used. It takes several positional arguments:
* `entity` - the entity to grab data from. Example: `python manage.py mls_grab BrightProperties`. This is a required argument.
* `limit` - the number of records to grab at one iteration. Example: `python manage.py mls_grab BrightProperties 100`. This is an optional argument. Default value is 10000.
* `last_pk` - the primary key of the record grabbed last time. Grabbing will start from the next record after this one. Example: `python manage.py mls_grab BrightProperties 100 2264400012`. This is an optional argument. Default tries to allocate the last PK from the DB and start from the next one. So any time you run the command, it will start from the next record after the last one grabbed, you do not need to specify this argument without special needs.

To populate the database with the data from the BrightMLS API, run the following commands:

1. `python manage.py mls_grab BrightMedia 5000` (each record is too big, so we need to limit the number of records to grab at one iteration) 	
1. `python manage.py mls_grab BrightMembers` 	
1. `python manage.py mls_grab BrightOffices` 	
1. `python manage.py mls_grab BrightOpenHouses` 	
1. `python manage.py mls_grab BrightProperties 2500` (each record is too big, so we need to limit the number of records to grab at one iteration) 	
1. `python manage.py mls_grab BuildingName` 	
1. `python manage.py mls_grab City` 	
1. `python manage.py mls_grab CityZipCode` 	
1. `python manage.py mls_grab Deletion` 	
1. `python manage.py mls_grab GreenVerification` 	
1. `python manage.py mls_grab History` 	
1. `python manage.py mls_grab Lookup` 	
1. `python manage.py mls_grab PartyPermissions` 	
1. `python manage.py mls_grab PropertyArea` 	
1. `python manage.py mls_grab RelatedLookup` 	
1. `python manage.py mls_grab Room` 	
1. `python manage.py mls_grab School` 	
1. `python manage.py mls_grab SchoolDistrict` 	
1. `python manage.py mls_grab Subdivision` 	
1. `python manage.py mls_grab SysAgentMedia` 	
1. `python manage.py mls_grab SysOfficeMedia` 	
1. `python manage.py mls_grab SysPartyLicense` 	
1. `python manage.py mls_grab Team` 	
1. `python manage.py mls_grab TeamMember` 	
1. `python manage.py mls_grab Unit` (this entity is not working properly, so it will not return the whole dataset)	

The inserting process is configuring to skip already existing records with the same PK. So, if you run the command again, it will not insert the duplicated records.

### Truncating the DB tables

To truncate the DB tables, run the following command:

`python manage.py mls_truncate <EntityName>` where `<EntityName>` is the name of the entity to truncate. 
Example: `python manage.py mls_truncate BrightProperties`

This will clear the table of the specified entity.


### Changing the structure of the DB

Please, do not change the structure of the DB using raw SQL queries. Use Django migrations instead.
You will get the problems with data compatibility if you change the structure of the DB using raw SQL queries 
and apply any Django migration after that.

If you need add some indexes or constraints, please, create a new migration using Django migrations. 
Refer to:
1. Django official documentation: https://docs.djangoproject.com/en/5.1/ref/models/indexes/ 
2. Or Quick howto: https://clouddevs.com/django/apply-custom-database-indexes/

## Logs

### For Docker setup:

To see logs of the web project, run `docker-compose logs -f` in the root of the project
       
### For Windows 

You can see logs in corresponding terminal windows. 

## Database

### Backup
Go to `/tmp/dumps` directory (it is volume mapped to the `dumps` directory in the root of the project)

Run the following command: 
`docker-compose exec db pg_dump -Z2 -Fc -t 'brightmls_*' --data-only --username=local_dbuser --host=localhost local_db > 2024-10-29.sql`

This will create a dump of all tables of brightmls app, but WITHOUT the schema. INSERT statements will be used to restore the data.


### Restore
To restore the database:

Put the dump file to your local `/dumps` directory in the root of the project (it is volume mapped to the `/tmp/dumps` directory in the container)

Run the following command:
`docker-compose exec db pg_restore --data-only --username=local_dbuser --host=localhost --dbname=local_db /tmp/dumps/2024-10-29.sql`

Beware, the dump file have to contain only the data, not the schema. Otherwise, the restore will fail.


## Found issues

### Metadata

There are some properties not existing in the odata Metadata ($metadata) of the BrightMLS API.
You have no access to the following entities:

1. BuilderModel
2. BusinessHistoryDeletions
3. LisBusinessHistory
4. ListingSubscription
5. PartyProfileOption

### Data retrieval

There are some problems with the data retrieval from the BrightMLS API.

1. Unit: parsing fails with the following error: `requests.exceptions.JSONDecodeError: Expecting ':' delimiter: line 1 column 15994 (char 15993)`

### Filtering

The API does not provide the complete filtering functionality described in the documentation.
* In some cases, the filtering/ordering does not work as expected.
* In some cases, the filtering/ordering does not work at all and returns connection timeout.
* In some cases, the filtering/ordering produce very slow responses (2-5 minutes).

### Pagination

The API provide two types of pagination: limit/offset and $skiptoken.

We can not use limit/offset pagination, because it is not working properly on large datasets (History, BrightProperties).
That is why the pagination is implemented using the $skiptoken Header parameter and nextLink URL.
This approach is straightforward, but it is not efficient for large datasets because of not using parallel requests.

### Counting

Total count of records is unknown for large datasets (History, BrightProperties). We can get the count of records only for some specific filterings. 