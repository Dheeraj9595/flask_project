def greet():
    return str('hello')

a = greet()
print(a)

import time 
  
  
def timeis(func): 
    '''Decorator that reports the execution time.'''
  
    def wrap(*args, **kwargs): 
        start = time.time() 
        result = func(*args, **kwargs) 
        end = time.time() 
          
        print(func.__name__, end-start) 
        return result 
    return wrap 

@timeis
def greet():
    print('hello')


obj = greet()    
