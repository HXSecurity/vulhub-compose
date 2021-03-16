#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午5:50
# project: vulhub-compose
import functools
import logging
import sys

from compose.cli.colors import AnsiMode
from compose.cli.docopt_command import DocoptDispatcher
from compose.cli.errors import UserError
from compose.cli.main import setup_logging, TopLevelCommand, setup_console_handler, setup_parallel_logger, \
    perform_command
from compose.cli.utils import get_version_info

log = logging.getLogger(__name__)


def dispatch(*args, **kwargs):
    console_stream = sys.stderr
    console_handler = logging.StreamHandler(console_stream)
    setup_logging(console_handler)
    dispatcher = DocoptDispatcher(
        TopLevelCommand,
        {'options_first': True, 'version': get_version_info('compose')})

    options, handler, command_options = dispatcher.parse(*args)

    ansi_mode = AnsiMode.AUTO
    try:
        if options.get("--ansi"):
            ansi_mode = AnsiMode(options.get("--ansi"))
    except ValueError:
        raise UserError(
            'Invalid value for --ansi: {}. Expected one of {}.'.format(
                options.get("--ansi"),
                ', '.join(m.value for m in AnsiMode)
            )
        )
    if options.get("--no-ansi"):
        if options.get("--ansi"):
            raise UserError("--no-ansi and --ansi cannot be combined.")
        log.warning('--no-ansi option is deprecated and will be removed in future versions.')
        ansi_mode = AnsiMode.NEVER

    setup_console_handler(console_handler,
                          options.get('--verbose'),
                          ansi_mode.use_ansi_codes(console_handler.stream),
                          options.get("--log-level"))
    setup_parallel_logger(ansi_mode)
    if ansi_mode is AnsiMode.NEVER:
        command_options['--no-color'] = True
    return functools.partial(perform_command, options, handler, command_options)
