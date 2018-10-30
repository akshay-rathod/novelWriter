# -*- coding: utf-8 -*
"""novelWriter GUI Document Tree

 novelWriter – GUI Document Tree
=================================
 Class holding the left side document tree view

 File History:
 Created: 2018-09-29 [0.1.0]

"""

import logging
import nw

from os              import path
from PyQt5.QtGui     import QIcon
from PyQt5.QtCore    import Qt, QSize
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QAbstractItemView

from nw.project.item import NWItem

logger = logging.getLogger(__name__)

class GuiDocTree(QTreeWidget):

    def __init__(self, theProject):
        QTreeWidget.__init__(self)

        logger.debug("Initialising DocTree ...")
        self.mainConf   = nw.CONFIG
        self.debugGUI   = self.mainConf.debugGUI
        self.theProject = theProject
        self.theMap     = {}

        self.setStyleSheet("QTreeWidget {font-size: 13px;}")
        self.setIconSize(QSize(13,13))
        self.setExpandsOnDoubleClick(True)
        self.setIndentation(13)
        self.setColumnCount(4)
        self.setHeaderLabels(["Name","","","Handle"])
        if not self.debugGUI:
            self.hideColumn(3)

        # Allow Move by Drag & Drop
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        for colN in range(len(self.mainConf.treeColWidth)):
            self.setColumnWidth(colN,self.mainConf.treeColWidth[colN])

        logger.debug("DocTree initialisation complete")

        return

    def saveTreeOrder(self):
        theList = []
        for i in range(self.topLevelItemCount()):
            theList = self._scanChildren(theList, self.topLevelItem(i), i)
        self.theProject.setTreeOrder(theList)
        return True

    def _scanChildren(self, theList, theItem, theIndex):
        tHandle = theItem.text(3)
        nwItem  = self.theProject.projTree[tHandle]
        nwItem.setExpanded(theItem.isExpanded())
        nwItem.setOrder(theIndex)
        theList.append(tHandle)
        for i in range(theItem.childCount()):
            self._scanChildren(theList, theItem.child(i), i)
        return theList

    def buildTree(self):
        self.clear()
        for tHandle in self.theProject.projTree:
            nwItem  = self.theProject.projTree[tHandle]
            tName   = nwItem.itemName
            tStatus = 0
            wCount  = 0
            pHandle = nwItem.parHandle
            newItem = QTreeWidgetItem([
                tName, str(tStatus), str(wCount), tHandle
            ])
            self.theMap[tHandle] = newItem
            if pHandle is None:
                self.addTopLevelItem(newItem)
            else:
                self.theMap[pHandle].addChild(newItem)
            newItem.setExpanded(nwItem.isExpanded)
            if nwItem.itemType == NWItem.TYPE_ROOT:
                newItem.setIcon(0, QIcon.fromTheme("drive-harddisk"))
            elif nwItem.itemType == NWItem.TYPE_FOLDER:
                newItem.setIcon(0, QIcon.fromTheme("folder"))
            elif nwItem.itemType == NWItem.TYPE_FILE:
                newItem.setIcon(0, QIcon.fromTheme("x-office-document"))
        return True

    def getColumnSizes(self):
        retVals = [
            self.columnWidth(0),
            self.columnWidth(1),
            self.columnWidth(2),
        ]
        return retVals

# END Class GuiDocTree
