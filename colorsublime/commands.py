"""
Collection of functions the plugin can invoke. Most if not all should be
non-blocking (@runasync) functions to keep the main UI thread from freezing.

These functions should catch all unexpected exceptions so the plugin does not
have to. Unexpected exceptions should return False. Expected exceptions should
be caught by other modules this module uses. Log all unusual behavior.

All @runasync functions have an optional callback parameter as the last argument.
"""
import os

from . import logger
from . import settings
from . import http
from . import io
from .asynclib import runasync
from .theme import Theme

log = logger.get(__name__)


def get_current_theme():
    return settings.get_current_theme()


def get_installed_themes():
    theme_filenames = os.listdir(settings.install_path())
    themes = []

    for t in theme_filenames:
        if t.endswith('.tmTheme'):
            name = t.replace('.tmTheme', '')
            themes.append(Theme(name=name, file_name=t))

    themes.sort()
    return themes


@runasync
def fetch_repo():
    """ Get current theme archive in a new thread """
    archive = http.get(settings.repo_url())
    io.extract(archive, settings.cache_path())
    themes_list = io.read_json(settings.themes_list_path())
    themes = [Theme.from_json(theme) for theme in themes_list]
    themes = {t.name: t for t in themes}
    return themes


def _exists(theme):
    if not os.path.exists(theme.cache_path.abs):
        log.error('Path %s not found!', theme.cache_path.abs)
        return False
    return True


def preview_theme(theme):
    log.debug('Previewing theme %s at %s', theme.name, theme.cache_path.abs)

    if not _exists(theme):
        return

    settings.set_theme(theme.cache_path.rel)


def install_theme(theme):
    log.debug('Installing theme %s to %s', theme.name, theme.install_path.abs)

    if not _exists(theme):
        return

    io.copy(theme.cache_path.abs, theme.install_path.abs)
    settings.commit_theme(theme.install_path.rel)

def revert_theme(path):
    log.debug('Reverting theme at path %s', path)
    settings.set_theme(path)


def uninstall_theme(theme):
    os.remove(theme.install_path.abs)
