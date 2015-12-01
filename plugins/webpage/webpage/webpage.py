# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller


if getCurrentVersion() < Version (1, 9, 0, 781, status=StatusSet.DEV):
    print ("TestPage plugin. OutWiker version requirement: 1.9.0.781")
else:
    class PluginWebPage (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super (PluginWebPage, self).__init__ (application)
            self.__controller = Controller(self, self._application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################
        @property
        def name (self):
            return u"WebPage"


        @property
        def description (self):
            return _(u"Download HTML pages from web")


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/WebPageEn")


        def initialize(self):
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################