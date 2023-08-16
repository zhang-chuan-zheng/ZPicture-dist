import sys

from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QMenu, QAction
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QCursor

from core.front.components import titleBar, statusBar, exhibitionFrame, rightClickedMenu, logFrame, payoffWidget
from core.front.components.parameterCard import renameCard,resizeCard,mappingColorCard,picCombCard


class MainWindow(QWidget):
    Margins = 2
    def __init__(self,parent = None,titleName = "ZPicture",iconName = "Z.svg",barLayoutStyle = 'V',barSize = None,qssFile = ''):
        super().__init__()
        with open(qssFile,'r') as qssFile:
            self.qss = qssFile.read()
        self.m_flag = None
        if barSize is None:
            barSize = {"titleBar": 36,
                       "statusBar":24,
                       }
        self.logFrameWidth = 242
        # self.workPlaceImageList = [
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\max.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\min.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\normal.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\payoff.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\shutDown.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\icon\Z.svg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\QR_Code\AliPay.jpg",
        #                            r"D:\Codes\Python\ZPicture\core\front\images\QR_Code\WeChat.jpg"
        #                            ]
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  ###  窗体设置成全透明，连上面的控件也是全透明，创建一个不透明的图片设置为mainFrame的背景
        self.title = titleName
        self.iconName = iconName
        self.layoutStyle = barLayoutStyle
        self.barSize = barSize
        self.Parent = parent
        self.subWindowLis = []
        self.payoffWindow = None
        self.newNameLis = None  ##  预览区的新文件名

        self._initUI()
    def _initUI(self):
        self.setObjectName("mainWindow")
        self.setStyleSheet(self.qss)
        self.resize(1220,900)
        self.show()
        self.x, self.y, self.wid, self.hei = self.geometry().getRect()
        # print(self.x, self.y, self.wid, self.hei)
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)  ##  设置布局器(left top right bottom)边界为 0
        vLayout.setSpacing(0)

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)  ##  设置布局器(left top right bottom)边界为 0
        hLayout.setSpacing(0)

        mainFrame = QFrame()
        mainFrame.setObjectName("mainFrame")  ##  给该组件起一个名字，设置样式时可以使用名字设置，避免所有相同父类的组件全都应用
        mainFrame.setStyleSheet(self.qss)
        body = QFrame()

        contentsFrame = QFrame()

        exhibitionLayout = QVBoxLayout(contentsFrame)

        self.workPlace = exhibitionFrame.ExhibitionFrame(frameTitle="Work \t Place", allowSelect=True)
        self.workPlace.imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth
        self.workPlace.showImage(self.workPlace.workPlaceImageList,QtImages=self.workPlace.qPixmapDic,
                                 imageExhibitionWidth=self.wid - self.barSize["titleBar"] - self.logFrameWidth)


        self.previewArea = exhibitionFrame.ExhibitionFrame(frameTitle="Preview \t Area")
        self.previewArea.imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth
        self.previewArea.showImage(self.previewArea.selectedFiles,QtImages=self.workPlace.qPixmapDic,
                                   imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth,previewTitleLis=self.newNameLis)

        self.workPlace.exFuncSlot(self._showPreviewImages)
        ##  创建右键菜单
        self.previewArea.setContextMenuPolicy(Qt.CustomContextMenu)
        self.previewArea.customContextMenuRequested.connect(lambda:rightClickedMenu.RightClickedMenu(self))




        exhibitionLayout.addWidget(self.previewArea)
        exhibitionLayout.addWidget(self.workPlace)
        contentsFrame.setLayout(exhibitionLayout)

        self.logPlace = logFrame.LogFrame()
        logLayout = QVBoxLayout()
        logLayout.addWidget(self.logPlace)
        logLayout.setContentsMargins(6,15,15,15)


        self.titleBarFrame = titleBar.TitleBar(parent=self,titleName = self.title,iconName=self.iconName)

        self.titleBarFrame.shutDownButton.clicked.connect(self.on_pushButton_close_clicked)
        self.titleBarFrame.maxAndNormalButton.clicked.connect(self.on_pushButton_max_clicked)
        self.titleBarFrame.minWindowButton.clicked.connect(self.on_pushButton_min_clicked)
        self.titleBarFrame.payoffButton.clicked.connect(self._showPayoffWindow)

        statusBarFrame = statusBar.StatusBar()
        # statusBarFrame.setMinimumSize(QSize(0,self.barSize-12))
        # statusBarFrame.setMaximumSize(QSize(15467815,self.barSize - 12))
        hLayout.addWidget(contentsFrame)
        hLayout.addWidget(self.titleBarFrame)
        hLayout.addLayout(logLayout)
        body.setLayout(hLayout)
        vLayout.addWidget(body)
        vLayout.addWidget(statusBarFrame)
        mainFrame.setLayout(vLayout)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(mainFrame)
        self.setLayout(self.layout)

        ##  窗口展示顺序

    def _showPreviewImages(self,images,QtImages):
        self.newNameLis = None
        self.previewArea.qPixmapDic = QtImages
        self.previewArea.selectedFiles = images
        try:
            self.renameWidget.rename()
        except:
            pass
        self.previewArea.showImage(self.previewArea.selectedFiles,QtImages = self.previewArea.qPixmapDic,
                                   imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth,
                                   previewTitleLis=self.newNameLis)



    def _showPayoffWindow(self):
        # x,y,w,h = self.x,self.y,self.wid,self.hei
        # payoffWindowW,payoffWindowH = 444,288
        if self.payoffWindow is None:
            self.payoffWindow = payoffWidget.PayoffWindow(self  # ,startX =x + w - self.barSize["titleBar"] - payoffWindowW - 242,
                                                          # startY = y + h - self.barSize["statusBar"] - payoffWindowH,
                                                          # w = payoffWindowW, h = payoffWindowH
                                                          )
        if not self.titleBarFrame.buttonStatus["payoffButton"]:
            self.titleBarFrame.buttonStatus["payoffButton"] = True
            self.subWindowLis.append(self.payoffWindow)
            self.payoffWindow.updatePayoffWindow(self.barSize["titleBar"] + self.logPlace.width() + 8,self.barSize["statusBar"] - 8).show()
        else:
            self.titleBarFrame.buttonStatus["payoffButton"] = False
            self.subWindowLis.remove(self.payoffWindow)
            self.payoffWindow.close()
            self.payoffWindow = None
    ###   窗口移动   ###
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


    ####   最大最小化以及关闭按钮   ###
    @pyqtSlot()
    def on_pushButton_max_clicked(self):
        if self.isMaximized():
            self.showNormal()
            if self.payoffWindow is not None:
                self.payoffWindow.updatePayoffWindow(self.barSize["titleBar"] + self.logPlace.width(), self.barSize["statusBar"]).show()

            self.x, self.y, self.wid, self.hei = self.frameGeometry().getRect()  ##  重新获取窗口尺寸
            self.workPlace.showImage(self.workPlace.workPlaceImageList,QtImages=self.workPlace.qPixmapDic,
                                     imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth)
            self.previewArea.showImage(self.previewArea.selectedFiles,QtImages=self.workPlace.qPixmapDic,
                                       imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth,previewTitleLis=self.newNameLis)


        else:
            self.showMaximized()
            if self.payoffWindow is not None:
                self.payoffWindow.updatePayoffWindow(self.barSize["titleBar"] + self.logPlace.width(),
                                                     self.barSize["statusBar"])

            self.x, self.y, self.wid, self.hei = self.frameGeometry().getRect()  ##  重新获取窗口尺寸
            self.workPlace.showImage(self.workPlace.workPlaceImageList,QtImages=self.workPlace.qPixmapDic,
                                     imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth)
            self.previewArea.showImage(self.previewArea.selectedFiles,QtImages=self.workPlace.qPixmapDic,
                                       imageExhibitionWidth = self.wid - self.barSize["titleBar"] - self.logFrameWidth,
                                       previewTitleLis=self.newNameLis)


    @pyqtSlot()
    def on_pushButton_min_clicked(self):
        self.showMinimized()

    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        for subWindow in self.subWindowLis:
            subWindow.close()
        self.close()

    def showRenameCard(self):
        self.renameWidget = renameCard.RenameCard(mainWindow=self)
        self.subWindowLis.append(self.renameWidget)
        self.renameWidget.show()

    def showResizeCard(self,mode = "stretch",method = 0):
        self.resizeWidget = resizeCard.ResizeCard(mainWindow = self,defaultMode = mode,defaultMethod=method)
        self.subWindowLis.append(self.resizeWidget)
        self.resizeWidget.show()

    def showMappingColorCard(self):
        self.mappingColorWidget = mappingColorCard.MappingColorCard(mainWindow = self)
        self.subWindowLis.append(self.mappingColorWidget)
        self.mappingColorWidget.show()

    def showPicCombCard(self):
        self.picCombWidget = picCombCard.PicCombCard(mainWindow=self)
        self.subWindowLis.append(self.picCombWidget)
        self.picCombWidget.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    app.exec_()
