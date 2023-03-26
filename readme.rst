=====
Leaky
=====

Djang application to show security flaws.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "leaky" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'leaky',
    ]

2. Include the leaky URLconf in your project urls.py like this::

    path('leaky/', include('leaky.urls')),

3. Run ``python manage.py migrate`` to create the leaky models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to participate in the poll.