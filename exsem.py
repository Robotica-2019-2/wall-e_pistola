# -*- coding: ISO-8859-1 -*-

import thread
import time, random

s = thread.allocate_lock()

def tempo(i):
   t = random.randint(3,7)
   print "Processo %i dormindo por %i" %(i, t)
   time.sleep(t)

def thread1():
   while True:
      print "Processo 1 - Adquirindo semáforo"
      s.acquire()
      print "Processo 1 - Seção crítica"
      tempo(1)
      print "Processo 1 - Liberando semáforo"
      s.release()
      print "Processo 1 - seção não crítica"
      tempo(1)

def thread2():
   while True:
      print "Processo 2 - Adquirindo semáforo"
      s.acquire()
      print "Processo 2 - Seção crítica"
      tempo(2)
      print "Processo 2 - Liberando semáforo"
      s.release()
      print "Processo 2 - seção não crítica"
      tempo(2)

thread.start_new_thread(thread1, ())
thread.start_new_thread(thread2, ())

while 1: pass