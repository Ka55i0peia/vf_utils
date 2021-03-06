## About

This git repo is about a swiss knife like tool collection for using [vereinsflieger.de](https://vereinsflieger.de/).
It is addresses vereinsflieger administrators faced to the task of managing datasets on this plattform (like user access management, supporting club accounting and generating statistics). For me its a private project allowing me to apply architecture and new language patterns of python next of supporting my flight club [aeroclub prina](https://www.aeroclub-pirna.de).

## Content

### bulk_edit

As first module [bulk_edit](bulk_edit/) supports you with a batch-like editing function for the painfully missing "bulk edit" functionality in the web gui of vereinsflieger (like known from JIRA). The usecase is the automatisation of "monkey edits" in the platform.

   Examples   
   * Change user status (e.g. in case of flight weeks by guests)
   * Grant (new) user permissions
   * Toggle flight permission ("Flugfreigabe")
   * Applying custom properties ("Mitgliedereigenschaften")
   * Updating flight accounting properties ("Abrechnungsart")

*In past* I was faced with this task where I need to change hundreds of datasets. I don't want todo this manually one by one. Approx. one year ago I started this idea based on [sikuli](https://de.wikipedia.org/wiki/Sikuli_(Software)) (a nice java tool for screenshot based mouse and keyboard automation). Because its screenshot based it is highly machine dependent. Thus this tool was hard to share/maintain among others.

*bulk_edit* does this automatisation job referencing DOM elements of the webpage within the browser engine using the library [selenium](https://en.wikipedia.org/wiki/Selenium_(software)).

#### IMPORTANT NOTE

**_Please use the tool `bulk_edit` with care and at your own risk!_**

The file [`bulk_edit/__main__.py`](bulk_edit/__main__.py) at the current stage of development contains hard coded the task preparation. See todo notes in source. Modify this file for your use case! **Run the script only if you know what you are doing!**

## Requirements

[Selenium](https://www.seleniumhq.org/) uses an browser on your machine. I used it with Firefox. So next to the dependencies specified in [`requirements.txt`](requirements.txt), you need the following on your machine:

For Selenium and FF:

1. Firefox installed
2. Geckodriver
   1. Get latest release from https://github.com/mozilla/geckodriver/releases
   2. Add the geckodriver executable to your `PATH` environment variable.

## Setup Dev Environment

The setup is pythonic simple. All dependencies are defined in the [`requirements.txt`](requirements.txt). I recommend to use the [python virtual environment](https://docs.python.org/3/library/venv.html):

```shell
# create virtual environment in folder env
python -m venv env
# install dependencies
pip install -r requirements.txt
```

I used [vscode](https://code.visualstudio.com/) as IDE. So take a look at [`.vscode/launch.json`](.vscode/launch.json) for program entry points for starting or debugging.

If you are using a different IDE (or like to start the program from command line),
please start the program as module (using the `python -m` option).

**!Before starting `bulk_edit` please read the [IMPORTANT NOTE] above!**

```shell
# Start program by calling the module
python -m bulk_edit
```
