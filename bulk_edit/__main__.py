from bulk_edit import tasks, log, TaskExecutor
# TODO we need to import all from comunity in order to load class by string from globals()
#      (not nice but working)
from bulk_edit.tasks.community import *
from bulk_edit.tasks.task_base import Task, print_subclass
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import argparse
import logging
from typing import Dict, List
logger = logging.getLogger(__name__)


def get_input_from_cli():
    parser = argparse.ArgumentParser(prog='bulk_edit',
                                     description='Doing bulk edit jobs for vereinsflieger.de')

    parser.add_argument('action', choices=['list', 'run'],
                        help='Action to perform')
    parser.add_argument('task_name', default='*',
                        help='task name to run / list. Use * to list all task\'s.')
    parser.add_argument('task_parameter', nargs='*', default=[],
                        help='parameter for task (syntax: name=value)')
    parser.add_argument('--uidFile', type=str, dest='uid_file_name',
                        help='If specified the task will be repeated with parameter `uid`s read '
                             'from file (one uid per line)')
    parser.add_argument('-v', '--silent', action='store_true', default=False)
    parser.add_argument('-o', '--keepOpen', action='store_true', default=False)
    parser.add_argument('--credentialFile', type=str,
                        help=('A simple text file with content the following content.\n'
                              'first line: user name\n'
                              'second line: password'))

    options = parser.parse_args()

    return options


if __name__ == '__main__':
    driver = None
    batchProcess = None
    closeDriver = True
    try:
        log.load_config()
        options = get_input_from_cli()
        closeDriver = not options.keepOpen

        if options.action == 'list':
            print('\nAvailable tasks:\n')
            print_subclass(Task, options.task_name)
            exit(0)

        def parse_parameters(params: List[str]) -> dict:
            parameters: Dict[str, str] = {}

            for param in params:
                try:
                    tokens = str(param).split('=')
                    parameters[tokens[0]] = tokens[1]
                except Exception as ex:
                    raise Exception(f"Unexpected parameter format '{param}'. It "
                                    "might be 'name=value'.") from ex
            return parameters

        parameters = parse_parameters(options.task_parameter)

        def parse_className(className: str) -> type:
            try:
                return globals()[className]
            except Exception as ex:
                raise Exception(f"Unexpected Task '{className}'. Call action `list` to show "
                                "available Tasks.") from ex

        task_t = parse_className(options.task_name)

        def generate_webdriver(headless: bool) -> webdriver:
            profile = webdriver.FirefoxProfile()
            options = Options()
            # this line starts FF in headless mode
            options.headless = headless
            return webdriver.Firefox(firefox_profile=profile, options=options)

        driver = generate_webdriver(options.silent)

        # read uid from user input or from file
        taskList = []
        try:
            if options.uid_file_name:
                # check if uid is specified explicit
                if 'uid' in parameters:
                    logger.warning("Option `--uidFile` and `uid` is specified. `uid` will be "
                                "discarded. Instead uids from file will be read.")
                    del parameters['uid']

                with open(options.uid_file_name, "r") as f:
                    line = f.readline()
                    while line:
                        # prepare task
                        task = task_t(driver=driver, uid=int(line), **parameters)
                        taskList.append(task)
                        # makes this loop a for each line
                        line = f.readline()

            else:
                task = task_t(driver=driver, **parameters)
                taskList.append(task)
        except TypeError as ex:
            logger.error(f"Task creation failed with message '{ex}'.\n"
                         "Check if you specified all parameters!")
            exit(1)

        # execute list
        loginParams = {}
        if options.credentialFile:
            loginParams['credentialFile'] = options.credentialFile
        login = tasks.LoginToVf(driver, **loginParams)
        login.execute()

        batchProcess = TaskExecutor()
        # executes all tasks
        batchProcess.execute(taskList)

    except KeyboardInterrupt:
        logger.info("User interrupted")

    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
        exit(1)

    finally:
        if batchProcess:
            batchProcess.log_summary(logger)
        if closeDriver and driver:
            driver.close()