# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Aug 12 17:58:35 2010

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class OverwriteDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: OverwriteDialog.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.textLabel = wx.StaticText(self, -1, "Overwrite file?", style=wx.ALIGN_CENTRE)
		self.overwrite = wx.Button(self, -1, "Overwrite")
		self.overwriteAll = wx.Button(self, -1, "Overwrite all")
		self.button_1 = wx.Button(self, -1, "Skip")
		self.skipAll = wx.Button(self, -1, "Skip all")
		self.cancel = wx.Button(self, -1, "Cancel")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.onOverwrite, self.overwrite)
		self.Bind(wx.EVT_BUTTON, self.onOverwriteAll, self.overwriteAll)
		self.Bind(wx.EVT_BUTTON, self.onSkip, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.onSkipAll, self.skipAll)
		self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancel)
		# end wxGlade

		self.ID_OVERWRITE = 1
		self.ID_SKIP = 2

		# Флаг, который сохраняет выбор пользователя, 
		# чтобы не показывать диалог после выбора "... all"
		self.flag = 0


	def __set_properties(self):
		# begin wxGlade: OverwriteDialog.__set_properties
		self.SetTitle("Overwrite Files")
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: OverwriteDialog.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(self.textLabel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 4)
		sizer_2.Add(self.overwrite, 0, wx.ALL, 2)
		sizer_2.Add(self.overwriteAll, 0, wx.ALL, 2)
		sizer_2.Add(self.button_1, 0, wx.ALL, 2)
		sizer_2.Add(self.skipAll, 0, wx.ALL, 2)
		sizer_2.Add(self.cancel, 0, wx.ALL, 2)
		sizer_1.Add(sizer_2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.Layout()
		# end wxGlade
	

	def ShowDialog (self, text):
		"""
		Показать диалог, если нужно спросить, что делать с файлов.
		Этот метод вызывается вместо Show/ShowModal.
		text - текст для сообщения в диалоге
		"""
		if self.flag == 0:
			self.textLabel.SetLabel (text)
			return self.ShowModal()

		return self.flag


	def onOverwrite(self, event): # wxGlade: OverwriteDialog.<event_handler>
		self.EndModal (self.ID_OVERWRITE)


	def onOverwriteAll(self, event): # wxGlade: OverwriteDialog.<event_handler>
		self.flag = self.ID_OVERWRITE
		self.EndModal (self.ID_OVERWRITE)

	
	def onSkip(self, event): # wxGlade: OverwriteDialog.<event_handler>
		self.EndModal (self.ID_SKIP)

	
	def onSkipAll(self, event): # wxGlade: OverwriteDialog.<event_handler>
		self.flag = self.ID_SKIP
		self.EndModal (self.ID_SKIP)

	
	def onCancel(self, event): # wxGlade: OverwriteDialog.<event_handler>
		self.EndModal (wx.ID_CANCEL)

# end of class OverwriteDialog


