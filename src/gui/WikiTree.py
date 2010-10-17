# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Apr 05 21:59:12 2010

import os
import ConfigParser

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

from core.controller import Controller
import core.exceptions
import core.commands
import core.system


class WikiTree(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: WikiTree.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.treeCtrl = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_LINES_AT_ROOT|wx.TR_EDIT_LABELS|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.ID_ADD_CHILD = wx.NewId()
		self.ID_ADD_SIBLING = wx.NewId()
		self.ID_RENAME = wx.NewId()
		self.ID_REMOVE = wx.NewId()
		self.ID_PROPERTIES = wx.NewId()
		
		self.ID_COPY_PATH = wx.NewId()
		self.ID_COPY_ATTACH_PATH = wx.NewId()
		self.ID_COPY_TITLE = wx.NewId()
		self.ID_COPY_LINK = wx.NewId()

		self.defaultIcon = os.path.join (core.system.getImagesDir(), "page.png")
		self.iconHeight = 16

		self.defaultBitmap = wx.Bitmap (self.defaultIcon)
		assert self.defaultBitmap.IsOk()
		
		self.defaultBitmap.SetHeight (self.iconHeight)

		self.dragItem = None
	
		# Картинки для дерева
		self.imagelist = wx.ImageList(16, self.iconHeight)
		self.treeCtrl.AssignImageList (self.imagelist)

		# Кеш для страниц, чтобы было проще искать элемент дерева по странице
		# Словарь. Ключ - страница, значение - элемент дерева wx.TreeItemId
		self._pageCache = {}

		self.__createPopupMenu()

		# Элемент, над которым показываем меню
		self.popupItem = None

		# Секция настроек куда сохраняем развернутость страницы
		self.pageOptionsSection = u"Tree"

		# Имя опции для сохранения развернутости страницы
		self.pageOptionExpand = "Expand"

		self.BindGuiEvents()
		self.BindControllerEvents()
		self.BindPopupMenuEvents()


	def BindControllerEvents(self):
		"""
		Подписка на события контроллера
		"""
		Controller.instance().onTreeUpdate += self.onTreeUpdate
		Controller.instance().onPageSelect += self.onPageSelect

		Controller.instance().onStartTreeUpdate += self.onStartTreeUpdate
		Controller.instance().onEndTreeUpdate += self.onEndTreeUpdate
		#Controller.instance().onWikiClose += self.onWikiClose
		
		# События, связанные с рендерингом страниц
		Controller.instance().onHtmlRenderingBegin += self.onHtmlRenderingBegin
		Controller.instance().onHtmlRenderingEnd += self.onHtmlRenderingEnd
	

	def BindGuiEvents (self):
		"""
		Подписка на события интерфейса
		"""
		# События, связанные с деревом
		self.Bind (wx.EVT_TREE_SEL_CHANGED, self.onSelChanged)

		# Перетаскивание элементов
		self.treeCtrl.Bind (wx.EVT_TREE_BEGIN_DRAG, self.onBeginDrag)
		self.treeCtrl.Bind (wx.EVT_TREE_END_DRAG, self.onEndDrag)
		
		# Переименование элемента
		self.treeCtrl.Bind (wx.EVT_TREE_END_LABEL_EDIT, self.onEndLabelEdit)

		# Показ всплывающего меню
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_MENU, self.onItemMenu)
		
		# Сворачивание/разворачивание элементов
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_COLLAPSED, self.onTreeStateChanged)
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_EXPANDED, self.onTreeStateChanged)
		

	def BindPopupMenuEvents (self):
		"""
		События, связанные с контекстным меню
		"""
		self.Bind(wx.EVT_MENU, self.onAddChild, id=self.ID_ADD_CHILD)
		self.Bind(wx.EVT_MENU, self.onAddSibling, id=self.ID_ADD_SIBLING)
		self.Bind(wx.EVT_MENU, self.onRename, id=self.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.onRemove, id=self.ID_REMOVE)
		
		self.Bind(wx.EVT_MENU, self.onCopyTitle, id=self.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.onCopyPath, id=self.ID_COPY_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyAttachPath, id=self.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyLink, id=self.ID_COPY_LINK)

		self.Bind(wx.EVT_MENU, self.onProperties, id=self.ID_PROPERTIES)
	

	def onHtmlRenderingBegin (self, page, htmlView):
		self.treeCtrl.Disable()
		self.treeCtrl.Update()

	
	def onHtmlRenderingEnd (self, page, htmlView):
		self.treeCtrl.Enable()


	def onTreeStateChanged (self, event):
		item = event.GetItem()
		assert item.IsOk()
		self.__saveItemState (item)


	#def onWikiClose (self, wikiroot):
	#	self.saveTreeState()

	def saveTreeState (self):
		"""
		Сохранить для каждой страницы развернутость ее узла в дереве
		"""
		for (page, itemid) in self._pageCache.iteritems():
			if page.parent != None:
				#expanded = self.treeCtrl.IsExpanded (itemid)
				#page.params.set (self.pageOptionsSection, self.pageOptionExpand, str (expanded))
				self.__saveItemState (itemid)
	

	def __saveItemState (self, itemid):
		assert itemid.IsOk()

		page = self.treeCtrl.GetItemData (itemid).GetData()
		expanded = self.treeCtrl.IsExpanded (itemid)
		page.params.set (self.pageOptionsSection, self.pageOptionExpand, str (expanded))


	def loadTreeState (self):
		"""
		Восстановить развернутость дерева
		"""
		for (page, itemid) in self._pageCache.iteritems():
			if page.parent != None:
				try:
					expanded = page.params.getbool (self.pageOptionsSection, self.pageOptionExpand)
				except ConfigParser.NoSectionError:
					continue
				except ConfigParser.NoOptionError:
					continue

				if expanded:
					self.treeCtrl.Expand (itemid)


	def onRemove (self, event):
		"""
		Удалить страницу
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.removePage (page)


	def onCopyLink (self, event):
		"""
		Копировать ссылку на страницу в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.copyLinkToClipboard (page)

	
	def onCopyTitle (self, event):
		"""
		Копировать заголовок страницы в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.copyTitleToClipboard (page)

	
	def onCopyPath (self, event):
		"""
		Копировать путь до страницы в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.copyPathToClipboard (page)


	def onCopyAttachPath (self, event):
		"""
		Копировать путь до прикрепленных файлов в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.copyAttachPathToClipboard (page)


	def __createPopupMenu (self):
		self.popupMenu = wx.Menu ()
		self.popupMenu.Append (self.ID_ADD_CHILD, u"Add child page...")
		self.popupMenu.Append (self.ID_ADD_SIBLING, u"Add sibling page...")
		self.popupMenu.Append (self.ID_RENAME, u"Rename")
		self.popupMenu.Append (self.ID_REMOVE, u"Remove...")
		self.popupMenu.AppendSeparator()
		
		self.popupMenu.Append (self.ID_COPY_TITLE, u"Copy page's title to clipboard")
		self.popupMenu.Append (self.ID_COPY_PATH, u"Copy page's path to clipboard")
		self.popupMenu.Append (self.ID_COPY_ATTACH_PATH, u"Copy attaches path to clipboard")
		self.popupMenu.Append (self.ID_COPY_LINK, u"Copy page link to clipboard")
		self.popupMenu.AppendSeparator()

		self.popupMenu.Append (self.ID_PROPERTIES, u"Properties...")
	

	def onRename (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		self.treeCtrl.EditLabel (self.popupItem)
	

	def onAddChild (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.createPageWithDialog (self, page)

	
	def onAddSibling (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None
		assert page.parent != None

		core.commands.createPageWithDialog (self, page.parent)

	
	def onProperties (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		core.commands.editPage (self, page)
	

	def onItemMenu (self, event):
		self.popupItem = event.GetItem()
		if not self.popupItem.IsOk ():
			return

		self.PopupMenu (self.popupMenu)
	

	def beginRename (self):
		selectedItem = self.treeCtrl.GetSelection()
		if not selectedItem.IsOk():
			return

		self.treeCtrl.EditLabel (selectedItem)


	def onEndLabelEdit (self, event):
		if event.IsEditCancelled():
			return

		# Новый заголовок
		label = event.GetLabel()

		item = event.GetItem()
		page = self.treeCtrl.GetItemData (item).GetData()
		
		# Не доверяем переименовывать элементы системе
		event.Veto()

		try:
			page.title = label
			page.root.selectedPage = page

		except core.exceptions.DublicateTitle:
			wx.MessageBox (u"Can't move page when page with that title already exists", u"Error", wx.ICON_ERROR | wx.OK)

		except OSError as e:
			wx.MessageBox (u"Can't rename page\n" + unicode (e), u"Error", wx.ICON_ERROR | wx.OK)


	def onStartTreeUpdate (self, root):
		Controller.instance().onTreeUpdate -= self.onTreeUpdate
		Controller.instance().onPageSelect -= self.onPageSelect
		self.Unbind (wx.EVT_TREE_SEL_CHANGED, handler = self.onSelChanged)

	
	def onEndTreeUpdate (self, root):
		Controller.instance().onTreeUpdate += self.onTreeUpdate
		Controller.instance().onPageSelect += self.onPageSelect
		self.Bind (wx.EVT_TREE_SEL_CHANGED, self.onSelChanged)

		self.treeUpdate (root)

	
	def onBeginDrag (self, event):
		event.Allow()
		self.dragItem = event.GetItem()


	def onEndDrag (self, event):
		if self.dragItem != None:
			# Элемент, на который перетащили другой элемент (self.dragItem)
			endDragItem = event.GetItem()

			# Перетаскиваемая станица
			draggedPage = self.treeCtrl.GetItemData (self.dragItem).GetData()

			# Будущий родитель для страницы
			newParent = self.treeCtrl.GetItemData (endDragItem).GetData() \
				if endDragItem.IsOk() else draggedPage.root

			core.commands.movePage (draggedPage, newParent)

		self.dragItem = None


	def onTreeUpdate (self, sender):
		self.treeUpdate (sender.root)


	def onPageSelect (self, page):
		"""
		Изменение выбранной страницы
		"""
		currpage = self.selectedPage
		if currpage != page:
			self.selectedPage = page


	def onSelChanged (self, event):
		page = self.selectedPage
		if page.root.selectedPage != page:
			page.root.selectedPage = page
	

	@property
	def selectedPage (self):
		item = self.treeCtrl.GetSelection ()
		if item.IsOk():
			page = self.treeCtrl.GetItemData (item).GetData()
			return page


	@selectedPage.setter
	def selectedPage (self, newSelPage):
		if newSelPage == None:
			return

		item = self._pageCache[newSelPage]
		self.treeCtrl.SelectItem (item)

	
	def __set_properties(self):
		# begin wxGlade: WikiTree.__set_properties
		pass
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: WikiTree.__do_layout
		mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
		mainSizer.Add(self.treeCtrl, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		# end wxGlade
	

	def treeUpdate (self, rootPage):
		"""
		Обновить дерево
		"""
		self.Unbind (wx.EVT_TREE_SEL_CHANGED, handler = self.onSelChanged)
		
		self.treeCtrl.DeleteAllItems()
		self.imagelist.RemoveAll()
		self.defaultImageId = self.imagelist.Add (self.defaultBitmap)
		self._pageCache = {}

		if rootPage != None:
			rootItem = self.treeCtrl.AddRoot (u"", data = wx.TreeItemData (rootPage) )
			self.appendChildren (rootPage, rootItem)
			self.selectedPage = rootPage.selectedPage

			self.loadTreeState()

		self.Bind (wx.EVT_TREE_SEL_CHANGED, self.onSelChanged)
	

	def appendChildren (self, parentPage, parentItem):
		"""
		Добавить детей в дерево
		"""
		self._pageCache[parentPage] = parentItem

		children = [child for child in parentPage.children]
		children.sort (self._sort)

		for child in children:
			#print child.title.encode ("866")
			item = self.treeCtrl.AppendItem (parentItem, child.title, data = wx.TreeItemData(child) )
			icon = child.icon

			if icon != None:
				image = wx.Bitmap (icon)
				image.SetHeight (self.iconHeight)
				imageId = self.imagelist.Add (image)
			else:
				imageId = self.defaultImageId
				
			self.treeCtrl.SetItemImage (item, imageId)
			
			#print self.treeCtrl.GetItemText (item).encode ("866")
			#print self.treeCtrl.GetItemData (item).GetData().title.encode("866")
			self.appendChildren (child, item)
	

	def _sort (self, page1, page2):
		"""
		Функция для сортировки страниц по алфавиту
		"""
		assert page1 != None
		assert page2 != None

		if page1.title.lower() > page2.title.lower():
			return 1
		elif page1.title.lower() < page2.title.lower():
			return -1

		return 0

# end of class WikiTree


