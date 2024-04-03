import os, zipfile, requests


class IpaSignatureChwckCls():

    def listFiles(self, dirPath):
        # 准备一个空列表，用来存储遍历数据
        fileList = []
        fileName = []
        ''' os.walk(dirPath) ：走查指定的文件夹路径
                root  ：代表目录的路径
                dirs  ：一个list，包含了dirpath下所有子目录文件夹的名字
                files ：一个list，包含了所有非目录文件的名字
        '''
        for root, dirs, files in os.walk(dirPath):

            # fileName.append()
            # 循环遍历列表：files【所有文件】，仅得到不包含路径的文件名
            for fileObj in files:
                # 空列表写入遍历的文件名称，兵勇目录路径拼接文件名称
                fileName.append(fileObj)
                path = os.path.join(root, fileObj).replace('\\', '/')
                fileList.append(path)

        # 打印一下列表存储内容：指定文件夹下所有的文件名
        # print(fileList)
        # print(fileName)
        return list(set(fileList))

    def analyze_ipa_with_plistlib(self, ipa_path, decompress_folder):
        ipa_file = zipfile.ZipFile(ipa_path)
        ipa_file.extractall(path=decompress_folder)
        ipa_file.close()

    def run_func(self, ipa_path, decompress_folder):
        try:
            self.analyze_ipa_with_plistlib(ipa_path, decompress_folder)
        except:
            return False, '检测失败1！'
        fileList = self.listFiles(decompress_folder)

        embedded_file, info_file = '', ''
        for f in fileList:
            if f.endswith('.app/Info.plist'):
                info_file = f
            if f.endswith('.app/embedded.mobileprovision'):
                embedded_file = f

        if not embedded_file or not info_file:
            return False, '分析文件失败！'

        if os.path.exists(embedded_file):
            mp = open(embedded_file, 'rb').read()
        else:
            mp = ""
        if os.path.exists(info_file):
            plist = open(info_file, 'rb').read()
        else:
            plist = ""

        url = 'https://admin.100-bt.cn/api/Index/check_p12'
        files = {'mp': ('embedded.mobileprovision', mp), 'plist': ('Info.plist', plist)}
        req = requests.post(url, files=files, timeout=15)
        data_json = req.json()
        if data_json.get('code') == 0:
            state = data_json.get('state')
            if state is None:
                return False, '检测失败3！'
            if state == '吊销':
                return True, '掉签'
            elif state == '正常':
                return True, '正常'
            else:
                return True, '未知'
        return False, '检测失败5！'

    def main(self, ipa_path, decompress_folder):
        # try:
        return self.run_func(ipa_path, decompress_folder)
        # except:
        #     return False, '检测失败6！'



# if __name__ == '__main__':
#     ipa_path = './TK88_3-30.ipa'
#     decompress_folder = './data'
#     if not os.path.exists(decompress_folder):
#         os.makedirs(decompress_folder)
#     print(IpaSignatureChwckCls().run_func(ipa_path, decompress_folder))

