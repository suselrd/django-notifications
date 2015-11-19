==========================
Django Event Notifications
==========================

Event Notifications for Django>=1.6.1

Allows to configure (using django admin, or system settings, or even decorating notifying functions)
all the notification system.

Changelog
=========

0.2.1
-----
- Added logging functionality where exceptions are silenced.

0.2.0
-----
- Auto-configuring notification system from django settings.
- notifier() decorator, for functions that mainly are for calling 'create_event' function.
They only have to return the 'create_event' necessary arguments, and the decorator make the call for them.
The decorator also configures the pertinent part of the notification system, if the necessary objects don't exist yet.

0.1.6
-----
-Adding the possibility of sending "immediate" notifications (no celery involved)
-Added possibility of using transports that do not allow subscription configuration

0.1.5
-----
-Fixing issues with no attendants transport
-Improved administration

0.1.4
-----
-Added public feed transport. Adapted tasks for supporting it

0.1.3
-----
-Fix Feed transport issue with single context

0.1.2
-----
-Fix in tasks multi-site behaviour.

0.1.1
-----
-Fix in Multisite behaviour.

0.1.0
-----
-Added Multisite support for feed items.

0.0.2
-----
-Added Default Subscription configuration functionality
-Added Event Type Category model

0.0.1
-----

PENDING...

Notes
-----

PENDING...

Usage
-----

1. Run ``python setup.py install`` to install.

2. Modify your Django settings to use ``notifications``:

3. Configure notifications settings using admin.

