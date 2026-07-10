#!/usr/bin/env python3

import inspect
import logging
import re
from collections.abc import Callable

from . import FilterType

LOGGER = logging.getLogger(__name__)

# CONSTANT
secret_keys = "pass|secret|token|salt"
secret_keys = f"{secret_keys}|{secret_keys.upper()}|pwd"
# Avoid to match some non relevant var compound with 'key'
secret_keys_regex = (
    f"(?:\\w|-)*(?:{secret_keys})\\w*|local key_?| key\\w*|\\w(?:\\w|-)*key\\w*|\\w*KEY\\w+|\\w+KEY"
)
operator_regex = "(?:\\s+\\-\\-value)?['\"]?\\s*(?:=|:|=>)\\s*"
value_regex = "'(?:[^']|'\\''){5,}'|\\S{5,}"
redact_regex = (
    f"({secret_keys_regex})"
    f"{operator_regex}"
    "(?:'?-----BEGIN [A-Z]+ '?KEY-----)?"
    f"({value_regex})"
    "(?:'?-----END'? [A-Z]+ KEY-----'?)?"
)
redact_regex = re.compile(redact_regex)
exclude_keys = [
    "manifest_key",
    "bind_key_",
    "local key",
    "local key_",
    "version_key",
    "version_key_",
    "cache_key",
    "foreign_key",
    "primary_key",
    "keys_zone",
    "meta_keywords",
    "csrf_token",
    "jsonwebtoken",
    "MYSQL_ROOT_PWD_FILE",
    "SALTCORN_BIN",
    "tls_passthrough_module",
    "translation_key",
    "tokenizer",
    "teampass",
    "misskeycalckeylibxcb-keysyms1",
]
exclude_keys_suffixes = (
    "_uri",
    "_url",
    "_path",
    "_key_expires",
    "_key_expires_date",
    "_enabled",
    "_algorithm",
    "_class",
    "file",
)
exclude_values = (
    "**********",
    "true",
    "false",
    "value",
    "value1",
    "value2",
    "value3",
    "version",
    "unbound variable",
    "db_pwd",
    "disabled",
    "enabled",
    "lambda",
    "by_order",
    r"\k\w+",
    "(generate_random_password)",
)


def find_data_to_redact_in_line(line: str) -> str | None:
    line = re.sub(r"^\d+-\d+-\d+ \d+:\d+:\d+,\d+: (DEBUG|ERROR|WARN(ING)?|INFO) - ", "", line)

    line = line.strip()
    if (match := re.search(redact_regex, line)) is None:
        return None

    redact_key, redact_value = match.group(1, 2)
    redact_key = redact_key.strip().removeprefix("--")
    redact_value = redact_value.strip().strip("\"'{}$,").removeprefix("base64:")

    if line.strip(" +").startswith(("POST_data=", "curl --silent")) or " --args '" in line:
        redact_value = redact_value.split("&")[0]

    redacting_tests: list[Callable[[str, str], bool]] = [
        # Empty string
        lambda key, value: value == "",
        # Some keys are false positive and should not be redacted
        lambda key, value: key in exclude_keys,
        # Keys that end ups by uri, url or path are just path and not secret
        lambda key, value: key.lower().endswith(exclude_keys_suffixes),
        # Python venv build could display some false positive library
        # like passlib or tokenizer
        # example: 'Collecting tokenizers==0.19.1'
        lambda key, value: line.strip(" +").startswith(
            ("Created serverSetting through seed key", "getent passwd ")
        ),
        # Python venv build could display some false positive library
        # like passlib or tokenizer
        # example: 'Collecting tokenizers==0.19.1'
        lambda key, value: (
            line.strip().startswith(("Collecting ", "Requirement already satisfied"))
            and value.startswith("=")
        ),
        # Some values are clearly vars or function call
        lambda key, value: value.lower() in (*exclude_values, key.lower(), key.upper()),
        # key='https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x0C54D189F4BA284D'
        # key=https://artifacts.elastic.co/GPG-KEY-elasticsearch
        # key=https://download.docker.com/linux/debian/gpg
        lambda key, value: (
            key == "key"
            and value.strip("'").startswith(
                ("https://", "--key=https://", "http://", "--key=http://")
            )
        ),
        lambda key, value: key == "pwd_output" and value.startswith("/var/cache/yunohost/"),
        lambda key, value: key == "ynh_key" and value.startswith("/etc/yunohost/certs"),
        lambda key, value: key == "ssh_keys" and "/etc/ssh/ssh_host_" in value,
        lambda key, value: key == "public_key" and value.startswith("ssh-"),
        lambda key, value: key == "AUTH_KEYS" and value == "/root/.ssh/authorized_keys",
        lambda key, value: key == "password" and "--password= --database=" in line,
    ]

    for test in redacting_tests:
        if test(redact_key, redact_value):
            i = inspect.getsource(test).index("\n")
            j = inspect.getsource(test).rindex(":", 0, i)
            testbody = inspect.getsource(test)[j + 1 :].strip().strip(",")
            LOGGER.debug("Redacting found %s, %s, but test excluded it:", redact_key, redact_value)
            LOGGER.debug(" %s ", testbody)
            return None

    # Synapse displayed strings like this difficult to catch properly
    # macaroon_secret_key_param='macaroon_secret_key: "*******"'
    # if key == "macaroon_secret_key_param":
    #     to_replace = "macaroon_secret_key_param='macaroon_secret_key: "
    #     value = value.replace(to_replace, '').strip('"')

    return redact_value


class Filter(FilterType):
    def fill(self, file: str) -> None:
        self.data = file

    def acceptable(self) -> bool:
        return True

    def _find_data_to_redact(self) -> list[str]:
        data_to_redact = []
        for line in self.data.splitlines():
            data = find_data_to_redact_in_line(line)
            if data and data not in data_to_redact:
                LOGGER.debug("Found data to redact: '%s'", data)
                data_to_redact.append(data)
        return data_to_redact

    def _redact(self) -> None:
        for data in self._find_data_to_redact():
            # we check that data is not empty string,
            # otherwise this may lead to super epic stuff
            # (try to run "foo".replace("", "bar"))
            if data:
                self.data = self.data.replace(data, "**********")
                # bash set -x display comparison like this: [[ ohno != \o\h\n\o ]]
                self.data = self.data.replace("\\" + "\\".join(data), "**********")

    def filtered(self) -> str:
        self._redact()
        return self.data
