## About

This git repo is about a swiss knife like tool agglomerate for using vereinsflieger.de.
It's designed for club administrators faced with the task to manage dataset like user
access or supporting club accounting. For me its a private python project allowing me
to test architecture patterns and new language patterns of python.

As first module [bulk_edit](bulk_edit/) supports you with a bulk editing functionality that was for me painfully missing in the web GUI of vereinsflieger. The usecase behind is some batch like setting of dataset values. In past I was faced with the some task where I need to change the user status of lets say 150 members. I don't want todo this manually one by one. Approx. one year ago I started this with a hacky solution of screenshot based mouse and keyboard automation (google sikuli for further info). That was working but is highly machine dependent. In a different context i found a (in my eyes) more stable way using the webgui testing tool [selenium](https://en.wikipedia.org/wiki/Selenium_(software)).

## IMPORTANT NOTE

Please use the tool **bulk_edit** with care and at your own risk!!! 

The tool is under development. The file [`bulk_edit/__main__.py`](bulk_edit/__main__.py) currenlty implements the construction of tasks to perfom in a hard coded way! Modify it for your use case. **Run the script only if you know what you are doing!**

## Requirements

Downloading data requires:

1. Firefox to be installed in your machine
2. Geckodriver executable in your PATH.
   * Get latest release from https://github.com/mozilla/geckodriver/releases
   * Setup your PATH environment variable.

## Setup Dev Environment

The setup is very simple. All dependencies are defined in the [requirements.txt].
I suggest to use the python virtual environment:

```shell
# create virtual environment
python -m venv env
# install dependencies
pip install -r requirements.txt
# Thats all.
```

I used vscode as IDE. Thus take a look at [.vscode/launch.json] for program entrie
points for starting/debugging.

If you are using a different IDE (or like to start the program from command line),
please start the program as module (using the `python -m` option).

**!Before starting the program please read the [IMPORTANT NOTE] above!**

```shell
# Start programm by
python -m bulk_edit
```
