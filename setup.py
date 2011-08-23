from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-dataforms',
    version=__import__('dataforms').__version__,
    description='Dynamic, database-driven Django forms',
    long_description=open('README.rst').read(),
    author='Jay McEntire',
    author_email='jay.mcentire@gmail.com',
    url='http://github.com/django-dataforms/django-dataforms',
    download_url='https://github.com/django-dataforms/django-dataforms/downloads',
    license='GNU GPL v3',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)