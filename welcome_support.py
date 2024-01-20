#! /usr/bin/env python
#
# Copyright 2023 BredOS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gettext
import logging
import os
from os import path
from time import sleep, monotonic
from pathlib import Path
from threading import Lock
from functools import wraps
from traceback import print_exception
from datetime import datetime
from pyrunning import LoggingHandler, Command, LogMessage
# from pysetting import JSONConfiguration

def setup_translations(lang: object = None) -> gettext.GNUTranslations:
    """
    Setup translations

        Does the following:
        - Loads the translations from the locale folder
        - Sets the translations for the gettext module

        Returns:  A gettext translation object
        :rtype: object
    """
    lang_path = path.join(path.dirname(__file__), "locale")
    # Load translations
    if lang is not None:
        gettext.bindtextdomain("bakery", lang_path)
        gettext.textdomain("bakery")
        translation = gettext.translation("bakery", lang_path, languages=[lang])
        translation.install()
        return translation.gettext  # type: ignore
    else:
        gettext.bindtextdomain("bakery", lang_path)
        gettext.textdomain("bakery")
        return gettext.gettext  # type: ignore


def setup_logging() -> logging.Logger:
    """
    Setup logging

        Does the following:
        - Creates a logger with a name
        - Sets the format for the logs
        - Sets up logging to a file and future console
    """

    logger = logging.getLogger("bredos-welcome")
    logger.setLevel(logging.DEBUG)

    log_dir = os.path.join(os.path.expanduser("~"), ".bredos", "welcome", "logs")
    log_file = os.path.join(
        log_dir, datetime.now().strftime("WELCOME-%Y-%m-%d-%H-%M-%S.log")
    )
    try:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.isdir(log_dir):
            raise FileNotFoundError("The directory {} does not exist".format(log_dir))
        # get write perms
        elif not os.access(log_dir, os.W_OK):
            raise PermissionError(
                "You do not have permission to write to {}".format(log_dir)
            )
    except Exception as e:
        print_exception(type(e), e, e.__traceback__)
        exit(1)

    print("Logging to:", log_file)

    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.DEBUG)
    log_file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)8s] %(message)s",
    )
    log_file_handler.setFormatter(log_file_formatter)
    logger.addHandler(log_file_handler)

    log_error_handler = logging.StreamHandler()
    log_error_handler.setLevel(logging.INFO)
    log_error_formatter = logging.Formatter("%(levelname)8s: %(message)s")
    log_error_handler.setFormatter(log_error_formatter)
    logger.addHandler(log_error_handler)
    return logger

print("Starting logger..")
logger = setup_logging()
logging_handler = LoggingHandler(
    logger=logger,
)

def lp(message, write_to_f=True, mode="info") -> None:
    if not write_to_f:
        LogMessage.Info(message)
    elif mode == "info":
        LogMessage.Info(message).write(logging_handler=logging_handler)
    elif mode == "debug":
        LogMessage.Debug(message).write(logging_handler=logging_handler)
    elif mode == "warn":
        LogMessage.Warning(message).write(logging_handler=logging_handler)
    elif mode == "crit":
        LogMessage.Critical(message).write(logging_handler=logging_handler)
    elif mode == "error":
        LogMessage.Error(message).write(logging_handler=logging_handler)
    elif mode == "exception":
        LogMessage.Exception(message).write(logging_handler=logging_handler)
    else:
        raise ValueError("Invalid mode.")
    
def lrun(cmd: list) -> None:
    Command(cmd).run_log_and_wait(logging_handler=logging_handler)

def create_settings_file(settings) -> None:
        settings.parents[0].mkdir(parents=True, exist_ok=True)
        os.chmod(settings.parents[0], 0o755)
        lrun(["cp", str(path.join(path.dirname(__file__), "data", "settings", "settings.json")), str(settings)])
        os.chmod(settings, 0o666)

# def get_settings() -> JSONConfiguration:
#     """
#     Get the settings from the settings file

#         Does the following:
#         - Checks if the settings file exists
#         - If not, creates it
#         - If it does, loads the settings from it

#         Returns:  A JSONConfiguration object
#         :rtype: object
#     """
#     settings = Path(
#         os.path.expanduser("~"), ".bredos", "welcome", "settings", "settings.json"
#     )
#     if not settings.exists():
#         lp("Settings file does not exist. Creating..")
#         create_settings_file(settings)
#     return JSONConfiguration(settings)
    
lp("Logger started.")
lp("Setting up translations..")
_ = setup_translations()
lp("Translations setup.")
# lp("Getting settings..")
# settings = get_settings()
# lp("Settings loaded.")
# print(settings)



# Gui support functions


def debounce(wait):
    """
    Decorator that will postpone a function's
    execution until after wait seconds
    have elapsed since the last time it was invoked.
    """

    def decorator(func):
        last_time_called = 0
        lock = Lock()

        @wraps(func)
        def debounced(*args, **kwargs):
            nonlocal last_time_called
            with lock:
                elapsed = monotonic() - last_time_called
                remaining = wait - elapsed
                if remaining <= 0:
                    last_time_called = monotonic()
                    return func(*args, **kwargs)
                else:
                    return None

        return debounced

    return decorator
