# -*- coding: utf-8 -*-
__author__ = 'LiYuanhe'


import os
import sys

from Python_Lib.My_Lib_PyQt import *

if not Qt.QApplication.instance():
    Application = Qt.QApplication(sys.argv)

import subprocess

if __name__ == '__main__':
    pyqt_ui_compile('VMD_Pov_Ray_Blur_UI.py')
    from UI.VMD_Pov_Ray_Blur_UI import Ui_VMD_Pov_Ray_Blur_UI

import os
def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

class myWidget(Ui_VMD_Pov_Ray_Blur_UI, Qt.QWidget, Qt_Widget_Common_Functions):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        self.open_config_file()

        connect_once(self.submit_pushButton,self.submit)
        connect_once(self.focal_atom_lineEdit.textChanged,self.select_focal_atom_mode)
        connect_once(self.gen_pov_filename_pushButton,self.generate_pov_filename)
        connect_once(self.load_pov_file_pushButton,self.main_process)
        connect_once(self.focal_atom_lineEdit.textChanged,self.check_submittable)
        connect_once(self.focal_atom_radioButton.clicked,self.check_submittable)
        connect_once(self.draft_submit_pushButton,self.draft_submit)
        connect_once(self.manual_focal_radioButton.clicked,self.check_submittable)

        self.res_height_spinBox.setEnabled(False)
        self.res_width_spinBox.setEnabled(False)
        self.submit_pushButton.setEnabled(False)
        
        self.blur_sampling_spinBox.setValue(self.load_config('blur_sampling_spinBox',70))
        self.ortho_doubleSpinBox.setValue(self.load_config('ortho_doubleSpinBox',100))
        self.depth_doubleSpinBox.setValue(self.load_config('depth_doubleSpinBox',50))
        self.field_width_doubleSpinBox.setValue(self.load_config('field_width_doubleSpinBox',50))
        self.res_width_spinBox.setValue(self.load_config('vmd_width',1000))
        self.res_height_spinBox.setValue(self.load_config('vmd_height',1000))


        connect_once(self.res_height_spinBox.valueChanged,self.adjust_width)
        connect_once(self.res_width_spinBox.valueChanged,self.adjust_height)

        self.center_the_widget()


        self.warning_label.hide()

        self.show()

    def select_focal_atom_mode(self):
        self.focal_atom_radioButton.setChecked(True)
        self.check_submittable()

    def generate_pov_filename(self):

        save_filename=[]
        while not save_filename:
            save_filename = Qt.QFileDialog.getSaveFileName(self,'Target png image filename',
                                                           self.load_config('Pov_Ray_output_file_folder'),
                                                           "png file (*.png)")
            if save_filename and ' ' in save_filename[0]:
                alert_UI("Having SPACEs in path or filename for computation is a TERRIBLE habit.\nRemove any spaces in path or filename then continue.")
                save_filename=""

        save_filename = save_filename[0]

        self.png_filename = save_filename

        self.config['Pov_Ray_output_file_folder']=filename_class(save_filename).path
        self.save_config()

        self.pov_filename = filename_class(self.png_filename).replace_append_to('pov')
        self.pov_filename_lineEdit.setText(self.pov_filename)

        addToClipBoard(self.pov_filename)

    def main_process(self):
        return_value = self.read_file()
        if return_value:
            self.find_camera_paragraph()
            self.find_atoms_paragraph()
            self.find_cpk_molecules()


    def read_file(self):
        if not hasattr(self,'pov_file') and self.pov_filename_lineEdit.text().strip():
            print("Gen .pov filename skipped...")
            self.pov_filename = self.pov_filename_lineEdit.text().strip()
            self.png_filename = filename_class(self.pov_filename).replace_append_to('png')
        else:
            return None

        if not os.path.isfile(self.pov_filename):
            alert_UI(".pov file not found in designated path. Make sure you follow the procedure.")
            return None

        with open(self.pov_filename) as original_file:
            self.original_file = original_file.readlines()

        is_vmd_1_9_3=False
        for line in self.original_file:
            if "VMD 1.9.3" in line:
                is_vmd_1_9_3=True
            re_ret = re.findall(r'\/\/.+povray.+\+W(\d+)',line)
            if re_ret:
                self.vmd_width =int(re_ret[0])
            re_ret = re.findall(r'\/\/.+povray.+\+H(\d+)',line)
            if re_ret:
                self.vmd_height =int(re_ret[0])
                
        if hasattr(self,'width') and hasattr(self,'height'):
            self.res_height_spinBox.setEnabled(True)
            self.res_width_spinBox.setEnabled(True)
            if self.vmd_height>self.vmd_width:
                self.adjust_width()
            else:
                self.adjust_height()

        self.warning_label.setVisible(not is_vmd_1_9_3)

        return "Normal reading file"

    def h_w_ratio_range(self):
        return [(self.res_height_spinBox.value()-0.5)/(self.res_width_spinBox.value()+0.5),(self.res_height_spinBox.value()+0.5)/(self.res_width_spinBox.value()-0.5)]

    def adjust_height(self):
        range = self.h_w_ratio_range()
        if not range[0]<self.vmd_height/self.vmd_width<range[1]:
            self.res_height_spinBox.setValue(self.res_width_spinBox.value()*self.vmd_height/self.vmd_width)

    def adjust_width(self):
        range = self.h_w_ratio_range()
        if not range[0]<self.vmd_height/self.vmd_width<range[1]:
            self.res_width_spinBox.setValue(self.res_height_spinBox.value()/self.vmd_height*self.vmd_width)

    def find_camera_paragraph(self):
        # 找到包含camera定义的一段
        self.camera_paragraph = []
        for count,line in enumerate(self.original_file):
            if "camera {" in line:
                self.camera_start = count
                for count2 in range(count,len(self.original_file[count:])):
                    line2 = self.original_file[count2]
                    self.camera_paragraph.append(line2)
                    if "}" in line2:
                        self.camera_end = count2
                        break
                break

        #去掉不需要的行
        to_be_removed = []
        markers = ["orthographic", "location", "angle","blur_samples","aperture", "focal_point"]
        for line in self.camera_paragraph:
            if True in [marker.lower() in line.lower() for marker in markers]:
                to_be_removed.append(line)
        self.camera_paragraph = [line.strip() for line in self.camera_paragraph if line not in to_be_removed]

    def check_submittable(self):
        if hasattr(self,'camera_paragraph') and self.camera_paragraph:
            if (self.focal_atom_radioButton.isChecked() and self.focal_atom_lineEdit.text()) or \
                    (self.manual_focal_radioButton.isChecked()):
                self.submit_pushButton.setEnabled(True)
                return None
        else:
            print("Camera_paragraph reading failure...")
        self.submit_pushButton.setEnabled(False)

    def find_cpk_molecules(self):
        self.cpks_lines = {} #key is a tuple (molecule ID,repr ID), value is a tuple record the start and end line number of that cpk molecule
        for count,line in enumerate(self.original_file):
            re_ret = re.findall(r"\/\/\s+MoleculeID:\s+(\d+)\s+ReprID:\s+(\d+)\s+Beginning\s+CPK",line)
            if re_ret:
                id = tuple(int(x) for x in re_ret[0])
                molecule=[count]
                for count2 in range(count+2,len(self.original_file)):
                    molecule_line = self.original_file[count2]
                    re_patterns = [r"VMD\_sphere\(\<(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\>",
                                   r'VMD_cylinder\(\<(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\>']

                    if not list_or(re.findall(pattern,molecule_line) for pattern in re_patterns):
                        molecule+=list(range(count+1,count2))
                        self.cpks_lines[id]=molecule
                        break


    def find_atoms_paragraph(self):
        self.molecules={} #key is molecule ID, value is list of np.array object for 3D coordinates
        for count,line in enumerate(self.original_file):
            re_ret = re.findall(r"\/\/\s+MoleculeID:\s+(\d+)\s+ReprID:\s+(\d+)\s+Beginning\s+CPK",line)
            if re_ret:
                id = tuple(int(x) for x in re_ret[0])
                molecule=[]
                for molecule_line in self.original_file[count+1:]:
                    re_ret = re.findall(r"VMD\_sphere\(\<(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\>",molecule_line)
                    if re_ret:
                        molecule.append([float(x) for x in re_ret[0]])
                    elif re.findall(r'VMD_cylinder\(\<(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\,(\-*\d+\.\d+e*-*\d*)\>',molecule_line):
                        break
                self.molecules[id]=molecule

        if self.molecules:
            self.focal_atom_radioButton.setChecked(True)
            self.manual_focal_radioButton.setChecked(False)
        else:
            self.focal_atom_radioButton.setChecked(False)
            self.manual_focal_radioButton.setChecked(True)

    def draft_submit(self):
        self.main_process()
        current_height = self.res_height_spinBox.value()
        current_sampling = self.blur_sampling_spinBox.value()
        self.res_height_spinBox.setValue(700)
        self.blur_sampling_spinBox.setValue(10)
        self.submit()
        self.res_height_spinBox.setValue(current_height)
        self.blur_sampling_spinBox.setValue(current_sampling)

    def submit(self):
        self.main_process()
        
        self.config['blur_sampling_spinBox']=self.blur_sampling_spinBox.value()
        self.config['ortho_doubleSpinBox']=self.ortho_doubleSpinBox.value()
        self.config['depth_doubleSpinBox']=self.depth_doubleSpinBox.value()
        self.config['field_width_doubleSpinBox']=self.field_width_doubleSpinBox.value()
        self.config['vmd_width']=self.res_width_spinBox.value()
        self.config['vmd_height']=self.res_height_spinBox.value()
                
        self.save_config()

        CPK_to_remove_text = self.CPK_to_remove_lineEdit.text().strip()
        forbidden_lines=[]
        for removing_cpk in CPK_to_remove_text.split():
            if len(removing_cpk.split(":"))==1:
                forbidden_lines+=self.cpks_lines[(int(removing_cpk),0)]
            elif len(removing_cpk.split(":"))==2:
                forbidden_lines+=self.cpks_lines[(int(removing_cpk.split(":")[0]),int(removing_cpk.split(":")[1]))]

        #Turn each value to 0~100

        # Blur sampling, 1 bad, 1000 great, use logrithm 0~100 matching 1~3000
        blur_sampling = int(10**(self.blur_sampling_spinBox.value()/80*math.log10(1000)))+1

        # Orthographicality: use as negative of original value
        position = -self.ortho_doubleSpinBox.value()

        # Depth of View(Aperture) is proportional to camera posision, should find the relationship (position -50 ~ depth 6), ratio 8 --> 0~50~100, linear(0 完全清楚，8差不多，16就只有一个原子清楚了）
        aperture = -position/(self.depth_doubleSpinBox.value()/50*8)

        # angle=Field_width / Orthographicality 300 is good, set as 50, linear
        # Width 300 --> 50, linear
        angle = -self.field_width_doubleSpinBox.value()*6 / position

        if self.focal_atom_radioButton.isChecked():
            atoms = self.focal_atom_lineEdit.text().strip().split()
            coordinates = []
            for atom in atoms:
                if len(atom.split(":"))==1:
                    coordinates.append(self.molecules[(0,0)][int(atom)])
                elif len(atom.split(":"))==2:
                    coordinates.append(self.molecules[(int(atom.split(":")[0]),0)][int(atom.split(":")[1])])
                elif len(atom.split(":"))==3:
                    coordinates.append(self.molecules[(int(atom.split(":")[0]),int(atom.split(":")[1]))][int(atom.split(":")[2])])

            centroid=[sum([x[0] for x in coordinates])/len(coordinates),
                      sum([x[1] for x in coordinates])/len(coordinates),
                      sum([x[2] for x in coordinates])/len(coordinates)]
            self.camera_paragraph.insert(-1,'focal_point <'+','.join([str(x) for x in centroid])+'>')

        else:
            self.camera_paragraph.insert(-1,'focal_point <0,0,'+str(self.manual_focal_doubleSpinBox.value())+'>')
        # camera {
        #   location <0.0000, 0.0000, -100.0000>
        #   look_at <-0.0000, -0.0000, 2.0000>
        #   angle 2.16
        #   up <0.0000, 3.0000, 0.0000>
        #   right <4.6750, 0.0000, 0.0000>
        #   blur_samples 1000 // Increase value for higher quality focal blur
        #   aperture 12 // Increase value for stronger focal blur (more shallow depth of field)
        #   focal_point <-0.4162,0.5208,-0.2403>
        # }

        self.camera_paragraph.insert(-1,'location <0.0000, 0.0000, '+str(position)+'>')
        self.camera_paragraph.insert(-1,'angle '+str(angle))
        self.camera_paragraph.insert(-1,'blur_samples '+str(blur_sampling))
        self.camera_paragraph.insert(-1,'aperture '+str(aperture))

        self.new_file = [x for count,x in enumerate(self.original_file[:self.camera_start]) if count not in forbidden_lines]+\
                        self.camera_paragraph+\
                        [x for count,x in enumerate(self.original_file[self.camera_end+1:]) if count+self.camera_end+1 not in forbidden_lines]

        self.new_file = [line.strip('\n') for line in self.new_file]
        self.new_pov_file = filename_class(self.pov_filename).only_remove_append+"_Modified_For_Focal.pov"
        with open(self.new_pov_file,'w') as output_file:
            output_file.write('\n'.join(self.new_file))

        self.launch_pov_ray()


    def launch_pov_ray(self):
        pov_ray_exe = self.load_config("pov_ray_exe",r"C:\Program Files\POV-Ray\v3.7\bin\pvengine64.exe")
        if not os.path.isfile(pov_ray_exe):
            exe = get_open_file_UI(self,r"C:\Program Files",'exe','Find POV-Ray executable pvengine64.exe for Me',single=True)
            if os.path.isfile(exe):
                pov_ray_exe = exe
                self.config["pov_ray_exe"]=pov_ray_exe
                self.save_config()

        if os.path.isfile(pov_ray_exe):
            if os.path.isfile(self.new_pov_file):
                print("Calling... "," ".join([pov_ray_exe,'+I'+self.new_pov_file,'+D','+fn','+O'+self.png_filename,'Antialias=On','Antialias_Threshold=0.3','+W'+str(self.res_width_spinBox.value()),'+H'+str(self.res_height_spinBox.value())]))
                #subprocess.Popen([pov_ray_exe,'Input_File_Name="'+self.new_pov_file+'"','+D','+fn','Output_File_Name="'+self.png_filename+'"','Antialias=On','Antialias_Threshold=0.3','Width='+str(self.res_width_spinBox.value()),'Height='+str(self.res_height_spinBox.value())],shell=True)
                subprocess.Popen([pov_ray_exe,'+I'+self.new_pov_file,'+D','+fn','+O'+self.png_filename,'Antialias=On','Antialias_Threshold=0.3','+W'+str(self.res_width_spinBox.value()),'+H'+str(self.res_height_spinBox.value())])
        else:
            self.SDF_pushButton.setText("Spartan Not Found")




if __name__ == '__main__':
    my_Qt_Program = myWidget()

    my_Qt_Program.show()
    sys.exit(Application.exec_())