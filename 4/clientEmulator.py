import xmlrpclib, sys
import imageModifier
from matplotlib.pyplot import imread

host, port = 'ross-LBL.dhcp.lbl.gov', 5010
server = xmlrpclib.ServerProxy("http://%s:%d" % (host, port))
available_methods = server.system.listMethods()
print "Available methods from server:"
for method in available_methods:
    print "\t" + method

print '''For help on a given method, type:
         print server.system.methodHelp(' <method name> ') '''
#img = imread('/home/ross/Dropbox/AY250/HW/3/50_categories/elk/elk_0001.jpg')
#imgVec = imageModifier.packImage(img)
#orig, rotated = server.rotateImage(imgVec, 45)
