This package makes it possible to run a Jupyter python kernel in the Django development web server process (`manage.py runserver`).


## Usage

Add this package to `INSTALLED_APPS`. The package also supplies a mixin class that can be used to add the `--kernel` argument to an existing `runserver` management command class.


`manage.py runserver --kernel`
