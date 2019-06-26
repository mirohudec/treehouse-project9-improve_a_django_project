# Improve a Django Project

## TreeHouse project 9

### Instructions:

We spent a weekend doing a hackathon a year or so ago and someone built this project. It's...not the best. It runs kind of slow and has been a real pain to debug and add onto. We need you to go through the project, find where it's inefficient, and fix it. Check the templates for bad inheritance and extra database calls. Check the views for extra views or extra database calls. Check the models to make sure they're using the best fields. Check the forms for proper validation and fields. Basically just check the whole thing over. Oh, and it doesn't have any tests, so please get test coverage up to at least 75%.

### Comments

- Replaced requirements with pipenv
- Upgraded django-debug-toolbar to 2.0 and django to 2.2
- longest query takes 20ms in form to load all items - could use choices(run only once) instead of queryset, but then it doesnt update if items are added
- added layout to templates
- in menu_list i replaced timezone.now with timedelta of -6 years to see items because most of the items expired in 2019
- Going for Exceed Expectations
