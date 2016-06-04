# -*- coding: UTF-8 -*-


class AppInfo (object):
    """
    Common for OutWiker and plug-ins items.

    Added in OutWiker 2.0.0.795.
    """
    def __init__(self,
                 appname,
                 author,
                 versionsList=[],
                 description=u"",
                 appwebsite=u"",
                 updatesUrl=u""):
        """
        appname - application or plug-in name.
        author - author info. It is instance of the AuthorInfo class.
        versionsList - information about every version.
                       It is a instance of the VersionInfo class.
        description - application's or plug-in's description.
        appwebsite - application or plug-in web site.
        updatesUrl - URL to XML file with updates information.
        """
        self.appname = appname
        self.author = author
        self.versionsList = versionsList[:]
        self.description = description
        self.appwebsite = appwebsite
        self.updatesUrl = updatesUrl


class AuthorInfo (object):
    """
    Information about plug-in's author
    """
    def __init__(self, name=u"", email=u"", website=u""):
        self.name = name
        self.email = email
        self.website = website


class VersionInfo (object):
    """
    Information about single version (version, change log, URL to download)
    """
    def __init__(self, version, date_str=u"", downloads={}, changes=[], hidden=False):
        """
        version   - instance of the Version class.
        date_str  - release date (string)
        downloads - dict with downloads links
                      (key - OS (name from the System class), value - URL)
        changes   - list of the string with changes in current version.
        hidden    - hide this version to users?
        """
        self.version = version
        self.date_str = date_str
        self.downloads = download.copy()
        self.changes = changes[:]
        self.hidden = hidden
