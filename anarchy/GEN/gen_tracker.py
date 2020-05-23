import os
from anarchy.cryptography.host import host

def replace_dir(server_name,path):
    ldir = os.listdir('TRACKER')
    os.mkdir(path+server_name)
    for i in ldir:
        inp = open('TRACKER/'+i,'r')
        outp = open(path+server_name+'/'+i,'w+')
        lines = inp.readlines()
        for j in lines:
            outp.write(j.replace('tracker',server_name))
        inp.close()
        outp.close()
    host.gen_key(host.gen_pk(path+server_name+'/TRACKER_PK',True,b'1234'),path+server_name+'/TRACKER_KEY',True)

if __name__ == '__main__':
    for i in range(2,5):
        replace_dir("tracker"+str(i),'../../')
