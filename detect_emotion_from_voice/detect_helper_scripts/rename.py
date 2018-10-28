#script to rename the Berlin Emo dataset (http://emodb.bilderbar.info/index-1024.html) to RAVDESS(https://zenodo.org/record/1188976)
import os
import sys
i = 1
pt = '/home/mainpetru/Downloads/audio_samples/download/www1/'
for fname in os.listdir('/home/mainpetru/Downloads/audio_samples/download/www1/'):
  s = os.path.splitext(os.path.basename(fname))
  in_clist = []
  for c in s[0]:
    in_clist.append(c)
  out_clist = ['0', '3', '-', '0', '1','-']
  if in_clist[5] == 'W':
    out_clist.append('0')
    out_clist.append('5')
    out_clist.append('-')
  elif  in_clist[5] == 'L':
    out_clist.append('0')
    out_clist.append('2')
    out_clist.append('-')
  elif in_clist[5] == 'E':
    out_clist.append('0')
    out_clist.append('7')
    out_clist.append('-')
  elif  in_clist[5] == 'A':
    out_clist.append('0')
    out_clist.append('6')
    out_clist.append('-')
  elif in_clist[5] == 'F':
    out_clist.append('0')
    out_clist.append('3')
    out_clist.append('-')
  elif  in_clist[5] == 'T':
    out_clist.append('0')
    out_clist.append('4')
    out_clist.append('-')
  elif  in_clist[5] == 'N':
    out_clist.append('0')
    out_clist.append('1')
    out_clist.append('-')

  out_clist.append('0')
  out_clist.append('1')
  out_clist.append('-')

  if(in_clist[2] == 'a'):
    if(in_clist[4] == '1'):
      out_clist.append('0')
      out_clist.append('3')
      out_clist.append('-')
    elif(in_clist[4] == '2'):
      out_clist.append('0')
      out_clist.append('4')
      out_clist.append('-')
    elif(in_clist[4] == '4'):
      out_clist.append('0')
      out_clist.append('5')
      out_clist.append('-')  
    elif(in_clist[4] == '5'):
      out_clist.append('0')
      out_clist.append('6')
      out_clist.append('-') 
    elif(in_clist[4] == '7'):
      out_clist.append('0')
      out_clist.append('7')
      out_clist.append('-')
  else:
    if(in_clist[4] == '1'):
      out_clist.append('0')
      out_clist.append('8')
      out_clist.append('-')
    elif(in_clist[4] == '2'):
      out_clist.append('0')
      out_clist.append('9')
      out_clist.append('-')
    elif(in_clist[4] == '3'):
      out_clist.append('1')
      out_clist.append('0')
      out_clist.append('-')  
    elif(in_clist[4] == '9'):
      out_clist.append('1')
      out_clist.append('1')
      out_clist.append('-') 
    elif(in_clist[4] == '0'):
      out_clist.append('1')
      out_clist.append('2')
      out_clist.append('-')



  if(in_clist[2] == 'a'):
    out_clist.append('0')
    out_clist.append('3')
    out_clist.append('-')
  elif(in_clist[2] == 'b'):
    out_clist.append('0')
    out_clist.append('3')
    out_clist.append('-')
  elif(in_clist[2] == 'c'):
    out_clist.append('0')
    out_clist.append('4')
    out_clist.append('-')
  elif(in_clist[2] == 'd'):
    out_clist.append('0')
    out_clist.append('5')
    out_clist.append('-')
  elif(in_clist[2] == 'e'):
    out_clist.append('0')
    out_clist.append('6')
    out_clist.append('-')
  elif(in_clist[2] == 'f'):
    out_clist.append('0')
    out_clist.append('7')
    out_clist.append('-')
  elif(in_clist[2] == 'g'):
    out_clist.append('0')
    out_clist.append('8')
    out_clist.append('-')
  elif(in_clist[2] == 'h'):
    out_clist.append('0')
    out_clist.append('9')
    out_clist.append('-')


  if (in_clist[1] == '3'):
    out_clist.append('2')
    out_clist.append('5')
  elif(in_clist[1] == '0'): 
    out_clist.append('2')
    out_clist.append('7')
  elif(in_clist[1] == '1'): 
    out_clist.append('2')
    out_clist.append('9')
  elif(in_clist[1] == '2'): 
    out_clist.append('3')
    out_clist.append('1')
  elif(in_clist[1] == '5'): 
    out_clist.append('3')
    out_clist.append('3')
  elif(in_clist[1] == '8'): 
    out_clist.append('2')
    out_clist.append('6')
  elif(in_clist[1] == '9'): 
    out_clist.append('2')
    out_clist.append('8')
  elif(in_clist[1] == '3'): 
    out_clist.append('3')
    out_clist.append('0')
  elif(in_clist[1] == '4'): 
    out_clist.append('3')
    out_clist.append('2')
  elif(in_clist[1] == '6'): 
    out_clist.append('3')
    out_clist.append('4')

  print(out_clist)
  out_name = ''.join(out_clist)

  new_name = out_name + ".wav"

  script = "sudo mv " + pt + fname + " " + pt + new_name
  os.system("bash -c '%s'" % script)
  i = i +1 



  
