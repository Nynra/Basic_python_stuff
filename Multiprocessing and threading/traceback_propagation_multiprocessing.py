# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 14:32:09 2022.

@author: baskl
"""


def full_traceback(func):
    """Return the traceback to the main process"""
    import traceback
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            msg = "{}\n\nOriginal {}".format(e, traceback.format_exc())
            raise type(e)(msg)
    return wrapper


if __name__ == '__main__':
    # Usage example
    def func0():
        raise NameError("func0 exception")

    def func1():
        return func0()

    # Key is here!
    @full_traceback
    def main(i):
        return func1()

    from multiprocessing import Pool
    pool = Pool(1)
    try:
        results = pool.map_async(main, range(5)).get(1e5)
    finally:
        pool.close()
        pool.join()
        print('Closed the process.')
