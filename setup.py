from setuptools import setup, find_packages

setup(
    name="django-notifications",
    #url = "http://github.com/dgarciavicente/django-notifications/",
    author="Diana Garcia Vicente",
    author_email="dianagv@gmail.com",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    description="Event Notifications for Django",
    install_requires=['django>=1.6.1', 'celery>=3.1.4'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],

)
