__author__ = 'LiYuanhe'
# -*- coding: utf-8 -*-

import sys
import os
import math
import copy
import shutil
import re
import random
import time
from My_Lib import *
from datetime import datetime
from datetime import timedelta

from PyQt5 import Qt

from smb.SMBConnection import SMBConnection

import matplotlib

matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as MpFigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as MpNavToolBar
from matplotlib.figure import Figure as MpFigure
import matplotlib.pyplot as MpPyplot
import mogli
import gr
from matplotlib import pylab
import matplotlib
import collections
from enum import Enum
import numpy as np
from functools import total_ordering

functional_keywords_of_orca = ["HFS","LDA","VWN","VWN3","PWLDA","BP86","BLYP","OLYP","GLYP","XLYP","PW91","mPWPW","mPWLYP","PBE","RPBE","REVPBE","PWP","B1LYP","B3LYP","O3LYP","X3LYP","B1P","B3P","B3PW","PW1PW","mPW1PW","mPW1LYP","PBE0","PW6B95","BHANDHLYP","Meta-GGA","TPSS","TPSSh","TPSS0","M06L","M06","M062X","B2PLYP","RI-B2PLYP","B2PLYP-D","B2PLYP-D3","RI-B2PLYP","mPW2PLYP","mPW2PLYP-D","mPW2PLYP-D3","B2GP-PLYP","B2K-PLYP","B2T-PLYP","PWPB95","RI-PWPB95"]
basis_set_keywords_of_orca = ['3-21+G*', '3-21++G*', '3-21G*', '3-21+G**', '3-21++G**', '3-21G**', '3-21+G(d)', '3-21++G(d)', '3-21G(d)', '3-21+G(d,p)', '3-21++G(d,p)', '3-21G(d,p)', '3-21+G(2d)', '3-21++G(2d)', '3-21G(2d)', '3-21+G(2d,2p)', '3-21++G(2d,2p)', '3-21G(2d,2p)', '3-21+G(2df)', '3-21++G(2df)', '3-21G(2df)', '3-21+G(2df,2pd)', '3-21++G(2df,2pd)', '3-21G(2df,2pd)', '3-21+G(3df)', '3-21++G(3df)', '3-21G(3df)', '3-21+G(3df,3pd)', '3-21++G(3df,3pd)', '3-21G(3df,3pd)', '3-21+G', '3-21++G', '3-21G', '3-21+GSP*', '3-21++GSP*', '3-21GSP*', '3-21+GSP**', '3-21++GSP**', '3-21GSP**', '3-21+GSP(d)', '3-21++GSP(d)', '3-21GSP(d)', '3-21+GSP(d,p)', '3-21++GSP(d,p)', '3-21GSP(d,p)', '3-21+GSP(2d)', '3-21++GSP(2d)', '3-21GSP(2d)', '3-21+GSP(2d,2p)', '3-21++GSP(2d,2p)', '3-21GSP(2d,2p)', '3-21+GSP(2df)', '3-21++GSP(2df)', '3-21GSP(2df)', '3-21+GSP(2df,2pd)', '3-21++GSP(2df,2pd)', '3-21GSP(2df,2pd)', '3-21+GSP(3df)', '3-21++GSP(3df)', '3-21GSP(3df)', '3-21+GSP(3df,3pd)', '3-21++GSP(3df,3pd)', '3-21GSP(3df,3pd)', '3-21+GSP', '3-21++GSP', '3-21GSP', '4-22+GSP*', '4-22++GSP*', '4-22GSP*', '4-22+GSP**', '4-22++GSP**', '4-22GSP**', '4-22+GSP(d)', '4-22++GSP(d)', '4-22GSP(d)', '4-22+GSP(d,p)', '4-22++GSP(d,p)', '4-22GSP(d,p)', '4-22+GSP(2d)', '4-22++GSP(2d)', '4-22GSP(2d)', '4-22+GSP(2d,2p)', '4-22++GSP(2d,2p)', '4-22GSP(2d,2p)', '4-22+GSP(2df)', '4-22++GSP(2df)', '4-22GSP(2df)', '4-22+GSP(2df,2pd)', '4-22++GSP(2df,2pd)', '4-22GSP(2df,2pd)', '4-22+GSP(3df)', '4-22++GSP(3df)', '4-22GSP(3df)', '4-22+GSP(3df,3pd)', '4-22++GSP(3df,3pd)', '4-22GSP(3df,3pd)', '4-22+GSP', '4-22++GSP', '4-22GSP', '6-31+G*', '6-31++G*', '6-31G*', '6-31+G**', '6-31++G**', '6-31G**', '6-31+G(d)', '6-31++G(d)', '6-31G(d)', '6-31+G(d,p)', '6-31++G(d,p)', '6-31G(d,p)', '6-31+G(2d)', '6-31++G(2d)', '6-31G(2d)', '6-31+G(2d,2p)', '6-31++G(2d,2p)', '6-31G(2d,2p)', '6-31+G(2df)', '6-31++G(2df)', '6-31G(2df)', '6-31+G(2df,2pd)', '6-31++G(2df,2pd)', '6-31G(2df,2pd)', '6-31+G(3df)', '6-31++G(3df)', '6-31G(3df)', '6-31+G(3df,3pd)', '6-31++G(3df,3pd)', '6-31G(3df,3pd)', '6-31+G', '6-31++G', '6-31G', '6-311+G*', '6-311++G*', '6-311G*', '6-311+G**', '6-311++G**', '6-311G**', '6-311+G(d)', '6-311++G(d)', '6-311G(d)', '6-311+G(d,p)', '6-311++G(d,p)', '6-311G(d,p)', '6-311+G(2d)', '6-311++G(2d)', '6-311G(2d)', '6-311+G(2d,2p)', '6-311++G(2d,2p)', '6-311G(2d,2p)', '6-311+G(2df)', '6-311++G(2df)', '6-311G(2df)', '6-311+G(2df,2pd)', '6-311++G(2df,2pd)', '6-311G(2df,2pd)', '6-311+G(3df)', '6-311++G(3df)', '6-311G(3df)', '6-311+G(3df,3pd)', '6-311++G(3df,3pd)', '6-311G(3df,3pd)', '6-311+G', '6-311++G', '6-311G',"cc-pVDZ","cc-(p)VDZ","aug-cc-pVDZ","cc-pVTZ","cc-(p)VTZ","aug-cc-pVTZ","cc-pVQZ","aug-cc-pVQZ","cc-pV5Z","aug-cc-pV5Z","cc-pV6Z","aug-cc-pV6Z","cc-pCVDZ","cc-pCVTZ","cc-pCVQZ","cc-pCV5Z","cc-pV6Z","aug-pCVDZ","aug-pCVTZ","aug-pCVQZ","aug-pCV5Z","aug-cc-pV6Z","DUNNING-DZP",'DZP++', 'DZP+', 'aug-DZP', 'DZP', 'DZ(P)++', 'DZ(P)+', 'aug-DZ(P)', 'DZ(P)', 'DZ(d)++', 'DZ(d)+', 'aug-DZ(d)', 'DZ(d)', 'DZ(d,p)++', 'DZ(d,p)+', 'aug-DZ(d,p)', 'DZ(d,p)', 'DZ(2D)++', 'DZ(2D)+', 'aug-DZ(2D)', 'DZ(2D)', 'DZ(2D,2P)++', 'DZ(2D,2P)+', 'aug-DZ(2D,2P)', 'DZ(2D,2P)', 'DZ(2d)++', 'DZ(2d)+', 'aug-DZ(2d)', 'DZ(2d)', 'DZ(2d,2p)++', 'DZ(2d,2p)+', 'aug-DZ(2d,2p)', 'DZ(2d,2p)', 'DZ(2df)++', 'DZ(2df)+', 'aug-DZ(2df)', 'DZ(2df)', 'DZ(2df,2pd)++', 'DZ(2df,2pd)+', 'aug-DZ(2df,2pd)', 'DZ(2df,2pd)', 'DZPPP++', 'DZPPP+', 'aug-DZPPP', 'DZPPP', 'DZPP++', 'DZPP+', 'aug-DZPP', 'DZPP', 'DZ(PP)++', 'DZ(PP)+', 'aug-DZ(PP)', 'DZ(PP)', 'DZ++', 'DZ+', 'aug-DZ', 'DZ', 'VTZP++', 'VTZP+', 'aug-VTZP', 'VTZP', 'VTZ(P)++', 'VTZ(P)+', 'aug-VTZ(P)', 'VTZ(P)', 'VTZ(d)++', 'VTZ(d)+', 'aug-VTZ(d)', 'VTZ(d)', 'VTZ(d,p)++', 'VTZ(d,p)+', 'aug-VTZ(d,p)', 'VTZ(d,p)', 'VTZ(2D)++', 'VTZ(2D)+', 'aug-VTZ(2D)', 'VTZ(2D)', 'VTZ(2D,2P)++', 'VTZ(2D,2P)+', 'aug-VTZ(2D,2P)', 'VTZ(2D,2P)', 'VTZ(2d)++', 'VTZ(2d)+', 'aug-VTZ(2d)', 'VTZ(2d)', 'VTZ(2d,2p)++', 'VTZ(2d,2p)+', 'aug-VTZ(2d,2p)', 'VTZ(2d,2p)', 'VTZ(2df)++', 'VTZ(2df)+', 'aug-VTZ(2df)', 'VTZ(2df)', 'VTZ(2df,2pd)++', 'VTZ(2df,2pd)+', 'aug-VTZ(2df,2pd)', 'VTZ(2df,2pd)', 'VTZPPP++', 'VTZPPP+', 'aug-VTZPPP', 'VTZPPP', 'VTZPP++', 'VTZPP+', 'aug-VTZPP', 'VTZPP', 'VTZ(PP)++', 'VTZ(PP)+', 'aug-VTZ(PP)', 'VTZ(PP)', 'VTZ++', 'VTZ+', 'aug-VTZ', 'VTZ', 'SVP++', 'SVP+', 'aug-SVP', 'SVP', 'SV(P)++', 'SV(P)+', 'aug-SV(P)', 'SV(P)', 'SV(d)++', 'SV(d)+', 'aug-SV(d)', 'SV(d)', 'SV(d,p)++', 'SV(d,p)+', 'aug-SV(d,p)', 'SV(d,p)', 'SV(2D)++', 'SV(2D)+', 'aug-SV(2D)', 'SV(2D)', 'SV(2D,2P)++', 'SV(2D,2P)+', 'aug-SV(2D,2P)', 'SV(2D,2P)', 'SV(2d)++', 'SV(2d)+', 'aug-SV(2d)', 'SV(2d)', 'SV(2d,2p)++', 'SV(2d,2p)+', 'aug-SV(2d,2p)', 'SV(2d,2p)', 'SV(2df)++', 'SV(2df)+', 'aug-SV(2df)', 'SV(2df)', 'SV(2df,2pd)++', 'SV(2df,2pd)+', 'aug-SV(2df,2pd)', 'SV(2df,2pd)', 'SVPPP++', 'SVPPP+', 'aug-SVPPP', 'SVPPP', 'SVPP++', 'SVPP+', 'aug-SVPP', 'SVPP', 'SV(PP)++', 'SV(PP)+', 'aug-SV(PP)', 'SV(PP)', 'SV++', 'SV+', 'aug-SV', 'SV', 'TZVP++', 'TZVP+', 'aug-TZVP', 'TZVP', 'TZV(P)++', 'TZV(P)+', 'aug-TZV(P)', 'TZV(P)', 'TZV(d)++', 'TZV(d)+', 'aug-TZV(d)', 'TZV(d)', 'TZV(d,p)++', 'TZV(d,p)+', 'aug-TZV(d,p)', 'TZV(d,p)', 'TZV(2D)++', 'TZV(2D)+', 'aug-TZV(2D)', 'TZV(2D)', 'TZV(2D,2P)++', 'TZV(2D,2P)+', 'aug-TZV(2D,2P)', 'TZV(2D,2P)', 'TZV(2d)++', 'TZV(2d)+', 'aug-TZV(2d)', 'TZV(2d)', 'TZV(2d,2p)++', 'TZV(2d,2p)+', 'aug-TZV(2d,2p)', 'TZV(2d,2p)', 'TZV(2df)++', 'TZV(2df)+', 'aug-TZV(2df)', 'TZV(2df)', 'TZV(2df,2pd)++', 'TZV(2df,2pd)+', 'aug-TZV(2df,2pd)', 'TZV(2df,2pd)', 'TZVPPP++', 'TZVPPP+', 'aug-TZVPPP', 'TZVPPP', 'TZVPP++', 'TZVPP+', 'aug-TZVPP', 'TZVPP', 'TZV(PP)++', 'TZV(PP)+', 'aug-TZV(PP)', 'TZV(PP)', 'TZV++', 'TZV+', 'aug-TZV', 'TZV', 'QZVPP++', 'QZVPP+', 'aug-QZVPP', 'QZVPP', 'QZVP(P)++', 'QZVP(P)+', 'aug-QZVP(P)', 'QZVP(P)', 'QZVP(d)++', 'QZVP(d)+', 'aug-QZVP(d)', 'QZVP(d)', 'QZVP(d,p)++', 'QZVP(d,p)+', 'aug-QZVP(d,p)', 'QZVP(d,p)', 'QZVP(2D)++', 'QZVP(2D)+', 'aug-QZVP(2D)', 'QZVP(2D)', 'QZVP(2D,2P)++', 'QZVP(2D,2P)+', 'aug-QZVP(2D,2P)', 'QZVP(2D,2P)', 'QZVP(2d)++', 'QZVP(2d)+', 'aug-QZVP(2d)', 'QZVP(2d)', 'QZVP(2d,2p)++', 'QZVP(2d,2p)+', 'aug-QZVP(2d,2p)', 'QZVP(2d,2p)', 'QZVP(2df)++', 'QZVP(2df)+', 'aug-QZVP(2df)', 'QZVP(2df)', 'QZVP(2df,2pd)++', 'QZVP(2df,2pd)+', 'aug-QZVP(2df,2pd)', 'QZVP(2df,2pd)', 'QZVPPPP++', 'QZVPPPP+', 'aug-QZVPPPP', 'QZVPPPP', 'QZVPPP++', 'QZVPPP+', 'aug-QZVPPP', 'QZVPPP', 'QZVP(PP)++', 'QZVP(PP)+', 'aug-QZVP(PP)', 'QZVP(PP)', 'QZVP++', 'QZVP+', 'aug-QZVP', 'QZVP', 'QZVPP(-g,-f)P++', 'QZVPP(-g,-f)P+', 'aug-QZVPP(-g,-f)P', 'QZVPP(-g,-f)P', 'QZVPP(-g,-f)(P)++', 'QZVPP(-g,-f)(P)+', 'aug-QZVPP(-g,-f)(P)', 'QZVPP(-g,-f)(P)', 'QZVPP(-g,-f)(d)++', 'QZVPP(-g,-f)(d)+', 'aug-QZVPP(-g,-f)(d)', 'QZVPP(-g,-f)(d)', 'QZVPP(-g,-f)(d,p)++', 'QZVPP(-g,-f)(d,p)+', 'aug-QZVPP(-g,-f)(d,p)', 'QZVPP(-g,-f)(d,p)', 'QZVPP(-g,-f)(2D)++', 'QZVPP(-g,-f)(2D)+', 'aug-QZVPP(-g,-f)(2D)', 'QZVPP(-g,-f)(2D)', 'QZVPP(-g,-f)(2D,2P)++', 'QZVPP(-g,-f)(2D,2P)+', 'aug-QZVPP(-g,-f)(2D,2P)', 'QZVPP(-g,-f)(2D,2P)', 'QZVPP(-g,-f)(2d)++', 'QZVPP(-g,-f)(2d)+', 'aug-QZVPP(-g,-f)(2d)', 'QZVPP(-g,-f)(2d)', 'QZVPP(-g,-f)(2d,2p)++', 'QZVPP(-g,-f)(2d,2p)+', 'aug-QZVPP(-g,-f)(2d,2p)', 'QZVPP(-g,-f)(2d,2p)', 'QZVPP(-g,-f)(2df)++', 'QZVPP(-g,-f)(2df)+', 'aug-QZVPP(-g,-f)(2df)', 'QZVPP(-g,-f)(2df)', 'QZVPP(-g,-f)(2df,2pd)++', 'QZVPP(-g,-f)(2df,2pd)+', 'aug-QZVPP(-g,-f)(2df,2pd)', 'QZVPP(-g,-f)(2df,2pd)', 'QZVPP(-g,-f)PPP++', 'QZVPP(-g,-f)PPP+', 'aug-QZVPP(-g,-f)PPP', 'QZVPP(-g,-f)PPP', 'QZVPP(-g,-f)PP++', 'QZVPP(-g,-f)PP+', 'aug-QZVPP(-g,-f)PP', 'QZVPP(-g,-f)PP', 'QZVPP(-g,-f)(PP)++', 'QZVPP(-g,-f)(PP)+', 'aug-QZVPP(-g,-f)(PP)', 'QZVPP(-g,-f)(PP)', 'QZVPP(-g,-f)++', 'QZVPP(-g,-f)+', 'aug-QZVPP(-g,-f)', 'QZVPP(-g,-f)',"Def2-SV(P)","Def2-SVP","Def2-TZVP","Def2-TZVP(-f)","Def2-TZVP(-df)","Def2-TZVPP","Def2-QZVPP","Def2-QZVPP(-g,-f)","ma-def2-SVP","ma-def2-TZVP","ma-def2-TZVPP","ma-def2-QZVPP","def2-SVPD","def2-TZVPD","def2-TZVPPD","def2-QZVPD","def2-QZVPPD","Def2-aug-TZVPP","PC-1","PC-2","PC-3","PC-4","Aug-PC-1","Aug-PC-2","Aug-PC-3","Aug-PC-4","ano-pVDZ","ano-pVTZ","ano-pVQZ","ano-pV5Z","saug-ano-pVDZ","saug-ano-pVTZ","saug-ano-pVQZ","aug-ano-pVDZ","aug-ano-pVTZ","aug-ano-pVQZ","BNANO-DZP","Bonn-ANO-DZP","BNANO-TZ2P","Bonn-ANO-TZ2P","BNANO-TZ3P","NASA-AMES-ANO","BAUSCHLICHER-ANO","ROOS-ANO-DZP","ROOS-ANO-TZP","DGAUSS","SADLEJ-PVTZ","EPR-II","EPR-III","IGLO-II","IGLO-III","Partridge-1,2,3","Wachters","cc-pVDZ-F12","cc-pVTZ-F12","cc-pVQZ-F12","cc-pVDZ-F12-CABS","cc-pVTZ-F12-CABS","cc-pVQZ-F12-CABS"]

fluctuation_message="" #用于记录震荡的提示，重复的不要输出
opt_flucturation_threshold_shown=False

class Date_Class:
    def __init__(self, link='', datetime_str = '', cycle=0, energy=0):
        self.link = link
        self.cycle = cycle
        self.energy = energy

        try:
            self.datetime = datetime.strptime(datetime_str,"%a %b %d %H:%M:%S %Y")
        except:
            pass

def print_link_List(data=[],running=False,modify_time = datetime.now()):
    returnStr = ""
    Format = ["","","","%H:","%M:","%S"," %m.%d"]

    ave_502=[]
    ave_703=[]


    for i,item in enumerate(data):
        returnStr += "L [" + "{:>4}".format(item.link) + "] End at "
        if i==0:
            returnStr += datetime.strftime(item.datetime,''.join(Format))
        else:
            last = data[i-1]
            delta = item.datetime-last.datetime

            if item.link=="502":
                ave_502.append(delta)
            if item.link=="703":
                ave_703.append(delta)
            # if item.link=='1002' or item.link=='1110':
                # print(item.link,"\t",delta.total_seconds()/60)

            if i==len(data)-16: #在倒数第16个显示完整时间
                returnStr+= "{:>8}".format(datetime.strftime(item.datetime,''.join(Format[:6])))
            else:
                for j in range(3,6):
                    if last.datetime.timetuple()[j] != item.datetime.timetuple()[j]:
                        returnStr+= "{:>8}".format(datetime.strftime(item.datetime,''.join(Format[j:6])))
                        break
                else:
                    returnStr = returnStr [:-4]
                    returnStr+= "{:>12}".format('-')

            if delta.seconds!=0:
                returnStr += " in "

                if delta.days>0:
                    returnStr += "{:>5.1}".format(delta.days+delta.seconds/86400)+"day"

                else:
                    delta_datetime = datetime.strptime(str(delta),"%H:%M:%S")
                    if delta.seconds>=3600:
                        returnStr = returnStr[:-1]
                        returnStr += "{:>6}".format(delta_datetime.strftime('[%H:%M]'))

                    elif delta.seconds>60:
                        returnStr += "{:<6}".format(delta_datetime.strftime('%M\'%Ss'))
                    else:
                        returnStr += "{:>6}".format(str(int(delta_datetime.strftime('%S')))+'s')

        returnStr+='\n'

    # if ave_502:
    #     print("L502:\t",sum(ave_502,timedelta(0)).total_seconds()/len(ave_502)/60)
    # if ave_703:
    #     print("L703:\t",sum(ave_703,timedelta(0)).total_seconds()/len(ave_703)/60)



    if running:
        # print('Running...')
        if len(data)>1: # current link running time
            current_delta = modify_time-data[-2].datetime
        else:
            current_delta = 0

        if current_delta:
            returnStr+="\nCurrent "+ "{:>5}".format("L"+data[-1].link) + " : "
            if current_delta.days>0:
                returnStr += str(current_delta.days)+" day "
            current_delta_datetime = datetime.strptime(re.findall(r"[\d]+:[\d]{2}:[\d]{2}",str(current_delta))[0],"%H:%M:%S")
            returnStr += current_delta_datetime.strftime('%H:%M:%S')


    if running:
        returnStr+='\n\n   '
        total_delta = modify_time-data[0].datetime
    else:
        returnStr+='\n'
        total_delta = data[-1].datetime-data[0].datetime

    returnStr+="Total time : "
    if total_delta.days>0:
        returnStr += str(total_delta.days)+" day "
    total_delta_datetime = datetime.strptime(re.findall(r"[\d]+:[\d]{2}:[\d]{2}",str(total_delta))[0],"%H:%M:%S")
    returnStr += total_delta_datetime.strftime('%H:%M:%S')

    # print("Total wall time:\t",total_delta.total_seconds()/60)

    returnStr+='\n'
    return(returnStr)

def count_pass_through(data, threshold):
    ret = 0
    for count in range(len(data)-1):
        if (data[count]-threshold)*(data[count+1]-threshold)<0:
            ret+=1
    return ret


def unify_basis(input_str:str):
    '''
    Unify multiple writing of the same basis, like 6-31G(d,p) and 6-31G*, def-TZVP and TZVP
    :param input_str:
    :return:
    '''
    input_str = input_str.lower()
    if input_str.endswith("(d,p)"):
        input_str = input_str.replace("(d,p)",'**')
    elif input_str.endswith("(d)"):
        input_str = input_str.replace("(d)",'*')
    elif input_str.startswith('def2-'):
        input_str = input_str.replace('def2-','def2')
    elif input_str.startswith('def-'):
        input_str = input_str.replace('def-','')
    if input_str.startswith('sv(p)'):
        input_str = input_str.replace('sv(p)','sv')
    return input_str

def unify_method(input_str:str):
    input_str = input_str.lower()
    input_str = input_str.replace('pbe1pbe','pbe0')
    input_str = input_str.replace('pbepbe','pbe')
    input_str = ''.join([x for x in input_str if 'a'<=x<='z' or "0"<=x<='9'])
    if input_str.startswith('u') or input_str.startswith('r'): #去掉开壳层闭壳层标记
        input_str = input_str[1:]
    return input_str

def load_factor_database(filename="校正因子.xlsx"):
    import pyexcel
    scaling_factor_database= pyexcel.get_records(file_name=filename)
    for line in scaling_factor_database:
        #储存一个原始的，一个最后的
        line['Basis'] = [line['Basis'],unify_basis(line['Basis'])]
        line['Method'] = [line['Method'],unify_method(line['Method'])]

    return scaling_factor_database

def fluctuation_determine(data=[],atom_count=-1):
    '''

    :param data:
    :param atom_count:  对较大的分子，应增加许可的循环数量
    :return:
    '''

    # 曲线最小值为第n值，取集合data[n:]的min，max
    # 对任意min,max能量间的阈值，计算折线穿越阈值的次数，超过一定次数报震荡

    # 对data[n:]排序，相邻数区间内的穿越次数是相同的，遍历取最大即可。

    min_index = data.index(min(data))
    test_sub_list = data[min_index:]
    test_sub_list.sort()
    thresholds = [(test_sub_list[i]+test_sub_list[i+1])/2 for i in range(len(test_sub_list)-1)]+[data[-1]]

    throughs = [count_pass_through(data,x) for x in thresholds]

    max_through = max(throughs)
    max_through_threshold = thresholds[throughs.index(max(throughs))]

    # print(max_through)
    global fluctuation_message
    global opt_flucturation_threshold_shown
    threshold = atom_count/3 if atom_count>50 else 16
    if not opt_flucturation_threshold_shown:
        print("Using flucturation threshold", threshold)
        opt_flucturation_threshold_shown=True
    if max_through>threshold: # 16 and 1/3 is an arbitrary sensitivity control number
        new_fluctuation_message = get_print_str("Fluctuation detected! Max fluctuation count:",max_through," Threshold:",max_through_threshold)
        if new_fluctuation_message!=fluctuation_message:
            print("Fluctuation detected! Max fluctuation count:",max_through," Threshold:",max_through_threshold)
            fluctuation_message=new_fluctuation_message
        return ("Definitive Fluctuation.",max_through_threshold)
    elif max_through>threshold/2:
        new_fluctuation_message=get_print_str("Possible Fluctuation! Max fluctuation count:",max_through," Threshold:",max_through_threshold)
        if new_fluctuation_message !=fluctuation_message:
            print("Possible Fluctuation! Max fluctuation count:",max_through," Threshold:",max_through_threshold)
            fluctuation_message=new_fluctuation_message
        return ("Possible Fluctuation.",max_through_threshold)
    else:
        return ("",max_through_threshold)


def find_approate_y_limit(data=[],origin_data = [], threshold=6, checkMin = True,atom_count=-1):

    if not origin_data:
        origin_data = data

    if len(data) == 1:
        return (data[0] - 0.01, data[0] + 0.01)
    else:
        fluc_determine_result = fluctuation_determine(data,atom_count=atom_count)
        if checkMin:
            maxData = max(data[data.index(min(data)):])
            DataInterval = maxData - min(data)

            if fluc_determine_result[0]=="Definitive Fluctuation.":
                return (min(data) - DataInterval * 0.1, maxData + DataInterval * 1.5, " Energy Fluctuation! ",fluc_determine_result[1])
            if min(data)!=data[-1]:
                dis_to_global_minimum = (origin_data[-1]-min(origin_data))*2625.499

                delta = [abs(data[-1] - num) for num in data]
                delta.sort()
                delta = [x for x in delta if x!=0]

                data_span = max(data)-min(data)
                if len(delta)<=threshold:
                    if dis_to_global_minimum>0.01:
                        dis_to_global_minimum = "{0:.2f}".format(dis_to_global_minimum)
                        return (min(data) - data_span * 0.3, min(data) + data_span * 1.5, " Global Minimum is "+dis_to_global_minimum+" kJ/mol lower! ")
                    else:
                        return (min(data) - data_span * 0.3, min(data) + data_span * 1.5,"hahaha")
                else:
                    if dis_to_global_minimum>0.01:
                        dis_to_global_minimum = "{0:.2f}".format(dis_to_global_minimum)
                        return (min(data) - DataInterval * 0.3, maxData + min(DataInterval * 10, data_span*1.5) , " Global Minimum is "+dis_to_global_minimum+" kJ/mol lower! ")
                    else:
                        return (min(data) - DataInterval * 0.3, maxData + min(DataInterval * 10, data_span*1.5), "hahaha")
            if fluc_determine_result[0]=="Possible Fluctuation.":
                return (min(data) - DataInterval * 0.1, maxData + DataInterval * 1.5, "Possible Energy Fluctuation.",fluc_determine_result[1])


        delta = [abs(data[-1] - num) for num in data]
        delta.sort()
        delta = [x for x in delta if x!=0]
        data_span = max(data)-min(data)
        if len(delta)>threshold:
            return (min(data) - delta[threshold-1] * 0.3, min(data) + min(delta[threshold-1] * 10, data_span*1.5))

        # 少于threshold个数据
        data_span = max(data)-min(data)
        return (min(data) - data_span * 0.3, min(data) + data_span * 1.5)

            # matrix = [(len(data)-1, i, abs(data[-1] - num)) for i, num in enumerate(data)]
            # matrix.sort(key=lambda x: x[2])
            # matrix = [x for x in matrix if x!=0]
            # if len(matrix) > threshold:
            #     return (min(data) - matrix[threshold][2] * 0.3, min(data) + matrix[threshold][2] * 5)
            # else:
            #     return (min(data) - matrix[-1][2] * 0.3, min(data) + matrix[-1][2] * 5)

class MpWidget_All(Qt.QWidget):
    def __init__(self, parent=None, y=[]):
        super(MpWidget_All, self).__init__()
        self.setParent(parent)
        self.setMinimumSize(Qt.QSize(300, 200))

        self.dpi = 50
        self.fig = MpPyplot.figure(figsize=(1, 1), dpi=self.dpi, )

        self.Cycle_subplot = MpPyplot.subplot2grid((4, 1),(0,0))
        self.opt_subplot = MpPyplot.subplot2grid((4,1),(1,0))
        self.Converged_subplot = MpPyplot.subplot2grid((4,1),(2,0),rowspan=2)

        self.bond_length_axis = self.opt_subplot.twinx()
        self.rmsd_axis = self.Converged_subplot.twinx()

        self.bond_length_axis,self.opt_subplot =self.opt_subplot,self.bond_length_axis

        self.opt_subplot.clear()
        self.opt_subplot.plot(range(len(y)), y, 'r')
        self.Cycle_subplot.clear()
        self.Cycle_subplot.plot(range(len(y)), y, 'r')
        self.Converged_subplot.clear()
        self.Converged_subplot.plot(range(len(y)), y, 'r')

        self.fig.subplots_adjust(top= 0.94, bottom = 0.06,hspace = 0.24, wspace=0.12, left=0.11, right=0.89)

        self.canvas = MpFigureCanvas(self.fig)
        self.canvas.setParent(self)

        self.canvas.draw()

        self.mpl_toolbar = MpNavToolBar(self.canvas, self)

        self.vLayout = Qt.QVBoxLayout()
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.addWidget(self.canvas)
        self.vLayout.addWidget(self.mpl_toolbar)
        self.setLayout(self.vLayout)

        self.converged_data = []
        self.cycle_energy=[]
        self.last_print=[] # record the printing of bond length, prevent redundant bonding printing
        self.opt_data=[]

        self.fluctuation_warned = False
        self.opt_limit = (-1,0)
        self.setParent(parent)


    def opt_Update(self, opt_Energy=[],atom_count=50,bond_length_list = [],show_bond_length = True):
        '''

        :param opt_Energy:  User has to prevent opt_Energy to be an enpty list
        :param atom_count:
        :param bond_length_list:
        :param show_bond_length:
        :return:
        '''

        assert opt_Energy,'Opt Energy List is Empty'

        self.bond_length_list = bond_length_list

        printing_str=""

        for bond in bond_length_list:
            # 最多取25个看大致趋势，不要输出太多数字
            spacing = int(len(bond)/25)+1
            printing_str += " ".join(["{:.2f}".format(x) for count,x in enumerate(bond) if count%spacing==0])+"\n"
        if printing_str!=self.last_print:
            print(printing_str)
            self.last_print=printing_str

        self.bond_length_axis.clear()
        if show_bond_length:
            for bond in bond_length_list:
                self.bond_length_axis.plot(range(1, len(bond) + 1),bond,'#888888')
                self.bond_length_axis.scatter(range(1, len(bond) + 1),bond,marker='o',color='#888888',s=20)

        self.opt_energy_count = len(opt_Energy)
        self.origin_opt_energy = copy.deepcopy(opt_Energy)
        self.atom_count=atom_count
        self.bond_length_list = bond_length_list
        self.show_bond_length = show_bond_length
        opt_Energy = [x*2625.499 for x in opt_Energy]

        # print(opt_Energy)
        # generate logarithm Y scale
        # to prevent log(0)
        presume_dist_to_converge = 0.001
        Opt_Energy_sorted = sorted(list(set(opt_Energy)))
        if len(Opt_Energy_sorted)>2:
            presume_dist_to_converge = Opt_Energy_sorted[1]-Opt_Energy_sorted[0]

        opt_Energy = [math.log10(x-min(opt_Energy)+presume_dist_to_converge) for x in opt_Energy]

        #
        # # 0.001 to prevent log(0)
        # opt_Energy = [math.log10(x-min(opt_Energy)+0.001)+3 for x in opt_Energy]
        # # remove last point to prevent off-scale low at the beginning phase of optimization
        # if len(opt_Energy)>1:
        #     opt_Energy[-1] = opt_Energy[-2]

        # print(opt_Energy)

        self.opt_subplot.clear()
        self.opt_subplot.plot(range(1, len(opt_Energy) + 1), opt_Energy, 'r')
        self.opt_subplot.plot(range(1, len(opt_Energy) + 1), opt_Energy, 'o')


        self.max = max(opt_Energy)
        self.min = min(opt_Energy)

        self.opt_data = copy.deepcopy(opt_Energy)

        if opt_Energy:
            self.opt_limit = find_approate_y_limit(opt_Energy,origin_data= self.origin_opt_energy,atom_count=atom_count)
        else:
            self.opt_limit = (-1,0)


        if (len(self.opt_limit) > 2):
            self.opt_subplot.plot(opt_Energy.index(min(opt_Energy))+1,min(opt_Energy), 'o',color='#FFA400',markersize=9)

            if self.opt_limit[2] == " Energy Fluctuation! ":
                self.opt_subplot.text(0.5, 0.95, self.opt_limit[2], horizontalalignment='center', verticalalignment='top',
                                      fontsize=17, transform=self.opt_subplot.transAxes,
                                      bbox=dict(facecolor='red', alpha=0.5))
                self.opt_subplot.plot((0,len(opt_Energy)+2),(self.opt_limit[3],self.opt_limit[3]),'g--')

            elif self.opt_limit[2] =="Possible Energy Fluctuation.":
                self.opt_subplot.plot((0,len(opt_Energy)+2),(self.opt_limit[3],self.opt_limit[3]),'g--')

            elif "Global Minimum" in self.opt_limit[2]:
                self.opt_subplot.text(0.50, 0.95, self.opt_limit[2], horizontalalignment='center', verticalalignment='top',
                                      fontsize=17, transform=self.opt_subplot.transAxes,
                                      bbox=dict(facecolor='yellow', alpha=0.5))


        self.opt_subplot.set_ylim(*self.opt_limit)
        # self.opt_subplot.set_xlim(0, len(opt_Energy) + 2)


        if len(opt_Energy)>50:
            self.opt_subplot.set_xlim(len(opt_Energy)-50, len(opt_Energy) + 2)
        else:
            self.opt_subplot.set_xlim(0, len(opt_Energy) + 2)

        if self.bond_length_list:
            self.max_bond_length = max(sum(self.bond_length_list,[]))
            self.min_bond_length = min(sum(self.bond_length_list,[]))
            self.delta_bond_length = self.max_bond_length-self.min_bond_length
            self.bond_length_axis.set_ylim(self.min_bond_length - self.delta_bond_length*0.2, self.max_bond_length + self.delta_bond_length*0.5)

        self.canvas.draw()


    def opt_zoom_out(self):
        if self.opt_data:
            self.delta = self.max-self.min
            self.opt_subplot.set_ylim(self.min - self.delta*0.2, self.max + self.delta*0.5)
            self.opt_subplot.set_xlim(0,len(self.opt_data)+2)
            if self.bond_length_list:
                self.max_bond_length = max(sum(self.bond_length_list,[]))
                self.min_bond_length = min(sum(self.bond_length_list,[]))
                self.delta_bond_length = self.max_bond_length-self.min_bond_length
                self.bond_length_axis.set_ylim(self.min_bond_length - self.delta_bond_length*0.2, self.max_bond_length + self.delta_bond_length*0.5)

            self.canvas.draw()

    def opt_zoom_back(self):
        self.opt_Update(self.origin_opt_energy,self.atom_count,self.bond_length_list,self.show_bond_length)
        #
        # if self.opt_data:
        #     self.opt_subplot.set_ylim(*self.opt_limit)
        #     if self.bond_length_list:
        #         self.max_bond_length = max(sum(self.bond_length_list,[]))
        #         self.min_bond_length = min(sum(self.bond_length_list,[]))
        #         self.delta_bond_length = self.max_bond_length-self.min_bond_length
        #         self.bond_length_axis.set_ylim(self.min_bond_length - self.delta_bond_length*0.2, self.max_bond_length + self.delta_bond_length*0.5)
        #
        #     # self.opt_subplot.set_xlim(0,len(self.opt_data)+2)
        #
        # if self.opt_energy_count>50:
        #     self.opt_subplot.set_xlim(self.opt_energy_count-50, self.opt_energy_count + 2)
        # else:
        #     self.opt_subplot.set_xlim(0, self.opt_energy_count + 2)
        #
        #     self.canvas.draw()

    def Cycle_Update(self, Cycle_Energy=[]):

        Cycle_Energy = [x*2625.499 for x in Cycle_Energy]

        # generate logarithm Y scale
        # to prevent log(0)
        presume_dist_to_converge = 1E-7
        Cycle_Energy_sorted = sorted(list(set(Cycle_Energy)))
        if len(Cycle_Energy_sorted)>2:
            presume_dist_to_converge = Cycle_Energy_sorted[1]-Cycle_Energy_sorted[0]

        Cycle_Energy = [math.log10(x-min(Cycle_Energy)+presume_dist_to_converge) for x in Cycle_Energy]
        # # remove last point to prevent off-scale low at the beginning phase of optimization
        # if len(Cycle_Energy)>1:
        #     Cycle_Energy[-1] = Cycle_Energy[-2]

        self.cycle_energy=Cycle_Energy

        self.Cycle_subplot.clear()
        X = range(1, len(Cycle_Energy) + 1)
        Y = Cycle_Energy

        self.Cycle_subplot.plot(X, Y, 'r')
        self.Cycle_subplot.plot(X, Y, 'o')

        self.cycle_max = max(Cycle_Energy)
        self.cycle_min = min(Cycle_Energy)


        try:
            self.Cycle_limit = find_scf_process_y_limit(Cycle_Energy)
        except:
            self.cycle_delta = self.cycle_max-self.cycle_min
            self.Cycle_limit = [self.cycle_min - self.cycle_delta*0.2, self.cycle_max + self.cycle_delta*0.2,len(self.cycle_energy)+1]

        self.length = len(Cycle_Energy)

        self.Cycle_subplot.set_ylim(*self.Cycle_limit[:2])

        range_min = self.Cycle_limit[2]
        range_max = self.Cycle_limit[2]+int((self.length-self.Cycle_limit[2])*1.1)+1
        if range_max - range_min >= 6:
            self.Cycle_subplot.set_xlim(range_min, range_max)
        else:
            self.Cycle_subplot.set_xlim(max(0,len(Cycle_Energy)-6),len(Cycle_Energy)+1)

        self.canvas.draw()

    def cycle_zoom_out(self):
        if self.cycle_energy:
            self.cycle_delta = self.cycle_max-self.cycle_min
            self.Cycle_subplot.set_ylim(self.cycle_min - self.cycle_delta*0.2, self.cycle_max + self.cycle_delta*0.2)
            self.Cycle_subplot.set_xlim(0,len(self.cycle_energy)+1)
            self.canvas.draw()

    def cycle_zoom_back(self):
        if self.cycle_energy:
            self.Cycle_subplot.set_ylim(*self.Cycle_limit[:2])

            range_min = self.Cycle_limit[2]
            range_max = self.Cycle_limit[2]+int((self.length-self.Cycle_limit[2])*1.1)+1
            if range_max - range_min >= 6:
                self.Cycle_subplot.set_xlim(range_min, range_max)
            else:
                self.Cycle_subplot.set_xlim(max(0,len(self.cycle_energy)-6),len(self.cycle_energy)+1)

            self.canvas.draw()

    def Converged_Update(self, data=[],geometries=[]):

        self.original_converged_data = copy.deepcopy(data)
        self.rmsd_geometries = copy.deepcopy(geometries)

        self.converged_data = data
        self.converged_data_backup = copy.deepcopy(data)

        self.converged_max = max([max(i) for i in data])
        self.converged_min = min([min(i) for i in data])
        self.converged_count = len(data)

        self.rmsd_axis.clear()
        self.rmsd = []
        if geometries:
            self.rmsd = generate_rmsd_list(geometries[-1],geometries[:-1],print_percentage=False)


        self.Converged_subplot.clear()
        self.Converged_subplot.plot((0,len(data)+2),(1,1),'g--')

        #(set, i, num) set: which criteria, i: which step, num: value
        Data_tuple = [(set,i,num) for i,list in enumerate(data) for set,num in enumerate(list)]
        Data_Converged = ([i+1 for set,i,num in Data_tuple if num<=1 ],[num for set,i,num in Data_tuple if num<=1 ])
        Data_Not_Converged = [(set,i+1,num) for set,i,num in Data_tuple if num>1 ]

        color = ['#FFA400','b','r','m','#888888']
        label = ["Max F","RMS F","Max D","RMS D",'Energy']

        if len(data[0])==4:
            self.Converged_subplot.plot(Data_Converged[0], Data_Converged[1], 'o',color='#00FF00')
        elif len(data[0])==5:
            self.Converged_subplot.scatter(Data_Converged[0], Data_Converged[1], marker = 'o',color='#00FF00',s=20)

        for set in range(len(data[0])):
            data_this_set = [x[set] for x in data]
            self.Converged_subplot.plot(range(1, len(data) + 1), data_this_set, color=color[set],label = label[set])

            plot_x = [item[1] for item in Data_Not_Converged if item[0]==set]
            plot_y = [item[2] for item in Data_Not_Converged if item[0]==set]
            if len(data[0])==4:
                self.Converged_subplot.plot(plot_x,plot_y,'o',color=color[set])
            elif len(data[0])==5:
                self.Converged_subplot.scatter(plot_x,plot_y,marker='o',color=color[set],s=20)

        if self.rmsd:
            self.rmsd_axis.plot(range(1, len(self.rmsd) + 1), self.rmsd, color='#00aaaa',label = 'RMSD')
            self.rmsd_axis.set_ylim(-0.005, max(max(self.rmsd[-50:]) + (max(self.rmsd[-50:])-min(self.rmsd[-50:]))*3,0.5))

        if self.converged_count>50:
            self.Converged_subplot.set_xlim(len(data)-50, len(data) + 2)
        else:
            self.Converged_subplot.set_xlim(0, len(data) + 2)

        self.upperLimit = max([max(x[-30:]) for x in data])

        self.Converged_subplot.set_ylim(10**(-2),self.upperLimit*10)
        self.Converged_subplot.set_yscale('log')
        # self.Converged_subplot.legend(loc='upper left',bbox_to_anchor=(0.02,0.98))
        if len(data[0])==4:
            self.Converged_subplot.legend(borderaxespad=0.,bbox_to_anchor=(0., 0.98),loc='upper left',ncol=2)
        elif len(data[0])==5:
            self.Converged_subplot.legend(borderaxespad=0.,bbox_to_anchor=(0., 0.98),loc='upper left',ncol=3)

        self.canvas.draw()

    def converged_zoom_out(self):
        if self.converged_data:
            self.converged_delta = self.converged_max / self.converged_min
            self.Converged_subplot.set_ylim(min(self.converged_min / self.converged_delta**0.2,10**(-2)), self.converged_max * self.converged_delta**0.2)
            self.Converged_subplot.set_xlim(0,self.converged_count+1)
            self.canvas.draw()

        if hasattr(self,"rmsd") and self.rmsd:
            self.rmsd_axis.set_ylim(-0.005, max(max(self.rmsd) + (max(self.rmsd)-min(self.rmsd))*3,0.5))


    def converged_zoom_back(self):
        self.Converged_Update(self.converged_data,self.rmsd_geometries)
        # if self.converged_data:
        #     self.Converged_subplot.set_ylim(10**(-2),self.upperLimit*10**0.2)
        #     if self.converged_count>50:
        #         self.Converged_subplot.set_xlim(self.converged_count -50, self.converged_count + 2)
        #     else:
        #         self.Converged_subplot.set_xlim(0, self.converged_count + 2)
        #     self.canvas.draw()


def find_scf_process_y_limit(energies:list):
    # input a list of energy, give the appropriate y limit,
    #  to show reasonable amount of point, but also reasonable resolution
    # example: -2130.1126, -2140.287717, -1685.757423, -2081.089339, -2093.857316, -2111.060361, -2161.96741, -2099.048807, -2149.287184, -2120.794705, -2162.410932, -2168.674928, -2171.365843, -2174.757894, -2173.607835, -2161.738868, -2175.859649, -2175.82097, -2176.196842, -2177.02269, -2176.744028, -2174.877316, -2175.645007, -2177.118231, -2177.164741, -2177.420542, -2177.305265, -2175.242023, -2176.836426, -2176.945783, -2176.479612, -2177.341249, -2177.39717, -2177.306138, -2177.285423, -2177.418284, -2177.229911, -2177.370679, -2177.340789, -2177.337012, -2177.344469, -2177.494044, -2177.449827, -2177.404641, -2177.436185, -2177.437823, -2177.376321, -2177.393095, -2177.41868, -2177.499767, -2177.416989, -2177.419145, -2177.416779, -2177.406059, -2177.407201, -2177.41017, -2177.40809, -2177.418699, -2177.426296, -2177.425052, -2177.425179, -2177.424793, -2177.424941, -2177.493018, -2177.435653, -2177.462163, -2177.470236, -2177.474246, -2177.476369, -2177.477708, -2177.478652, -2177.47934, -2177.479866, -2177.480289, -2177.48066, -2177.480984, -2177.481272, -2177.481536, -2177.481778, -2177.482023, -2177.482253, -2177.482474, -2177.482685, -2177.482889, -2177.483084, -2177.483275, -2177.483459, -2177.483638, -2177.483812, -2177.483981, -2177.484147, -2177.484308, -2177.484466, -2177.48462, -2177.484771, -2177.484919, -2177.485064, -2177.485207, -2177.485346, -2177.48552, -2177.485667, -2177.485869, -2177.486049, -2177.486267, -2177.486479, -2177.486768, -2177.487028, -2177.487284, -2177.487504, -2177.487689, -2177.487812, -2177.48801, -2177.488204, -2177.488437,
    # give something like [-2177.49, -2177.48]

    # the last point must be insight

    # return a three-tuple: [y-limit_min, y-limit_max, x_limit_min]


    if len(energies)<=2:
        dist = abs(energies[-1]-energies[0])
        return [min(energies)-dist*1.3-0.01,max(energies)+dist*1.3+0.01,0]


    last = energies[-1]

    # 从最后一个元素依次前数，所需区间有多大
    pos_interval = [(min(energies[-x:]),max(energies[-x:])) for x in range(2,len(energies)+1)]
    pos_interval = [(x[0]-(x[1]-x[0])*0.3,x[1]+(x[1]-x[0])*0.3) for x in pos_interval] # 扩大30%

    # 区间内有哪些元素
    interval_element = [[x for x in energies if interval[0]<=x<=interval[1]]
                        for interval in pos_interval] # 能显示多少个值
    interval_element = [sorted(x) for x in interval_element]

    # 分辨率
    interval_resolution=[]
    for interval in interval_element:

        if interval[-1]==interval[0]:
            interval_resolution.append(0)
        else:
            ret = [(interval[x+1]-interval[x])/(interval[-1]-interval[0]) for x in range(len(interval)-1)]
            ret = sum([x**(-2) for x in ret])/len(ret) # 取二次倒数平均，以去除特别大的interval的影响
            interval_resolution.append(ret**(-1/2))


    score = []
    for count in range(len(interval_element)):
        # 平均分辨率乘以元素个数，即，如果是线性的曲线，可以全部显示
        # 在分辨率上给了1.1次方，稍微倾向于分辨
        score.append((len(interval_element[count]))*(interval_resolution[count]**1.1))

    #在区间内只有两个元素的时候，定义的分辨率是100%，故需要忽略区间只包含两个元素的情况
    for count in range(len(interval_element)):
        if len(interval_element[count])==2:
            score[count] = 0

    # for i in score:
    #     print(i)

    for count in range(len(interval_element)-1,-1,-1):
        if score[count]>[x for x in score if x][0]*0.1: #把前面的零值去掉
            ret_index = count
            break
    else:
        ret_index = score.index(max(score))


    high = interval_element[ret_index][-1]
    low = interval_element[ret_index][0]
    dist = high-low
    ret = [low-dist*0.2,high+dist*0.2]

    x_min = 0
    for i in range(len(energies)):
        if ret[0]<=energies[i]<=ret[1]:
            x_min=i
            break

    return ret+[x_min]


def read_comp_config():
    '''
    read computer configurations from Comp_configs.txt
    :return:a list of dict, each dict contains the information like system, path, etc.
    '''

    with open('Comp_configs.txt') as file:
        file = file.readlines()
    file = [x.strip() for x in file][2:] # 删掉说明行
    file = split_list_by_item(file,"")

    ret = []

    for computer in file:

        temp = collections.OrderedDict()
        temp['title'] = computer[0]
        temp["system"]=computer[1].lstrip("system=")
        temp['path']=computer[2].lstrip("path=")
        temp['mem']=float(computer[3].lstrip("mem="))
        temp['proc']=int(computer[4].lstrip("proc="))

        ret.append(temp)

    return ret


class RS_from_pdb:
    def __init__(self,pdb_file:str):
        with open(pdb_file) as pdb_file:
            self.pdb_file = pdb_file.readlines()
        #according to the PDB format standard
        coord = []

        for line in self.pdb_file:
            if line.startswith('HETATM'):
                atom = line[12:16]
                xyz=line[30:54]
                coord.append(atom+xyz)

        self.coord = Coordinates(coord)

        self.connectivity = [[] for x in range(self.coord.atom_count)]
        for line in self.pdb_file:
            if line.startswith("CONECT"):
                line.split()
                center_atom = int(line[1])
                self.connectivity[center_atom] = [int(x) for x in line[2:]]


class Coordinates:
    def __init__(self,coordinates = [],charge=999,multiplet = 999,selected_atom_range = []):
        '''

        :param coordinates:  a list of lines containing coordinate information, several accepted format is supported
        :param charge:
        :param multiplicity:
        :return:
        '''

        if isinstance(coordinates,str) and os.path.isfile(coordinates):
            #可以传一个文件进来，读取最后一个坐标，不过charge和multiplet读不了，需要指定
            self.coordinates=[]
            with open(coordinates) as coordinates_file:
                coordinates_lines = coordinates_file.readlines()
            for count in range(len(coordinates_lines)-1,-1,-1):
                line = coordinates_lines[count]
                if std_coordinate(line):
                    #插入时是倒序的
                    self.coordinates.append(std_coordinate(line))
                    for coord_line_count in range(count-1,-1,-1):
                        self.coordinates.append(std_coordinate(coordinates_lines[coord_line_count]))
                        if not self.coordinates[-1]:
                            self.coordinates.pop()
                            break
                    self.coordinates.reverse()
                    break
        elif isinstance(coordinates,list):
            self.coordinates = [std_coordinate(x) for x in coordinates]
        else:
            alert_UI("Coordinates object input invalid.")
            exit()


        if selected_atom_range:
            self.coordinates = [x for count,x in enumerate(self.coordinates) if count in selected_atom_range]

        self.charge = int(charge)
        self.multiplicity = int(multiplet)

        if None in self.coordinates:
            print("Internal coordinate system. Further coordinate operation not supported.")
            self.is_fault = True

        else:
            self.is_fault = False
            self.elements = [coord.split('\t')[0].upper() for coord in self.coordinates]
            self.coordinates_numer = [[float(x) for x in coord.split('\t')[1:4]] for coord in self.coordinates]
            self.coordinates_np = [np.array(coord) for coord in self.coordinates_numer]
            self.atom_count = len(self.coordinates_numer)

            # self.get_distance_matrix()

    def replace_element(self,element_list):
        assert len(element_list)==self.atom_count
        #用于构象搜索时替换元素
        self.elements=element_list
        self.coordinates = [element_list[count]+"\t"+"\t".join(coord.split('\t')[1:]) for count,coord in enumerate(self.coordinates)]

    def get_distance_matrix(self):

        if not hasattr(self,'distance_matrix'):
            self.distance_matrix = [[-1]*self.atom_count for i in range(self.atom_count)] # n*n matrix
            for i in range(self.atom_count):
                self.distance_matrix[i][i]=0
            for i in range(self.atom_count):
                for j in range(i):
                    distance = np.linalg.norm(self.coordinates_np[i]-self.coordinates_np[j])
                    self.distance_matrix[i][j]=distance
                    self.distance_matrix[j][i]=distance
            assert -1 not in sum(self.distance_matrix,[]),'Distance Matrix Error'

        return self.distance_matrix

    def __hash__(self):
        #用于放到excel里用来表明结构相同性的数值，这个hash的重复处理的不好，谨慎使用
        hash_num = sorted(sum(self.get_distance_matrix(),[]))
        hash_num = int((sum(hash_num,0)*10000)%1000000) # 精确到5位，取后六位

        return hash_num #取一个6位的hash

    def is_linear(self):
        if len(self.coordinates)<=2:
            return True

        #分子共线性判断
        #得到第一个原子和第二个原子的坐标

        coord_0 = self.coordinates_np[0]
        coord_1 = self.coordinates_np[1]
        ref_distance_vec = coord_1-coord_0 # -->(C1-C2)
        ref_distance_norm = np.linalg.norm(ref_distance_vec) # |-->(C1-C2)|

        for coord in self.coordinates_np[2:]:
            distance_vec = coord-coord_0  # -->(C1-Cn)
            distance_norm = np.linalg.norm(distance_vec) # |-->(C1-Cn)|

            ratio = distance_norm / ref_distance_norm # norm ratio
            compair_vec = ref_distance_vec*ratio # if the molecule is linear, this should be exact eq to _distance_vec_

            # the diff_vec can be scaled in two directions, chose the smaller one
            pos_diff_vec = (distance_vec-compair_vec)/ratio
            neg_diff_vec = (distance_vec+compair_vec)/ratio

            # 若差的模大于5E-6(相当于[2E-6,2E-6,2E-6])，判定为非线性
            if min(np.linalg.norm(pos_diff_vec),np.linalg.norm(neg_diff_vec))>5E-6:
                return False

        return True

    def __eq__(self, other):
        #原子顺序不得改变，但分子可旋转
        assert isinstance(other,Coordinates)

        if self.atom_count!=other.atom_count:
            return False

        if self.elements != other.elements:
            return False
        
        if hasattr(self,'distance_matrix'):
            self_distance_matrix = self.distance_matrix
        else:
            self_distance_matrix=self.get_distance_matrix()

        if hasattr(other,'distance_matrix'):
            other_distance_matrix = other.distance_matrix
        else:
            other_distance_matrix=other.get_distance_matrix()
        
        diff_distance_matrix = np.array(sum(self_distance_matrix,[]))-np.array(sum(other_distance_matrix,[]))
        diff_distance_matrix=[abs(x) for x in list(diff_distance_matrix)]
        if max(diff_distance_matrix)>2E-6:
            return False

        return True

    def __str__(self):
        return '\n'.join(self.coordinates)

    def gjf(self,title='Geometry from coordinate object'):
        return '#p\n\n'+title.strip()+'\n\n0 1\n'+str(self)

def get_bond_order_from_mol2_file(file,selected_atoms = []):
    '''
    get the bond order information in mol2 file
    :param file:
    :param exclude_atoms: 用于排除其中的几个原子，搞自由基的时候用
    :return: a list of 3-tuples, (atom1, atom2, bond_order)
    '''

    ret=[]

    with open(file) as mol2_file:
        mol2_file_lines = mol2_file.readlines()

    for count,line in enumerate(mol2_file_lines):
        if "@<TRIPOS>BOND" in line:
            for bonding_line in mol2_file_lines[count+1:]:
                if '@' in bonding_line:
                    break
                bonding_line = bonding_line.replace('ar','1') #芳香键问题
                ret.append([int(x) for x in bonding_line.split()[1:]])

            break
    ret = sorted([sorted([atom1-1,atom2-1])+[bond_order] for atom1,atom2,bond_order in ret])
    # print(ret)
    if selected_atoms:
        ret = [x for x in ret if x[0] in selected_atoms and x[1] in selected_atoms]

        max_num = max(sum([bond[:2] for bond in ret],[]))

        swap_pair=collections.OrderedDict()
        #因为去掉了一些，所以后面的原子要前移
        for x in range(max_num+1):
            swap_pair[x] = x-len([i for i in range(x) if i not in selected_atoms])

        for bond in ret:
            bond[0] = swap_pair[bond[0]]
            bond[1] = swap_pair[bond[1]]

    return ret


class Dihedral:
    def __init__(self,coordinate:Coordinates, atom_indexes):
        '''

        :param coordinate:
        :param atom_indexes:  should be left-atom, center_bond1, center_bond2, right-atom. center_bond1 must be smaller than center_bond2
        :return:
        '''
        # read this for the symbols http://math.stackexchange.com/questions/47059/how-do-i-calculate-a-dihedral-angle-given-cartesian-coordinates

        assert len(atom_indexes)==4
        self.coordinate = coordinate
        self.atom_indexes = atom_indexes
        self.atom1, self.atom2, self.atom3, self.atom4 = self.atom_indexes
        self.atom_index_compare = 1E12*self.atom1+1E8*self.atom2+1E4*self.atom3+self.atom4 # 产生一个数字，用于两对象相同的快速比对，假设原子坐标不会超过10000

        assert self.atom2<self.atom3 #应该以此顺序传入
        self.elements = [self.coordinate.elements[index] for index in self.atom_indexes]

        # calculate dihedral
        self.coord1, self.coord2, self.coord3, self.coord4 = [self.coordinate.coordinates_np[index] for index in self.atom_indexes]

        self.vec1 = self.coord2 - self.coord1
        self.vec2 = self.coord3 - self.coord2
        self.vec3 = self.coord4 - self.coord3

        self.normal1=np.cross(self.vec1,self.vec2)
        self.normal2=np.cross(self.vec2,self.vec3)

        self.normal1 = self.normal1/np.linalg.norm(self.normal1)
        self.normal2 = self.normal2/np.linalg.norm(self.normal2)

        self.x = self.normal1
        self.y = self.vec2/np.linalg.norm(self.vec2)
        self.z = np.cross(self.x, self.y)

        self.n2_x = np.dot(self.normal2,self.x)
        self.n2_y = np.dot(self.normal2,self.z)

        self.dihedral = -math.atan2(self.n2_y,self.n2_x)/math.pi*180

    def __lt__(self, other):
        if self.atom2!=other.atom2:
            return self.atom2<other.atom2
        elif self.atom3!=other.atom3:
            return self.atom3<other.atom3
        elif self.atom1!=other.atom1:
            return self.atom1<other.atom1
        return self.atom4<other.atom4

    def __eq__(self, other):
        return self.atom_index_compare==other.atom_index_compare

    def __gt__(self, other):
        return not self<other and not self==other

    def __ge__(self, other):
        return not self<other

    def __le__(self, other):
        return self<other or self==other

    def __sub__(self, other):
        # return the abs() of angle difference of two dihedral angle
        # note that -180 and 180 are the same point, -170 and 170 has difference of 20
        # it will verify the atom indexes are the same
        assert self.atom_indexes==other.atom_indexes

        candidate = [abs(self.dihedral-other.dihedral),abs(self.dihedral+360-other.dihedral),abs(self.dihedral-360-other.dihedral)]

        return min(candidate)

    def __str__(self):
        return '-'.join([self.coordinate.elements[x] for x in self.atom_indexes])+" "\
               +'-'.join([str(x+1) for x in self.atom_indexes])\
               +'  {:.2f}'.format(self.dihedral)

def get_dihedrals(coordinate:Coordinates,
                  bond_orders = [],
                  ignore_hydrogens = True,
                  return_dict=False,
                  only_pick_one_necessary=True):
    '''
    :param coordinate:
    :param bond_orders: 从mol2文件读入的bond order，list of 3-tuple，或者没有bond order也可以，list of 2-tuple；如果此参数为空，将用mogli判断的键级
    :param ignore_hydrogens: 是否计算含H的二面角，默认为否
    :param return_dict: 如果开启，将*额外*返回一个字典，用于通过四原子tuple访问二面角对象
    :param only_pick_one_necessary: 如果开启，即假设键角不变，如乙烷的3*3共9个二面角中，只挑选1个代表
    :return: if not return dict: a list of Dihedral objects;
             else: a two tuple, the first is the above list; the second is a dict, the dict can be accessed by
                        dict[(1,2,3,4)] == dict[(4,3,2,1)]
    '''

    if isinstance(coordinate, tuple) and bond_orders==[]:
        # 从pool传过来的
        coordinate, bond_orders,ignore_hydrogens,return_dict,only_pick_one_necessary=coordinate

    # print(coordinate)
    temp_filename = 'temp.xyz'
    with open(temp_filename,'w') as temp_structure_file:
        temp_structure_file.write(str(coordinate.atom_count))
        temp_structure_file.write("\nTemp file for Molecule object\n")
        temp_structure_file.write(str(coordinate))

    if not bond_orders:
        bonds = get_bonds(temp_filename)
        print("Warning, bond order not pre-specified in dihedral calculation")
    else:
        bonds = [x[0:2] for x in bond_orders]

    connection_table = bonds_to_connect_table(coordinate,bonds)
    single_bonding_atoms = [x for x in range(coordinate.atom_count) if len(connection_table[x])==1]
    hydrogens = [atom for atom in range(coordinate.atom_count) if coordinate.elements[atom]=='H']

    ret = []


    #选取一根键，找两边的键，做排列组合
    for bond in bonds:

        # if bond[0]==4 and bond[1]==7:
        #     print("test")

        assert bond[0]<bond[1],'Bonds setting error.'
        left_bonding_atoms = [x for x in connection_table[bond[0]] if x!=bond[1]]
        right_bonding_atoms = [x for x in connection_table[bond[1]] if x!=bond[0]]

        # print(left_bonding_atoms)
        # print(right_bonding_atoms)
        
        # 如果键连的几个原子相同，直接忽略其二面角，如CF3整体旋转120°；对同取代烯烃相同
        have_CX3 = False
        for bonding_atoms in [left_bonding_atoms, right_bonding_atoms]:
            have_CX3 = len(bonding_atoms) in [2,3] and \
                       not [x for x in bonding_atoms if x not in single_bonding_atoms] and \
                       len(set([coordinate.elements[x] for x in bonding_atoms]))==1
            if have_CX3:
                break

        if have_CX3:
            continue

        # 如果键连的三个原子中有两个原子都是单键原子且相同，则认定余下的一个为关键原子
        def remove_duplicate_nonbonding_atom(bonding_atoms):
            if len(bonding_atoms)==3:
                singles = [x for x in bonding_atoms if x in single_bonding_atoms]
                if len(singles)>1:
                    singles_elements = [coordinate.elements[x] for x in singles]
                    duplicate_element = [x for x in singles_elements if singles_elements.count(x)>1]
                    if duplicate_element:
                        return [x for x in bonding_atoms if not(x in singles and coordinate.elements[x]==duplicate_element[0])]
            return bonding_atoms


        if only_pick_one_necessary:
            left_bonding_atoms = remove_duplicate_nonbonding_atom(left_bonding_atoms)
            right_bonding_atoms = remove_duplicate_nonbonding_atom(right_bonding_atoms)
        # print("left",left_bonding_atoms)
        # print("right",right_bonding_atoms)

        found_one = False
        for left_atom in left_bonding_atoms:

            if found_one and only_pick_one_necessary:
                break
            if ignore_hydrogens and left_atom in hydrogens:
                continue

            for right_atom in right_bonding_atoms:

                if found_one and only_pick_one_necessary:
                    break
                if ignore_hydrogens and right_atom in hydrogens:
                    continue

                ret.append(Dihedral(coordinate,[left_atom]+bond+[right_atom]))
                found_one=True

    ret.sort()
    if not return_dict:
        return ret
    else:
        ret_dict = {}
        for dihedral in ret:
            ret_dict[tuple(dihedral.atom_indexes)]=dihedral
            ret_dict[tuple(reversed(dihedral.atom_indexes))]=dihedral
        return (ret,ret_dict)

def bonds_to_connect_table(coordinate:Coordinates, bonds):
    '''

    :param bonds: list of 2-tuple bonds, index start from 0
    :return: a list, length same as the atom count, of lists
    '''
    ret = [[] for x in range(coordinate.atom_count)]
    for atom in range(coordinate.atom_count):
        ret[atom] = [bond for bond in bonds if atom in bond]
        ret[atom] = [bond[0] if bond[0]!=atom else bond[1] for bond in ret[atom]]

    return ret


class Molecule_Stereo:
    def __init__(self,coordinates:Coordinates,bond_orders = []):
        '''
        ZE的判断需要bond order提前定义好
        :param coordinates:
        :param bond_orders: a list of 3-tuples, (atom1, atom2, bond-order)
        :return:
        '''
        self.coordinates = coordinates
        temp_filename = 'temp.xyz'
        with open(temp_filename,'w') as temp_structure_file:
            temp_structure_file.write(str(coordinates.atom_count))
            temp_structure_file.write("\nTemp file for Molecule object\n")
            temp_structure_file.write(str(coordinates))

        self.bond_orders=bond_orders
        self.bonds_detected = get_bonds(temp_filename)
        if not self.bond_orders:
            self.bonds = self.bonds_detected
        else:
            self.bonds = [x[0:2] for x in self.bond_orders]
        self.bonds_str = ", ".join(["-".join([str(atom) for atom in x]) for x in self.bonds])

        self.has_bond_order = True if self.bond_orders else False
        self.methyl_carbons = []
        self.recognize_methyl_carbon()

        self.get_chirality()
        self.get_ZE()


    def recognize_methyl_carbon(self):
        #包括甲基和三氟甲基
        for atom in range(self.coordinates.atom_count):
            bonding_atoms = [pair[0] if pair[0]!=atom else pair[1] for pair in self.bonds if atom in pair]
            if len(bonding_atoms)==4:
                if len([H_check for H_check in bonding_atoms if self.coordinates.elements[H_check]=='H'])==3:
                    self.methyl_carbons.append(atom)
                if len([H_check for H_check in bonding_atoms if self.coordinates.elements[H_check]=='F'])==3:
                    self.methyl_carbons.append(atom)


    def get_chirality(self):
        '''

        :return: a list of chirality of each atom, 0 for no chiral, 1 for positive projection, -1 for neg
        '''

        self.chirality = [0 for x in range(self.coordinates.atom_count)]
        for atom in range(self.coordinates.atom_count):
            bonding_atoms = [pair[0] if pair[0]!=atom else pair[1] for pair in self.bonds if atom in pair]
            if len(bonding_atoms)==4:

                #亚甲基、甲基、三氟甲基等的氢、氟容易两个互相翻转，数相同元素的数量，如果有两个无其他成键的原子（如H，卤素）就排除掉
                #选取某个碳上连接的所有无其他键连的元素，考虑有无重复的
                non_bonding_atoms=[atom2 for atom2 in bonding_atoms if len([pair for pair in self.bonds if atom2 in pair])==1]
                element_of_non_bonding_atoms = [self.coordinates.elements[atom2] for atom2 in non_bonding_atoms]
                if len(set(element_of_non_bonding_atoms))<len(element_of_non_bonding_atoms):
                    continue

                #去除甲基碳
                if len([x for x in bonding_atoms if x in self.methyl_carbons])>1:
                    continue

                bonding_atoms.sort()
                bonding_coord = [self.coordinates.coordinates_np[atom] for atom in bonding_atoms]
                #以序号最小的原子为原点，计算其他三个原子的相对坐标
                rel_coord = [bonding_coord[i]-bonding_coord[0] for i in range(1,4)]
                #将序号最大的向量向其他两个向量的叉乘上投影
                projection = np.dot(rel_coord[2],np.cross(*rel_coord[0:2]))
                self.chirality[atom] = int(np.sign(projection))

        self.chirality_str = "".join(["P" if x>0 else "N" if x<0 else "-" for x in self.chirality])

    def get_ZE(self):
        self.ZE = [0 for x in range(self.coordinates.atom_count)]
        if self.bond_orders:
            for atom1,atom2,bond_order in self.bond_orders:
                if bond_order==2:
                    # print(atom1,atom2)
                    # 只支持C
                    # N的翻转无特殊情况被视为同一种结构，有需要的时候直接改代码
                    bonding_atoms1 = [pair[0] if pair[0]!=atom1 else pair[1] for pair in self.bonds if atom1 in pair]
                    bonding_atoms2 = [pair[0] if pair[0]!=atom2 else pair[1] for pair in self.bonds if atom2 in pair]
                    element1 = self.coordinates.elements[atom1].strip().lower()
                    element2 = self.coordinates.elements[atom2].strip().lower()

                    # print(element1,element2,bonding_atoms1,bonding_atoms2)

                    ######################################
                    # if you wants C=N-R Z/E inversion to be forbiddened, activate the following if statement
                    # if ((element1=='c' and len(bonding_atoms1)==3) or (element1=='n' and len(bonding_atoms1)==2)) and \
                    #    ((element2=='c' and len(bonding_atoms2)==3) or (element2=='n' and len(bonding_atoms2)==2)):

                    ######################################
                    # if you wants C=N-R Z/E inversion to be allowed, activate the following if statement
                    if (element1=='c' and len(bonding_atoms1)==3) and (element2=='c' and len(bonding_atoms2)==3):
                        # for R1-C1(-R2)=C2(-R3)-R4, get vector of R1-C1, and R3-C2
                        # result for C1 and C2 should be the same

                        #亚甲基、甲基、三氟甲基等的氢、氟容易两个互相翻转，数相同元素的数量，如果有两个无其他成键的原子（如H，卤素）就排除掉
                        #选取某个碳上连接的所有无其他键连的元素，考虑有无重复的
                        non_bonding_atoms=[test_atom for test_atom in bonding_atoms1 if len([pair for pair in self.bonds if test_atom in pair])==1]
                        element_of_non_bonding_atoms = [self.coordinates.elements[test_atom] for test_atom in non_bonding_atoms]
                        if len(set(element_of_non_bonding_atoms))==1:
                            continue
                        non_bonding_atoms=[test_atom for test_atom in bonding_atoms2 if len([pair for pair in self.bonds if test_atom in pair])==1]
                        element_of_non_bonding_atoms = [self.coordinates.elements[test_atom] for test_atom in non_bonding_atoms]
                        if len(set(element_of_non_bonding_atoms))==1:
                            continue

                        atom1,atom2 = sorted([atom1,atom2])
                        R1 = min([x for x in bonding_atoms1 if x not in [atom1, atom2]])
                        R3 = min([x for x in bonding_atoms2 if x not in [atom1, atom2]])

                        vector1 = self.coordinates.coordinates_np[R1]-self.coordinates.coordinates_np[atom1]
                        vector2 = self.coordinates.coordinates_np[R3]-self.coordinates.coordinates_np[atom2]

                        projection = np.dot(vector1,vector2)
                        self.ZE[atom1] = int(np.sign(projection))
                        self.ZE[atom2] = int(np.sign(projection))
                        # break

        self.ZE_str = "".join(["A" if x>0 else "B" if x<0 else "-" for x in self.ZE])
        self.stereo_str = "".join([self.ZE_str[count] if self.ZE_str[count]!='-' else self.chirality_str[count] for count in range(len(self.ZE_str))])


def print_incorrect_chiral(std_chiral,current_chiral):
    label = []
    for i in range(int(len(std_chiral)/10)+1):
        if i<10:
            label.append(" "+str(i))
        else:
            label.append(str(i))
        label.append("1234567890")

    ret = "".join(label)+"\n"
    ret += "  "+"  ".join([std_chiral[x:x+10] for x in range(0,len(std_chiral),10)])+'\n'
    ret += "  "+"  ".join([current_chiral[x:x+10] for x in range(0,len(current_chiral),10)])

    print(ret)
    return ret

def std_coordinate(line):
    '''
    A input line, allowed format see below
    :return: A standardized coordinate output; if no coordinate was found, return None
    '''
    re_patterns = [] # store the possible reg_ex patterns, each pattern should return a list:
                        # [symbol or No., X, Y, Z]

    #  C                    -0.46615   1.1295   -1.46282 "
    # C19	2.197	5.321	-4.291 (amber)
    re_patterns.append(r'([A-Z][a-z]{0,2})\d*\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)')

    # ---------------------------------------------------------------------
    # Center     Atomic      Atomic             Coordinates (Angstroms)
    # Number     Number       Type             X           Y           Z
    # ---------------------------------------------------------------------
    #      1          6           0        0.420470   -1.186773   -0.704665

    re_patterns.append(r"\d+\s+(\d+)\s+\d+\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)")
    # 这个必须放在下一个上面


    #                Cartesian Coordinates (Ang):
    # ---------------------------------------------------------------------
    # Center     Atomic                     Coordinates (Angstroms)
    # Number     Number                        X           Y           Z
    # ---------------------------------------------------------------------
    #      1          6                    0.839826   -1.280127    0.071692

    re_patterns.append(r"\d+\s+(\d+)\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)")

    # C,0,0.4732857814,-1.2321049177,-0.7321261073
    re_patterns.append(r"([A-Z][a-z]{0,2}),\d+,(-*\d+\.\d*),(-*\d+\.\d*),(-*\d+\.\d*)")
    # 'C,2.8527268394,0.1892117596,0.7450890036'
    re_patterns.append(r"([A-Z][a-z]{0,2}),(-*\d+\.\d*),(-*\d+\.\d*),(-*\d+\.\d*)")

    # ----------------------------
    # CARTESIAN COORDINATES (A.U.)
    # ----------------------------
      # NO LB      ZA    FRAG    MASS        X           Y           Z
      # 0 C     6.0000    0    12.011         -3.225857992764711         -4.974951500825070         -1.229933675247557

    # re_patterns.append(r"\s*\d+\s+([A-Z][a-z]{0,2})\s+\d+\.\d+\s+\d+\s+\d+\.\d+\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)\s+(-*\d+\.\d*)")
    #上面需要转换单位，未实现

    for re_pattern in re_patterns:
        re_result =re.findall(re_pattern,line)
        if re_result:
            re_result = list(re_result[0])
            if re_result[0].isdigit() and int(re_result[0]) in elements_dict:
                re_result[0]=elements_dict[int(re_result[0])]

            # Bq 原子会显示为0号，用以下语句排除一票乱七八糟的情况
            if re_result[0].isdigit() and int(re_result[0]) not in elements_dict:
                continue

            return '\t'.join(re_result)

def std_coordinate_mopac_arc(line):
    #   F     6.84338961 +1  -1.29346408 +1   9.54649274 +1
    mopac_pattern = r"([A-Z][a-z]{0,2})\d*\s+(-*\d+\.\d*)\s+\+*\-*(1|0)\s+(-*\d+\.\d*)\s+\+*\-*(1|0)\s+(-*\d+\.\d*)\s+\+*\-*(1|0)"
    re_ret = re.findall(mopac_pattern,line)
    if re_ret:
        re_ret = list(re_ret[0])
        #去掉mopac的默认冻结标记
        re_ret.pop(-1)
        re_ret.pop(-2)
        re_ret.pop(-3)
        return '\t'.join(re_ret)


class Gaussian_input:
    def __init__(self,path):
        with open(path) as input_file:
            input = input_file.readlines()

        input = [x.strip() for x in input]

        self.step_list = remove_blank(split_list_by_item(input,"--link1--",lower_case_match=True))

        self.step_count = len(self.step_list)

        self.steps = [Gaussian_input_step(x) for x in self.step_list]

        pass

class Gaussian_input_step:
    def __init__(self,input_list:list): # input 为SplitStep内的一个Step

        self.charge=0
        self.multiplet=1
        self.proc = 1
        self.mem = 0.1
        self.chk = ""
        self.rwf = ""

        self.input_list = input_list

        self.phrase_annotates()

        # devide paragraphs
        self.paragraphs = []

        temp = []
        for line in self.input_list:
            if line.strip(): # 如果不是空行
                temp.append(line)
            else:
                self.paragraphs.append(temp)
                temp = []
        if temp:
            self.paragraphs.append(temp)

        #此时已分成独立的paragraphs

        # read link0 command
        self.link0_list=[]
        link0_line_count = 0
        for i,line in enumerate(self.paragraphs[0]):
            line = line.lower()
            if line.strip(" ").startswith("%"):
                self.link0_list.append(line)

                if "%nprocshared=" in line:
                    self.proc = int(re.findall(r"%nprocshared=(.+)",line)[0].strip())
                elif "%mem=" in line and 'mb' in line:
                    self.mem = int(float((re.findall(r"%mem=(.+)mb",line)[0].strip()))/100)/10
                elif "%chk=" in line:
                    self.chk = re.findall(r"%chk=(.+)",line)[0].strip()
                elif "%rwf=" in line:
                    self.rwf = re.findall(r"%rwf=(.+)",line)[0].strip()

            else:
                link0_line_count = i
                break

        self.saved = [0,1,2] # 记录访问了多少paragraph，访问当前第一个paragraph使用len

        self.route_list = self.paragraphs[0][link0_line_count:] # 除了Link0命令外，为route部分
        self.route_str = self.join(self.route_list)
        self.route_dict = Route_dict(self.route_str)
        if 'connectivity' in self.route_str:
            self.connectivity = self.paragraphs.pop(3)


        if not self.route_dict.from_gaussview and 'allcheck' in get_dict_value(self.route_dict,'geom'):
            self.title = []
            self.geom = []
            self.other = self.paragraphs[1:]

        else:
            self.title = self.paragraphs[1]
            if not [x for x in self.title if x.strip()]:
                self.title = ["Empty Title"]

            self.geom = self.paragraphs[2]

            self.other = self.paragraphs[3:]

            #extract charge and multiplet
            self.charge_and_multiplet = [x for x in self.geom[0].split() if x!='']
            self.charge = int(self.charge_and_multiplet[0])
            self.multiplet = int(self.charge_and_multiplet[1])

            #delete LP, charge & multiplet
            self.geom = [x for x in self.geom[1:] if not x.lower().strip().startswith('lp')]

        self.other_str=""
        for paragraph in self.other:
            for line in paragraph:
                self.other_str+=line+'\n'
            self.other_str+='\n'

        self.route_dict = Route_dict(self.route_str,self.other_str) # 重新产生一个Route_dict 把其他段落包括进去

        self.geom_text = self.join(self.geom)

    def phrase_annotates(self):
        #phrase annotate setting like "!__NAMETAG__=Orbital_Energy"
        self.annotate_lines = []
        for line in self.input_list:
            if line.startswith('!'):
                self.annotate_lines.append(line)
        for line in self.annotate_lines:
            self.input_list.remove(line)

        self.command_lines = [] # a preset of RUN command can be issued and will be phrased by qsubg09.py
        for line in self.annotate_lines:
            #"!__NAMETAG__=Orbital_Energy"
            re_ret = re.findall(r'!RUN (.+)',line)
            if re_ret:
                self.command_lines.append(line)

        for line in self.command_lines:
            if line in self.input_list:
                self.input_list.remove(line)

        self.annotates_dict = {}
        for line in self.annotate_lines:
            #"!__NAMETAG__=Orbital_Energy"
            re_ret = re.findall(r'!__(.+?)__=(.+)',line)
            if re_ret:
                re_ret = re_ret[0]
                self.annotates_dict[re_ret[0]]=re_ret[1]

    def join(self,item):
        ret=""
        for i in item:
            if not isinstance(i,str):
                return repr(item)
            ret+=i.strip()+'\n'

        ret = ret.strip()
        return ret

class Keyword:
    def __init__(self,input,slash):
        # accept input
        # opt
        # opt = calcfc
        # opt = (calcfc, ts)
        # opt(calcfc,ts)
        # opt(calcfc)

        input = input.strip()
        self.keyword = ""
        self.option = []

        self.origin_input = input

        #identify method
        if slash:
            self.keyword = "level"
            slash_pos = input.index('/')
            self.option = [re.sub(" ","",input[:slash_pos]),re.sub(" ","",input[slash_pos+1:])]
            # print("Level in keyword:",self.option)

        else:
            if '=' not in input and '(' not in input:
                self.keyword = input
                self.option=[]
            elif 'iop' in input:
                equal_pos = input.index('=')
                self.keyword = input[:equal_pos]
                self.option = [input[equal_pos+1:]]
            else:

                for i,chr in enumerate(input):
                    if chr=="=" or chr=='(':
                        self.keyword = input[:i].strip()
                        break

                input = input[len(self.keyword):]
                if input.startswith("=("):
                    input = input[2:-1]
                elif input.startswith('('):
                    input = input[1:-1]
                elif input.startswith("="):
                    input = input[1:]

                parenthesis = 0
                current_word = ""
                for i,chr in enumerate(input):

                    current_word+=chr
                    if chr==')':
                        parenthesis-=1
                    elif chr=='(':
                        parenthesis+=1
                    if parenthesis!=0:
                        continue

                    if chr ==',' and parenthesis==0:
                        self.option.append(current_word[:-1])
                        current_word = ""
                self.option.append(current_word)

class Route_dict(collections.OrderedDict):
    def __init__(self,route_input:str,other_paragraph = "",remove_genchk = True):
        '''

        :param route_input:
        :param other_paragraph:
        :param remove_genchk:  产生输入的时候会自动去掉genchk，用于读取输出时应将此项设为False
        :return:
        '''
        super(self.__class__,self).__init__()

        self.origin_route_input = route_input

        if isinstance(route_input,Route_dict): # 用于copy.deepcopy的复制
            for key,value in route_input.items():
                self[key]=value
                self.other_paragraph=route_input.other_paragraph

        else:

            route_input = route_input.replace('\n',' ').strip()
            other_paragraph = other_paragraph.strip()

            if route_input.startswith('#'):
                route_input = route_input[2:].strip(' ').lower() #remove #p or #
            parenthesis = 0
            current_word = ''
            slash = False #identify method/basis

            for i,chr in enumerate(route_input):
                current_word+=chr

                if chr==')':
                    parenthesis-=1
                elif chr=='(':
                    parenthesis+=1
                if parenthesis!=0:
                    continue
                if parenthesis==0 and chr=='/':
                    slash = True
                if (chr ==' ' or chr == "\n" or i==len(route_input)-1) and parenthesis==0:
                    keyword = Keyword(current_word,slash)
                    self.add_item(keyword.keyword,keyword.option)
                    current_word = ""
                    slash = False

            # 'genchk'和'connectivity'用来防止由GV产生的gjf文件默认带有geom=allchk，其会自动加上genchk，但我们自己永远不会自己写genchk
            self.from_gaussview = False
            if 'connectivity' in list(get_dict_value(self,'geom')):
                self["geom"].remove('connectivity')
                self.from_gaussview = True

            if 'genchk' in self:
                if remove_genchk:
                    self.pop('genchk')
                self.from_gaussview = True

            if self.from_gaussview and 'allcheck' in get_dict_value(self,'geom'):
                self['geom'].remove('allcheck')

            if 'geom' in self and (not self['geom']):
                self.pop('geom')

            if 'level' not in self:
                self['level'] = ['Blank_Method','Black_Basis']

            # scrf = (smd, dovacuum) 没用，必须重写一个不带scrf的
            if 'dovacuum' in get_dict_value(self,'scrf'):
                self['scrf'].remove('dovacuum')

            try:
                self.pop("sp")
                self.pop("test")
            except:
                pass

            self.other_paragraph=other_paragraph

        # self['method'] = self['level'] #这里的method是勿用，应用Level代替，此处用以下兼容

    def get_keyword(self,keyword):
        if keyword in self:
            return self[keyword]
        else:
            return []

    def option_exist(self,keyword,option):
        # eg for opt=tight
        # check whether option tight is in opt
        # return false if opt not exist
        # return false if opt=() without tight

        if keyword not in self:
            return False

        return option in self[keyword]

    def add_item(self,key,option):
        key = key.strip()

        if not key: # key 为空
            return None

        #combine new list with exist list, which is a value of a key in database
        if key == "level":
            self[key] = option
        elif key in self:
            self[key] = list(set(self[key]+option))
        else:
            self[key] = list(set(option))

    def remove_item(self,key,option):
        if key in self:
            if isinstance(option,str):
                if option in self[key]:
                    self[key].remove(option)
            if isinstance(option,list):
                for item in option:
                    if item in self[key]:
                        self[key].remove(item)
            if self[key]==[] and key not in ['opt','freq','scan','irc']:
                self.pop(key)

    def remove_key(self,key):
        if key in self:
            self.pop(key)

    def add_and_remove_of_dict(self,key,option,button):

        # combine new list with exist list, which is a value of a key in database
        # true for add, false for remove
        # do not pass key='method' in this

        bool = button.isChecked()

        if bool: # to add
            self.add_item_to_dict(key,option)
        else: # to remove
            self.remove_item_from_dict(key,option)


    def print_value(self,value): # get a output like "(calcfc,ts)" in opt=(calcfc,ts)
        ret = ''
        if value:
            ret+= '='
            if len(value)>1:
                ret+='('
                for i,item in enumerate(value):
                    ret+=item
                    if i==len(value)-1:
                        ret+=')'
                    else:
                        ret+=','
            else:
                ret+=value[0]
        return ret

    def __str__(self):
        ret = ""
        if 'level' in self:
            if self['level']!=['Blank_Method','Black_Basis']:
                ret = self['level'][0] + '/' +self['level'][1] + '\n'

        for key,value in self.items():
            if key!='level':
                ret+= key
                ret+=self.print_value(value)
                ret+='\n'

        return ret

class Gaussian_summary:
    def __init__(self,summary_lines:list):
        '''
        Return a formatted result for Gaussian summary at the end of each gaussian job

        :param input: 用于接受别的输入

        :return: Something like:
        --------------------------------------------------------------
        [[['1', '1', 'GINC-LIYUANHE-UBUNTU', 'FOpt', 'RB3LYP', '6-31+G(d,p)', 'C19H25N3', 'GAUUSER',
        '12-Oct-2015', '0'], ['#p b3lyp/6-31+g(d,p) opt freq empiricaldispersion=gd3bj'], ['Me2_23_Prod'],
         ['0,1', 'C,0.4732857814,-1.2321049177,-0.7321261073', ............],
          ['Version=ES64L-G09RevD.01', 'State=1-A',
          'HF=-903.4719536', 'RMSD=5.576e-09', 'RMSF=7.235e-06', 'Dipole=-0.4275145,1.6510886,-0.6033573',
           'Quadrupole=8.9935258,-6.1414828,-2.8520429,-2.2448542,-0.1231134,2.7069082', 'PG=C01 [X(C19H25N3)]'],
            ['@']], [['1', '1', 'GINC-LIYUANHE-UBUNTU', 'Freq', 'RB3LYP', '6-31+G(d,p)', 'C19H25N3', 'GAUUSER',
             '12-Oct-2015', '0']...........]............]
        --------------------------------------------------------------
        '''

        summary = ""


        for summary_line in summary_lines:
            summary_line = summary_line.strip('\n')
            summary+=summary_line[1:] if summary_line[0]==" " else summary_line

        if r'1\1' in summary: # windows
            summary = summary.replace('\\','|')
        summary = summary.split('||')
        summary = [x.split("|") for x in summary]

        self.summary = summary

        self.basic_information = self.summary[0]
        self.route = self.summary[1][0]
        self.route_dict = Route_dict(self.route)

        self.name = self.summary[2]
        self.charge,self.multiplet = self.summary[3][0].split(',')

        self.coordinate = Coordinates(self.summary[3][1:],self.charge,self.multiplet)

        self.results = self.summary[4]
        self.results = {x.split("=")[0]:x.split("=")[1] for x in self.results}
        # contains "HF", "ZeroPoint","Thermal","NImag"

class ORCA_output:
    # only one step orca was supported
    def __init__(self,output):
        if isinstance(output,str) and file_type(output)==Filetype.orca_output:
            with open(output,encoding='utf-8') as file:
                self.lines = file.readlines()

        elif isinstance(output,list): # input as list
            self.lines = output

        else:
            raise MyException('Not valid file')

        self.normal_termination = False

        self.is_optimization=False
        self.has_finalgrid = False
        self.opt_energies = []
        self.converged = [[],[],[],[],[]]
        self.opt_coordinates = []

        self.gCP_correction=0

        self.has_freq = False
        self.harmonic_freqs=[]
        self.G_correction =0
        self.H_correction = 0
        self.S = 0
        self.G = 0
        self.H = 0
        self.imaginary_count = 0
        self.has_imaginary_freq = False

        self.input_file_lines = []
        self.input_filename = ""
        self.coordinates = []
        self.scf_converged=False
        self.electronic_energy = 0
        self.process()

        self.charge = 0
        self.multiplicity = 1

        self.coords = [] # list of Coordinate Class Object
        self.get_coords()

        self.keywords = []
        self.level = []
        self.get_keywords()
        if 'opt' in self.keywords:
            self.is_optimization=True

        self.geom_steps = [] # contain list of [list of lines] <-- each step of optimization
        self.finalgrid_calculation = [] # contain list of lines of FINAL ENERGY EVALUATION AT THE STATIONARY POINT
        if self.is_optimization:
            self.geom_steps = split_list(self.lines,lambda x:"GEOMETRY OPTIMIZATION CYCLE" in x,include_separator=True)[1:]

            # ORCA 可能会最后单独算一个高格点单点，把这个过程分离出来。
            split_last_step = split_list(self.geom_steps[-1],lambda x:"FINAL ENERGY EVALUATION AT THE STATIONARY POINT" in x,include_separator=True)
            assert len(split_last_step) in [1,2],'Split final grid calculation error'
            if len(split_last_step)==2:
                self.has_finalgrid=True
                self.geom_steps[-1] = split_last_step[0]
                self.finalgrid_calculation=split_last_step[1]

            self.get_opt_energies()
            self.get_opt_coords()
            self.get_converged()

        self.get_MP2_progress()
        self.get_SCF_progress()
        self.get_freq_result()
        # print(self.keywords)

        self.level_str = '/'.join(self.level)

    def get_opt_coords(self):
        re_pattern="CARTESIAN COORDINATES (ANGSTROEM)"
        for step_content in self.geom_steps:
            for count,line in enumerate(step_content):
                if re_pattern in line:
                    coordinate_lines = []
                    for line2 in step_content[count+2]:
                        if std_coordinate(line2):
                            coordinate_lines.append(line2)
                        else:
                            break
                    self.opt_coordinates.append(Coordinates(coordinate_lines))

    def get_opt_energies(self):

        re_pattern="FINAL SINGLE POINT ENERGY\s+(-[0-9]+\.[0-9]+)"
        for step_content in self.geom_steps:
            for line in reversed(step_content):
                re_ret = re.findall(re_pattern,line)
                if re_ret:
                    self.opt_energies.append(''.join(re_ret[0]))
                    break

        self.opt_energies = [float(x) for x in self.opt_energies]

    def get_converged(self):
        for step_count,step_content in enumerate(self.geom_steps):
            for count,line in enumerate(step_content):
                if "Geometry convergence" in line:

                    for k,line2 in enumerate(step_content[count+3:count+8]):
                        re_ret = re.findall(r"-*\d\.\d+", line2)
                        if len(re_ret)==2:
                            value = abs(float(re_ret[0]))/float(re_ret[1])
                            # print(value)
                            if value < 0.01:
                                value = 0.01 #防止log时出现负无穷
                            if step_count==0:
                                if k==0: #第一步时没有energy difference的输出，应识别
                                    self.converged[0].append(100)
                                self.converged[k+1].append(value)
                            else:
                                self.converged[k].append(value)

                    break


        #调整顺序为
        # ["Max F","RMS F","Max D","RMS D",'Energy']

        self.converged = [self.converged[2]]+[self.converged[1]]+[self.converged[4]]+[self.converged[3]]+\
                         [[x**0.5 for x in self.converged[0]]]


        #从[[...],[...],[...],[...]] 换成 [[ , , , ]...]
        self.converged = [[self.converged[x][step] for x in range(5)] for step in range(len(self.converged[0]))]


    def process(self):
        for count,line in enumerate(self.lines):
            if not self.input_file_lines and "INPUT FILE" in line:
                for input_lines in self.lines[count+1:]:
                    if "****END OF INPUT****" in input_lines:
                        break

                    if self.input_filename=="":
                        match = re.findall('NAME\s+\=\s+(.+)',input_lines)
                        if match:
                            self.input_filename = match[0]

                    match = re.findall("\|\s*\d+\>(.+)",input_lines)
                    if match:
                        self.input_file_lines.append(match[0])

            if "****ORCA TERMINATED NORMALLY****" in line:
                self.normal_termination = True

            if "gCP correction" in line:
                match = re.findall('gCP correction\s+(\-*\d+\.\d+)',line)
                if match:
                    self.gCP_correction = float(match[0])*2625.49962

            if "FINAL SINGLE POINT ENERGY" in line:
                match = re.findall('FINAL SINGLE POINT ENERGY\s+(\-\d+\.\d+)',line)
                if match:
                    self.electronic_energy = float(match[0])*2625.49962
        pass


    def get_keywords(self):
        for line in self.input_file_lines:
            if line.strip().startswith('!'):
                self.keywords+=line.strip().strip('!').split()
        self.keywords = [x.lower() for x in self.keywords]
        for keyword in self.keywords:
            for functional in functional_keywords_of_orca:
                if keyword.lower()==functional.lower():
                    self.level.append(functional)
            for basis in basis_set_keywords_of_orca:
                if keyword.lower()==basis.lower():
                    self.level.append(basis)

    def read_charge_and_multiplet(self):
        # acquire changes
        for count,line in enumerate(self.lines):
            charge_re_result =re.findall(r'''Total Charge +Charge +.... +(\d)+''',line) # match " Total Charge           Charge          ....    0"
            multiplet_re_result = re.findall(r'''Multiplicity +Mult +.... +(\d)+''',line) # match "Multiplicity           Mult            ....    1"
            input_re_result = re.findall(r'''\* +xyz \+(\d+) +(\d+)''',line) # match "* xyz 0   1"

            if len(charge_re_result)==1:
                self.charge = int(charge_re_result[0])
            elif len(multiplet_re_result)==1:
                self.multiplicity = int(multiplet_re_result[0])
            elif len(input_re_result)==1:
                self.charge,self.multiplicity = input_re_result[0]
                self.charge = int(self.charge)
                self.multiplicity = int(self.multiplicity)

    def get_MP2_progress(self):
        self.window = -1
        self.per_batch = -1
        self.processed_MP2 = []
        self.has_MP2 = False
        for count in range(len(self.lines)-1,-1,-1):
            line = self.lines[count]
            re_ret = re.findall(r'Operator \d+  - window\s+\.\.\.\s+\(\s*\d+\-\s*(\d+)\)',line)
            if re_ret:
                self.window = int(re_ret[0])
                for count2,line2 in enumerate(self.lines[count:]):
                    re_ret = re.findall(r'Operator \d+  - Number of orbitals per batch ...\s+(\d+)',line2)
                    if re_ret:
                        self.per_batch = int(re_ret[0])

                    #Process  5:   Internal MO  65
                    re_ret = re.findall(r'Process\s+\d+:\s+Internal MO\s+(\d+)',line2)
                    if re_ret:
                        self.has_MP2=True
                        self.processed_MP2.append(int(re_ret[0]))

                break

        # for count,line in enumerate(self.lines):
        #     if "Starting loop over batches of integrals:" in line:
        #         for count2,line2 in enumerate(self.lines[count:]):
        #             #Operator 0  - window                       ... (  0-149)x(150-2839)
        #             re_ret = re.findall(r'Operator 0  - window\s+\.\.\.\s+\(\s+\d+\-\s+(\d+)\)',line2)
        #             if re_ret:
        #                 self.window = int(re_ret[0])
        #
        #         break


    def get_SCF_progress(self):
        self.scf_iter = []
        self.scf_converged=False
        for count,line in enumerate(self.lines):
            if "SCF ITERATIONS" in line:
                self.scf_iter = []
                self.scf_converged=False
                for count2,line2 in enumerate(self.lines[count:]):
                    re_ret = re.findall('\s*\d+\s+(\-\d+\.\d+)\s+',line2)
                    if re_ret:
                        self.scf_iter.append(float(re_ret[0]))
                    if 'SCF CONVERGED AFTER ' in line2:
                        self.scf_converged=True
                        break


    def get_coords(self):

        marks = {r"\* +xyz":1,r"CARTESIAN COORDINATES \(ANGSTROEM\)":2} # ,r"CARTESIAN COORDINATES \(A\.U\.\)":3 需要调单位，暂未实现
        # see the discription in the Gaussian version of this function
        # Numbers are the value till the coordinates starts (coordinate start from the next line is 1)

        for count,line in enumerate(self.lines):
            for mark in marks:
                if re.findall(mark,line):

                    coords = []

                    for coord_line in self.lines[count+marks[mark]:]:
                        if std_coordinate(coord_line): # 确认这一行中存在坐标
                            coords.append(coord_line)
                        else:
                            break
                    if coords:
                        self.coords.append(Coordinates(coords,self.charge,self.multiplicity))

        if self.coords:
            self.coordinates = self.coords[-1]
        else:
            self.coordinates=Coordinates()

    def get_freq_result(self):

        # these information are NOT sufficient for a Thermo calculation

        for count in range(len(self.lines)-1,-1,-1): # read the last one
            if "ORCA SCF HESSIAN" in self.lines[count]:
                Hessian_lines = self.lines[count:]


                self.has_freq=True
                self.has_imaginary_freq = False

                for count2,line in enumerate(Hessian_lines):
                    # get frequencies in cm**-1
                    if "VIBRATIONAL FREQUENCIES" in line:
                        self.harmonic_freqs = []
                        for vib_count, vib_line in enumerate(Hessian_lines[count2+3:]):
                            re_ret = re.findall(r'\d+:\s+(-*\d+\.\d+)\s+cm\*\*\-1',vib_line)
                            if re_ret:
                                assert len(re_ret)==1
                                re_ret = re_ret[0]
                                if vib_count<6: #前六个是投影掉的振动和转动，为0
                                    assert float(re_ret)==0
                                    continue
                                else:
                                    self.harmonic_freqs.append(float(re_ret))
                            else:
                                break

                        self.imaginary_count = len([x for x in self.harmonic_freqs if x<0])
                        if self.imaginary_count!=0:
                            self.has_imaginary_freq = True

                    if "THERMOCHEMISTRY AT" in line:
                        self.temp = float(re.findall(r'Temperature\s+\.+\s+(\d+\.\d+)\s+K',Hessian_lines[count2+3])[0])
                        self.pressure = float(re.findall(r'Pressure\s+\.+\s+(\d+\.\d+)\s+atm',Hessian_lines[count2+4])[0])


                    # ORCA cannot determine the rotation symm number, assume 1 for all molecules

                    # get corrections
                    # enthalpy_corr_pattern =r"Thermal Enthalpy correction\s+\.+\s+(-*\d+\.\d+)\s+Eh"
                    gibbs_corr_lead_pattern =r"For completeness - the Gibbs free enthalpy minus the electronic energy"
                    gibbs_corr_pattern =r"G\-E\(el\)\s+\.+\s+(-*\d+\.\d+)\s+Eh"
                    enthalpy_pattern =r"Total Enthalpy\s+\.+\s+(-*\d+\.\d+)\s+Eh"
                    gibbs_pattern =r"Final Gibbs free enthalpy\s+\.+\s+(-*\d+\.\d+)\s+Eh"
                    entropy_pattern =r'sn\= 1\s+qrot\/sn\=\s+-*\d+\.\d+\s+T\*S\(rot\)\=\s+-*\d+\.\d+\s+kcal\/mol\s+T\*S\(tot\)\=\s+(-*\d+\.\d+)\s+kcal\/mol'

                    # orca的 enthalpy correction不是Gaussian里的ZPE+H(0->T)
                    # re_ret = re.findall(enthalpy_corr_pattern,line)
                    # if re_ret: self.H_correction = float(re_ret[0])*2625.49962

                    re_ret = re.findall(entropy_pattern,line)
                    if re_ret: self.S = float(re_ret[0])*4.184*1000/self.temp

                    re_ret = re.findall(enthalpy_pattern,line)
                    if re_ret: self.H = float(re_ret[0])*2625.49962

                    re_ret = re.findall(gibbs_pattern,line)
                    if re_ret: self.G = float(re_ret[0])*2625.49962


                    if gibbs_corr_lead_pattern in line:
                        re_ret = re.findall(gibbs_corr_pattern,Hessian_lines[count2+1])
                        if re_ret:
                            self.G_correction =float(re_ret[0])*2625.49962

        self.H_correction=self.H-self.electronic_energy

class Gaussian_output:
    def __init__(self,output,filename=""):

        if isinstance(output,str) and file_type(output)==Filetype.gaussian_output:
            with open(output,encoding='utf-8') as file:
                self.lines = file.readlines()
            if not filename:
                filename = output

        elif isinstance(output,list): # input as list
            self.lines = output

        else:
            raise MyException('Not valid file')

        self.filename = filename

        # verify that "#p" was written in route, otherwise Gaussian_output cannot read that
        hash_p_found = False
        for line in self.lines:
            if '#p' in line or "#P" in line:
                hash_p_found=True
                break
        if not hash_p_found:
            print(self.lines[:150])
            Qt.QMessageBox.critical(Qt.QWidget(),"Output Files without #P in route is not supported.","Output Files without #P in route is not supported.\n"+self.filename+"\nProgram Terminating...",Qt.QMessageBox.Abort)
            exit()

        self.steps_list = split_list(self.lines,lambda x:("l1.exe" in x))
        self.steps = [Gaussian_output_step(x,self.filename) for x in self.steps_list if self.steps_list]

        for count,step in enumerate(self.steps):
            if count==len(self.steps)-1:
                break
            if self.steps[count+1].is_freq_step_after_opt and self.steps[count+1].normal_termination:
                step.is_opt_step_before_freq=True

        # for step in self.steps:
        #     print(step.is_opt_step_before_freq,step.is_freq_step_after_opt)

        self.remove_empty_head()

        self.last_opt_pos = [x for x in range(len(self.steps)) if "opt" in self.steps[x].route_dict or  "irc" in self.steps[x].route_dict]
        if self.last_opt_pos:
            self.last_opt_pos = self.last_opt_pos[-1]
        else:
            self.last_opt_pos = -1

        for count,step in enumerate(self.steps):
            if count-1>=0:
                if step.mixed_basis_str=='chk':
                    step.mixed_basis_str = self.steps[count-1].mixed_basis_str

        #读取输出的标题（其中含有“[EXTRACT_GEOM]”部分）
        self.title = ""
        self.extract_geoms=[]
        for link in self.steps[0].links:
            if link.num==101:
                for count,line in enumerate(link.lines):
                    if "Symbolic Z-matrix:" in line or "Structure from the checkpoint file" in line:
                        # [1:]是除去每行开头的空格
                        title1 = [x[1:] for x in link.lines[1:count]] # 高斯有时会把标题写在Structure from the checkpoint file前面
                        title2 = [x[1:] for x in link.lines[count+1:]] # 有时会写在后面
                        if True in ['-----' in x for x in title1]: #检测有无'--------'行，但这个行会随着标题长度而改变，故而仅支持超过5字符的
                            title=title1
                        else:
                            title=title2
                        self.title = ''.join(split_list(title,lambda x:'-----' in x)[0])
                        break
            if self.title:
                break

        # print("Title:",self.title)
        re_ret = re.findall(r"\[EXTRACT_GEOM\]\:(\d)((\,\d+)*)",self.title)
        if re_ret:
            re_ret=re_ret[0]
            self.extract_geoms = (re_ret[0]+re_ret[1]).split(',')
            self.extract_geoms = [int(x)-1 for x in self.extract_geoms]

        self.frozen_bonds=[]
        re_ret = re.findall(r"\[FROZEN\_BONDS\]\:(.+)\[\/FROZEN\_BONDS\]",self.title)
        if re_ret:
            re_ret=re_ret[0]
            self.frozen_bonds =eval(re_ret)


        #按照相同的结构分成几个部分
        # self.step_groups_by_structure is a list of (list of steps), each step in the same list should have the same structure in l9999
        # only completed steps was included
        # IRC not included
        self.step_groups_by_structure = []
        self.extract_groups = [] # 需要提取的group的编号
        for count,step in enumerate(self.steps):
            if 'irc' in step.route_dict:
                continue

            true_count = count #排除opt+freq生成的多余步数
            for i,previous_step in enumerate(self.steps[:count]):
                if 'opt' in previous_step.route_dict and 'freq' in previous_step.route_dict:
                    true_count-=1

            if step.normal_termination:
                belonged=False #是否已经插入到某一个group里了
                for step_group in self.step_groups_by_structure:
                    if step.summary:
                        if step.summary.coordinate == step_group[0].summary.coordinate:
                            step_group.append(step)

                            # 看这一组的构象要不要提取
                            if true_count in self.extract_geoms:
                                self.extract_groups.append(self.step_groups_by_structure.index(step_group))

                            belonged=True
                            break
                if not belonged:
                    self.step_groups_by_structure.append([step])
                    # 看这一组的构象要不要提取
                    if true_count in self.extract_geoms:
                        self.extract_groups.append(len(self.step_groups_by_structure)-1)

        #如果没规定，全收
        if not self.extract_geoms:
            self.extract_groups=list(range(len(self.step_groups_by_structure)))

        # print("File\t\t\t\t:",self.filename)
        # print("Defined extract geometry\t:",self.extract_geoms)

        #包含需要提取的各步骤
        # self.step_groups_require_extract = [self.step_groups_by_structure[count] for count in self.extract_groups]

        self.get_solvation_energy()
        self.get_group_coordinate()

        self.normal_terminated = False not in [step.normal_termination for step in self.steps]

        pass

    def get_group_coordinate(self):
        #提取组内每一step的坐标，并检查是不是唯一的
        self.coordinate_of_groups = [None for x in self.step_groups_by_structure]
        self.geom_hash_of_groups = [-1 for x in self.step_groups_by_structure]

        for group_count,group in enumerate(self.step_groups_by_structure):
            if group_count not in self.extract_groups: #不需要提取就滚蛋
                continue

            #提取组内每一step的坐标，并检查是不是唯一的
            coordinate = [step.summary.coordinate for step in group]
            for count in range(len(coordinate)-1,0,-1):
                if coordinate[count]==coordinate[count-1]:
                    coordinate.pop(count)
            assert len(coordinate)==1, "group_coordinate not singular"
            self.coordinate_of_groups[group_count]=coordinate[0]

            #提取geom_hash
            geom_hash = [hash(step.summary.coordinate) for step in group]
            if len(list(set(geom_hash)))!=1:
                print("Warning! Group_coordinate_hash not singular.\nHowever it doesn't necessarily means different stucture.")
            self.geom_hash_of_groups[group_count]=geom_hash[0]

    def remove_empty_head(self):

        # 排除Linux下调用的第一个文件头
        # if self.steps:
        #     non_blank_links = [x for x in self.steps[0].links if x.num!=-1]
        #     if not non_blank_links:
        #         self.steps.pop(0)

        # 排除一个link都没有的情况（Linux下调用，文件有初始指令头）
        pop=[]
        for count,step in enumerate(self.steps):
            non_blank_links = [x for x in step.links if x.num!=-1]
            if not non_blank_links:
                pop.append(count)
        for count in reversed(pop):
            self.steps.pop(count)

    def get_solvation_energy(self):
        '''

        :return: solvation energy (△HF) in kJ/mol
        '''

        # 每组structure有一个solvation
        self.solvation_energy = [0 for x in self.step_groups_by_structure]
        self.solvation_method = ["" for x in self.step_groups_by_structure]
        self.solvent = ["" for x in self.step_groups_by_structure]
        self.solvation_steps = [[] for x in self.step_groups_by_structure] #直接存储step对象


        for count,step_group in enumerate(self.step_groups_by_structure):
            if len(step_group)>=2:
                for step_count,step1 in enumerate(step_group):
                    for step2 in step_group[:step_count]:
                        if step1.summary and step2.summary: # 确认已经算完了

                            # verify that some 2 routes' only difference is the scrf command
                            route1 = Route_dict(step1.route_dict.origin_route_input)
                            route2 = Route_dict(step2.route_dict.origin_route_input)


                            for route in [route1,route2]:
                                remove_key_from_dict(route,'geom')
                                remove_key_from_dict(route,'sp')
                                remove_key_from_dict(route,'guess')

                            keys_to_remove = []

                            for key in route1:
                                if key!='scrf' and key in route2:
                                    if set(route1[key])==set(route2[key]):
                                        keys_to_remove.append(key)

                            for key in keys_to_remove:
                                remove_key_from_dict(route1,key)
                                remove_key_from_dict(route2,key)

                            if list(route1.keys())==['scrf'] and 'smd' in route1['scrf'] and list(route2.keys())==[]:

                                self.solvation_steps[count] = [step1,step2]

                                HF_sol = float(step1.summary.results['HF'])
                                HF_gas = float(step2.summary.results['HF'])
                                self.solvation_energy[count] = (HF_sol-HF_gas)*2625.49962
                                self.solvation_method[count] = step1.summary.route_dict['level']
                                self.solvation_method[count] = (self.solvation_method[count][0]+'/'+self.solvation_method[count][1]).upper()

                                self.solvent[count] = "NOT FOUND"
                                for scrf_setup in step1.summary.route_dict['scrf']:
                                    match = re.findall(r'solvent\s*\=\s*(.+)',scrf_setup)
                                    if match:
                                        self.solvent[count] = match[0]
                                        #第一个字母大写
                                        self.solvent[count] = self.solvent[count][0].upper()+self.solvent[count][1:].lower()

            #                 return None
            #
            # self.solvation_energy = 0
            # self.solvation_method = ""
            # return None

class Gaussian_output_step:
    def __init__(self,step_list,original_filename = ""):

        self.links = []
        self.route = ""
        self.route_dict={}

        self.original_filename = original_filename

        self.has_freq = False
        self.is_freq_step_after_opt = False #是单独计算的freq还是opt freq的第二步
        self.is_opt_step_before_freq=False #是freq前面的opt步骤，这样opt步骤的单点就不用取了

        self.harmonic_freqs=[]
        self.G_correction =0
        self.H_correction = 0
        self.S = 0
        self.G = 0
        self.H = 0
        self.imaginary_count = 0
        self.has_imaginary_freq = False
        self.is_IRC = False
        self.IRC_coords = []

        self.lines = step_list
        self.split_by_link()

        try:
            # print([x.leave_time for x in self.links])
            self.last_leave_time = max([x.leave_time for x in self.links])
            self.last_leave_time = Chronyk(datetime.strptime(self.last_leave_time,"%a %b %d %H:%M:%S %Y"))
            # print(self.last_leave_time.timestring("%Y-%m-%d",timezone = 8*3600))
        except:
            self.last_leave_time = ""
            pass

        self.normal_termination = 'Normal termination' in "".join(self.links[-1].lines)
        self.error_termination = 'Error termination' in "".join(self.links[-1].lines)
        self.summary = self.find_summary()
        self.get_last_coords()
        self.get_routes()

        self.method = ""
        self.basis=""
        self.mixed_basis_str = ""
        self.mixed_basis_list=[]
        self.get_level()

        self.opt_energies = []
        self.get_opt_energies()

        self.converged = [[],[],[],[]]
        self.get_converged()

        self.last_scf_iteration = []
        for link in reversed(self.links):
            if link.scf_iteration:
                self.last_scf_iteration = link.scf_iteration
                break

        if 'irc' in self.route_dict:
            self.is_IRC=True
            self.get_irc_coords()

        self.frozen_bonds = [] # a list of 2-tuples represents the frozen bonds
        self.get_freeze()

        self.get_freq_result()

        self.chk_filename = ""
        for count,line in enumerate(self.lines):
            re_ret = re.findall(r"\%chk\=(.+)",line)
            if re_ret:
                self.chk_filename = re_ret[0]
                while '.chk' not in self.chk_filename: # Gaussian一行显示不完chk的文件名
                    count+=1
                    self.chk_filename+=self.lines[count][1:]
                break


        self.is_solvated=False #SCF能量里带没带溶剂化
        self.solvent = ""
        self.read_step_solvent()


    def read_step_solvent(self):
        for count,link in enumerate(self.links):
            if link.num==301:
                # print(link.lines)
                for count,line in enumerate(link.lines):
                    if "Polarizable Continuum Model (PCM)" in line:
                        for line2 in link.lines[count:]:
                            # print(line2)
                            re_ret = re.findall("Solvent\s+:\s*(\w+)",line2)
                            if re_ret:
                                self.is_solvated=True
                                self.solvent=re_ret[0]
                                break
                        break
        # print(self.solvent)

    def get_irc_coords(self):
        for count,link in enumerate(self.links):
            for line in link.lines:
                if "Calculating another point on the path." in line:
                    for coord_link in reversed(self.links[:count]):
                        if coord_link.coords:
                            assert len(coord_link.coords)==1,'No. of IRC coords not 1'
                            self.IRC_coords.append(coord_link.coords)
                            break
                    break

        # for i in self.IRC_coords:
        #     print(i)
        # print('---------------',len(self.IRC_coords))

    def get_freq_result(self):
        if "freq" in self.route_dict and 'opt' not in self.route_dict:
            self.has_freq=True


            if 'genchk' in self.route_dict:

                self.is_freq_step_after_opt=True

            for link in reversed(self.links):
                if link.num==716:

                    # get T, P, rotation symm
                    for count,line in enumerate(link.lines):
                        re_ret = re.findall(r"Temperature\s+(\d+\.\d+)\s+Kelvin.  Pressure\s+(\d+\.\d+)\s+Atm.",line)
                        if re_ret: self.temp, self.pressure = [float(x) for x in re_ret[0]]

                        re_ret = re.findall(r'Rotational symmetry number\s+(\d+)\.',line)
                        if re_ret: self.rotation_symm_number = int(re_ret[0][0])

                        re_ret = re.findall(r'Rotational constants \(GHZ\)\:\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)',line)
                        if re_ret:
                            self.rotation_constants = [float(x) for x in re_ret[0]]

                        re_ret = re.findall(r'Rotational constant \(GHZ\)\:\s+(-*\d+\.\d+)',line)
                        if re_ret:
                            self.rotation_constants = [float(x) for x in re_ret]*3

                        # Gaussian 有时会因为惯性矩太大而显示为*****************，所以不用它了
                        # if 'Principal axes and moments of inertia in atomic units' in line:
                        #     re_ret=re.findall(r'Eigenvalues --\s+(\d+\.\d{5})\s*(\d+\.\d{5})\s*(\d+\.\d+)',
                        #                       link.lines[count+2])
                        #     self.moment_of_inertia = [float(x) for x in re_ret[0]]


                    # moment_of_inertia in SI
                    if hasattr(self,'rotation_constants'):
                        self.moment_of_inertia = [h/(B*1E9)/8/pi**2 for B in self.rotation_constants]
                    else:
                        self.moment_of_inertia = [0,0,0]

                    # get isotopes
                        # "Atom     1 has atomic number  6 and mass  12.00000"
                    self.isotopes = []
                    for line in link.lines:
                        re_ret = re.findall(r"Atom\s+\d+\s+has atomic number\s+\d+\s+and mass\s+(\d+\.\d+)"
                                            ,line)
                        if re_ret:
                            self.isotopes.append(float(re_ret[0]))

                    # get frequencies
                    self.harmonic_freqs = []
                    freq_reg = r"Frequencies\s+--\s+(-*\d+\.\d+)\s*(-*\d+\.\d+)*\s*(-*\d+\.\d+)*"
                    for line in link.lines:
                        match = re.findall(freq_reg,line)
                        if match:
                            self.harmonic_freqs+=match[0]

                    self.harmonic_freqs = [float(x) for x in remove_blank(self.harmonic_freqs)]


                    # get corrections
                    enthalpy_corr_reg =r"Thermal correction to Enthalpy\=\s+(\-*\d+\.\d+)"
                    gibbs_corr_reg =r"Thermal correction to Gibbs Free Energy\=\s+(\-*\d+\.\d+)"
                    enthalpy_reg =r"Sum of electronic and thermal Enthalpies\=\s+(\-\d+\.\d+)"
                    gibbs_reg =r"Sum of electronic and thermal Free Energies\=\s+(\-\d+\.\d+)"


                    for line in link.lines:
                        match = re.findall(enthalpy_corr_reg,line)
                        if match: self.H_correction = float(match[0])*2625.49962

                        match = re.findall(gibbs_corr_reg,line)
                        if match: self.G_correction = float(match[0])*2625.49962

                        match = re.findall(enthalpy_reg,line)
                        if match: self.H = float(match[0])*2625.49962

                        match = re.findall(gibbs_reg,line)
                        if match: self.G = float(match[0])*2625.49962

                    entropy_lead_reg = r"\s+E\s+\(Thermal\)\s+CV\s+S"
                    entropy_reg =r'Total\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)\s+(-*\d+\.\d+)'

                    for i,line in enumerate(link.lines):
                        if re.findall(entropy_lead_reg,line):
                            match = re.findall(entropy_reg,link.lines[i+2])
                            if match:
                                self.S =float(match[0][2])*4.184
                            break
                    break

            self.imaginary_count = len([x for x in self.harmonic_freqs if x<0])
            if self.imaginary_count!=0:
                self.has_imaginary_freq = True

    def split_by_link(self):
        self.links = []
        # elements are something like [502,["Output","Lines", 'of','L502.exe']]
        # the resting (if not terminated), is -1
        # "Normal termination" is 9999

        leave_time = ""

        current_link = []
        for line in self.lines:
            match =re.findall(r' Leave Link +([\d]+) at ([A-Za-z]{3} [A-Za-z]{3} +[\d]+ [\d]{2}:[\d]{2}:[\d]{2} [\d]{4}).+cpu\:\s+(\d+\.\d+)',line)
            if match and match[0][0].isnumeric() and current_link:
                match = match[0]
                link_num=int(match[0])
                leave_time = match[1]
                cpu_time = match[2]
                self.links.append(Gaussian_output_link(link_num,current_link,leave_time,cpu_time))
                # if match and match[1]:
                #     self.last_leave_time = max(self.last_leave_time,match[1])
                current_link = []
            else:
                current_link.append(line)

        if current_link: # 最后剩下的，有时不输出leave link 9999
            re_ret = re.findall(r"\(Enter .+l([\d]{1,4}).exe\)",current_link[0])

            if re_ret and re_ret[0].isnumeric():
                self.links.append(Gaussian_output_link(int(re_ret[0]),current_link,leave_time))
            else:
                self.links.append(Gaussian_output_link(-1,current_link,leave_time))

    def find_summary(self):

        l9999_link = [link for link in self.links if link.num ==9999]

        if len(l9999_link)!=1:
            if "Entering Gaussian System" not in self.lines[0]:
                # print("No summary find")
                return ""
        else:
            ret=""
            sum_lines = l9999_link[0].lines
            for count,line in enumerate(sum_lines):
                if r'1\1' in line or '1|1' in line:
                    summary = []
                    for summary_line in sum_lines[count:]:
                        summary.append(summary_line)
                        if "@" in summary_line:
                            break
                    if summary:
                        ret = Gaussian_summary(summary)
                        l9999_link[0].coords.append(ret.coordinate)
                        return ret


    def get_last_coords(self):

        self.last_coord = Coordinates()

        self.all_coords = sum([link.coords for link in self.links if link.coords],[])
        if self.all_coords:
            self.last_coord = self.all_coords[-1]

        correct_c_and_m = [coord for coord in self.all_coords if coord.charge!=999]
        if correct_c_and_m:
            self.last_coord.charge = correct_c_and_m[-1].charge
            self.last_coord.multiplicity = correct_c_and_m[-1].multiplicity

    def get_freeze(self):

        if 'opt' in self.route_dict and 'modredundant' in self.route_dict['opt']:
            for link in self.links:
                if link.num==101:
                    for count,line in enumerate(link.lines):
                        if 'The following ModRedundant input section has been read:' in line:
                            for line2 in link.lines[count+1:]:
                                re_ret = re.findall(r"B\s+(\d+)\s+(\d+)\s+F",line2)
                                if re_ret:
                                    self.frozen_bonds.append([int(x)-1 for x in re_ret[0]])
                                else:
                                    break
                            break

    def get_routes(self):

        self.route=""
        for link in self.links:
            if link.num==1:

                for i,line in enumerate(link.lines):
                    match = re.findall(r'^\ #',line)
                    if match:
                        for route_line in link.lines[i:]:
                            if '---' in route_line:
                                break
                            if route_line[0]!=" ":
                                print("Route Line Process Error!")
                            self.route += route_line[1:].strip('\n')
                break
        self.route_dict = Route_dict(self.route,remove_genchk=False)
        pass


    def get_level(self):
        if "level" in self.route_dict and ("genecp" in self.route_dict['level'] or 'gen' in self.route_dict['level']):
            self.mixed_basis_list = []
            for link in self.links:
                if link.num==301:
                    basis_list = []
                    current_basis = []
                    for i,line in enumerate(link.lines):

                        if "Basis read from chk" in line:
                            self.mixed_basis_list.append("Check")
                            break

                        if "General basis read from cards:" in line: # 从这一行开始读
                            for basis_line in link.lines[i+1:]:
                                if "Ernie" in basis_line:
                                    break
                                if "****" in basis_line:
                                    current_basis.append(basis_line)
                                    basis_list.append(current_basis)
                                    current_basis = []
                                else:
                                    current_basis.append(basis_line)
                            break

                    for basis in basis_list:
                        if "****" in basis[-1]:
                            for basis_line in basis:
                                if "Centers:" not in basis_line and "****" not in basis_line:
                                    self.mixed_basis_list.append(basis_line.strip())
            if self.mixed_basis_list:
                self.mixed_basis_str = '[' + ' + '.join(self.mixed_basis_list) + ']'
            else:
                self.mixed_basis_str = ""
                self.mixed_basis_list=[]

            self.method = self.route_dict['level'][0]
            self.basis = self.mixed_basis_list
            if len(self.basis)==1:
                self.basis = self.basis[0]
        else:
            self.method,self.basis = self.route_dict['level']

    def get_opt_energies(self):
        for link in self.links:
            if link.num==502:
                re_pattern = r" SCF Done:  E\([0-9A-Za-z\-]+\) =  (-[0-9]+\.[0-9]+)"

                for line in link.lines:
                    match = re.findall(re_pattern,line)
                    if len(match) > 0:
                        self.opt_energies.append(''.join(match[0]))
                        break


    def get_converged(self):
        for link in self.links:
            if link.num==103:
                for count,line in enumerate(link.lines):
                    match = re.findall("Converged\?", line)
                    if match:
                        for k,line in enumerate(link.lines[count+1:count+5]):
                            re_ret = re.findall(r" \d\.\d+", line)
                            if len(re_ret)==2:
                                value = float(re_ret[0])/float(re_ret[1])
                                if value < 0.01:
                                    value = 0.01 #防止log时出现负无穷
                                self.converged[k].append(value)

                            # 数值超过9.999999时会将其显示为*******
                            else:
                                re_ret = re.findall(r" \*{4,}\s+(\d\.\d+)", line)
                                if re_ret:
                                    self.converged[k].append(10/float(re_ret[0]))
                                else:
                                    print("Converged Energy Finding Error.")

                #从[[...],[...],[...],[...]] 换成 [[ , , , ]...]
        self.converged = [[self.converged[x][step] for x in range(4)] for step in range(len(self.converged[0]))]

class Gaussian_output_link:
    def __init__(self,link_num,link_lines,leave_time=0,cpu_time=-1):
        self.num = link_num
        self.lines = link_lines
        self.coords = []
        self.get_coords()

        self.leave_time = leave_time
        self.cpu_time = float(cpu_time)
        self.date_class = Date_Class(str(link_num),leave_time)

        self.scf_iteration = []
        self.get_scf_iteration()


    def get_scf_iteration(self):
        if self.num==502:
            for i,line in reversed(list(enumerate(self.lines))):
                match = re.findall("Cycle[ ]+([0-9]+) ", line)
                if match:
                    for j in range(1, 100):
                        if i+j >=len(self.lines):
                            break
                        if len(re.findall("Cycle[ ]+([0-9]+) ", self.lines[i + j])) > 0:
                            break

                        findEnergy = re.findall(r"E= (-\d+\.\d+)", self.lines[i + j])

                        if len(findEnergy) > 0:
                            energy = float(findEnergy[0])
                            self.scf_iteration.append(energy)
                            break

                    if int(match[0]) == 1:
                        break

        # QC
        if self.num==508:
            for i,line in reversed(list(enumerate(self.lines))):
                match = re.findall(r"Iteration +(\d+) +EE\=", line)
                if match:
                    findEnergy = re.findall(r"Iteration +\d+ +EE= (-\d+\.\d+)", line)
                    if len(findEnergy) > 0:
                        energy = float(findEnergy[0])
                        self.scf_iteration.append(energy)

        self.scf_iteration.reverse()

    def get_coords(self):
        if self.num!=9999:

            marks = {"Symbolic Z-matrix:":0,
                     "Input orientation:":4,
                     "Standard orientation:":4,
                     "Redundant internal coordinates found in file":0,
                     "CURRENT STRUCTURE":5}
            # key is a title mark
            # value is a number indicating how many lines should be skipped after the title
            #
            ###############################################################################
            # Symbolic Z-matrix:
            # Charge =  0 Multiplicity = 1
            # C                     0.42047  -1.18677  -0.70467

            # key is "Symbolic Z-matrix:", value should be 0
            ###############################################################################
            ###############################################################################
            #                           Input orientation:
            # ---------------------------------------------------------------------
            # Center     Atomic      Atomic             Coordinates (Angstroms)
            # Number     Number       Type             X           Y           Z
            # ---------------------------------------------------------------------
            #      1          6           0        0.420470   -1.186773   -0.704665

            # key is "Input orientation:" value should be 4
            ###############################################################################

            self.charge = 999
            self.multiplicity = 999

            for count,line in enumerate(self.lines):
                for mark in marks:
                    if mark in line:
                        coords = []

                        re_result = re.findall(r'Charge = +(-*\d+) Multiplicity = +(\d+)',self.lines[count+1]+'\n'+self.lines[count-1]) # 在某些标题的前面一行有，有的后面一行有
                        if re_result:
                            self.charge,self.multiplicity = re_result[0]   # 如果找到了，就使用新的；如果找不到，沿用上一个
                            count+=1

                        for coord_line in self.lines[count+marks[mark]+1:]:
                            # print(link.num,mark)
                            # print(coord_line)
                            if std_coordinate(coord_line): # 确认这一行中存在坐标
                                coords.append(coord_line)
                            else:
                                break
                        if coords:
                            self.coords.append(Coordinates(coords,self.charge,self.multiplicity))

def split_gaussian_output_file_steps(filename):
    # split Gaussian output file to each step (except opt+freq and vacuum-sol SMD calc. pair were viewed as single step)
    # return False if no split was required (already "single step")

    header=''' Entering Gaussian System, Link 0=/home/gauuser/g09/g09
 Input=/home/gauuser/Gaussian/PK/OAcOAc_H/BP86_Fix_Lactone/Insertion_TS_NoBJ_01.gjf
 Output=/home/gauuser/Gaussian/PK/OAcOAc_H/BP86_Fix_Lactone/Insertion_TS_NoBJ_01.out
 Initial command:
 /home/gauuser/g09/l1.exe "/home/gauuser/g09/scratch/Gau-6482.inp" -scrdir="/home/gauuser/g09/scratch/"
 Entering Link 1 = /home/gauuser/g09/l1.exe PID=      6483.

 Copyright (c) 1988,1990,1992,1993,1995,1998,2003,2009,2013,
            Gaussian, Inc.  All Rights Reserved.

 This is part of the Gaussian(R) 09 program.  It is based on
 the Gaussian(R) 03 system (copyright 2003, Gaussian, Inc.),
 END OF MAN MADE HEADER

 ******************************************
 Gaussian 09:  ES64L-G09RevD.01 24-Apr-2013
                24-Dec-2015
 ******************************************
 '''

    if isinstance(filename,Gaussian_output):
        output_object = filename
        filename = output_object.filename
    elif os.path.isfile(filename):
        output_object =Gaussian_output(filename)
    else:
        return None

    if len(output_object.steps)==1:
        return False

    if len(output_object.steps)==2:
        if 'opt' in output_object.steps[0].route_dict and \
                        'freq' in output_object.steps[0].route_dict:
            return False
        if output_object.solvation_energy:
            return False

    processed = []

    if output_object.solvation_energy:
        processed+=output_object.solvation_steps
        solvation_gas = output_object.steps[output_object.solvation_steps[0]]
        solvation_sol = output_object.steps[output_object.solvation_steps[1]]

        ret=""

        if output_object.solvation_steps[1]!=0:
            ret+=header

        ret += "".join(solvation_sol.lines) + '\n'
        ret += "".join(solvation_gas.lines) + '\n'

        output_filename = filename_class(filename).only_remove_append+'__solvation.out'
        if not os.path.isfile(output_filename):
            with open(output_filename,'w') as output_file:
                output_file.write(ret)
        # else:
        #     print("File",output_filename,"already exist!")


    for count,step in enumerate(output_object.steps):
        ret=""
        if count in processed:
            continue

        if count!=0:
            ret+=header

        ret += "".join(step.lines) + '\n'
        processed.append(count)
        if 'opt' in step.route_dict and 'freq' in step.route_dict and count+1<len(output_object.steps):
            ret += "".join(output_object.steps[count+1].lines) + '\n'
            processed.append(count+1)

        output_filename = filename_class(filename).only_remove_append+'__STEP_'+str(count+1)+'.out'
        if not os.path.isfile(output_filename):
            with open(output_filename,'w') as output_file:
                output_file.write(ret)
        else:
            print("File",output_filename,"already exist!")

    return True


def file_type(filename):

    if filename_class(filename).append.lower() in ['gjf','com']:
        return Filetype.gaussian_input

    if filename_class(filename).append.lower() == 'log':
        return Filetype.gaussian_output

    if filename_class(filename).append.lower() == 'inp':
        return Filetype.orca_input

    if filename_class(filename).append.lower() == 'orca':
        return Filetype.orca_output

    if filename_class(filename).append.lower() == 'mopac':
        return Filetype.mopac_output

    if filename_class(filename).append.lower() == 'out':
        # fast determine required for MOPAC files
        with open(filename,encoding='utf-8',errors='ignore') as file:
            for count,line in enumerate(file):
                if count>20:
                    break
                if "**                                MOPAC2012                                  **" in line:
                    return Filetype.mopac_output
                if "**                                MOPAC2016                                  **" in line:
                    return Filetype.mopac_output

        with open(filename,encoding='utf-8',errors='ignore') as file:
            for line in file:
                line = line.strip().lower()
                #remove filename lines like %rwf, %chk, %base to prevent "!" or "#" appear in filename
                if True in [line.startswith(key) for key in ['%rwf',"%chk",'%base',"%oldchk"]]:
                    continue
                if line.startswith('Entering Gaussian System'.lower()):
                    return Filetype.gaussian_output
                if line.startswith("Gaussian 09, Revision ".lower()):
                    return Filetype.gaussian_output
                if line.startswith("* O   R   C   A *".lower()):
                    return Filetype.orca_output
                if line.startswith('#'):
                    return Filetype.gaussian_output


    # if filename_class(filename).append.lower() == 'out':
    #     with open(filename,encoding='utf-8',errors='ignore') as file:
    #         for count,line in enumerate(file):
    #             line = line.strip().lower()
    #             #remove filename lines like %rwf, %chk, %base to prevent "!" or "#" appear in filename
    #             if True in [line.startswith(key) for key in ['%rwf',"%chk",'%base',"%oldchk"]]:
    #                 continue
    #             if line.startswith('Entering Gaussian System'.lower()):
    #                 return Filetype.gaussian_output
    #             if line.startswith("Gaussian 09, Revision ".lower()):
    #                 return Filetype.gaussian_output
    #             if line.startswith("* O   R   C   A *".lower()):
    #                 return Filetype.orca_output
    #             if line.startswith('#'):
    #                 return Filetype.gaussian_output
    #             if "**                                MOPAC2012                                  **".lower() in line:
    #                 return Filetype.mopac_output
    #             if "**                                MOPAC2016                                  **".lower() in line:
    #                 return Filetype.mopac_output

class Filetype:

    gaussian_input = "Gaussian Input *##*(@#"
    orca_input = "ORCA INPUT *##*(@#"
    gaussian_output= "Gaussian Output *##*(@#"
    orca_output= "ORCA Output *##*(@#"
    mopac_input = 'MOPAC INPUT *##*(@#'
    mopac_output = 'MOPAC Output *##*(@#'
    input=[gaussian_input,orca_input]
    output=[gaussian_output,orca_output]
    valid = input+output

class MOPAC_Input:
    def __init__(self,path):
        with open(path) as input_file:
            input = input_file.readlines()
        input = [x.strip() for x in input]
        self.route = input[0]

        pass

class MOPAC_Archieve:
    def __init__(self,path):

        self.filename = path
        self.normal_termination=True
        self.H=0
        self.method = ""
        self.coordinate_filename = ""
        self.coordinates=""

        with open(path) as input_file:
            input = input_file.readlines()

        for count,line in enumerate(input):
            if not self.method:
                if "SUMMARY OF" in line:
                    re_ret = re.findall(r'SUMMARY OF\s+(\S+)\s+CALCULATION',line)
                    if re_ret:
                        self.method=re_ret[0]

            if "HEAT OF FORMATION" in line:
                re_ret = re.findall(r'HEAT OF FORMATION\s*=\s*-*\d+\.\d+\s*KCAL\/MOL\s*=\s*(-*\d+\.\d+)\s*KJ\/MOL',line)
                if re_ret:
                    self.H = float(re_ret[0])

            if "FINAL GEOMETRY OBTAINED" in line and not self.coordinates:
                for coordinate in input[count+4:]:
                    coordinate_output = std_coordinate_mopac_arc(coordinate)
                    if not coordinate_output:
                        break
                    self.coordinates+=coordinate_output+'\n'

        if self.normal_termination:
            self.coordinate_filename =filename_class(path).only_remove_append+"_result.xyz"
            with open(self.coordinate_filename,'w') as output_stucture_file:
                output_stucture_file.write(str(len(self.coordinates.splitlines()))+"\n"+str(self.H)+"\n")
                output_stucture_file.write(self.coordinates)

        self.coordinate_object = Coordinates(self.coordinates.splitlines())


class MOPAC_Output:
    def __init__(self,path):

        arc_file = filename_class(path).replace_append_to('arc')
        if os.path.isfile(arc_file):
            arc_object = MOPAC_Archieve(arc_file)
            self.filename = path
            self.normal_termination=True
            self.H = arc_object.H
            self.method = arc_object.method
            self.coordinate_filename = arc_object.coordinate_filename
            self.coordinates = arc_object.coordinates
            self.coordinate_object = arc_object.coordinate_object

        else:
            self.filename = path
            self.normal_termination=False
            self.H=0
            self.method = ""
            self.coordinate_filename = ""
            self.coordinates=""

            with open(path) as input_file:
                input = input_file.readlines()

            for count,line in enumerate(input):
                if "CALCULATION RESULTS" in line:
                    re_ret = re.findall(r'\s+(\S+)\s+CALCULATION RESULTS',line)
                    if re_ret:
                        self.method=re_ret[0]

                if "CARTESIAN COORDINATES" in line:
                    self.coordinates=""
                    for coordinate in input[count+2:]:
                        coordinate_output = std_coordinate(coordinate)
                        if not coordinate_output:
                            break
                        self.coordinates+=coordinate_output+'\n'


            for line in reversed(input):

                if "* JOB ENDED NORMALLY *" in line:
                    self.normal_termination = True

                if "FINAL HEAT OF FORMATION" in line:
                    re_ret = re.findall(r'FINAL HEAT OF FORMATION\s*=\s*-*\d+\.\d+\s*KCAL/MOL\s*=\s*(-*\d+\.\d+)\s*KJ/MOL',line)
                    if re_ret:
                        self.H = float(re_ret[0])
                        break

            if self.normal_termination:
                self.coordinate_filename =filename_class(path).only_remove_append+"_result.xyz"
                with open(self.coordinate_filename,'w') as output_stucture_file:
                    output_stucture_file.write(str(len(self.coordinates.splitlines()))+"\n"+str(self.H)+"\n")
                    output_stucture_file.write(self.coordinates)

            self.coordinate_object = Coordinates(self.coordinates.splitlines())


class ORCA_Input:
    def __init__(self,path):
        with open(path) as input_file:
            input = input_file.readlines()

        input = [x.strip() for x in input]
        for count,x in enumerate(input):
            if '#' in x:
                input[count] = x[:x.find("#")]

        input = remove_blank(input)

        self.step_list=remove_blank(split_list_by_item(input,"$new_job"))
        self.step_count = len(self.step_list)
        self.steps=[ORCA_Step(x) for x in self.step_list]


class ORCA_Step:
    def __init__(self,text_list:list):

        self.charge=0
        self.multiplet=1
        self.proc = 1
        self.mem_per_core = 85
        self.mem=0.1
        self.base = ""
        self.geom=[]
        self.xyzfile=""
        self.read_geom=False

        self.input_lines = text_list

        skip_line_count = []

        for count,line in enumerate(self.input_lines):
            pal_find = re.findall(r'\%pal +nprocs +(\d+) end',line)
            maxcore_find=re.findall(r"\%maxcore (\d+)",line)
            base_find=re.findall(r'''%base "(.+)"''',line)
            geometry_find=re.findall(r'''\* *xyz +(\d+) +(\d+)''',line)
            read_geometry_find=re.findall(r'''\* *xyzfile +(\d+) +(\d+) +(.+\.xyz)''',line)


            if len(geometry_find)==1:
                self.charge,self.multiplet=[int(x) for x in geometry_find[0]]

                for count_geom,geom_line in enumerate(self.input_lines[count+1:]):
                    if geom_line.strip()=="*":
                        skip_line_count.append(count_geom+count+1)
                        break
                    self.geom.append(geom_line)
                    skip_line_count.append(count_geom+count+1)
                self.geom_text = '\n'.join(self.geom)


            if len(read_geometry_find)==1:
                self.read_geom=True
                self.charge,self.multiplet,self.xyzfile=read_geometry_find[0]


            if len(pal_find)==1:
                self.proc=int(pal_find[0])

            if len(maxcore_find)==1:
                self.mem_per_core=int(maxcore_find[0])

            if len(base_find)==1:
                self.base=base_find[0]

            if sum([len(x) for x in [pal_find,maxcore_find,base_find,read_geometry_find,geometry_find]])==1:
                skip_line_count.append(count)

        self.mem=self.proc*self.mem_per_core/1000/0.85

        self.other=[x for count,x in enumerate(self.input_lines) if count not in skip_line_count]

    def __str__(self):
        return "\n".join(self.other)

from RMSD import *


if __name__ == "__main__":
    # coords1 = MOPAC_Output(r"D:\Gaussian\C26H54\C26H54_Confsearch\C26H54_P0_0.mopac").coordinate_object
    # coords2 = MOPAC_Output(r"D:\Gaussian\C26H54\C26H54_Confsearch\C26H54_P0_2.mopac").coordinate_object
    # a=get_dihedrals(coords1,
    #               get_bond_order_from_mol2_file(r"D:\Gaussian\C26H54\C26H54_Confsearch\C26H54_clean.mol2"))
    # for i in a:
    #     print(i)
    # print("-----------")

    # b=get_dihedrals(coords2,
    #               get_bond_order_from_mol2_file(r"D:\Gaussian\C26H54\C26H54_Confsearch\C26H54_clean.mol2"),
    #                 only_pick_one_necessary=False)
    #
    # for i in b:
    #     print(i)
    # print("-----------")
    #
    # from RMSD_by_dihedral import *
    # fadfa=generate_dihedral_diff_matrix([coords1, coords2],get_bond_order_from_mol2_file(r"D:\Gaussian\Asy-DA\di_CF3_OCF3\Binding_Ketone_sub\Confsearch1_Confsearch\Confsearch1_clean.mol2"),80)
    # test=get_one_diff_list(a,b,80)
    # print(test)
    # print(std_coordinate("| 22> C 2.6513679581 0.7151000717 1.8317834944"))
    # a=MOPAC_Archieve(r"D:\Gaussian\StableEnol\Pic\19_Confsearch\19_P9_22.arc")
    # for i in range(10):
    #     Gaussian_output(r'D:\Gaussian\Asy-DA\di_CF3_OCF3\Binding_Ketone_TS\upper_disfavor\TS[Complete_B3LYP]reopt_lintor_small_step_imag2.out')
    #     print(i)
    a=ORCA_output(r"C:\Users\LiYuanhe\Desktop\test.orca")
    # print(get_bond_order_from_mol2_file(r"D:\Gaussian\Asy-DA\Total\Sub_complex_Confsearch\Sub_complex.mol2"))
    print("testing")
    pass
    # Gaussian_output(r"D:\Gaussian\PK\OCOO_H\Before PBE\Insertion_TS_01_IRC.out")
    #
    # split_gaussian_output_file_steps("D:\Gaussian\PK\OCOO_H\BP86\DeCO_Prod_BP86_O_Coordinate_NoBJ.out")
    # a=Gaussian_output(r'D:\Gaussian\TEST_for_Gaussian_Series\4pi[Complete_M062X].out')
    # a=Gaussian_output(r'D:\Gaussian\TEST_for_Gaussian_Series\Gaussian_with_ORCA\CO[Opt_ECP_M06L_TZ].out')
    # for step in a.steps:
    #     step.last_coord.is_linear()
    # MOPAC_Output("D:\Gaussian\Epoxy\ConfSearch\Conf_Search_sdf_M0010.out")

    # pdb_for_connectivity(r"D:\Gaussian\StableEnol\Spiro_Open\enol.pdb")

    # print(Molecule_Chiral(Coordinates(r"C:\Users\LiYuanhe\Desktop\test.gjf")).chirality)
    # print(Molecule_Chiral(Coordinates(r"C:\Users\LiYuanhe\Desktop\test2.gjf")).chirality)

    # print(get_bond_order_from_mol2_file(r'D:\Gaussian\Prof_Luo\Confsearch\Sub.mol2'))
    # for i in range(100):
    # print(Route_dict('#P Geom=AllCheck Guess=TCheck SCRF=Check GenChk UB3LYP/6-31G(d) Freq'))

    pass