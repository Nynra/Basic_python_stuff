# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 11:34:37 2022.

Edited from:
https://stackoverflow.com/questions/55110733/python-multiprocessing-pipe-communication-between-processes
@author: baskl
"""
from multiprocessing import Process, Pipe
from datetime import datetime

SENTINEL = 'SENTINEL'
EOM_CHAR = 'EOM'


def poll_pipe(conn):
    """Check if there is a message waiting."""
    try:
        state = conn.poll()
    except OSError:
        return None
    return state


def read_pipe_msg(conn):
    """
    Read the data from the pipe.

    Parameters
    ----------
    conn : TYPE
        DESCRIPTION.

    Returns
    -------
    msg : unknown
        The message that was waiting in the Pipe.

    """
    try:
        # Get the event
        msg = conn.recv()
    except OSError:
        # Catch the error if the other side closes unexpected
        close_pipe(conn)
        msg = None
        print('OSError received from pipe')
    return msg


def read_pipe_list(child_conn, feedback=False):
    """
    Read the data from the pipe.

    Parameters
    ----------
    child_conn : multiprocessing.Pipe connector
    feedback : bool, optional
        Boolean indicating if the reader should send a conformation to the 
        sender or not. The default is False.

    Returns
    -------
    result : list
        List containing all the data that was waiting in the Pipe.

    """
    result = []
    try:
        # Check if there is a message ready
        if child_conn.poll():
            for msg in iter(child_conn.recv, EOM_CHAR):
                result.append(msg)
        else:
            pass
    except OSError:
        # Catch the error if the other side closes unexpected
        close_pipe(child_conn)
        print("OSError received from pipe.")
        return result

    if feedback:
        # Send the reived conformation to parent
        write_pipe(child_conn, result)

    # Check if the closing request was given
    if SENTINEL in result:
        close_pipe(child_conn)
        # Put the SENTINEL command at the end
        result.append(result.pop(result.index(SENTINEL)))
        # print('RECEIVED SENTINEL COMMAND.')

    return result


def close_pipe(conn):
    """Close the pipe connection."""
    conn.close()


def write_pipe(conn, data):
    """Write the data to the pipe."""
    conn.send(data)
    conn.send(EOM_CHAR)


if __name__ == '__main__':
    # Example usage
    parent_conn, child_conn = Pipe()  # default is duplex!
    update_data_process = Process(target=read_pipe_list, args=(child_conn,
                                                          True,))
    update_data_process.daemon = True
    update_data_process.start()

    data = [i for i in range(5)]
    data.append(SENTINEL)
    write_pipe(parent_conn, data)

    for msg in iter(parent_conn.recv, EOM_CHAR):
        print(f'{datetime.now()} parent received {msg}')

    print(f'{datetime.now()} parent received SENTINEL')
    parent_conn.close()
    update_data_process.join()
