import os
from unnamed.cryptography.host import host

def replace_dir(server_name,path):
    ldir = os.listdir('SERVER')
    os.mkdir(path+server_name)
    for i in ldir:
        inp = open('SERVER/'+i,'r')
        outp = open(path+server_name+'/'+i,'w+')
        lines = inp.readlines()
        for j in lines:
            outp.write(j.replace('test_server1',server_name))
        inp.close()
        outp.close()
    host.gen_key(host.gen_pk(path+server_name+'/SERVER_PK',True,b'1234'),path+server_name+'/SERVER_KEY',True)

if __name__ == '__main__':

    replace_dir("server1",'../../')
