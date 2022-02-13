# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 15:55:24 2022

https://stackoverflow.com/questions/6126007/python-getting-a-traceback-from-a-multiprocessing-process/26096355#26096355
"""
import traceback, functools

def full_traceback(func):
    """Wrapper to pass the full traceback of a process."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            msg = "{}\n\nOriginal {}".format(e, traceback.format_exc())
            raise type(e)(msg)
    return wrapper

# =============================================================================
# # Example of the wrapper function usage
# def func0():
#     raise NameError("func0 exception")
# 
# def func1():
#     return func0()
# 
# # Key is here!
# @full_traceback
# def main(i):
#     return func1()
# 
# if __name__ == '__main__':
#     from multiprocessing import Pool
#     pool = Pool(4)
#     try:
#         results = pool.map_async(main, range(5)).get(1e5)
#     finally:
#         pool.close()
#         pool.join()
# =============================================================================
