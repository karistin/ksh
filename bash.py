#!/usr/bin/env python
import os
import signal
import sys
import curses

'''
1. local var 
2. export err (re)
err case 
    echo $A
3. local var tests
4. stream : 시간에 흐름에 따라 이용가능한 데이터 원소의 수열 
(과거나 마래의 데이터를 읽지 못한다.)
'''
local_dict={}

def get_env(cmd):
    env_paths = os.getenv('PATH').split(":")
    for env_path in env_paths:
        if os.path.isfile(f'{env_path}/{cmd}'):
            return f'{env_path}/{cmd}'
    return 0

def changedir(args):
    if len(args) == 1:
        os.chdir("/home/ksj")
    elif args[1] == "..":
        os.chdir("..")
    else:
        if os.path.isdir(args[1]):
            os.chdir(f'{args[1]}')
        else:
            print(f'cd: no such file or directory: {args[1]}')
            return

def exefile(args):
    filename = args[0][2:]
    if os.path.isfile(filename):
        pid = os.fork()
        if pid == 0:
            os.execvp(args[0],[" "])
        else:
            os.waitpid(pid,0)
    else:
        print(f'ksh: no such file of directory : {args[0]}')
        return

def export_var(cmds, args):
    # print(cmds)
    if len(cmds) < 2:
        env = os.environ
        for key in env.keys():
            print(f'{key}={env[key]}')
    elif cmds[1].find("=") > 0:
        words=args[1].split("=")
        if len(words)==2:
            os.environ[words[0]] = words[1]

def unset(key):
    if os.getenv(key[1]):
        if key[1] in os.environ:
            os.environ.pop(key[1])
    elif local_dict[key[1]]:
        local_dict.pop(key[1])
    else:
        print("ksh : no unset environ")

def local_var(cmds):
    words=cmds[1].split("=")
    if len(words)==2:
        local_dict[words[0]] = words[1]

def print_set():
    env = os.environ
    for key in env.keys():
        print(f'{key}={env[key]}')
    for dict in local_dict.keys():
        print(f'{dict}={local_dict[dict]}')
    #좀 다른듯?

def main():
    print(f'{os.getcwd()}') #pwd
    t = input("#> ")
    if t == "exit": #종료
        exit(0)
    if t == "":
        return 0
    cmds = t.split(' ')  
    cmd = cmds[0]
    words = cmd.split("=")
    args = cmds[0:]

    if not args:
        args = [" "]
    
    # FIXME: errors...
    for arg in args:
        if arg[0] == "$":
            # print(arg)
            if os.getenv(arg[1:]):
                args[args.index(arg)] = os.environ[arg[1:]] # 환경 변수에서 찾기
            elif local_dict.get(arg[1:]):
                args[args.index(arg)] = local_dict[arg[1:]]
    #a=3
    if len(words)==2:
        local_dict[words[0]] = words[1]
    elif cmd == "cd": # cd
        changedir(args)
    elif cmd[:2] == "./": #shebang
        exefile(args)
    elif cmd =="export":
        export_var(cmds , args) #export
    elif cmd =="unset":
        unset(args)
    elif cmd == "local":
        local_var(cmds)
    elif cmd == "set":
        print_set()
    else:
        path = get_env(cmd)
        if path == 0:
            print(f'ksh: command not found: {cmd}')
        else:
            pid = os.fork()

            if pid == 0:
                os.execvp(f'{path}', args )
            else:
                os.waitpid(pid,0)
    print()#줄 한칸 뛰기

def Exit_gracefully(signal, frame):
    print("program shutdown")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    while True:
        main()