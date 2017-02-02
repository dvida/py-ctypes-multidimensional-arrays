#!/usr/bin/env python

import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
import os

# Init ctypes types
DOUBLE = ct.c_double
PDOUBLE = ct.POINTER(DOUBLE)
PPDOUBLE = ct.POINTER(PDOUBLE)
PPPDOUBLE = ct.POINTER(PPDOUBLE)


# Reconstruct the structure from the .h file
class MyStruct(ct.Structure):
    _fields_ = [
        ('n', ct.c_int),
        ('sum', ct.c_double),
        ('x', ct.POINTER(ct.c_double)),
        ('y', PPDOUBLE),
        ('z', PPPDOUBLE)
    ]



def double2ArrayToPointer(arr):
    """ Converts a 2D numpy to ctypes 2D array. 
    
    Arguments:
        arr: [ndarray] 2D numpy float64 array

    Return:
        arr_ptr: [ctypes double pointer]

    """

    # Init needed data types
    ARR_DIMX = DOUBLE*arr.shape[1]
    ARR_DIMY = PDOUBLE*arr.shape[0]

    # Init pointer
    arr_ptr = ARR_DIMY()

    # Fill the 2D ctypes array with values
    for i, row in enumerate(arr):
        arr_ptr[i] = ARR_DIMX()

        for j, val in enumerate(row):
            arr_ptr[i][j] = val


    return arr_ptr


def double2pointerToArray(ptr, n, m):
    """ Converts ctypes 2D array into a 2D numpy array. 
    
    Arguments:
        arr_ptr: [ctypes double pointer]

    Return:
        arr: [ndarray] 2D numpy float64 array
        
    """

    arr = np.zeros(shape=(n, m))

    for i in range(n):
        for j in range(m):
            arr[i,j] = ptr[i][j]

    return arr



def double3ArrayToPointer(arr):
    """ Converts a 3D numpy to ctypes 3D array. 
    
    Arguments:
        arr: [ndarray] 3D numpy float64 array

    Return:
        arr_ptr: [ctypes double pointer]

    """

    # Init needed data types
    ARR_DIMX = DOUBLE*arr.shape[2]
    ARR_DIMY = PDOUBLE*arr.shape[1]
    ARR_DIMZ = PPDOUBLE*arr.shape[0]

    # Init pointer
    arr_ptr = ARR_DIMZ()

    # Fill the 2D ctypes array with values
    for i, row in enumerate(arr):
        arr_ptr[i] = ARR_DIMY()

        for j, col in enumerate(row):
            arr_ptr[i][j] = ARR_DIMX()

            for k, val in enumerate(col):
                arr_ptr[i][j][k] = val

    return arr_ptr



def double3pointerToArray(ptr, n, m, o):
    """ Converts ctypes 3D array into a 3D numpy array. 
    
    Arguments:
        arr_ptr: [ctypes double pointer]

    Return:
        arr: [ndarray] 3D numpy float64 array
        
    """

    arr = np.zeros(shape=(n, m, o))

    for i in range(n):
        for j in range(m):
            for k in range(o):
                arr[i,j,k] = ptr[i][j][k]

    return arr


# Load the compiled library
libmyfunc = npct.load_library('libmyfunc', os.path.dirname(__file__))

# Define the return type of the C function
libmyfunc.myfunc.restype = ct.c_double

# Define arguments of the C function
libmyfunc.myfunc.argtypes = [
    ct.POINTER(ct.c_double),
    ct.POINTER(MyStruct)
]

# Init example arrays
x = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([[10, 7, 8], [2, 9, 10]], dtype=np.float64)
z = np.arange(60).reshape(3, 4, 5)

# Init input array
arr = np.arange(4).astype(np.float64)


# Generate a 2D ctypes array from numpy array
y_ptr = double2ArrayToPointer(y)

# Generate a 3D ctypes array from numpy array
z_ptr = double3ArrayToPointer(z)

# Init the structure
mystruct = MyStruct()

# Init structure attributes
mystruct.n = len(x)
mystruct.x = npct.as_ctypes(x)
mystruct.sum = 0
mystruct.y = y_ptr
mystruct.z = z_ptr

# Run the function
res = libmyfunc.myfunc(npct.as_ctypes(arr), mystruct)

# Convert the scalar from the structure back to a Python variable
#sum_res = np.frombuffer(mystruct.sum, np.float64)


# Convert multidimensiional ctypes arrays to numpy arrays
y_res = double2pointerToArray(y_ptr, *y.shape)
z_res = double3pointerToArray(z_ptr, *z.shape)

# Print out the results
print '\nResults:'
print 'return: ', res
print 'sum:', mystruct.sum
print 'x:', x
print 'y:', y_res
print 'z:', z_res
