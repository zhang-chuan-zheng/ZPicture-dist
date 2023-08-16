import os


class QRCFile:
    def __init__(self):
        qrcFile = open('core/front/resource.qrc','w+')
        qrcFile.write("<RCC>\n")

        ##  写入图片资源
        qrcFile.write("\t<qresource prefix=\"/images\">\n")
        imagesLis = self.getDir("core/front/images")
        for image in imagesLis:
            qrcFile.write(f"\t\t<file>{image}</file>\n")
        qrcFile.write("\t</qresource>\n")

        ##  写入样式文件
        qrcFile.write("\t<qresource prefix=\"/styles\">\n")
        styleLis = self.getDir("core/front/styles")
        for style in styleLis:
            qrcFile.write(f"\t\t<file>{style}</file>\n")
        qrcFile.write("\t</qresource>\n")

        qrcFile.write("</RCC>")
        qrcFile.close()

    def getDir(self,folder):
        fileList = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                path = os.path.join(dirpath,filename)
                fileList.append(path)
        # print(fileList)
        return fileList

QRCFile()
