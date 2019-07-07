# -*- coding: utf-8 -*-
'''
Classes to recognize href URI for HtmlRenders
'''

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Union

import idna


class Recognizer(metaclass=ABCMeta):
    '''
    Base class for all recognizers
    '''

    def recognize(self, href: Union[str, None]) -> Union[str, None]:
        if href is None:
            return None

        href = self._prepareHref(href)
        return self._recognize(href)

    def _prepareHref(self, href: str) -> str:
        # WebKit appends 'file://' string to end of URI without protocol.
        href = self._removeFileProtokol(href)
        href = href.replace('\\', '/')
        return href

    def _removeFileProtokol(self, href):
        """
        Remove 'file://' protocol
        """
        fileprotocol = u"file://"
        if href.startswith(fileprotocol):
            return href[len(fileprotocol):]

        return href

    @abstractmethod
    def _recognize(self, href: str) -> str:
        pass


# URL recognizer
class URLRecognizer(Recognizer):
    '''
    Recognize internet URL
    '''

    def _prepareHref(self, href: str) -> str:
        return href

    def _recognize(self, href: str) -> str:
        isUrl = (href.lower().startswith("http:") or
                 href.lower().startswith("https:") or
                 href.lower().startswith("ftp:") or
                 href.lower().startswith("mailto:"))

        return href if isUrl else None


# Anchor recognizers

class AnchorRecognizerBase(Recognizer):
    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognizeAnchor(self, href: str, basepath: str) -> Union[str, None]:
        anchor = None
        if (href.startswith(basepath) and
                len(href) > len(basepath) and
                href[len(basepath)] == "#"):
            anchor = href[len(basepath):]
        else:
            pos = href.rfind("/#")
            if pos != -1:
                anchor = href[pos + 1:]

        return anchor


class AnchorRecognizerIE(AnchorRecognizerBase):
    '''
    Recognize an anchor in href.
    For Internet Explorer engine.
    '''

    def _removeAnchor(self, basepath: str) -> str:
        basepath_processed = basepath.replace('\\', '/')
        last_slash_pos = basepath.rfind('/')
        if last_slash_pos == -1:
            return basepath

        sharp_pos = basepath_processed.rfind('#')
        if sharp_pos > last_slash_pos:
            return basepath[:sharp_pos]

        return basepath

    def _recognize(self, href: str) -> str:
        basepath = self._basepath.replace('\\', '/')
        if href.startswith('/'):
            href = href[1:]

        # Remove anchor from basepath
        basepath = self._removeAnchor(basepath)

        return self._recognizeAnchor(href, basepath)


class AnchorRecognizerWebKit(AnchorRecognizerBase):
    '''
    Recognize an anchor in href.
    For WebKit engine.
    '''

    def _recognize(self, href: str) -> Union[str, None]:
        basepath = self._basepath
        if not basepath.endswith('/'):
            basepath += '/'

        return self._recognizeAnchor(href, basepath)


# File recognizers

class FileRecognizerBase(Recognizer):
    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognize(self, href: str) -> Union[str, None]:
        return self._recognizeFile(href, self._basepath)

    def _recognizeFile(self, href: str, basepath: str) -> Union[str, None]:
        try:
            href_path_abs = Path(href)
            # Check absolute path
            if href_path_abs.exists():
                return str(href_path_abs.resolve())

            # Check relative path
            basepath = Path(basepath)
            if basepath.is_file():
                basepath = basepath.parent

            href_path_relative = Path(basepath, href)
            if href_path_relative.exists():
                return str(href_path_relative.resolve())
        except OSError:
            return None


class FileRecognizerIE(FileRecognizerBase):
    pass


class FileRecognizerWebKit(FileRecognizerBase):
    pass


# Page recognizers

class PageRecognizerBase(Recognizer, metaclass=ABCMeta):
    def __init__(self, basepath: str, application):
        self._basepath = basepath
        self._application = application

    @abstractmethod
    def _findPageByPath(self, href: str):
        pass

    def _findPageByProtocol(self, href: str):
        """
        Find page by href like page://..
        """
        protocol = u"page://"
        page = None

        # Если есть якорь, то отсечем его
        anchorpos = href.rfind("/#")
        if anchorpos != -1:
            href = href[:anchorpos]

        if href.startswith(protocol):
            uid = href[len(protocol):]

            try:
                uid = idna.decode(uid)
            except UnicodeError:
                # With Internet Explorer will be thrown UnicodeError exception
                pass

            if uid.endswith("/"):
                uid = uid[:-1]

            page = (self._application.pageUidDepot[uid] or
                    self._application.selectedPage[uid] or
                    self._application.wikiroot[uid])

        return page

    def _recognize(self, href: str) -> str:
        page = (self._findPageByProtocol(href) or
                self._findPageByPath(href))
        return page


class PageRecognizerWebKit(PageRecognizerBase):
    def _findPageByPath(self, href: str):
        currentPage = self._application.selectedPage

        if currentPage is None:
            return None

        if href.startswith(self._basepath):
            href = href[len(self._basepath):]
            if href.startswith('/'):
                href = href[1:]

        if len(href) == 0:
            return None

        newSelectedPage = None

        if href[0] == "/":
            if href.startswith(currentPage.root.path):
                href = href[len(currentPage.root.path):]

            if len(href) > 1 and href.endswith("/"):
                href = href[:-1]

        if href[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = currentPage.root[href[1:]]
        else:
            # Сначала попробуем найти вложенные страницы с таким href
            newSelectedPage = currentPage[href]

            if newSelectedPage is None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = currentPage.root[href]

        return newSelectedPage


class PageRecognizerIE(PageRecognizerBase):
    def _findPageByPath(self, href: str):
        return None
