#!/usr/bin/env python
# -*-coding:utf-8-*-
import sys
import os
import time
import threading
import re

a = 0
out = sys.stdout
pr_s = False
pr_pause = False
wr_s = False
sgkdir = unicode("D:\\wy52g\\126\\126\\", "utf8").encode("gbk")
result_file = "d:\\126\\126.txt"
result_n = 3
result_queue = []
max_size = 500 * 1024 * 1024 #MB


class config_handler(object):
    __choose = None
    __remind = True
    __ig_temp = 0
    __ig_n = 0

    def __init__(self):
        self.__configs = []
        jump = 12 - 1
        n = 0
        with open("rulers.txt", "rt") as config_file:
            rulers_lines = config_file.readlines()
        line_sum = len(rulers_lines)
        while jump < line_sum:
            line = rulers_lines[jump].strip()
            if re.match(r"\d+:", line):
                self.__configs.append([])
                for i in range(6):
                    jump += 1
                    self.__configs[n].append(rulers_lines[jump].strip())
                if self.__configs[n][0] == "{%None%}":
                    raise ValueError("signatures can't be empty!")
                n += 1
            jump += 1
        self.__last = len(self.__configs)

    def get(self):
        return self.__configs

    def __re_handle(self, re_text):
        n = None
        if re.search(r"{%(\d+)%}$", re_text):
            n_re = re.search(r"{%(\d+)%}$", re_text)
            n_text = n_re.group(0)
            n = int(n_re.group(1))
            re_text = re_text.replace(n_text, "")
        if re.search(re_text, self.o_text):
            f_re = re.search(re_text, self.o_text)
            if n is None:
                return f_re.group(0)
            else:
                if f_re.group(n) is None:
                    return "{%None%}"
                else:
                    return f_re.group(n)
        else:
            return "{%None%}"

    def __handele_re(self, re_text):
        while True:
            if re_text == "":
                return "{%None%}"
            else:
                if re.search(re_text, self.o_text):
                    temp = re.search(re_text, self.o_text)
                    if len(temp.groups()) > 0:
                        print "Multiple sub-matching results:"
                        print "0:"
                        print temp.group(0)
                        n = 1
                        for i in temp.groups():
                            print str(n) + ":"
                            print i
                            n += 1
                        choose = raw_input("Which to choose?:")
                        if choose > 0:
                            re_text += "{%" + choose + "%}"
                            print "result:"
                            result = self.__re_handle(re_text)
                            print result
                            confirm = raw_input("confirm?(Y/N)")
                            if confirm == 'Y' or confirm == 'y':
                                print "ok"
                                self.__result += result
                                self.__result += "{%|%}"
                                return re_text
                            if confirm == 'N' or confirm == 'n':
                                re_text = raw_input("Enter again:")
                                continue
                        else:
                            print "result:"
                            result = self.__re_handle(re_text)
                            print result
                            confirm = raw_input("confirm?(Y/N)")
                            if confirm == 'Y' or confirm == 'y':
                                print "ok"
                                self.__result += result
                                self.__result += "{%|%}"
                                return re_text
                            if confirm == 'N' or confirm == 'n':
                                re_text = raw_input("Enter again:")
                                continue
                    else:
                        print "result:"
                        result = self.__re_handle(re_text)
                        print result
                        confirm = raw_input("confirm?(Y/N)")
                        if confirm == 'Y' or confirm == 'y':
                            print "ok"
                            self.__result += result
                            self.__result += "{%|%}"
                            return re_text
                        if confirm == 'N' or confirm == 'n':
                            re_text = raw_input("Enter again:")
                            continue
                else:
                    return None

    def __add_information(self):
        username = raw_input("username:")
        email = raw_input("email:")
        password = raw_input("password:")
        salt = raw_input("salt:")
        other = raw_input("other:")
        result = username + "{%|%}" + email + "{%|%}" + password + "{%|%}" + salt + "{%|%}" + other
        if result == "{%|%}{%|%}{%|%}{%|%}":
            return ""
        else:
            return result

    def add(self):
        self.__result = ""
        signatures = ""
        username = ""
        email = ""
        password = ""
        salt = ""
        other = ""
        while True:
            signatures = raw_input("signatures(re):")
            if signatures == "":
                print "can't be empty!"
                continue
            if re.search(signatures, self.o_text):
                break
            else:
                print "Unable to match!"
        while True:
            username = raw_input("username(re):")
            username = self.__handele_re(username)
            if username is None:
                print "Unable to match!"
            else:
                break
        while True:
            email = raw_input("email(re):")
            email = self.__handele_re(email)
            if email is None:
                print "Unable to match!"
            else:
                break
        while True:
            password = raw_input("password(re):")
            password = self.__handele_re(password)
            if password is None:
                print "Unable to match!"
            else:
                break
        while True:
            salt = raw_input("salt(re):")
            salt = self.__handele_re(salt)
            if salt is None:
                print "Unable to match!"
            else:
                break
        while True:
            other = raw_input("other(re):")
            other = self.__handele_re(other)
            if other is None:
                print "Unable to match!"
            else:
                break
        with open("rulers.txt", "at") as config_file:
            self.__configs.append([])
            self.__configs[self.__last].append(signatures)
            self.__configs[self.__last].append(username)
            self.__configs[self.__last].append(email)
            self.__configs[self.__last].append(password)
            self.__configs[self.__last].append(salt)
            self.__configs[self.__last].append(other)
            self.__last += 1
            config_file.write(str(self.__last) + ":\n")
            config_file.write(signatures + "\n")
            config_file.write(username + "\n")
            config_file.write(email + "\n")
            config_file.write(password + "\n")
            config_file.write(salt + "\n")
            config_file.write(other + "\n")
        self.__result = self.__result[:-5]
        return self.__result

    def handle(self, o_text):
        global a, pr_s, pr_pause
        self.o_text = o_text
        f_text = []
        f_n = -1
        for i1 in self.__configs:
            s = 0
            for i2 in i1:
                re_text = i2
                if s == 0:
                    if re.search(re_text, self.o_text):
                        f_n += 1
                        f_text.append("")
                    else:
                        break
                else:
                    if i2 == "{%None%}":
                        f_text[f_n] += "{%|%}"
                    else:
                        f_text[f_n] += self.__re_handle(i2)
                        f_text[f_n] += "{%|%}"
                s += 1
        if f_n == 0 or f_n == 1:
            return f_text[0][:-5]
        elif f_n == -1:
            if self.__remind:
                pr_pause = True
                time.sleep(1)
                print "\nUnable to match!create a new rule or manually add information" \
                      " or don't remind(C(creat),M(manually),N(don't remind))"
                print "line:%d original:%s" % (a, o_text)
                choose = raw_input("choose:")
                if choose == 'C' or choose == 'c':
                    temp = self.add()
                elif choose == 'N' or choose == 'n':
                    self.__remind = False
                    temp = ""
                else:
                    temp = self.__add_information()
                pr_pause = False
            else:
                pr_pause = True
                if a - self.__ig_temp == 1:
                    self.__ig_temp = a
                    self.__ig_n += 1
                    if self.__ig_n > 3:
                        self.__remind = True
                else:
                    self.__ig_n = 0
                    self.__ig_temp = a
                print "ignored+1"
                pr_pause = False
                temp = ""
            return temp
        elif f_n > 0:
            if self.__choose is None:
                result_n = 1
                pr_pause = True
                time.sleep(1)
                print "Multiple sub-matching results:"
                for result in f_text:
                    print str(result_n) + ":"
                    print result
                    result_n += 1
                self.__choose = int(raw_input("Which to choose?:"))
                self.__choose -= 1
                pr_pause = False
                return f_text[self.__choose][:-5]
            else:
                return f_text[self.__choose][:-5]


def get_file(sgk_dir):
    result = []
    for parent, dirnames, filenames in os.walk(sgk_dir):
        for filename in filenames:
            result.append(os.path.join(parent, filename))
    return result


def get_result_n():
    global result_file, result_n
    result_dir = os.path.dirname(result_file)
    for parent, dirnames, filenames in os.walk(result_dir):
        for filename in filenames:
            if re.search(r"\.\((\d+)\)\.", filename):
                result_re = re.search(r"\.\((\d+)\)\.", filename)
                result_temp = int(result_re.group(1))
                if result_temp > result_n:
                    result_n = result_temp + 1


def pr():
    global a, out, pr_s, pr_pause
    while pr_s:
        time.sleep(0.5)
        if pr_pause:
            pass
        else:
            out.write("\rCompleted:(%s)" % a)
            out.flush()


def wr():
    global wr_s, result_file, result_queue, result_n, max_size
    r_len = 0
    get_result_n()
    result_file_dir = os.path.splitext(result_file)
    result_file_dir = result_file_dir[0] + ".(%s)" % result_n + result_file_dir[1]
    r_file = open(result_file_dir, "wt")
    while True:
        if wr_s:
            if not result_queue:
                time.sleep(1.5)
            else:
                line_temp = result_queue.pop(0)
                r_len += len(line_temp)
                if r_len > max_size:
                    r_file.close()
                    r_len = 0
                    result_n += 1
                    result_file_dir = os.path.splitext(result_file)
                    result_file_dir = result_file_dir[0] + ".(%s)" % result_n + result_file_dir[1]
                    r_file = open(result_file_dir, "wt")
                r_file.write(line_temp + '\n')
        else:
            for line_temp in result_queue:
                r_file.write(line_temp + '\n')
            r_file.close()
            print ("\ndone")
            break


def main():
    global a, sgkdir, pr_s, result_queue, wr_s
    pr_p = threading.Thread(target=pr)
    wr_p = threading.Thread(target=wr)
    pr_s = True
    wr_s = True
    pr_p.start()
    wr_p.start()
    for target_file in get_file(sgkdir):
        b = config_handler()
        a = 0
        print "Start handle %s" % target_file
        for line in open(target_file, "rb"):
            a += 1
            line_temp = line.strip()
            if line_temp != "":
                line_temp = b.handle(line_temp)
                result_queue.append(line_temp)
        print "\nCompleted: %s" % target_file
    wr_s = False
    pr_s = False
    exit(0)

if __name__ == "__main__":
    start = time.clock()
    main()