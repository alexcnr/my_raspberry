import os, time, sys
import subprocess
import os
#f = open('/opt/vc/bin/vcgencmd measure_temp', 'r')
#print(f)
#f.read()

print(subprocess.check_output(["echo", "Hello World!"]))

#code = subprocess.call("/opt/vc/bin/vcgencmd measure_temp")

myCmd = 'ls -la' 
os.system (myCmd)
myCmd2 = '/opt/vc/bin/vcgencmd measure_temp'
print(type(myCmd2))
myCmd3 = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()
print(myCmd3)


#vb = subprocess.Popen(['watch -n 1 "vcgencmd measure_temp"'])
#ptint(vb)