#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import subprocess
import urllib2
import poster

Project_Path='/Users/wujia/Documents/code/ynoteios'
Workspace='/Users/wujia/Documents/code/ynoteios/YNote.xcworkspace'
Scheme='有道笔记'
Configuration='Debug'
App_Path='/Users/wujia/Library/Developer/Xcode/DerivedData/YNote-ewvbkrazcxnhicayktmrgqqwzltv/Build/Products/Debug-iphoneos/有道云笔记.app'
Out_Path='/Users/wujia/Library/Developer/Xcode/DerivedData/YNote-ewvbkrazcxnhicayktmrgqqwzltv/Build/Products/Debug-iphoneos/有道云笔记.ipa'

uploadurl='http://www.pgyer.com/apiv1/app/upload'

ukey='c527645eccdf97653af73e7732858a04'
apikey='b5036ab32debc03ea0d1d3ca16ee70ef'


class Build():

    def git_pull(self):

        subprocess.Popen('cd %s'%Project_Path, shell=True)
        subprocess.Popen('git pull',shell=True)

    #building
    def build_project(self,workspace,scheme,configuration):
        print "build start ====="
        cmd="xcodebuild -workspace %s -scheme %s -configuration %s" %(workspace,scheme,configuration)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
        return process.returncode

    #export ipa
    def export_ipa(self,frompath,topath):

        print "export ipa start===="
        cmd='xcrun -sdk iphoneos -v PackageApplication %s -o %s' %(frompath,topath)
        process = subprocess.Popen(cmd, shell=True)
        (outdata, rrdata) = process.communicate()
        return process.returncode

    #upload to pgyer.com
    def uploadipa(self,file_path):
        #upload to fir

        print "upload ipa to pgyer.com  start ===="
        #upload to pgyer.com
        post_data={'uKey':ukey,'_api_key':apikey,'file':open(file_path,'rb')}
        poster.streaminghttp.register_openers()
        datagen,header=poster.encode.multipart_encode(post_data)
        request=urllib2.Request(uploadurl,datagen,header)
        result=urllib2.urlopen(request)
        print result.read()
        print  "upload pyger finish"

    #编译－打包－导出为ipa－上传
    def buildxcworkspace(self):
        #build
        code=self.build_project(Workspace,Scheme,Configuration)

        if code  !=0:
            print "build fail  !!!! "
        else:
            print "build finish !!!"
            # export ipa
            code1=self.export_ipa(App_Path,Out_Path)
            if code1 !=0:
                print "export ipa fail  !!!!"
            else:
                print "export ipa finish: %s" %Out_Path
                #upload
                self.uploadipa(Out_Path)


oo=Build()
#oo.buildxcworkspace()
oo.buildxcworkspace()










