#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

import wx

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from .guiconfig import TrayConfig, GeneralGuiConfig
from .mainid import MainId


class OutwikerTrayIcon (wx.TaskBarIcon):
    """
    Класс для работы с иконкой в трее
    """
    def __init__ (self, mainWnd):
        wx.TaskBarIcon.__init__ (self)
        self.mainWnd = mainWnd
        self.config = TrayConfig (Application.config)

        self.ID_RESTORE = wx.NewId()
        self.ID_EXIT = wx.NewId()

        self.icon = wx.Icon(os.path.join (outwiker.core.system.getImagesDir(), "outwiker_16x16.png"), wx.BITMAP_TYPE_ANY)

        self.__bind()

        self.__initMainWnd()
        self.updateTrayIcon()
    

    def updateTrayIcon (self):
        """
        Показать или скрыть иконку в трее в зависимости от настроек
        """
        if self.config.alwaysShowTrayIcon.value:
            # Если установлена эта опция, то иконку показываем всегда
            self.ShowTrayIcon()
            return

        if self.config.minimizeToTray.value and self.mainWnd.IsIconized():
            self.ShowTrayIcon()
        else:
            self.removeTrayIcon()
    

    def __bind (self):
        self.Bind (wx.EVT_TASKBAR_LEFT_DOWN, self.__OnTrayLeftClick)
        self.mainWnd.Bind (wx.EVT_ICONIZE, self.__onIconize)
        self.mainWnd.Bind (wx.EVT_CLOSE, self.__onClose)
        self.mainWnd.Bind (wx.EVT_MENU, self.__onExit, id=MainId.ID_EXIT)

        self.Bind(wx.EVT_MENU, self.__onExit, id=self.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.__onRestore, id=self.ID_RESTORE)

        Application.onPreferencesDialogClose += self.__onPreferencesDialogClose
    

    def __unbind (self):
        self.Unbind (wx.EVT_TASKBAR_LEFT_DOWN, handler = self.__OnTrayLeftClick)
        self.mainWnd.Unbind (wx.EVT_ICONIZE, handler = self.__onIconize)
        self.mainWnd.Unbind (wx.EVT_CLOSE, handler=self.__onClose)
        self.mainWnd.Unbind (wx.EVT_MENU, handler=self.__onExit, id=MainId.ID_EXIT)

        self.Unbind(wx.EVT_MENU, handler = self.__onExit, id=self.ID_EXIT)
        self.Unbind(wx.EVT_MENU, handler = self.__onRestore, id=self.ID_RESTORE)

        Application.onPreferencesDialogClose -= self.__onPreferencesDialogClose


    def __onClose (self, event):
        if self.config.minimizeOnClose.value:
            self.mainWnd.Iconize(True)
            event.Veto()
            return

        if (self.__allowExit()):
            self.mainWnd.Destroy()
        else:
            event.Veto()


    def __allowExit (self):
        """
        Возвращает True, если можно закрывать окно
        """
        generalConfig = GeneralGuiConfig (Application.config)
        askBeforeExit = generalConfig.askBeforeExit.value

        return (not askBeforeExit or 
                outwiker.core.commands.MessageBox (_(u"Really exit?"), 
                    _(u"Exit"), 
                    wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES )
    

    def __onPreferencesDialogClose (self, prefDialog):
        self.updateTrayIcon()


    def __initMainWnd (self):
        if self.config.startIconized.value:
            self.mainWnd.Iconize (True)
        else:
            self.mainWnd.Show()
    

    def __onIconize (self, event):
        if event.Iconized():
            # Окно свернули
            self.__iconizeWindow ()
        else:
            self.restoreWindow()

        self.updateTrayIcon()
    

    def __iconizeWindow (self):
        """
        Свернуть окно
        """
        if self.config.minimizeToTray.value:
            # В трей добавим иконку, а окно спрячем
            self.ShowTrayIcon()
            self.mainWnd.Hide()


    def removeTrayIcon (self):
        """
        Удалить иконку из трея
        """
        if self.IsIconInstalled():
            self.RemoveIcon()


    def __onRestore (self, event):
        self.restoreWindow()


    def __OnTrayLeftClick (self, event):
        if self.mainWnd.IsIconized():
            self.restoreWindow()
        else:
            self.mainWnd.Iconize()
    

    def restoreWindow (self):
        self.mainWnd.Iconize (False)
        self.mainWnd.Show ()
        if not self.config.alwaysShowTrayIcon.value:
            self.removeTrayIcon()
        self.mainWnd.Raise()
        self.mainWnd.SetFocus()

    
    def __onExit (self, event):
        if (self.__allowExit()):
            self.mainWnd.Destroy()


    def CreatePopupMenu (self):
        trayMenu = wx.Menu()
        trayMenu.Append (self.ID_RESTORE, _(u"Restore"))
        trayMenu.Append (self.ID_EXIT, _(u"Exit"))

        Application.onTrayPopupMenu (trayMenu, self)

        return trayMenu


    def Destroy (self):
        self.removeTrayIcon()
        self.__unbind()
        super (OutwikerTrayIcon, self).Destroy()


    def ShowTrayIcon (self):
        if not self.IsIconInstalled():
            self.SetIcon(self.icon)
