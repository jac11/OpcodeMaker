#!/usr/bin/env python3

import re
import os
import time 
import sys
import shutil
import subprocess  
import argparse
import pathlib

W = '\033[0m'     
R = '\033[31m'    
G = '\033[0;32m'  
O = '\33[37m'     
B = '\033[34m'    
P = '\033[35m'   
Y = '\033[1;33m' 
  
class Shell_Dump:

      def __init__(self):
              
        self.parser()       
        self.main()
        
      def Banner(self):
         self.Banner = """   
                                                                                                         
                         8                      8               
.d8b. 88b. .d8b .d8b. .d88 .d88b 8d8b.d8b. .d88 8.dP .d88b 8d8b 
8' .8 8  8 8    8' .8 8  8 8.dP' 8P Y8P Y8 8  8 88b  8.dP' 8P   
`Y8P' 88P' `Y8P `Y8P' `Y88 `Y88P 8   8   8 `Y88 8 Yb `Y88P 8    
      8   by:jacstory                                                                                                                  
                      """ 
         print(self.Banner)
      def Create_file(self):
         try: 
             try: 
                    
                 self.dir_1= "Shell_Dump"
                 self.ShellCode = 'ShellCode'
                 path = os.getcwd()   
                 create= os.path.join(path,self.dir_1)
                 create1= os.path.join(path,self.ShellCode)
                 os.mkdir(create)
                 os.mkdir(create1)
                 time.sleep(2) 
                 os.chdir(self.dir_1)
                  
                 print(O+"\n[+] Create file .....| ",os.getcwd())       
                 
             except OSError:
                 time.sleep(2)
                 os.chdir(self.dir_1)
                 print(O+"\n[+] file Exist .....| ",os.getcwd())
                 time.sleep(2)
         except KeyboardInterrupt:
              print(self.Banner)
              exit() 
      def file_path(self):
          
          try:
            try: 

                if self.args.code: 
                    self.file_cname = os.path.basename(self.args.code)
                    self.path_code =  os.path.abspath(self.args.code)
                if self.file_cname[-4::]==".asm":
                   pass
                else:
                     time.sleep(2)
                     print(R+"\n[*] Error ......| File Extension Not Correct "+W)
                     exit()
                time.sleep(2)
                
                self.fpath = shutil.copy(self.path_code , "./")
                self.file1 = str( self.file_cname[:-4] +  ".obj")
                self.file2 = str( self.file_cname[:-4] +  ".dump")
                self.file3 = str( self.file_cname[:-4] +  "_shellcode")
                self.file4 = str( self.file_cname[:-4] +  ".Linker")
            except IOError  as E:
                 time.sleep(1)
                 print(R+"\n[+] Error ......| ",E)
                 exit() 
            except Exception as E:
                 time.sleep(1)
                 print(R+"\n[+] Error ......| ",E)
                 exit()                       
          except KeyboardInterrupt:
              print(self.Banner)
              exit()   
      def IF_OPtion(self):
           try:     
                 if self.args.arch86 and "0" in sys.argv[4] :         
                    self.fpath = shutil.copy(self.path_code,"./") 
                    code = subprocess.call(['nasm','-f','elf32',"{}".format(self.file_cname),'-o','{}'.format(self.file1)])
                    if code == 1 :
                           print()
                           print(R+"\n[+] Error ......| Instruction Not Completed Not Supported in 86-bit Mode [!]"+W)  
                           time.sleep(1)
                           exit()
                    else:
                          time.sleep(2)
                          print("\n[*] Status .......| The Object File x86 is Generated  !! ")                  
                 elif self.args.arch64 and "1" in sys.argv[4] :               
                       code = subprocess.call(['nasm','-f','elf64',"{}".format(self.file_cname),'-o','{}'.format(self.file1)])                     
                       if code == 1 :
                           print()
                           print(R+"\n[+] Error ......| Instruction Not Completed Not Supported in 64-bit Mode [!]"+W)
                           time.sleep(2)
                           exit()
                       else:
                          print("\n[*] Status .......| The Object File x64 is Generated !! ") 
                          time.sleep(2)  
                 else :
                       print(Y+"\n[+] Error ......| ArgumentParser "+W)
                       exit()    
                        
           except KeyboardInterrupt:
              print(self.Banner)
              exit()  
                         
      def LINKER_ASSEMBLY(self):
          try:
             time.sleep(2)        
             print("\n[*] Status .......| The Linker Process Started \n ")
             time.sleep(2)
             subprocess.call(['ld','-n','-o','{}'.format(self.file4),'{}'.format(self.file1)])
             with open(self.file2,'w')as file:                 
                stdout =  subprocess.call(['objdump','-d','{}'.format(self.file1)], stdout=file, stderr=file)   
          except KeyboardInterrupt:
              print(self.Banner)            
              exit()                    
      def replace(self):
          try:
              with open(self.file2,"r") as file:
                        read = file.read()  
              findall= str(re.findall(":....................\D",read))
           
              Header = findall.replace(":","")
              Header = Header.replace("   ",'')
              Header = Header.replace("\\s","") 
              Header = Header.replace("\\t","")
              Header = Header.replace(",","")
              Header = Header.replace("' '","") 
              Header = Header.replace(" ","")
              Header = Header.replace("[","")
              Header = Header.replace("]","")
              Header = Header.replace("'","")
             
              Header= "".join("\\x%s"%Header[i:i+2] for i in range(0, len(Header), 2))
              Header= "".join('\n"%s"'%Header[i:i+56] for i in range(0, len(Header),56))
              
              with open(self.file3,'w')as file: 
                     file.write(Header) 
              with open (self.file3,'r')as test:
                      self.test= test.read()
                      print()
                      print(Y+"\t\t\t\t\t\t{%}THE SHELLCODE{%}"+W)
                      print(Y+"\t\t\t\t\t[@]++++++++++++++++++++++++++[@]\n"+W)
                      time.sleep(1)
                      print(B+self.test+W)
                      print(Y+"\n\t\t\t\t\t[@]++++++++++++++++++++++++++[@]\n"+W)
                      time.sleep(1)
              print(P+"\n[*] Status Files save at .....| ",os.getcwd())
              print(W)
          except KeyboardInterrupt:
              print(self.Banner)            
              exit()  
      def Copy_file(self):
           
            with open("../ShellCode/"+self.file_cname[:-4]+".c",'w') as Pro :
                  Pro.write("#include <stdio.h>\n"+"#include <string.h>\n\n"+"const unsigned char code[] = \\"+'\r'+self.test+";\n\nint main ()\n{\t\n"\
                  + '\tprintf("Shellcode Length:  %d\\n"'+", strlen(code));\n"+"\tint (*ret)() = (int(*)())code;\n"+"\tret();\n\n}") 
            print(self.Banner)
            exit()
      def parser(self):
           try:
               parser = argparse.ArgumentParser( description="Usage: <OPtion> <arguments> ")
               parser = argparse.ArgumentParser(description=" ")
               parser.add_argument( '-c'  ,"--code"     ,metavar=''   , action=None  ,help ="  file has assembly code  ")
               parser.add_argument( '-x86',"--arch86"   ,metavar=''   , action=None  ,help ="  Process architecture 32bit")
               parser.add_argument( '-x64',"--arch64"   ,metavar=''   , action=None  ,help ="  Process architecture 64bit ")
               self.args = parser.parse_args()
               if len(sys.argv)!=1 and len(sys.argv) != 3:
                   pass
               else:
                  parser.print_help()
                  exit()
           except argparse.ArgumentError : 
                    parser.print_help()
                    exit()                            
      def main(self): 
             if ( self.args.code and self.args.arch86) \
             or  (self.args.code and self.args.arch64) :
                     self.Banner()
                     self.Create_file()
                     self.file_path()       
                     self.IF_OPtion()
                     self.LINKER_ASSEMBLY()
                     self.replace()  
                     self.Copy_file()
                
               
if __name__=="__main__": 
       Shell_Dump()
        

