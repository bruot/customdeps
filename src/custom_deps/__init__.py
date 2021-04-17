#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the CustomDeps software, a Python module to help
# loading modules from Git repositories checked out to specific commits.
#
# Copyright 2018, 2021 Nicolas Bruot (https://www.bruot.org/hp/)
#
#
# custom_deps is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# custom_deps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with custom_deps.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import shutil
import importlib.util
import appdirs
import configparser
import git


def _is_sha1(s):
    """Returns True if string is a SHA1 hash in lower case"""

    if s.lower() != s:
        return False
    if len(s) != 40:
        return False
    try:
        int(s, 16)
    except ValueError:
        return False
    return True


class GitRepos(object):
    """Maintains a set of Git repositories checked out at various heads"""

    @staticmethod
    def _set_default(config_sec, key, val):
        """Set key to the given default value if it does not already exist"""

        try:
            config_sec[key]
        except KeyError:
            config_sec[key] = val
            return True
        return False


    def __init__(self):
        self._config = None


    def _local_repo_path(self, local_name):
        """Returns the expanded path to a local dev repository"""

        full_path = os.path.join(self.config['dev_dir'], local_name)
        return os.path.expanduser(full_path)


    def _local_snapshot_path(self, local_name, commit):
        """Returns the expanded path to a local snapshot repository"""

        full_path = os.path.join(self.config['snaps_dir'],
                                 local_name,
                                 commit)
        return os.path.expanduser(full_path)


    @property
    def config(self):
        """Returns the config file dat parsed as a dict"""

        if self._config is None:
            directory = appdirs.user_config_dir('CustomDeps')
            filename = 'config'
            path = os.path.join(directory, filename)

            cp = configparser.ConfigParser()
            cp.read(path)
            default = cp['DEFAULT']
            default_params = (
                    ('dev_dir', appdirs.user_data_dir('CustomDeps/dev')), # (key, val)
                    ('snaps_dir', appdirs.user_data_dir('CustomDeps/snaps')),
                    )
            if any([self._set_default(default, k, v) for k, v in default_params]):
                # Config file has been edited with new default values
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                with open(path, 'w') as f:
                    cp.write(f)
            self._config = dict(default)
        return self._config


    def add(self, clone_url, local_name):
        """Adds a dev repository"""

        git.Repo.clone_from(clone_url, self._local_repo_path(local_name))


    def insert_path(self, local_name, commit, inner_rel_path=''):
        """Inserts an import path based on a specific commit"""

        if not _is_sha1(commit):
            raise ValueError('Commit specifier should be a full length SHA1 lower case string.')

        snaps_path = self._local_snapshot_path(local_name, commit)
        if not os.path.isdir(snaps_path):
            dev_path = self._local_repo_path(local_name)
            repo = git.Repo(dev_path)
            repo.remote().pull()
            snaps_repo = git.Repo.clone_from(dev_path, snaps_path)
            try:
                snaps_repo.git.checkout(commit)
            except git.GitCommandError:
                shutil.rmtree(snaps_path)
                raise

        py_path = os.path.join(snaps_path, inner_rel_path)
        if not os.path.isdir(py_path):
            raise ValueError('The inner path "%s" does not exist.' % inner_rel_path)
        sys.path.insert(0, py_path)
