import threading

class container:
    def __init__(self):
        self.lst = []
    def run_function(self,func,args):
        t = threading.Thread(target=func,args=args)
        self.lst.append(t)
        t.start()
        return t
