#  Wingz Python/Django Developer Test

Create a RESTful API using Django REST Framework for managing ride information.

### Main features

* CRUD for model Ride, User, and RideEvent
* Ride List API:
    * sorting by pickup_time and distance to pickup given a GPS position
    * filtering result by ride status and rider email‬
    * showing related ride events for the last 24 hours


# Getting Started
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver


### API endpoints
 * /api/users/
 * /api/rides/
 * /api/ride-events/

For distance-related sorting, `lat` and `lng` should be provided as query parameters in the URL.

    /api/rides/?lat=14&lng=120&ordering=distance


# Bonus - SQL
    select month, driver, count(*) as total_rides
                from (
                    select strftime('%Y-%m', ride.pickup_time) as month, 
                            driver.first_name as driver,
                            (JULIANDAY(dropoff_event.created_at) - JULIANDAY(pickup_event.created_at)) * 24 * 60 as duration
                    from rides_ride as ride
                    inner join users_user as driver on ride.driver_id = driver.id
                    left join rides_rideevent as pickup_event on pickup_event.ride_id = ride.id and pickup_event.description like 'Status changed to pickup'
                    left join rides_rideevent as dropoff_event on dropoff_event.ride_id = ride.id and dropoff_event.description like 'Status changed to dropoff' 
                    where duration >= 60
                    order by ride.pickup_time asc
                ) as rides_durations
                group by month, driver;
