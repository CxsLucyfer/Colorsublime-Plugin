from .downloader_base import DownloaderBase
from ... import logger
log = logger.get(__name__)
import traceback
from urllib import request, error


try:
    import ssl
    SSL = True
except ImportError:
    SSL = False


class UrllibDownloader(DownloaderBase):
    """Downloader that uses the native Python HTTP library.
    WARNING: Does not verify HTTPS certificates."""

    @staticmethod
    def is_available():
        return SSL

    def get(self, url):
        # Proxy support
        request.install_opener(request.build_opener(request.ProxyHandler()))
        try:
            log.debug('Urllib downloader getting url %s', url)
            result = request.urlopen(url)
        except error.URLError as e:
            log.error('Urllib downloader failed: %s' % e.reason)
            raise e
        if result.getcode() >= 400:
            log.error('Urllib downloader failed with code: %s' % result.getcode())
            return b''
        return result.read()
