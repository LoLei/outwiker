# -*- coding: utf-8 -*-

# Плагин для вставки свернутого текста

import os.path

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .guicontroller import GUIController


def _no_translate(text):
    return text


class PluginSpoiler(Plugin):
    """
    Плагин, добавляющий обработку команды spoiler в википарсер
    """
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)
        self._controller = Controller(application)
        self._GUIController = GUIController(application)

    def initialize(self):
        self._initlocale(u"spoiler")
        self._controller.initialize()
        self._GUIController.initialize()

    def _initlocale(self, domain):
        from .i18n import set_
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException as e:
            print(e)
            _ = _no_translate

        set_(_)

    @property
    def name(self):
        return u"Spoiler"

    @property
    def description(self):
        return _(u"""Add (:spoiler:) wiki command to parser.

<B>Usage:</B>
<PRE>(:spoiler:)
Text
(:spoilerend:)</PRE>

For nested spoilers use (:spoiler0:), (:spoiler1:)...(:spoiler9:) commands. 

<U>Example:</U>

<PRE>(:spoiler:)
Text
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Nested spoiler
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Params:</B>
<U>inline</U> - Spoiler will be in inline mode.
<U>expandtext</U> - Link text for the collapsed spoiler. Default: "Expand".
<U>collapsetext</U> - Link text for the expanded spoiler. Default: "Collapse".

<U>Example:</U>

<PRE>(:spoiler expandtext="More..." collapsetext="Less" inline :)
Text
(:spoilerend:)</PRE>
""")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/SpoilerEn")

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий и удалить свои кнопки,
        пункты меню и т.п.
        """
        self._controller.destroy()
        self._GUIController.destroy()