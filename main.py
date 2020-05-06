import os
import sys
import threading

try:
    import re, requests
except ModuleNotFoundError:
    os.system('pip install re && pip install requests')

#----- Color Format -----#
R = '\033[31m'
G = '\033[32m'
Y = '\033[33m'
B = '\033[34m'
M = '\033[35m'
C = '\033[36m'
W = '\033[37m'
BR= '\033[91m'
BG= '\033[92m'
BY= '\033[93m'
BB= '\033[94m'
BM= '\033[95m'
BC= '\033[96m'
BW= '\033[97m'

#----- Table Format -----#
def tables(a,b,c,d):
	return "{:10}  {:10} {:10} {:10}".format(a,b,c,d)
def table(a,b,c,d,e):
	return "{:22}  {:20} {:20} {:20} {:13}".format(a,b,c,d,e)

if not os.path.exists('data'):
    os.mkdir('data')

#----- Open TXT File -----#
tulis = open('data/proxy_result.txt','a+')
RouterOS = open('data/RouterOS.txt','a+')
Mikrotik = open('data/Mikrotik.txt','a+')

tempw = open('data/temp','a+')
tempr = open('data/temp','r+')


#----- All Variables Here -----#
mode = 'http://'
r1b = r1a = r2b = r2a = 0
count=1
succ=0
fail=0
to = 10
ip=[]
threads=[]

#----- All Functions -----#
def prints(teks):
        sys.stdout.write(teks)

def welcome():
  def printf(p1, p2):
    return "{:<27}  {:>0}".format(p1, p2)
  os.system('clear')
  print(G)
  print(printf(f'{G}         _____',f'|  {Y}PROXY{W}'))
  print(printf(f'{G}        / //  \\',f'|    {Y}PORT{W}'))
  print(printf(f'{G}       / // /\\ \\',f'|      {Y}SCANNER{W}'))
  print(printf(f'{G}      / // /__\\_\\',f'| {C}V1.0{W}'))
  print(printf(f'{G}     / //_______ \\','|'))
  print(printf(f'{G}    / //_/______\\ \\','| Created by.'))
  print(printf(f'{G}   / //____________\\',f'|   {BR}Luthfi zXc{W}'))
  print(printf(f'{G}   \\_______________/','|'))
  print('\n\033[31m        Yt: \033[33mhttp://youtube.com/luthfizxc\n')
  print(f'{Y}Make sure your internet connection stabil and fast before using this tool')

def menu():
        global tb,ta,pb,pa
        welcome()
        print(C+'\n#------------------------------------------------#'+W)
        print(f'{Y} Masukkan Range Proxy ')
        print(f'{BM} Contoh: min = 127.28.88.0  | max = 127.28.91.255')
        tb = str(input(f'   {R}[!]{G} Masukkan Batas Bawah (min) : {Y}'))
        tempw.write(tb+'\n')
        ta = str(input(f'   {R}[!]{G} Masukkan Batas atas  (max) : {Y}'))
        tempw.write(ta+'\n')
        print(C+'#------------------------------------------------#'+W)
        os.system('clear')
        welcome()
        print(C+'\n#------------------------------------------------#'+W)
        print(f'{Y} Masukkan Range Port')
        print(f'{BM} Contoh: from 80 to 1000 ')
        pb = int(input(f'   {R}[!]{G} From : {Y}'))
        pa = int(input(f'   {R}[!]{G} To   : {Y}'))
        print(C+'#------------------------------------------------#'+W)
        os.system('clear')
        welcome()
        print(C+'\n#------------------------------------------------#'+W)


def filter():
        global r1b,r1a,r2b,r2a
        i=0
        head = re.search(r'(.*)\.\d+\.\d+', tb).group(1)
        r1b = re.search(r'\d+\.\d+\.(.*?)\.\d+', tb).group(1)
        r1a = re.search(r'\d+\.\d+\.(.*?)\.\d+', ta).group(1)
        r2b = re.search(r'\d+\.\d+\.\d+\.(.*)', tb).group(1)
        r2a = re.search(r'\d+\.\d+\.\d+\.(.*)', ta).group(1)
        for r1 in range(int(r1b), int(r1a) + 1):
                for r2 in range(int(r2b), int(r2a) + 1):
                        v = f'{head}.{str(r1)}.{str(r2)}'
                        ip.append(v)
                        i = i + 1
        return ip

def req(ip,port):
        global count,succ,fail
        try:
                zz = 'http://' + str(ip) + ':'+str(port)
                r = requests.get(zz, timeout=to)
                tulis.write(ip + ':'+port+'\n')
                if 'RouterOS' in r.text:
                	RouterOS.write(ip + ':'+port+'\n')
                if 'Mikrotik' in r.text:
                	Mikrotik.write(ip + ':'+port+'\n')
                succ = succ+1
        except KeyboardInterrupt:
                print('\nExit')
                tulis.close()
                exit()
        except:
                fail = fail+1
        
        cck= table(f'\r{Y}|{BM}  {count}',f'{Y}|{BG}  {succ}',f'{Y}|{BR}  {fail}',f'{Y}|{W}  {str(threading.active_count())}',f'   {Y}|{W}')
        prints(cck)
        count +=1


#----- RUN PROGRAM -----#
if __name__ == '__main__':
        menu()
        filter()
        global cck
        hitung = (int(r1a)-int(r1b)+1)*(int(r2a)-int(r2b)+1)*(pa-pb+1)
        print(f'{Y}Proxy: {tb} - {ta}  | Port: {pb} - {pa}')
        print(f'{BG}Checking '+str(hitung)+' proxies\n')
        print(f'{BY}Please wait....')
        print(' ________________________________________________')
        print(tables('|  Checking','|  Success','|  Fail','| Thread Core |'))

        for b in ip:
                for d in range(pb,pa+1):

                    t= threading.Thread(target=req,args=(b,str(d),))
                    threads.append(t)
                    

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f'\n\n{W}Scanned Proxy saved to : {os.getcwd()}/data/proxy_result.txt')
tulis.write('\n')
tulis.close()