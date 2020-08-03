import paramiko
from ftplib import FTP
def sftp_conn(ip,port,username,password):
    sshd = paramiko.SSHClient()
    sshd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshd.connect(ip,port,username,password)
    return sshd.open_sftp()
def ftp_conn(ip,port,username,password):
    ftp = FTP()
    ftp.connect(ip,port)
    ftp.login(username,password)
    return ftp
def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


