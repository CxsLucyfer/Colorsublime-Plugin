"""
Global settings module
By @blopker
"""
import sublime

plugin_name = 'Colorsublime'

PLUGIN_PREF = plugin_name + '.sublime-settings'
SUBLIME_PREF = 'Preferences.sublime-settings'
REPO_MASTER = 'Colorsublime-Themes-master'


def get(*args):
    return sublime.load_settings(PLUGIN_PREF).get(*args)


def repo_url():
    return get('repo_url')


def cache_path():
    return sublime.packages_path() + '/' + get('cache_path')


def repo_path():
    return sublime.packages_path() + '/' + get('cache_path') + '/' + REPO_MASTER


def themes_list_path():
    return repo_path() + '/themes.json'


def install_path():
    return sublime.packages_path() + '/' + get('install_path')


def packages_path():
    return sublime.packages_path()


def get_current_theme():
    return sublime.load_settings(SUBLIME_PREF).get('color_scheme', '')


def set_theme(path):
    return sublime.load_settings(SUBLIME_PREF).set('color_scheme', path)


def commit_theme(path):
    def callback():
        set_theme(path)
        sublime.save_settings(SUBLIME_PREF)
    # Timeout so sublime can get caught up with the filesystem
    sublime.set_timeout_async(callback, 1000)


def is_debug():
    return get('debug')


def is_windows():
    return sublime.platform() == 'windows'
