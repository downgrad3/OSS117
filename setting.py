#!/usr/bin/env python
# -*- coding: utf-8 -*
import configparser
import os

# todo: voir si je peux pas faire ca par défaut, ie le code detecte la classe et en fct de la classe met le log où il faut
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOOT_DIR = os.path.join(PROJECT_DIR, 'loot')
MODULE_DIR = os.path.join(PROJECT_DIR, 'modules')
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
TESTS_DIR = os.path.join(PROJECT_DIR, 'tests')

COLLECTORS_DIR = os.path.join(PROJECT_DIR, 'collectors')
CORE_DIR = os.path.join(PROJECT_DIR, 'core')
INFERORS_DIR = os.path.join(PROJECT_DIR, 'inferors')
EVALUATORS_DIR = os.path.join(PROJECT_DIR, 'evaluators')

LOGS_COLLECTORS_DIR = os.path.join(LOG_DIR, 'collectors')
LOGS_CORE_DIR = os.path.join(LOG_DIR, 'core')
LOGS_INFERORS_DIR = os.path.join(LOG_DIR, 'inferors')
LOGS_EVALUATORS_DIR = os.path.join(LOG_DIR, 'evaluators')

# Reading the configuration from file
config = configparser.ConfigParser()
config.read(os.path.join(PROJECT_DIR, 'config.ini'))
