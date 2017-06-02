# AirlineSeatsAllocatingProject

Suppose you work for an airline, and your job is to write software algorithm to allocate seats when passengers
make bookings. For each fight, you'll be given the seating configuration of the plane. Then as bookings
come in, your job will be to allocate the seats to the passengers. Each booking will be for one or more
passengers, and naturally bookings of multiple passengers should be allocated seats together where possible.
The bookings will be provided in a CSV file where each line consists of one integer representing the
number of passengers in the party and one name, the name of the person making the booking. You should
allocate all seats for the booking in that name. You have to allocate the seats for one booking before looking
at the next booking (i.e. the next line).
A database file will be provided representing the seating plan of the aircraft, the empty and occupied
seats. After each booking you must update the database with the allocation you have made.
When a booking can be accommodated, you should allocate the seats -- together if possible, but split
up if necessary. When a booking cannot be accommodated at all, because there are too few free seats, you
should not allocate seats.
After each booking has been processed (either allocated or refused) you must also update two metrics in
the database:

1> a number representing how many passengers have been refused outright (this is total passengers, not
number of bookings that have been refused);

2> and a number representing how many passengers are seated away from any other member of their
party.

Fields for these metrics will already be present in the database.
Your program should be structured into multiple functions as appropriate.
Your program must include appropriate comments and tests for individual functions.
A sample database and sample bookings file are available. You should inspect these to understand their
structure and format. Your program will be tested against other files in the same formats.
