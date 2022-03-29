# -*- coding: utf-8 -*-
__author__ = 'LiYuanhe'


import sys
import os
import re
from PyQt5 import Qt
from PyQt5 import uic
import string
from chronyk import Chronyk
import copy
import math

# ALL Numbers in SI if not mentioned
R=8.3144648
k_B=1.3806503E-23
N_A=6.02214179E23
c=299792458
h=6.62606896E-34
pi = math.pi

# units
Hartree__kcal_mol=627.51
Hartree__KJ_mol=2625.5
Hartree__J=4.359744575E-18
Hartree__cm_1=219474.6363

kcal__kJ=4.184
atm__Pa = 101325

bohr__m = 5.2917721092E-11
amu__kg = 1.660539040E-27
#
# if not Qt.QApplication.instance():
#     Application = Qt.QApplication(sys.argv)

def listdir(filename:str):
    # listdir of a file or a folder, return a list, contain the absolute path of the
    if os.path.isfile(filename):
        path = filename_class(filename[0]).path
        return [os.path.join(path,x) for x in os.listdir(path)]
    elif os.path.isdir(filename):
        path=filename
        return [os.path.join(path,x) for x in os.listdir(path)]

def toggle_layout(layout,hide=-1,show=-1):
    '''
    Hide (or show) all elements in layout
    :param layout:
    :param hide: to hide layout
    :param show: to show layout
    :return:
    '''

    for i in reversed(range(layout.count())):
        assert hide!=-1 or show!=-1
        assert isinstance(hide,bool) or isinstance(show,bool)

        if isinstance(show,bool):
            hide = not show

        if hide:
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().hide()
        else:
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().show()



class Qt_Widget_Common_Functions():

    def center_the_widget(self,activate_window=True):
        frame_geometry = self.frameGeometry()
        screen_center = Qt.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
        if activate_window:
            self.window().activateWindow()


    def open_config_file(self):

        config_file_failure = False
        if not os.path.isfile('Config.ini'):
            config_file_failure = True
        else:
            with open("Config.ini",'r') as self.config_File:
                try:
                    self.config=eval(self.config_File.read())
                except:
                    config_file_failure = True

        if config_file_failure:
            with open("Config.ini",'w') as self.config_File:
                self.config_File.write('{}')

        with open("Config.ini",'r') as self.config_File:
            self.config=eval(self.config_File.read())

    def load_config(self,key,absence_return=""):
        if key in self.config:
            return self.config[key]
        else:
            self.config[key]=absence_return
            self.save_config()
            return absence_return

    def save_config(self):
        with open("Config.ini",'w') as self.config_File:
            self.config_File.write(repr(self.config))


class SSH_Account:
    def __init__(self,input_str:str):
        '''
        :param input_str: "2643" 162.105.27.162:2643 hahaha 64764764
        '''
        input_str = input_str.strip().split(" ")
        self.tag = input_str[0]
        self.ip_port = input_str[1]
        self.ip,self.port = self.ip_port.split(":")

        try:
            self.port = int(self.port)
        except:
            self.port = 22

        self.username = input_str[2]
        self.password = input_str[3]
    def __str__(self):
        return self.username+' @ '+self.tag

def download_sftp_file(ssh_account:SSH_Account,remote_filepath,local_filepath,transport_object=None,sftp_object=None):
    #产生一个随机的临时文件，然后改名为想要的文件名，某种程度上保证原子性
    remove_append = filename_class(local_filepath).only_remove_append
    append = filename_class(local_filepath).append

    local_temp_filepath = remove_append+"_TEMP_For_atomicity."+append

    import paramiko
    if not transport_object:
        transport = paramiko.Transport((ssh_account.ip, ssh_account.port))
        transport.connect(username = ssh_account.username, password = ssh_account.password)
    else:
        transport = transport_object

    if not sftp_object:
        sftp = paramiko.SFTPClient.from_transport(transport)
    else:
        sftp=sftp_object

    sftp.get(remote_filepath,local_temp_filepath)

    if os.path.isfile(local_filepath):
        os.remove(local_filepath)
    os.rename(local_temp_filepath,local_filepath)

    if not sftp_object:
        sftp.close()


class Drag_Drop_TextEdit(Qt.QTextEdit):
    drop_accepted_signal = Qt.pyqtSignal(list)
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setText(" Drop Area")
        self.setAcceptDrops(True)

        font = Qt.QFont()
        font.setFamily("arial")
        font.setPointSize(13)
        self.setFont(font)

        self.setAlignment(Qt.Qt.AlignCenter)

    def dropEvent(self, event):
        if event.mimeData().urls():
            event.accept()
            self.drop_accepted_signal.emit([x.toLocalFile() for x in event.mimeData().urls()])
            self.reset_dropEvent(event)

    def reset_dropEvent(self,event):
        mimeData = Qt.QMimeData()
        mimeData.setText("")
        dummyEvent = Qt.QDropEvent(event.posF(), event.possibleActions(),
        mimeData, event.mouseButtons(), event.keyboardModifiers())

        super(self.__class__, self).dropEvent(dummyEvent)

# def remove_unseen(input_str:str):
#     return ''.join([x for x in input_str if x in string.printable or ord(x)>127])

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def Chronyk_new(input_time:str):# chronyk will give a 1 day less result when wap arround time string
    if isinstance(input_time,float):
        return Chronyk(input_time)
    elif isinstance(input_time,str):
        return Chronyk(Chronyk(input_time).timestamp()+86400)

def show_molecule(file,molecule_count=-1):
    import subprocess
    subprocess.Popen(['python',r'E:\My_Program\Python_Lib\show_molecule.py',file,str(molecule_count)])

def disconnect_Signal_Until_Dead(signal, slot):
    disconnect_all(signal,slot)

def disconnect_all(signal, slot):

    if isinstance(signal,Qt.QPushButton):
        signal = signal.clicked
    marker = False
    while not marker:
        try:
            signal.disconnect(slot)
        except:
            marker = True


def urlopen_inf_retry(url,prettify = True,use_cookie = False,retry_limit = 100,opener=None,timeout=60):
    from bs4 import BeautifulSoup

    from http.cookiejar import CookieJar
    from urllib import request
    import socket
    import urllib

    def request_page(url,opener,timeout=60):
        if use_cookie:
            if not opener:
                opener = request.build_opener(request.HTTPCookieProcessor(CookieJar()))
            return opener.open(url,timeout=timeout)
        else:
            return request.urlopen(url,timeout=timeout)

    fail=True
    retry_count = 1
    while fail and retry_count<=retry_limit:
        print("Requesting:",url,end='\t')
        try:
            
            html = request_page(url,opener,timeout=timeout).read()
            fail=False
            print("Request Finished.")
        except (socket.gaierror,urllib.error.URLError,ConnectionResetError,TimeoutError,socket.timeout,UnboundLocalError):
            print('\nURL open failure. Retrying... '+str(retry_count)+'/'+str(retry_limit))
            retry_count+=1
            import time
            time.sleep(2)

    if prettify:
        html = BeautifulSoup(html).prettify()
        return BeautifulSoup(html)
    else:
        return html


def connect_Signal_Only_Once(signal, slot):
    connect_signal_only_once(signal, slot)

def reverse(string):
    l = list(string)
    l.reverse()
    return "".join(l)

def rreplace(string, old, new, count=None):
    """string right replace"""
    string = str(string)
    r = reverse(string)
    if count is None:
        count = -1
    r = r.replace(reverse(old), reverse(new), count)
    return type(string)(reverse(r))

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def get_canonical_smiles(original_smiles):

    # import time
    #
    # t1=time.time()

    if not original_smiles:
        return ""

    from indigo.indigo import Indigo
    indigo = Indigo()
    try:
        mol = indigo.loadMolecule(original_smiles)
    except:
        print("Ineffective SMILES:",original_smiles)
        return ""

    mol.aromatize()
    try:
        ret = mol.canonicalSmiles() #有时有问题
    except:
        ret = original_smiles
        print("Indigo SMILES Bug Detected:",original_smiles)

    # print("Canonicalization time","{:.2f}".format(time.time()-t1))

    return ret

def connect_signal_only_once(signal, slot):
    connect_once(signal,slot)

def connect_once(signal, slot):
    if isinstance(signal,Qt.QPushButton) or isinstance(signal,Qt.QToolButton) or isinstance(signal,Qt.QRadioButton) or isinstance(signal,Qt.QCheckBox):
        signal = signal.clicked
    elif isinstance(signal,Qt.QLineEdit):
        signal = signal.textChanged
    elif isinstance(signal,Qt.QDoubleSpinBox) or isinstance(signal,Qt.QSpinBox):
        signal = signal.valueChanged
    disconnect_Signal_Until_Dead(signal, slot)
    signal.connect(slot)

def list_or(input_list):
    # input [a,b,c] return a or b or c
    ret = False
    for i in input_list:
        ret = ret or i
    return ret

def list_and(input_list):
    # input [a,b,c] return a and b and c
    ret = True
    for i in input_list:
        ret = ret and i
    return ret

class filename_class:
    def __init__(self, fullpath):
        fullpath=fullpath.replace('\\','/')
        self.re_path_temp = re.match(r".+/", fullpath)
        if self.re_path_temp:
            self.path = self.re_path_temp.group(0) #包括最后的斜杠
        else:
            self.path = ""
        self.name = fullpath[len(self.path):]
        self.name_stem = self.name[:self.name.rfind('.')] # not including "."

        self.append = self.name[len(self.name_stem)-len(self.name)+1:]
        self.only_remove_append = self.path+self.name_stem  # not including "."

    def replace_append_to(self,new_append):
        return self.only_remove_append+'.'+new_append


def get_dict_value(dict,key):
    return dict[key] if key in dict else ""

def remove_key_from_dict(dict,key):
    if key in dict:
        dict.pop(key)
    return dict

def build_fileDialog_filter(allowed_appendix:list,tags=[]):
    '''

    :param allowed_appendix: a list of list, each group shows together [[xlsx,log,out],[txt,com,gjf]]
    :param note: list, tag for each group, default ""
    :return: a compiled filter ready for Qt.getOpenFileNames or other similar functions
            e.g. "Input File (*.gjf *.inp *.com *.sdf *.xyz)\n Output File (*.out *.log *.xlsx *.txt)"
    '''

    if not tags:
        tags = [""]*len(allowed_appendix)
    else:
        assert len(tags)==len(allowed_appendix)

    ret = ""
    for count,appendix_group in enumerate(allowed_appendix):
        ret+=tags[count].strip()
        ret+="(*."
        ret+=' *.'.join(appendix_group)
        ret+=')'
        if count+1!=len(allowed_appendix):
            ret+='\n'

    return ret

def alert_UI(message="",title="",parent=None):

    #旧版本的alert UI定义是alert_UI(parent=None，message="")
    if not isinstance(message,str):
        message,parent = parent,message
    print(message)
    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)
    if not title:
        title=message
    Qt.QMessageBox.critical(parent,title,message)

def secure_print(*object_to_print):
    # print some character will cause UnicodeEncodeError,
    # if the message is not necessarily printed, use this function will just print nothing and aviod the error

    try:
        print(*object_to_print)
    except:
        print("Print function error. Print of information omitted.")

def get_print_str(*object_to_print,sep=" "):
    ret = ""
    for object in object_to_print:
        try:
            ret+=str(object)+sep
        except:
            print("get_print_str Error...")

    return ret

def warning_UI(message="",parent=None):
    #旧版本的alert UI定义是alert_UI(parent=None，message="")
    if not isinstance(message,str):
        message,parent = parent,message
    print(message)
    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)
    Qt.QMessageBox.warning(parent,message,message)

def information_UI(message="",parent=None):
    #旧版本的alert UI定义是alert_UI(parent=None，message="")

    if not isinstance(message,str):
        message,parent = parent,message
    print(message)
    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)
    Qt.QMessageBox.information(parent,message,message)

def wait_confirmation_UI(parent=None,message=""):
    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)
    button = Qt.QMessageBox.warning(parent,message,message,Qt.QMessageBox.Ok|Qt.QMessageBox.Cancel)
    if button == Qt.QMessageBox.Ok:
        return True
    else:
        return False

def get_open_file_UI(parent,start_path:str,allowed_appendix,title="No Title",tags=[],single=False):
    '''

    :param start_path:
    :param allowed_appendix: same as function (build_fileDialog_filter)
            but allow single str "txt" or single list ['txt','gjf'] as input, list of list is not necessary
    :param title:
    :param tags:
    :param single:
    :return: a list of files if not single, a single filepath if single
    '''

    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)

    if isinstance(allowed_appendix,str): # single str
        allowed_appendix = [[allowed_appendix]]
    if [x for x in allowed_appendix if isinstance(x,str)]: # single list not list of list
        allowed_appendix = [allowed_appendix]

    filter = build_fileDialog_filter(allowed_appendix,tags)

    if single:
        ret = Qt.QFileDialog.getOpenFileName(parent,title,start_path,filter)
        if ret: # 上面返回 ('E:/My_Program/Python_Lib/elements_dict.txt', '(*.txt)')
            ret = ret[0]
    else:
        ret = Qt.QFileDialog.getOpenFileNames(parent,title,start_path,filter)
        if ret: # 上面返回 (['E:/My_Program/Python_Lib/elements_dict.txt'], '(*.txt)')
            ret = ret[0]

    return ret


def show_pixmap(image_filename,graphicsView_object):
    # must call widget.show() holding the graphicsView, otherwise the View.size() will get a wrong (100,30) value
    if os.path.isfile(image_filename):
        pixmap = Qt.QPixmap()
        pixmap.load(image_filename)

        print(graphicsView_object.size())

        if pixmap.width() > graphicsView_object.width() or pixmap.height() > graphicsView_object.height():
            pixmap = pixmap.scaled(graphicsView_object.size(), Qt.Qt.KeepAspectRatio,Qt.Qt.SmoothTransformation)
    else:
        pixmap = Qt.QPixmap()

    graphicsPixmapItem = Qt.QGraphicsPixmapItem(pixmap)
    graphicsScene = Qt.QGraphicsScene()
    graphicsScene.addItem(graphicsPixmapItem)
    graphicsView_object.setScene(graphicsScene)

def split_list_by_item(input_list:list,separator,lower_case_match = False,include_separator = False, include_empty = False):
    return split_list(input_list,separator,lower_case_match,include_separator, include_empty)

def split_list(input_list:list,separator,lower_case_match = False,include_separator = False,include_separator_after=False, include_empty = False):
    '''

    :param input_list:
    :param separator: a separator, either a str or function. If it's a function, it should take a str as input, and return
    :param lower_case_match:
    :param include_separator:
    :param include_empty:
    :return:
    '''
    ret = []
    temp = []

    if include_separator or include_separator_after:
        assert not (include_separator and include_separator_after), 'include_separator and include_separator_after can not be True at the same time'

    for item in input_list:

        split_here_bool = False
        if callable(separator):
            split_here_bool = separator(item)
        elif isinstance(item,str) and item == separator:
            split_here_bool = True
        elif lower_case_match and isinstance(item,str) and item.lower() == separator.lower():
            split_here_bool = True


        if split_here_bool:
            if include_separator_after:
                temp.append(item)
            ret.append(temp)
            temp = []
            if include_separator:
                temp.append(item)
        else:
            temp.append(item)
    ret.append(temp)

    if not include_empty:
        ret = [x for x in ret if x]

    return ret

def update_UI():
    Qt.QCoreApplication.processEvents()

def exit_UI():
    Qt.QCoreApplication.instance().quit()

def remove_special_chr_from_str(input_str):
    '''
    A function for fuzzy search "3-propyl-N'-ethylcarbodiim"-->"propylnethylcarbodiim"
    :param input_str:
    :return:
    '''

    return ''.join(ch for ch in input_str if ch not in string.punctuation+string.whitespace+string.digits).lower()

def get_unused_filename(input_filename,replace_hash = True):
    '''
    verify whether the filename is already exist, if it is, a filename like filename_01.append; filename_02.append will be returned.
    maximum 99 files can be generated
    :param input_filename:
    :return: a filename
    '''

    input_filename = filename_filter(input_filename,replace_hash=replace_hash)

    if not os.path.isfile(input_filename):
        # 是新的
        return input_filename
    else:
        no_append = filename_class(input_filename).only_remove_append
        append = filename_class(input_filename).append

        number = 1
        while (os.path.isfile(no_append + "_" + '{:0>2}'.format(number) + '.'+append)):
            number += 1
            if number == 99:
                Qt.QMessageBox.critical(None, "YOU HAVE 99 INPUT FILE?!", "AND YOU DON'T CLEAN IT?!",
                                        Qt.QMessageBox.Ok)
                break

        return no_append + "_" + '{:0>2}'.format(number) + '.'+append


def clear_layout(layout):
    while not layout.isEmpty():
        layout.itemAt(0).widget().deleteLater()
        layout.removeItem(layout.itemAt(0))

def remove_duplicate(input_list:list):
    ret = []
    for i in input_list:
        if i not in ret:
            ret.append(i)

    return ret

def remove_blank(input_list:list):
    return [x for x in input_list if x]

def add_list_to_layout(layout,list_of_item):
    for item in list_of_item:
        if isinstance(item,Qt.QWidget):
            layout.addWidget(item)
        if isinstance(item,Qt.QLayout):
            layout.addLayout(item)

class MyException(Exception):
    '''你定义的异常类。'''
    def __init__(self,explanation):
        Exception.__init__(self)
        print(explanation)

def excel_formula(formula:str,*cells):
    if isinstance(cells[0],list):
        cells=cells[0]
    for count,cell in enumerate(cells):
        formula = formula.replace('[cell'+str(count+1)+']',cell)
    return formula

def cell(column_num,row_num):
    # start from 0
    if column_num<26:
        return chr(ord('A')+column_num)+str(row_num+1)
    if column_num>=26:
        return chr(ord('A')+int(column_num/26)-1)+chr(ord('A')+column_num%26)+str(row_num+1)


def cas_wrapper(input:str,strict=False,correction = False):
    '''
    Match or not:
                    Partial     strict
    111-11-5           Yes        Yes     normal match
    111-11-1           No!         No     not match CAS number with wrong check digit
    111-11-5aa         Yes        Yes     match if other non [digit,'-'] concatenate with it

    # partial (will print a warning)
    111-11             Yes                partial match
    111-11-aa          Yes                same for partial match
    111-11aa           Yes                same for partial match
    111-1

    # not match with other number concatenate with it (prevent phone-number match)
    111-11-523          No
    0111-11-5           No

    # wrong format
    111-112-3           No
    111-119             No
    12345678-12-2       No

    :param input:
    :param strict: match complete or partial
    :param correction:允许纠正验证位错误
    :return: completed CAS number, if not find or the check digit not match the initial input, return '',
    '''

    prefix = r"(^|[^\d-])" # prevent 0111-11-1
    base = r"([1-9]\d{1,6}-\d{2})" # matches 111-11
    postfix = r"(\-\d)"
    closure_complete = r"($|[^\d-])" # matches 111-11-1, prevent 111-11-123
    closure_partial =  r"|(\-($|[^\d-]))|($|[^\d-])" # matches 111-11-, 111-11

    re_complete = ''.join([prefix,"(",base,postfix,")",closure_complete])
    re_partial  = ''.join([prefix,base,'((',postfix,closure_complete,')',closure_partial,')'])

    find_complete = re.findall(re_complete,input) # match complete 128-38-2-->128-38
    find_partial = re.findall(re_partial,input) # match the former digits of 128-38-2-->128-38

    
    if strict:
        if len(find_complete)>1:#找到多个结果
            print('\n\n\nMultiple CAS match.',input,'\n\n\n')
        
        if not find_complete:
            return ""

        find_complete = find_complete[0][1]
        find_partial = find_partial[0][1]
    
    else:
        if len(find_partial)>1:#找到多个结果
            print('\n\n\nMultiple CAS match.',input,'\n\n\n')
        
        if not find_partial:
            return ""

        find_partial = find_partial[0][1]

        if find_complete:
            find_complete = find_complete[0][1]
        else:
            find_complete = ""


    #计算验证位
    only_digit = list(reversed([int(dig) for dig in find_partial if dig.isdigit()]))
    check_digit = sum([only_digit[i]*(i+1) for i in range(len(only_digit))])%10

    ret = find_partial+'-'+str(check_digit)

    if find_complete and ret==find_complete:
        return ret

    else:
        if strict: # 如果 strict，不满足检验直接跳出检测，返回空
            return ""

    if not find_complete:
        print('CAS Wrapper Doubt! Find:', repr(ret), '. Complete wrapper:', repr(find_complete),'. Original:',repr(input))
        return ret

    if find_complete and ret!=find_complete:
        print('CAS Wrapper Disagree! Find:', repr(ret), '. Complete wrapper:', repr(find_complete),'. Original:',repr(input))
        if correction: #允许纠正错误的验证位
            return ret
        else:
            return ""

    if not find_partial:
        return ""

def pyqt_ui_compile(filename):

    # 允许将.ui文件放在命名为UI的文件夹下，或程序目录下，但只输入文件名，而不必输入“UI/”

    if filename[:3] in ['UI\\','UI/']:
        filename = filename[3:]

    ui_filename = filename_class(filename).replace_append_to('ui')
    # print(os.path.abspath(ui_filename))
    if not os.path.isfile(ui_filename):
        ui_filename = 'UI/'+ui_filename
    modify_log_filename = filename_class(ui_filename).replace_append_to('txt')
    py_file = filename_class(ui_filename).replace_append_to('py')

    modify_time = ""
    if os.path.isfile(modify_log_filename):
        with open(modify_log_filename) as modify_log_file:
            modify_time = modify_log_file.read()

    if modify_time!=str(int(os.path.getmtime(ui_filename))):
        print("GUI MODIFIED:",ui_filename)
        with open(modify_log_filename,'w') as modify_log_file:
            modify_log_file.write(str(int(os.path.getmtime(ui_filename))))

        ui_File_Compile = open(py_file, 'w')
        uic.compileUi(ui_filename, ui_File_Compile)
        ui_File_Compile.close()


month = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def filename_filter(input_filename,including_appendix = True,path_as_filename=False,replace_hash = True):
    return proper_filename(input_filename,including_appendix,path_as_filename,replace_hash)

def is_float(input_str):
    # 确定字符串可以转换为float
    try:
        float(input_str)
        return True
    except:
        return False

def is_int(input_str):
    if not is_float(input_str):
        return False
    num = float(input_str)
    if int(input_str)==num:
        return True
    else:
        return False

def proper_filename(input_filename,including_appendix = True,path_as_filename=False,replace_hash = True):
    '''

    :param input_filename:
    :param including_appendix:
    :param path_as_filename: 是否将路径转换为文件名(/home/gauuser/file.txt --> __home__gauuser__file.txt )
    :return:
    '''
    if path_as_filename:
        path=""
        filename_stem=filename_class(input_filename).only_remove_append
    else:
        path = filename_class(input_filename).path
        filename_stem = filename_class(input_filename).name_stem
    append = filename_class(input_filename).append

    # remove illegal characters of filename
    if replace_hash:
        forbidden_chr = "<>:\"/\\|?*-\n."
    else:
        forbidden_chr = "<>:\"/\\|?*\n."
    for chr in forbidden_chr:
        filename_stem = filename_stem.replace(chr, '__')

    if append:
        if including_appendix:
            ret = filename_stem+'.'+append
        else:
            ret = filename_stem+'_'+append
    else:
        ret = filename_stem

    return os.path.join(path,ret)

def phrase_range_choice(input_str,by_index=True):
    '''
    Input a range like 1,5,7-9; output a list by index [0,4,6,7,8]; if not index [1,5,7,8,9]
    :param input_str:
    :return:
    '''

    input_list = input_str.replace(',',' ').split(' ')
    choices = copy.deepcopy(input_list)

    for choice in input_list:
        if '-' in choice:
            choices.remove(choice)
            if not re.findall('\d+\-\d+',choice):
                print("Invalid")
                return None

            start,end = choice.split('-')
            choices+=[str(x) for x in range(int(start),int(end)+1)]
    if by_index:
        choices = sorted(list(set([int(x)-1 for x in choices if '-' not in x])))
    else:
        choices = sorted(list(set([int(x) for x in choices if '-' not in x])))
    return choices


def filename_from_url(url):
    forbidden_chr = "<>:\"/\\|?*-"
    if 'http://' in url:
        ret = re.findall(r"http://(.+)", url)[0]
    else:
        ret = url
    for chr in forbidden_chr:
        ret = ret.replace(chr, '___')
    ret = 'Download/' + ret
    return ret

script_path = filename_class(os.path.abspath(__file__)).path
with open(os.path.join(script_path,"elements_dict.txt")) as elements_dict:
    elements_dict = eval(elements_dict.read())

num_to_element_dict = elements_dict
element_to_num_dict = {value: key for key, value in elements_dict.items()}

def smiles_from_xyz(input_file):
    import subprocess
    babel_exe = r"C:\Program Files (x86)\OpenBabel-2.3.2\babel.exe"
    assert os.path.isfile(babel_exe),"OpenBabel not found."
    temp_file = r"D:\Gaussian\Temp\temp_xyz_file_for_smiles.smi"

    subprocess.call([babel_exe,'-ixyz',input_file,"-osmi",temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(temp_file) as temp_file:
        ret = temp_file.read().split()
        if ret:
            return(get_canonical_smiles(ret[0]))
        else:
            print("SMILES ERROR! Original str:",ret)

def smiles_from_mol2(input_file):
    import subprocess
    babel_exe = r"C:\Program Files (x86)\OpenBabel-2.3.2\babel.exe"
    assert os.path.isfile(babel_exe),"OpenBabel not found."
    temp_file = r"D:\Gaussian\Temp\temp_xyz_file_for_smiles.smi"

    subprocess.call([babel_exe,'-imol2',input_file,"-osmi",temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(temp_file) as temp_file:
        ret = temp_file.read().split()
        if ret:
            return(get_canonical_smiles(ret[0]))
        else:
            print("SMILES ERROR! Original str:",ret)

def chr_is_chinese(char):
    return 0x4e00<=ord(char)<=0x9fa5

def has_chinese_char(string):
    for char in string:
        if chr_is_chinese(char):
            return True

    return False

def has_only_alphabat(string):
    for char in string.lower():
        if not ord('a')<=ord(char)<=ord('z'):
            return False
    return True

def wait_messageBox(message,title="Please Wait..."):
    if not Qt.QApplication.instance():
        Application = Qt.QApplication(sys.argv)

    message_box = Qt.QMessageBox()
    # message_box.setAttribute(Qt.Qt.WA_DeleteOnClose)
    message_box.setWindowTitle(title)
    message_box.setText(message)

    return message_box

def get_bonds(filename):
    '''

    :param filename: ALL file format supported by mogli
    :return: a list of tuple of bonded atoms,no bond order information
            e.g. [(0, 1), (0, 2), (0, 13), (0, 26), (2, 3), (2, 4), (2, 5), (5, 6), (5, 9), (5, 10), (6, 7), (6, 8), (7, 13), (10, 11), (10, 12), (12, 13), (12, 38), (13, 14), (14, 15), (14, 16), (14, 20), (16, 17), (16, 18), (16, 19), (20, 21), (20, 22), (20, 23), (23, 24), (23, 25), (23, 26), (26, 27), (27, 28), (27, 32), (28, 29), (28, 30), (28, 31), (32, 33), (32, 34), (32, 35), (35, 36), (35, 37), (35, 38), (38, 39), (38, 40), (40, 41), (40, 45), (40, 46), (41, 42), (41, 43), (41, 44), (46, 47), (46, 48), (46, 49)]
    '''
    import mogli
    import time
    molecules = mogli.read(filename)
    retry_attempts = 0
    while not molecules:
        print("Mogli reading error, retrying...")
        time.sleep(0.2)
        molecules=mogli.read(filename)
        retry_attempts+=1
        if retry_attempts>5:
            break

    molecule = molecules[-1]
    molecule.calculate_bonds()
    bonds = molecule.bonds
    bonds = [sorted(list(x)) for x in bonds.index_pairs]
    return bonds

pass