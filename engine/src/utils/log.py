from colorama import Fore, Back, Style
import inspect

def error(e):
    # get caller funciton name  
    curname = inspect.currentframe()
    calframe = inspect.getouterframes(curname, 2)
    f = calframe[1][3]
    print(Fore.GREEN + f"{f}:" + Fore.RED + f"\t {e}")

def info(e):
    curname = inspect.currentframe()
    calframe = inspect.getouterframes(curname, 2)
    f = calframe[1][3]
    print(Fore.GREEN + f"{f}:" + Fore.YELLOW + f"\t {e}")

def debug(e):
    curname = inspect.currentframe()
    calframe = inspect.getouterframes(curname, 2)
    f = calframe[1][3]
    print(Fore.GREEN + f"{f}:" + Fore.WHITE + f"\t {e}")

def log(e, p=True):
    f = open('log.txt', 'a')
    line = ''

    caller = inspect.stack()
    for call in caller[::-1]:
        call = f"{call[1].split('/')[-1]} • {call[3]} • {call[2]} • {call[4][0].strip()}"
        line += call + ' ► '
    
    line += f" => {e} \n"
    f.write(line)
    f.close()
    if p:
        print(line)

def pprint(e):
    print(e)