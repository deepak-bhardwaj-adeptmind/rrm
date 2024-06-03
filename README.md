# rrm(Room Rate Management)

## About
Helps in setting up:
- Room Rates
- Overridden Room Rates
- Discounts
- Room Discounts
- Getting the minimum prices for a particular room in a given date range

## Getting started 
Clone the project and jump into project directory(`cd rrm`). Assuming you have `virtualenv` with python3.9 available.
- Run `make init`. 
- Run `make start`

The project will be accessible on http://127.0.0.1:8000/api/

### Database use:
The project uses `sqlite` database by default but you can switch to use `MySQL` database by:
- enabling the commented `MySQL` DATABASE settings in the settings.py file.
- running the MySQL database server on the same port as is mentioned in the settings.
 


