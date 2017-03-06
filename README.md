# The Dojo

This is an open source console application that help users manage the allocation of rooms. This application allows the creation of two types of person which are `staff` and `fellow`. Both staff and fellow can be randomly allocated to an office when available while only a fellow can be alloacted to a livingspace on request. The state of each application can be saved to and loaded from a database. The application is written in python and uses docopt framework to give the user an interactive user experience.

## Installation

These are the basic steps to install and run the application locally;

### Install necessary packages

Install python 3 on the system.

#### On a linux system

On the terminal, run the commands below;
```
$ sudo apt-get install python3-dev
$ pip install virtualenv
```

#### On a windows system

Download [Python 3 `exe` file](https://www.python.org/downloads/release/python-360/) and run the file.
Open the commandline (cmd) and run the command;
`pip install virtualenv`

### Download the project

On the commandline/terminal, run the command;
```
git clone https://github.com/andela-aolasode/The-Dojo.git
cd The-Dojo

virtualenv --python=python3 venv-dojo
source venv-dojo/bin/activate

pip install -r requirements.txt
```

### Run the application

While still inside The-Dojo folder, run `nosetests` to check the testcases and run `python thedojo.py` to actually use the application.

## Built With

* [Docopt](http://docopt.org/) - A console framework that define the interface for a command-line app, and automatically generate a parser for it.
* [Nose](https://pypi.python.org/pypi/nose/1.3.7) - The python framework that extends the test loading and running features of unittest, making it easier to write, find and run tests.
* [Termcolor](https://pypi.python.org/pypi/termcolor) - This is a python framework for ANSII Color formatting for output in terminal.
* [Pyfiglet](https://pypi.python.org/pypi/pyfiglet) - This is a full port of FIGlet (http://www.figlet.org/) into pure python. It takes ASCII text and renders it in ASCII art fonts

## Authors

* **Olasode Adeyemi Abdul-Mumeen** - *Software Developer at Andela*

## Acknowledgments

* Thanks to my facilitator **Njira Perci** and my wonderful **Pygo Teammates**
