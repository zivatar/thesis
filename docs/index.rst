Appendix I -- Code documentation
********************************

Generated from the docstrings of the Django application with Sphinx

Standalone classes
==================

.. automodule:: climate.classes.BadRequestException
   :members:

.. automodule:: climate.classes.Climate
   :members:

.. automodule:: climate.classes.Weather
   :members:

.. automodule:: climate.classes.Gravatar
   :members:

.. automodule:: climate.classes.Month
   :members:

.. automodule:: climate.classes.Year
   :members:

.. automodule:: climate.classes.Report
   :members:

.. automodule:: climate.classes.MonthlyReport
   :members:

.. automodule:: climate.classes.YearlyReport
   :members:

Unit tests
----------

Django files
============

Models
------

.. automodule:: climate.models.Site
   :members:

.. automodule:: climate.models.Instrument
   :members:

.. automodule:: climate.models.UnprocessedData
   :members:

.. automodule:: climate.models.RawManualData
   :members:

.. automodule:: climate.models.RawData
   :members:

.. automodule:: climate.models.RawObservation
   :members:

.. automodule:: climate.models.DailyStatistics
   :members:

.. automodule:: climate.models.MonthlyStatistics
   :members:

.. automodule:: climate.models.YearlyStatistics
   :members:

.. automodule:: climate.models.Profile
   :members:

Views
-----

.. automodule:: climate.views.climate
   :members:

.. automodule:: climate.views.delete_instrument
   :members:

.. automodule:: climate.views.delete_site_image
   :members:

.. automodule:: climate.views.edit_site
   :members:

.. automodule:: climate.views.edit_user
   :members:

.. automodule:: climate.views.edit_users
   :members:

.. automodule:: climate.views.guide
   :members:

.. automodule:: climate.views.instrument_details
   :members:

.. automodule:: climate.views.main
   :members:

.. automodule:: climate.views.monthly_report
   :members:

.. automodule:: climate.views.my_instrument_list
   :members:

.. automodule:: climate.views.my_site_list
   :members:

.. automodule:: climate.views.my_user
   :members:

.. automodule:: climate.views.new_instrument
   :members:

.. automodule:: climate.views.new_observation
   :members:

.. automodule:: climate.views.new_site
   :members:

.. automodule:: climate.views.observations
   :members:

.. automodule:: climate.views.public_site_list
   :members:

.. automodule:: climate.views.register
   :members:

.. automodule:: climate.views.site_details
   :members:

.. automodule:: climate.views.upload_data
   :members:

.. automodule:: climate.views.UploadClimateHandler
   :members:

.. automodule:: climate.views.UploadHandler
   :members:

.. automodule:: climate.views.yearly_report
   :members:

Templates
---------

``/climate``

Files of the web app excluding user handling
(registration, login and reset password templates are in ``/registration``).
Each .html file depends on base.html.

* climate.html
* edit_user.html
* edit_users.html
* guide.html
* instrument_details.html
* instrument_list.html
* main.html
* monthly_view.html
* my_sites.html
* my_user.html
* new_instrument.html
* new_site.html
* site_details.html
* site_edit.html
* site_list.html
* site_observations.html
* upload.html
* yearly_view.html

``/registration``

Template files of user handling.

* login.html
* password_reset.html
* password_reset_complete.html
* password_reset_confirm.html
* password_reset_done.html
* signup.html

Forms
-----

.. automodule:: climate.forms
   :members:

Other files
-----------

.. automodule:: climate.utils
   :members:


.. toctree::
   :maxdepth: 2
   :caption: Contents:


