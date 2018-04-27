import shutil
import os.path
from fileinput import close
import subprocess

debug_file = "get_geometry.py"
blender_exe = "c:\\eclipse\\blender\\blender.exe"
argument = " -v -P \"%s\""

shutil.copy("C:\\ws3_ox\\Blender_Optimizations\\"+debug_file,"C:\\ws3_ox\\Blender_Optimizations\\__copied.py")

abs_copied = os.path.abspath("C:\\ws3_ox\\Blender_Optimizations\\__copied.py")

test =  "start \"\" \"%s\"" % blender_exe

subprocess.run([blender_exe,"-P", abs_copied])
