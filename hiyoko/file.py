
import os 
import sys 

def open_stdin (mode, *args, **kwargs): #dup and open stdin.
  fd = os.dup(sys.stdin.fileno())
  return os.fdopen(fd, mode, *args, **kwargs)

def open_stdout (mode, *args, **kwargs): #dup and open stdout.
  fd = os.dup(sys.stdout.fileno())
  return os.fdopen(fd, mode, *args, **kwargs)

def open_stderr (mode, *args, **kwargs): #dup and open stderr.
  fd = os.dup(sys.stderr.fileno())
  return os.fdopen(fd, mode, *args, **kwargs)
