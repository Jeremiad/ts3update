from lxml import etree as etree
import platform
import re
import urllib.request as req
import tarfile
import zipfile
import os.path as path
import shutil as util
import cfscrape
import time
import sys
from subprocess import call


def Upgrade():

    scraper = cfscrape.create_scraper(js_engine="Node")
    html = scraper.get("http://teamspeak.com/downloads#server").content
    response = etree.HTML(html)

    urls = response.xpath('//div[@class="uk-width-medium-2-5 uk-text-nowrap uk-text-right"]/select[@class="mirror"]/option/@value')

    os = platform.system()
    arch = platform.machine()

    mirrors = list()

    if os == "Windows":
        if arch == "AMD64":
            for index, u in enumerate(urls):
                result = re.search('win64', u)
                if result:
                    print("Mirrors:", result.string, index)
                    mirrors.append(result.string)
            DownloadFile(mirrors[0])

        elif arch == "i386":
            for index, u in enumerate(urls):
                result = re.search('win32', u)
                if result:
                    print("Mirrors:", result.string, index)
                    mirrors.append(result.string)
            DownloadFile(mirrors[0])
        else:
            print("Unknown arch")
    elif os == "Linux":
        if arch == "x86_64":
            for index, u in enumerate(urls):
                result = re.search('linux_amd64', u)
                if result:
                    print("Mirrors:", result.string, index)
                    mirrors.append(result.string)
            DownloadFile(mirrors[0])
    elif os == "Linux":
        if arch == "x86":
            for index, u in enumerate(urls):
                result = re.search('linux_x86', u)
                if result:
                    print("Mirrors:", result.string, index)
                    mirrors.append(result.string)
            DownloadFile(mirrors[0])
        else:
            print("Unknown arch")
    version = CurrentVersionCheck()
    WriteVersion(version)

def DownloadFile(mirrorUrl):
    filename = mirrorUrl.split('/')[-1]
    req.urlretrieve(mirrorUrl, filename)
    Extract(filename)

def CurrentVersionCheck():
    scraper = cfscrape.create_scraper(js_engine="Node")
    html = scraper.get("http://teamspeak.com/downloads#server").content
    response = etree.HTML(html)
    versionList = response.xpath('//div[@class="download__icon-offset"][normalize-space(text())="Server 64-bit"]/span[@class="version"]/text()')

    return versionList[0]

def WriteVersion(version):
    file = open(".ts3version", 'w')
    file.write(version)
    file.close()

def LastUpdatedVersion():
    if path.isfile(".ts3version"):
        file = open(".ts3version", "r")
        version = file.readline()
        file.close()
        return version
    else:
        file = open(".ts3version", "w")
        file.close()

def Extract(filename):
    if zipfile.is_zipfile(filename):
        print("Extracting", filename)
        zip = zipfile.ZipFile(filename)
        Backup(zip.filelist[0].filename.strip('/'))
        zip.extractall()
        zip.close()

    elif tarfile.is_tarfile(filename):
        print("Extracting ", filename)
        tar = tarfile.open(filename, "r:bz2")
        for tarinfo in tar:
            tar.extract(tarinfo)
        tar.close()

def Backup(folderName):
    if path.exists(folderName):
        util.copytree(folderName, folderName + time.strftime("-%d-%m-%Y") + ".backup")
    else:
        print("Folder " + folderName + " not found. No need to backup?")

def PreCommand():
    print(str(sys.argv[1]))
    if not sys.argv[1]:
        call(sys.argv[1])

def PostCommand():
    print(str(sys.argv[2]))
    if not sys.argv[2]:
        call(sys.argv[2])


if CurrentVersionCheck() != LastUpdatedVersion():
#    PreCommand()
    Upgrade()
#    PostCommand()

else:
    print("Already up to date")

