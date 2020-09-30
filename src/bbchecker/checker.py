#!/usr/bin/env python

# -*- coding: utf-8 -*-

import json
import random
import subprocess
from configparser import ConfigParser
from datetime import datetime
from typing import Union

import requests

from .formatting import *


class CheckerError(Exception):

    def __init__(self, title, details: Union[str, list] = ''):
        self.title = title
        self.details = details

    def __repr__(self) -> str:
        return f"{self.title} --> {self.str_details}"

    def telegram(self) -> str:
        return f'[<i>python checker</i>] {bold(self.title)}\n{self.str_details}'

    @property
    def str_details(self) -> str:
        if type(self.details) == list:
            return "\n".join(self.details)
        else:
            return str(self.details)


class Checker:

    def __init__(self, config: ConfigParser):
        self.config = config
        self.base_url = config['bbdata'].get('url')

        # setup requests headers and auth
        self.session = requests.Session()
        self.session.auth = ( config['bbdata'].get('bbuser'),  config['bbdata'].get('bbtoken'))

        headers = {
            'Content-Type': 'application/json',
            'accepts': 'application/json',
        }
        hostname =  config['bbdata'].get('hostname', '').strip()
        if len(hostname) > 0:
            headers['hostname'] = hostname
        self.session.headers.update(headers)

        self.session.verify = self.config['bbdata'].getboolean('verify', len(hostname) == 0)

        if self.base_url.endswith('/'):
            self.base_url = self.base_url[0:-1]

    def is_api_reachable(self):
        # check overall api
        try:
            r = self.session.get(f'{self.base_url}/about')
            if r.status_code != 200:
                raise CheckerError('API', [f'got status code {r.status_code}', f'upon querying {pre(r.url)}'])
        except requests.exceptions.ConnectionError:
            raise CheckerError('API unreachable', [f'using base URL {pre(self.base_url)}'])

    def is_flink_running(self):
        if self.config.has_option('flink', 'script'):
            script = self.config.get('flink', 'script')
            try:
                res = subprocess.run([script, 'list'], stdout=subprocess.PIPE)
                output = res.stdout.decode('utf-8')

                if res.returncode != 0:
                    raise CheckerError(f'flink', [f'{script} returned exit code {res.returncode}', pre(output)])

                jobs = output.splitlines()
                if len(jobs) != 2:
                    raise CheckerError('flink', [f'expecting two running jobs, got {len(jobs)}', pre(output)])

            except FileNotFoundError as e:
                raise CheckerError(f'flink', ['invalid script file (<i>not found</i>)', pre(script)])

    def is_ingestion_working(self):
        oid, ts = self.config.get('input', 'object_id'), datetime.utcnow().isoformat()

        # create measure
        measure = dict(
            objectId=oid,
            value=random.randint(0, 500),
            token=self.config.get('input', 'token'),
            timestamp=ts,
            comment='bbchecker'
        )
        # submit measure
        r = self.session.post(f'{self.base_url}/objects/values', json=[measure])

        if r.status_code != 200:
            raise CheckerError(
                "new measure submission failed",
                ["measure:", pre(json.dumps(measure)), "answer:", pre(r.text)])

        # get measure
        r = self.session.get(f'{self.base_url}/objects/{oid}/values', params={'from': ts, 'to': ts})

        if r.status_code != 200:
            raise CheckerError(f'new measure GET failed with status code {r.status_code}', pre(r.text))
        elif len(r.json()) != 1:
            raise CheckerError(f'new measure GET failed: {len(r.json())} measure for timestamp {ts}')
