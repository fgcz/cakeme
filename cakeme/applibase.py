from collections import namedtuple
import logging
import shlex
import os
import subprocess
import fileutils

ProcessValues = namedtuple("ProcessValues", "return_code out err")

def setUpLogging(destination='/var/tmp/myapp.log'):
    logger = logging.getLogger('myapp')
    fileutils.make_path_to_file(destination)
    hdlr = logging.FileHandler(destination)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

class ApplicationBase:
    APP_NAME = ""
    LOGFILE = ""
    RESULT = ProcessValues(-1, "", "")

    def __init__(self, app_name, result_directory):
        self.logger = setUpLogging(os.path.join(result_directory,"{}.{}".format(app_name,"log")))
        self.APP_NAME = app_name

    def executeCommand(self,command):
        self.logger.info("Running {}".format(command))
        cmd = shlex.split(command)
        try:
            process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
            out, err = process.communicate()
            self.RESULT = ProcessValues(process.returncode, out, err)
            return self.RESULT
        except OSError as e:
            self.logger.error("test {}".format(str(e)))

    def logResults(self):
        self.logger.info("{appname} : ret {returnval} out {out}  err {err}".format(appname = self.APP_NAME,
                                                                    returnval=self.RESULT.return_code,
                                                                    out = self.RESULT.out,
                                                                    err= self.RESULT.err))
    def run(self):
        pass


class SCPCopy(ApplicationBase):
    def __init__(self,result_dir):
        ApplicationBase.__init__(self, "SCPCopy", result_dir)

    def stageFileTo(self, user, destination_computer, fromfile , tofile):
        if not os.path.exists(fromfile):
            self.logger.error("no such file : {}".format(fromfile))
        fromfile.strip()
        scp_command = "scp {file} {user}@{machine}:{tofile} ".format(file=fromfile, user=user,
                                                                     machine=destination_computer,
                                                                     tofile=tofile)
        self.executeCommand(scp_command)
        self.logResults()
        return self.RESULT.return_code

    def getFileFrom(self, user, source_computer, fromfile,  tofile):
        if not os.path.exists(file):
            self.logger.error("no such file : {}".format(file))
        fromfile.strip()
        scp_command = "scp {user}@{machine}:{fromfile} {tofile} ".format(user=user, machine=source_computer,
                                                                         fromfile=fromfile, tofile=tofile)
        self.executeCommand(scp_command)
        self.logResults()
        return self.RESULT.return_code


#class SpecLApplication(ApplicationBase):
if __name__ == "__main__":
    '''
    datfile = sys.argv[1]
    res = get_db_from_mascot_dat(datfile)
    print res
    res = cakeme.fileutils.find_file(res, "/usr/local/mascot/sequence/")
    print res
    '''
    scp = SCPCopy("testlog.log")
    ret= scp.stageFileTo("bfabric", "fgcz-s-021", "setup.py" ,"/srv/www/htdocs//p1000/bfabric/Proteomics/DIA_Assay_Library_Generator/2015/2015-10/2015-10-27//workunit_136124/206686.zip")
    print ret