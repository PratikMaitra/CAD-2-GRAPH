from tkPDFViewer import tkPDFViewer as pdf
#from tkterminal import Terminal
import yaml
import networkx as nx
import sys
import os
from os.path import exists
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.font import Font
from ttkthemes import ThemedTk
import customtkinter as ctk
import subprocess
import time
import shutil
import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cairosvg
from PIL import ImageTk,Image,ImageOps


ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()

root.title("Dxf to Graph Converter")

root.attributes('-zoomed', True)

root.grid_columnconfigure((0), weight=0)
root.grid_columnconfigure((1), weight=1)
root.grid_rowconfigure((0), weight=1)


fram1=ctk.CTkFrame(root, corner_radius=0,fg_color="transparent")

fram1.grid(row=0, column=0, sticky="nsew")


fram2=ctk.CTkScrollableFrame(root,fg_color="white")

fram2.grid(row=0, column=1, sticky="nsew")


myfont= ctk.CTkFont(family="Helvetica",size=14,weight="bold")


height, width = 50,50

for row in range(height):
    fram1.grid_rowconfigure(row, weight=1)
for column in range(width):
    fram1.grid_columnconfigure(column, weight=1)

global img_label
global input_arch_file
global input_label_file
global cdir
cdir = os.getcwd()

####################################################################

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

def change_scaling_event( new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    ctk.set_widget_scaling(new_scaling_float)
    
    
        
##################################################

image = Image.open("blank.png")
image.thumbnail((1500, 1000))
photo = ctk.CTkImage(light_image=image,size=(1500,1000))
img_label = ctk.CTkLabel(fram2, image=photo,text="")
img_label.pack(fill="both", expand=True)


####################################################

   
def update_canvas():
    # Check if a new image is found
    try:

        image = Image.open("out.png")
        image.thumbnail((1500, 1000))
        new_photo = ctk.CTkImage(light_image=image,size=(1500,1000))
        img_label.configure(image=None)
        img_label.configure(image=new_photo,bg_color="white")
        img_label.pack(fill="both", expand=True)
         
    except Exception as e:
        pass
    
    
def dark_canvas():
    # Check if a new image is found
    try:

        image = Image.open("out_dark.png")
        image.thumbnail((1500, 1000))
        new_photo = ctk.CTkImage(light_image=image,size=(1500,1000))
        img_label.configure(image=None)
        img_label.configure(image=new_photo,bg_color="black")
        img_label.pack(fill="both", expand=True)
        
         
    except Exception as e:
        pass
    
def clear_canvas():
    try:
        image = Image.open("blank.png")
        image.thumbnail((1500, 1000))
        new_photo = ctk.CTkImage(light_image=image,size=(1500,1000))
        img_label.configure(image=None)
        img_label.configure(image=new_photo)
        progressbar.stop()  # stop progress bar before resetting to 0
        progressbar.set(0)
        input_arch_file =""
        input_label_file=""
        v=""
        vv=""
        sz=""
        bl=""
        l=""
        
    except Exception as e:
        pass
   
    
    
def mat_plot():
    
    img = plt.imread('out.png')
    plt.imshow(img)
    plt.show()
    
    
    
def dmat_plot():
    
    img = plt.imread('out_dark.png')
    plt.imshow(img)
    plt.show()
    
      

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, text):
        # Display text in tooltip window
        if self.tip_window or not text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")     
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=text, justify='left',
                      background="#ffffe0", relief='solid', borderwidth=1,
                      font=myfont)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
            
def save_file():
    
    global cdir
    save_path = filedialog.askdirectory()
    if save_path:
        src_file = cdir + "/out.png"
        dst_file = save_path + "/out.png"
        shutil.copy2(src_file, dst_file)
    
    
def save_yaml():
    
    global cdir
    save_path = filedialog.askdirectory()
    if save_path:
        src_file = cdir + "/outfile.yaml"
        dst_file = save_path + "/outfile.yaml"
        shutil.copy2(src_file, dst_file)
               
def in_arch():
    
    global input_arch_file
    
    input_arch_file = filedialog.askopenfilename(initialdir = cdir + "/cad_files/",defaultextension=".dxf", filetypes=[("CAD Files", "*.dxf"), ("All Files", "*.*")])
    
    input_arch2.configure(text= os.path.basename(input_arch_file))
       
def in_label():
    
    global input_label_file

    input_label_file = filedialog.askopenfilename(initialdir = cdir + "/cad_files/",defaultextension=".dxf", filetypes=[("CAD Files", "*.dxf"), ("All Files", "*.*")])
    
    input_label2.configure(text=  os.path.basename(input_label_file))
    
 
def run_script():
     
    global input_arch_file
    global input_label_file
    global cdir


    progressbar.start()
    progressbar.configure(mode="determinate")
    
    
     
    if input_arch_file:    
        input_arch_file = "-fa " + input_arch_file
    
    if input_label_file:
        input_label_file = "-fl " + input_label_file
    
    
    if p1b.get():
        v = "-v " 
    else:
        v = ""
    
    if p2b.get():
        vv = "-vv "
    else:
        vv = ""
    
    if sz_entry.get():
        sz = "-sz " + sz_entry.get()
    else:
        sz = ""
        
    if bl_entry.get():
        bl = "-bl " + bl_entry.get()
    else:
        bl = ""
        
    if p3b.get():
        l = "-l " 
    else:
        l = ""
      
    output_file = "outfile"
       
    os.system("python dxf_to_graph_converter_label.py {} {} {} {} {} {} {} {}".format(input_arch_file, input_label_file,"-o "+ output_file ,v,vv,sz,bl,l))
    input_arch_file =""
    input_label_file=""
    v=""
    vv=""
    sz=""
    bl=""
    l=""
    
    # Waiting time to create the CAD file
    
    time.sleep(10)
    
    # Open the output file
    
    output_file = cdir + "/" + output_file
    if os.path.exists(output_file+".svg"):
        
        with open(output_file+".svg", "rb") as f:
            svg_file = f.read()
        cairosvg.svg2png(bytestring=svg_file, write_to='out.png',output_width=1500,output_height=1000)
        cairosvg.svg2png(bytestring=svg_file, write_to='out_dark.png',background_color='#222222',output_width=1500,output_height=1000)
        
        output_file_name = "out.png"

    else:
        print("Output file not found.")
        

    output_label2.configure(text="Output File: "+ "out.png")
    fram2.after(100, update_canvas)
    
    progressbar.set(100)
    progressbar.stop()
    

    
    # G = nx.Graph()
    
    
    # # Read in the YAML data
    # with open(cdir + "/"+"outfile.yaml", "r") as f:
    #     data = yaml.safe_load(f)
        
    # # Add nodes with attributes    
    # for node, attrs in data["nodes"]:
    #     G.add_node(node, **attrs)
     
    # # Add edges with attributes
    # for source, targets in data["edges"]:
    #     for target, attrs in targets:
    #         G.add_edge(source, target, **attrs)   
    
    # print(G)    
    # nx.draw(G)
    # plt.show()

       
def help_update():
    
    if help_button.configure('relief')[-1] == 'sunken':
        
        tooltip.show_tip(" The documentation for the software is provided in the README file. \n To use the converter, you can try the following steps. \n 1. Choose an architecture file\n 2. Choose an input label file \n 3. Select Verbose or  Very verbose checkboxes \n 4. Enter a step size \n 5. Click on Run script to again run the converter. ")
   
    pass 
    
      

#############################################

input_arch = ctk.CTkLabel(fram1, text="Input Architecture File:",font=myfont,wraplength=300)
input_arch.grid(row=0, column=0,padx=10, pady=(10, 0))

input_arch2 = ctk.CTkLabel(fram1,font=myfont,wraplength=300,text="")
input_arch2.grid(row=0, column=1,padx=10, pady=(10, 0))

input_arch_button = ctk.CTkButton(fram1, text="Select Input Architecture File", font=myfont,command=in_arch)
input_arch_button.grid(row=1, column=0,padx=10, pady=(10, 0))


tooltip_arc = ToolTip(input_arch_button)
input_arch_button.bind("<Enter>", lambda event: tooltip_arc.show_tip("Provide an architecture file"))
input_arch_button.bind("<Leave>", lambda event: tooltip_arc.hide_tip())

####################################################

input_label = ctk.CTkLabel(fram1, text="Input Label File:",font=myfont,wraplength=300)
input_label.grid(row=2, column=0,padx=10, pady=(10, 0))

input_label2 = ctk.CTkLabel(fram1,font=myfont,wraplength=300,text="")
input_label2.grid(row=2, column=1,padx=10, pady=(10, 0))

input_label_button = ctk.CTkButton(fram1, text="Select Label Input File",font=myfont, command=in_label)
input_label_button.grid(row=3, column=0,padx=10, pady=(10, 0))

tooltip_lbl = ToolTip(input_label_button)
input_label_button.bind("<Enter>", lambda event: tooltip_lbl.show_tip("Provide a label file"))
input_label_button.bind("<Leave>", lambda event: tooltip_lbl.hide_tip())

#################################################

p1b = tk.IntVar()
param1_box = ctk.CTkCheckBox(fram1,text="  Verbose",font=myfont,variable=p1b)
param1_box.grid(row=4, column=0,padx=10, pady=(10, 0))

###############################################

p2b = tk.IntVar()
param2_box = ctk.CTkCheckBox(fram1,text="  Very Verbose",font=myfont,variable=p2b)
param2_box.grid(row=4, column=1,padx=10, pady=(10, 0))

###############################################################3

p3b = tk.IntVar()
param3_box = ctk.CTkCheckBox(fram1,text="  Labels",font=myfont,variable=p3b)
param3_box.grid(row=5, column=0,padx=10, pady=(10, 0))


###########################################################
sz_label = ctk.CTkLabel(fram1, text="Step Size:",font=myfont)
sz_label.grid(row=6, column=0,padx=10, pady=(10, 0))


sz_entry = tk.Entry(fram1)
sz_entry.grid(row=6, column=1,padx=10, pady=(10, 0))


########################################################

bl_label = ctk.CTkLabel(fram1, text="Building Name:",font=myfont)
bl_label.grid(row=7, column=0,padx=10, pady=(10, 0))

bl_entry = tk.Entry(fram1)
bl_entry.grid(row=7, column=1,padx=10, pady=(10, 0))

tooltip_bl = ToolTip(bl_entry)
bl_entry.bind("<Enter>", lambda event: tooltip_bl.show_tip("Provide a building name."))
bl_entry.bind("<Leave>", lambda event: tooltip_bl.hide_tip())

########################################################

output_label2 = ctk.CTkLabel(fram1, text="Output File: ",font=myfont)
output_label2.grid(row=8, column=0,padx=10, pady=(10, 0))

###########################################################

clear_button = ctk.CTkButton(fram1, text="Reset", font=myfont,command=clear_canvas)
clear_button.grid(row=9, column=0,padx=10, pady=(10, 0))


###########################

run_button = ctk.CTkButton(fram1, text="Run Script", font=myfont,command=run_script)
run_button.grid(row=9, column=1,padx=10, pady=(10, 0))



######################################################

yaml_button = ctk.CTkButton(fram1, text="Save Graph File", font=myfont,command=save_yaml)
yaml_button.grid(row=10, column=0,padx=10, pady=(10, 0))

###############################################################3

save_button = ctk.CTkButton(fram1, text="Save PNG File",font=myfont, command=save_file)
save_button.grid(row=10, column=1,padx=10, pady=(10, 0))

##################################################################

# Create the Zoom In and Zoom Out buttons
d_img_btn = ctk.CTkButton(fram1, text="Dark Mode Image", font=myfont, command=dark_canvas)

d_img_btn.grid(row=11, column=0,padx=10, pady=(10, 0))

#######################################################################################

l_img_btn = ctk.CTkButton(fram1, text="Light Mode Image", font=myfont, command=update_canvas)

l_img_btn.grid(row=11, column=1,padx=10, pady=(10, 0))

##############################################################
dm_plot_btn  = ctk.CTkButton(fram1, text="Open Dark Image in Matplot", font=myfont, command=dmat_plot)
dm_plot_btn.grid(row=12, column=0,padx=10, pady=(10, 0))

#####################################################################3

m_plot_btn = ctk.CTkButton(fram1, text="Open Image in Matplot", font=myfont, command=mat_plot)

m_plot_btn.grid(row=12, column=1,padx=10, pady=(10, 0))

################################################################
appearance_mode_label = ctk.CTkLabel(fram1, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=13, column=0, padx=10, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(fram1, values=["Dark", "Light", "System"],command=change_appearance_mode_event)

appearance_mode_optionemenu.grid(row=13, column=1, padx=10, pady=(10, 0))

############################################################

scaling_label = ctk.CTkLabel(fram1, text="UI Scaling:", anchor="w")
scaling_label.grid(row=14, column=0, padx=10, pady=(10, 0))
scaling_optionemenu = ctk.CTkOptionMenu(fram1, values=["100%","50%","60%","70%","80%", "90%", "110%", "120%","130%","140%","150%"],command=change_scaling_event)

scaling_optionemenu.grid(row=14, column=1, padx=10, pady=(10,0))

####################################################################

prog_label = ctk.CTkLabel(fram1, text="Progress")
prog_label.grid(row=15, column=0, padx=10, pady=(10, 0))

progressbar = ctk.CTkProgressBar(fram1)
progressbar.grid(row=15,column=1,padx=10, pady=(10, 0))
progressbar.configure(mode="determinate")
progressbar.set(0)

###################################################################3

# terminal = Terminal(fram1)
# terminal.grid(row =18,column = 0)

###############################################################

help_button = ctk.CTkButton(fram1, text="Help",font=myfont,command= lambda: (help_update, tooltip.show_tip(" The documentation for the software is provided in the README file. \n To use the converter, you can try the following steps. \n 1. Select an architecture file\n 2. Select an input label file \n 3. (Optional) Tick the Verbose or  Very verbose checkboxes \n 4. (Optional) Enter a step size \n 5. (Optional) Provide a building name \n If you want to provide a different set of inputs,  use the Run Script button")))
help_button.grid(row=17, column=1,padx=10, pady=(10, 0))

##################################################
# Create a tooltip for the update button
tooltip = ToolTip(help_button)
help_button.bind("<Leave>", lambda event: tooltip.hide_tip())

######################################################################3

def force_quit():
    root.destroy()

force_quit_button = ctk.CTkButton(fram1, text="Quit", font=myfont,command=force_quit)
force_quit_button.grid(row=17, column=0,padx=10, pady=(10, 0))


root.mainloop()

############################################
