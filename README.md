# Hagan Realty monolith app

## Architecture

Project is designed as a Django-admin application for Hagan Realty internal usage.
It uses PostgreSQL as a database

## Pre-requirements

### Docker

You need to have installed Docker and Docker-compose on your machine.

After installing Docker and Docker-compose, you need to change some Docker settings:
1. Open Docker Desktop
2. Go to Settings
3. Go to Resources
4. Set CPU, Memory and Swap to the values you need (it totaly depends on your machine)
5. Disable ResourceSaver
6. Apply and restart Docker Desktop

### BrightMLS API

Also you need to have prepaid BrightMLS API account


# Local deployment

## Installation

Local development is done with docker-compose.
1. Clone the repository
2. Copy .env.example to .env and fill in the variables
4. Run `docker-compose up -d --build`
5. Run `docker-compose exec web python manage.py migrate`
6. To access adminpanel, run `docker-compose exec ft_web python manage.py createsuperuser` and fill in the required fields
7. Open http://localhost:8000 in your browser

                              
## Usage

### Populating the DB

For populating the DB the `mls_grab` command is used. It takes several positional arguments:
* `entity` - the entity to grab data from. Example: `python manage.py mls_grab BrightProperties`. This is a required argument.
* `limit` - the number of records to grab at one iteration. Example: `python manage.py mls_grab BrightProperties 100`. This is an optional argument. Default value is 10000.
* `offset` - the number of records to skip. Example: `python manage.py mls_grab BrightProperties 1000 22000`. This is an optional argument. Default value is 0 to start from the beginning.
* `stop` - the number of records to stop at. Example: `python manage.py mls_grab BrightProperties 1000 22000 100000`. This is an optional argument. Default value is None to stop at the end of the data.

This command runs in 20 threads. That means that it will grab `20 * limit` records at a time. And then next `20 * limit` and so on in the cycle until the `stop` argument is reached or the end of the data is reached.

To populate the database with the data from the BrightMLS API, run the following commands:

1. `docker-compose exec web python manage.py mls_grab BrightMedia 5000` (each record is too big, so we need to limit the number of records to grab at one iteration) 	
1. `docker-compose exec web python manage.py mls_grab BrightMembers` 	
1. `docker-compose exec web python manage.py mls_grab BrightOffices` 	
1. `docker-compose exec web python manage.py mls_grab BrightOpenHouses` 	
1. `docker-compose exec web python manage.py mls_grab BrightProperties 2500` (each record is too big, so we need to limit the number of records to grab at one iteration) 	
1. `docker-compose exec web python manage.py mls_grab BuildingName` 	
1. `docker-compose exec web python manage.py mls_grab City` 	
1. `docker-compose exec web python manage.py mls_grab CityZipCode` 	
1. `docker-compose exec web python manage.py mls_grab Deletion` 	
1. `docker-compose exec web python manage.py mls_grab GreenVerification` 	
1. `docker-compose exec web python manage.py mls_grab History` 	
1. `docker-compose exec web python manage.py mls_grab Lookup` 	
1. `docker-compose exec web python manage.py mls_grab PartyPermissions` 	
1. `docker-compose exec web python manage.py mls_grab PropertyArea` 	
1. `docker-compose exec web python manage.py mls_grab RelatedLookup` 	
1. `docker-compose exec web python manage.py mls_grab Room` 	
1. `docker-compose exec web python manage.py mls_grab School` 	
1. `docker-compose exec web python manage.py mls_grab SchoolDistrict` 	
1. `docker-compose exec web python manage.py mls_grab Subdivision` 	
1. `docker-compose exec web python manage.py mls_grab SysAgentMedia` 	
1. `docker-compose exec web python manage.py mls_grab SysOfficeMedia` 	
1. `docker-compose exec web python manage.py mls_grab SysPartyLicense` 	
1. `docker-compose exec web python manage.py mls_grab Team` 	
1. `docker-compose exec web python manage.py mls_grab TeamMember` 	
1. `docker-compose exec web python manage.py mls_grab Unit` (this entity is not working properly, so it will not return the whole dataset)	


### Truncating the DB tables

To truncate the DB tables, run the following command:

`docker-compose exec web python manage.py mls_truncate <EntityName>` where `<EntityName>` is the name of the entity to truncate. 
Example: `docker-compose exec web python manage.py mls_truncate BrightProperties`

This will clear the table of the specified entity.

### Updating the data

This section is not finished yet... 


## Logs

To see logs of the web project, run `docker-compose logs -f` in the root of the project
       

## Database

### Backup
Go to `/tmp/dumps` directory (it is volume mapped to the `dumps` directory in the root of the project)

Run the following command: 
`docker-compose exec db pg_dump -Fc --data-only --username=local_dbuser --host=localhost local_db > 2024-10-29.sql`

This will create a dump of all tables but WITHOUT the schema. INSERT statements will be used to restore the data.


### Restore
To restore the database:

Put the dump file to your local `/dumps` directory in the root of the project (it is volume mapped to the `/tmp/dumps` directory in the container)

Run the following command:
`docker-compose exec db psql -U local_dbuser -h localhost -d local_db < "/tmp/dumps/2024-10-29.sql"`

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
2. Room: do not respond on any request (connection timeout)
3. Some tables like `History` are not responding on the request after some big offset.

### Filtering

The API does not provide the complete filtering functionality described in the documentation.
In some cases, the filtering/ordering does not work as expected.
In some cases, the filtering/ordering does not work at all and returns connection timeout.