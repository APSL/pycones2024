from configparser import ConfigParser, NoOptionError


class Config:
    _config: ConfigParser

    def __init__(self, configfile: str = "app.ini", local_configfile: str = "app.local.ini"):
        self._config = ConfigParser()
        self._config.read([configfile, local_configfile])

    def get(self, section: str, key: str, default=None):
        res = self._get("getint", section, key)
        if res is not None:
            return res  # int
        res = self._get("getfloat", section, key)
        if res is not None:
            return res  # float
        res = self._get("getboolean", section, key)
        if res is not None:
            return res  # boolean

        try:
            value = self._config.get(section, key)
            if self._is_none(value):
                return None
            return self._get_list_or_string(value)
        except IndexError:
            pass
        except NoOptionError as ex:
            if default is None:
                raise ex
            return default

        raise Exception

    @staticmethod
    def _get_list_or_string(value):
        """Try to cast to list the string, otherwise gets the string value"""
        if "[" in value and "]" in value:
            left = value.index("[") + 1
            right = value.index("]")
            return [x.strip() for x in value[left:right].split(",")]  # list
        return value  # string

    @staticmethod
    def _is_none(value):
        """Checks if value is `"None"`"""
        return value == "None"

    def _get(self, getter, section, key):
        try:
            return getattr(self._config, getter)(section, key)
        except Exception:  # noqa
            pass
