import numpy as np

# Create a numpy array from a list
larr = np.array([1, 2, 3, 4, 5])
print(larr)
print(type(larr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(larr.dtype) #The data type of the elements in the 1D array is int64, so dtype is int64

# Create a numpy array from a list of strings
sarr = np.array(['apple', 'banana', 'cherry'])
print(sarr)
print(type(sarr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(sarr.dtype) #The data type of the elements in the array is string, so dtype is <U6 (Unicode string of length 6)>
print(np.sort(sarr))

# Create a numpy array from a tuple
tarr = np.array((1, 2, 3, 4, 5))
print(tarr) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(type(tarr))

# Create a numpy array from a list of boolean values
boolarr = np.array([True, False, True])
print(np.sort(boolarr))

#Different dimensions of arrays a) 0D array
zero_arr = np.array(42)
print(zero_arr)
print(type(zero_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(zero_arr.ndim) #0D array has no dimensions, so ndim is 0

# b) 1D array
larr = np.array([1, 2, 3, 4, 5])
print(larr)
print(type(larr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(larr.ndim) #1D array has one dimension, so ndim is 1
slarr = np.where(larr == 4) #Find the indexes where the value is 4
slaar1 = np.where(larr%2 == 0) #Find the indexes where the values are odd
slaar2 = np.where(larr%2 == 1) #Find the indexes where the values are even:
sstdlaar1 = np.searchsorted(larr, 3) #Find the indexes where the value 3 should be inserted to maintain order in the array
sstdlaar2 = np.searchsorted(larr, 2, side='right') #Find the indexes where the value 2 should be inserted to maintain order in the array
print(np.sort(larr))
sstdlaar3 = np.searchsorted(larr, [2, 4, 6]) #Find the indexes where the values 2, 4, and 6 should be inserted
print(sstdlaar1) #The value 3 should be inserted at index 2 to maintain order in the array, so it will print 2
print(sstdlaar2) #The value 2 should be inserted at index 2 to maintain order in the array, so it will print 2 
print(sstdlaar3) #the three indexes where 2, 4, 6 would be inserted in the original array 

print(slarr)
print(slaar1)
print(slaar2)

#Iterate on the elements of the following 1-D array
for i in larr:
    print(i) 
    
for x in np.nditer(larr, flags=['buffered'], op_dtypes=['S']):
  print(x)
  
#Enumerate on following 1D arrays elements:
for idx, x in np.ndenumerate(larr):
  print(idx, x)

# c) 2D array
two_arr = np.array([[1, 2, 3], [4, 5, 6]])
print(two_arr)
print(type(two_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(two_arr.ndim) #2D array has two dimensions, so ndim is 2
print(np.sort(two_arr))#The sort function sorts each row of the 2D array independently, resulting in a new 2D array where each row is sorted in ascending order.

for i in two_arr:
    print(i) #Iterate on the elements of the following 2-D array using a single for loop

#Iterate on the elements of the following 2-D array using nested loops    
for i in two_arr:
    for j in i:
        print(j) 
        
#Iterate through every scalar element of the 2D array skipping 1 element:
for x in np.nditer(two_arr[:, ::2]):
  print(x)
  
#Enumerate on following 2D arrays elements:
for idx, x in np.ndenumerate(two_arr):
  print(idx, x)

# d) 3D array
three_arr = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])
print(three_arr)
print(type(three_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(three_arr.ndim) #3D array has three dimensions, so ndim is 3

#Iterate on the elements of the following 3-D array using a single for loop
for i in three_arr:
    print(i)
 
 #Iterate on the elements of the following 3-D array using nested loops    
for i in three_arr:
    for j in i:
        print(j)

#Iterate on the elements of the following 3-D array using nested loops  
for i in three_arr:
    for j in i:
        for k in j:
            print(k) 
            
#Iterate through the following 3-D array using nditer :
for x in np.nditer(three_arr):
  print(x)

#Create a array with Higher dimensions
arr_hd = np.array([1, 2, 3, 4], ndmin=5) #This creates a 5D array with the specified elements
print(arr_hd)
print(type(arr_hd)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(arr_hd.ndim) #The number of dimensions of the array is 5, so ndim is 5
print(np.shape(arr_hd))

#Create a array with specified data type 
crS_arr = np.array([1, 2, 3, 4], dtype='S') #This creates a 1D array with the specified elements and data type of string (S)
print(crS_arr)
print(type(crS_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(crS_arr.dtype) #The data type of the elements in the array is string, so dtype is |S1 (string of length 1)

#Create an array with data type 4 bytes integer
cr_int_arr = np.array([1, 2, 3, 4], dtype='i4') #This creates a 1D array with the specified elements and data type of 4 bytes integer (i4)
print(cr_int_arr)
print(type(cr_int_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(cr_int_arr.dtype) #The data type of the elements in the array is 4 bytes integer, so dtype is int32 (i4)


#Change data type from float to integer by using 'i' as parameter value
cr_float_arr = np.array([1.5, 2.5, 3.5, 4.5])
cr_new_float_to_i_arr = cr_float_arr.astype('i') #This creates a new array with the same elements as cr_float_arr but with data type of integer (i)
cr_new_float_to_int_arr1 = cr_float_arr.astype('int') #This creates a new array with the same elements as cr_float_arr but with data type of integer (int)
print(cr_new_float_to_i_arr)
print(cr_new_float_to_int_arr1)
print(type(cr_new_float_to_i_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(cr_new_float_to_i_arr.dtype) #The data type of the elements in the new array is integer, so dtype is int32 (i)
print(type(cr_new_float_to_int_arr1)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(cr_new_float_to_int_arr1.dtype) #The data type of the elements in the new array is integer, so dtype is int64 (int)

#Change data type from integer to boolean:
cr_int_arr = np.array([0, 1, 2, 3, 4])
cr_new_int_to_bool_arr = cr_int_arr.astype(bool) #This creates a new array with the same elements as cr_int_arr but with data type of boolean (bool)
print(cr_new_int_to_bool_arr)
print(type(cr_new_int_to_bool_arr)) #The type of the array is <class 'numpy.ndarray'>, which indicates that it is a numpy array
print(cr_new_int_to_bool_arr.dtype) #The data type of the elements in the new array is boolean, so dtype is bool

#Make a copy, change the original array, and display both arrays
org_arr = np.array([1, 2, 3, 4, 5])
copy_arr = org_arr.copy() #This creates a copy of the original array
copy_arr[0] = 10 #This changes the first element of the original array to 10
print(org_arr) #The original array remains unchanged, so it will print [1 2 3 4 5]
print(copy_arr) #The copy array has the first element changed to 10, so it will print [10 2 3 4 5]
print(copy_arr.base) #The base attribute of the copy array will show None, because it is a copy and does not share the same data, so it will print None 


#Make a view, change the view, and display both arrays:
org_arr = np.array([1, 2, 3, 4, 5])
view_arr = org_arr.view() #This creates a view of the original array
view_arr[0] = 10 #This changes the first element of the view array to 10
print(org_arr) #The original array is also changed because the view shares the same data, so it will print [10 2 3 4 5]
print(view_arr) #The view array has the first element changed to 10, so it will print [10 2 3 4 5]
print(view_arr.base) #The base attribute of the view array will show the original array, so it will print [10 2 3 4 5]

#Convert the following 1-D array with 12 elements into a 2-D array,The outermost dimension will have 4 arrays, each with 3 elements:
d1arr = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
new_d1_to_d2  = d1arr.reshape(4,3)
print(new_d1_to_d2)

##Convert the following 1-D array with 12 elements into a 3-D array,The outermost dimension will have 2 arrays that contains 3 arrays, each with 2 elements:
new_d1_to_d3 = d1arr.reshape(2,3,2)
print(new_d1_to_d3)

#Check if the returned array is a copy or a view:
print(d1arr.reshape(4,3).base) #Check if the returned array is a copy or a view , The example above returns the original array, so it is a view.
print(d1arr.reshape(2,3,2).base) #Check if the returned array is a copy or a view , The example above returns the original array, so it is a view.

#Unknown Dimension , Convert 1D array with 8 elements to 3D array with 2x2 elements
new_d1_to_d3_unknown = d1arr.reshape(2,2,-1) #The -1 in the reshape method allows numpy to automatically calculate the size of that dimension based on the total number of elements and the other specified dimensions.
print(new_d1_to_d3_unknown)

#Join two arrays
jarr1 = np.array([1, 2, 3])
jarr2 = np.array([4, 5, 6])
jarr = np.concatenate((jarr1, jarr2)) #This concatenates the two arrays along the specified axis (in this case, the default axis 0 for 1D arrays)
print(jarr)

#Join two 2-D arrays along rows (axis=1):
jjarr1 = np.array([[1, 2], [3, 4]])
jjarr2 = np.array([[5, 6], [7, 8]])
jjarr = np.concatenate((jjarr1, jjarr2), axis=1) #This concatenates the two 2-D arrays along rows (axis=1), resulting in a new array with the same number of rows but more columns.
print(jjarr)

#Joining Arrays Using Stack Functions
stk_arr1 = np.array([1, 2, 3])
stk_arr2 = np.array([4, 5, 6])
stk_arr = np.stack((stk_arr1, stk_arr2), axis=1)
print(stk_arr)

#hstack() to stack along rows
hstack_arr1 = np.array([1, 2, 3])
hstack_arr2 = np.array([4, 5, 6])
hstack_arr = np.hstack((hstack_arr1, hstack_arr2))
print(hstack_arr)

#vstack() to stack along columns
vstack_arr1 = np.array([1, 2, 3])
vstack_arr2 = np.array([4, 5, 6])
vstack_arr = np.vstack((vstack_arr1, vstack_arr2))
print(vstack_arr)

#dstack() to stack along height, which is the same as depth
dstack_arr1 = np.array([1, 2, 3])
dstack_arr2 = np.array([4, 5, 6])
dstack_arr = np.dstack((dstack_arr1, dstack_arr2))
print(dstack_arr)

#Split the array in 3 & 4 parts:
spt_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
spt_arr1 = np.array_split(spt_arr, 3)
spt_arr2 = np.array_split(spt_arr, 4)
print(spt_arr1)
print(spt_arr2)
print(spt_arr1[2]) #Accessing the second element of the second array in the list of arrays created by splitting the original array into 3 parts
print(spt_arr2[2]) #Accessing the third array in the list of arrays created by splitting the original array into 4 parts

#Split the 2-D array into three 2-D arrays
twospt_arr = np.array([[1, 2, 3], [4, 5, 6]])
spt_two_arr = np.array_split(twospt_arr, 3)
hspt_two_arr = np.hsplit(twospt_arr, 3) #This splits the 2-D array into three 2-D arrays along the second axis (columns), resulting in a list of three 2-D arrays.
vspt_two_arr = np.vsplit(twospt_arr, 1) #This splits the 2-D array into one 2-D array along the first axis (rows), resulting in a list with the original array.
print(spt_two_arr)
print(hspt_two_arr)
print(vspt_two_arr)
print(spt_two_arr[0]) #Accessing the first array in the list of arrays created by splitting the original 2-D array into three 2-D arrays





print(larr[0]) #Accessing the first element of the 1D array
print(larr[1] + larr[2]) #Accessing the third and fourth elements of the 1D array and adding them together
print(two_arr[0][1]) #Accessing the second element of the first row of the 2D array
print(two_arr[0 , 1]) #Accessing the second element of the first row of the 2D array using a different indexing method
print(three_arr[1][0][2]) #Accessing the third element of the first row of the second 2D array in the 3D array
print(three_arr[1 , 0 , 2]) #Accessing the third element of the first row of the second 2D array in the 3D array using a different indexing method
print(two_arr[-1 , 1]) #Accessing the second element of the last row of the 2D array using negative indexing
print(larr[1:4]) #Accessing elements from index 1 to 3 of the 1D array
print(larr[:3]) #Accessing the first three elements of the 1D array
print(larr[2:4]) #Accessing elements from index 2 to 3 of the 1D array
print(larr[-3:-1]) #Accessing elements from index -3 to -1 of the 1D array
print(two_arr[0:2 , 1]) #Accessing the second column of the first two rows of the 2D array
print(two_arr[1 , 0:2]) #Accessing the first two columns of the second row of the 2D array
print(two_arr[0:2 , 0:2]) #Accessing the first two rows and first two columns of the 2D array



print(np.__version__)

# NumPy ufuncs
# Create your own ufunc
def myadd(x, y):
  return x+y

myadd = np.frompyfunc(myadd, 2, 1)

print(myadd([1, 2, 3, 4], [5, 6, 7, 8]))#
print(type(np.add))# The type of np.add is <class 'numpy.ufunc'>, which indicates that it is a universal function (ufunc) in NumPy.

#Simple Arithmetic in ufuncs
# ADD function
Aarr1 = np.array([1, 2, 3, 4])
Aarr2 = np.array([5, 6, 7, 8])
ARarr = np.add(Aarr1, Aarr2) #This adds the two arrays element-wise using the np.add ufunc
print(ARarr)

#Subtract function
SBarr1 = np.array([1, 2, 3, 4])
SBarr2 = np.array([5, 6, 7, 8])
SBarr = np.subtract(SBarr1, SBarr2) #This subtracts the second array from the first array element-wise using the np.subtract ufunc
print(SBarr)

#Multiply function
MLarr1 = np.array([1, 2, 3, 4])
MLarr2 = np.array([5, 6, 7, 8]) 
MLarr = np.multiply(MLarr1, MLarr2) #This multiplies the two arrays element-wise using the np.multiply ufunc
print(MLarr)

#Divide function
DVarr1 = np.array([1, 2, 3, 4])
DVarr2 = np.array([5, 6, 7, 8])
DVarr = np.divide(DVarr1, DVarr2) #This divides the first array by the second array element-wise using the np.divide ufunc
print(DVarr)

#Power function
PWarr1 = np.array([1, 2, 3, 4])
PWarr2 = np.array([5, 6, 7, 8])
PWarr = np.power(PWarr1, PWarr2) #This raises the first array to the power of the second array element-wise using the np.power ufunc
print(PWarr)

#Modulus function
MDarr1 = np.array([1, 2, 3, 4]) 
MDarr2 = np.array([5, 6, 7, 8])
MDarr = np.mod(MDarr1, MDarr2) #This calculates the modulus of the first array by the second array element-wise using the np.mod ufunc
print(MDarr)

#Absolute function
ABarr = np.array([-1, -2, -3, -4])
ABarr_abs = np.absolute(ABarr) #This calculates the absolute value of each element in the array using the np.absolute ufunc
print(ABarr_abs)

#Quotient and Remainder functions
QRarr1 = np.array([1, 2, 3, 4])
QRarr2 = np.array([5, 6, 7, 8])
QRarr_quotient = np.divmod(QRarr1, QRarr2)[0] #This calculates the quotient of the first array divided by the second array element-wise using the np.divmod ufunc and returns the quotient part
QRarr_remainder = np.divmod(QRarr1, QRarr2)[1] #This calculates the remainder of the first array divided by the second array element-wise using the np.divmod ufunc and returns the remainder part
print(QRarr_quotient)
print(QRarr_remainder)

# Numpy Rounding Decimals Ufuncs
#Truncation and Fix functions
TRarr = np.array([1.5, 2.5, 3.5, 4.5])
TRarr_trunc = np.trunc(TRarr) #This truncates the decimal part of each element in the array using the np.trunc ufunc
print(TRarr_trunc)
TRarr_fix = np.fix(TRarr) #This rounds each element in the array towards zero using the np.fix ufunc
print(TRarr_fix)

#Round function
RDarr = np.array([1.5, 2.5, 3.5, 4.5])
RDarr_round = np.round(RDarr) #This rounds each element in the array to the nearest integer using the np.round ufunc
print(RDarr_round)

#Rounding to a specific number of decimals
RDarr_decimals = np.round(RDarr, decimals=2) #This rounds each element in the array to 2 decimal places using the np.round ufunc
print(RDarr_decimals)

#Around function
ARarr = np.array([1.5, 2.5, 3.5, 4.5])
ARarr_around = np.around(ARarr) #This rounds each element in the array to the nearest integer using the np.around ufunc, which is an alias for np.round
print(ARarr_around)

#Floor and Ceil functions
FLarr = np.array([1.5, 2.5, 3.5, 4.5])
FLarr_floor = np.floor(FLarr) #This rounds each element in the array down to the nearest integer using the np.floor ufunc
print(FLarr_floor)
FLarr_ceil = np.ceil(FLarr) #This rounds each element in the array up to the nearest integer using the np.ceil ufunc
print(FLarr_ceil)

#NumPy Logs
LGarr = np.array([1, 10, 100, 1000])
LGarr_log = np.log(LGarr) #This calculates the natural logarithm (base e) of each element in the array using the np.log ufunc
print(LGarr_log)

#Logat base 10 function
LGarr_log10 = np.log10(LGarr) #This calculates the base-10 logarithm of each element in the array using the np.log10 ufunc
print(LGarr_log10)

#Logat base 2 function
LGarr_log2 = np.log2(LGarr) #This calculates the base-2 logarithm of each element in the array using the np.log2 ufunc
print(LGarr_log2)

#Log at Any Base
def log_base(x, base):
    return np.log(x) / np.log(base)
LGarr_log_base_5 = log_base(LGarr, 5) #This calculates the logarithm of each element in the array to the base 5 using the custom log_base function defined above
print(LGarr_log_base_5)

#Numpy Summation Ufuncs
#Sum function
Smarr = np.array([1, 2, 3, 4])
Smarr_sum = np.sum(Smarr) #This calculates the sum of all elements in the array using the np.sum ufunc
print(Smarr_sum)

# Summation along an axis
Smarr_2d = np.array([[1, 2], [3, 4]])
Smarr_sum_axis0 = np.sum(Smarr_2d, axis=0)#This calculates the sum of elements along the first axis (columns) of the 2D array using the np.sum ufunc with axis=0, resulting in an array of sums for each column.
Smarr_sum_axis1 = np.sum(Smarr_2d, axis=1)#This calculates the sum of elements along the second axis (rows) of the 2D array using the np.sum ufunc with axis=1, resulting in an array of sums for each row.
print(Smarr_sum_axis0)    
print(Smarr_sum_axis1)

#Cummulative Sum
CSmarr = np.array([1, 2, 3, 4])
CSmarr_cumsum = np.cumsum(CSmarr) #This calculates the cumulative sum of the elements in the array using the np.cumsum ufunc, resulting in an array where each element is the sum of all previous elements up to that index.
print(CSmarr_cumsum)

#NumPy Products
#Product function
Prarr = np.array([1, 2, 3, 4])
Prarr_prod = np.prod(Prarr) #This calculates the product of all elements in the array using the np.prod ufunc
print(Prarr_prod)

#Product Over an Axis
Prarr_2d = np.array([[1, 2], [3, 4]])
Prarr_prod_axis0 = np.prod(Prarr_2d, axis=0) #This calculates the product of elements along the first axis (columns) of the 2D array using the np.prod ufunc with axis=0, resulting in an array of products for each column.
Prarr_prod_axis1 = np.prod(Prarr_2d, axis=1) #This calculates the product of elements along the second axis (rows) of the 2D array using the np.prod ufunc with axis=1, resulting in an array of products for each row.
print(Prarr_prod_axis0)
print(Prarr_prod_axis1)

#Cummulative Product
CParr = np.array([1, 2, 3, 4])
CParr_cumprod = np.cumprod(CParr) #This calculates the cumulative product of the elements in the array using the np.cumprod ufunc, resulting in an array where each element is the product of all previous elements up to that index.
print(CParr_cumprod)

#NumPy Differences and Other Ufuncs
#Difference function
Dfarr = np.array([1, 2, 4, 7])
Dfarr_diff = np.diff(Dfarr) #This calculates the difference between consecutive elements in the array using the np.diff ufunc, resulting in an array of differences.
print(Dfarr_diff)

#Compute discrete difference of the following array twice
Dfarr_diff_twice = np.diff(Dfarr, n=2) #This calculates the discrete difference of the array twice using the np.diff ufunc with n=2, resulting in an array of second differences.
print(Dfarr_diff_twice)

#NumPy LCM Lowest Common Multiple
LCMarr1 = np.array([4, 6, 8])
LCMarr2 = np.array([12, 15, 20])
LCMarr_lcm = np.lcm(LCMarr1, LCMarr2) #This calculates the least common multiple of corresponding elements in the two arrays using the np.lcm ufunc, resulting in an array of least common multiples.
print(LCMarr_lcm)

#NumPy GCD Greatest Common Divisor
GCDarr1 = np.array([4, 6, 8])
GCDarr2 = np.array([12, 15, 20])
GCDarr_gcd = np.gcd(GCDarr1, GCDarr2) #This calculates the greatest common divisor of corresponding elements in the two arrays using the np.gcd ufunc, resulting in an array of greatest common divisors.
print(GCDarr_gcd)

#NumPy Trigonometric Functions
#Sine , Cosine, and Tangent functions
Sine_arr = np.array([0, np.pi/2, np.pi])
Sine_arr_sin = np.sin(Sine_arr) #This calculates the sine of each element in the array using the np.sin ufunc, resulting in an array of sine values.
print(Sine_arr_sin)
Cosine_arr = np.array([0, np.pi/2, np.pi])
Cosine_arr_cos = np.cos(Cosine_arr) #This calculates the cosine of each element in the array using the np.cos ufunc, resulting in an array of cosine values.
print(Cosine_arr_cos) 
Tangent_arr = np.array([0, np.pi/4, np.pi/2])
Tangent_arr_tan = np.tan(Tangent_arr) #This calculates the tangent of each element in the array using the np.tan ufunc, resulting in an array of tangent values.
print(Tangent_arr_tan)  

#Inverse Sine , Cosine, and Tangent functions
ASine_arr = np.array([0, 1, -1])  
ASine_arr_asin = np.arcsin(ASine_arr) #This calculates the inverse sine of each element in the array using the np.arcsin ufunc, resulting in an array of inverse sine values.
print(ASine_arr_asin)
ACosine_arr = np.array([1, 0, -1])
ACosine_arr_acos = np.arccos(ACosine_arr) #This calculates the inverse cosine of each element in the array using the np.arccos ufunc, resulting in an array of inverse cosine values.
print(ACosine_arr_acos)
ATangent_arr = np.array([0, 1, -1])
ATangent_arr_atan = np.arctan(ATangent_arr) #This calculates the inverse tangent of each element in the array using the np.arctan ufunc, resulting in an array of inverse tangent values.
print(ATangent_arr_atan)

#Convert Degrees Into Radians
Degrees_arr = np.array([0, 90, 180])
Radians_arr = np.deg2rad(Degrees_arr) #This converts each element in the array from degrees to radians using the np.deg2rad ufunc, resulting in an array of radian values.
print(Radians_arr)

#Convert Radians Into Degrees
Radians1_arr = np.array([0, np.pi/2, np.pi])
Degrees1_arr = np.rad2deg(Radians1_arr) #This converts each element in the array from radians to degrees using the np.rad2deg ufunc, resulting in an array of degree values.
print(Degrees1_arr)

#Finding Angles
x_angle= np.arcsin(1.0)
y_angle = np.arccos(0.0)
z_angle = np.arctan(1.0)
print(x_angle) #This calculates the angle whose sine is 1.0 using the np.arcsin ufunc, resulting in an angle in radians.
print(y_angle) #This calculates the angle whose cosine is 0.0 using the np.arccos ufunc, resulting in an angle in radians.
print(z_angle) #This calculates the angle whose tangent is 1.0 using the np.arctan ufunc, resulting in an angle in radians.

#Angles of Each Value in Arrays
angles_arr = np.array([0, 1, -1])
angles_arr_angle = np.angle(angles_arr) #This calculates the angle of each element in the array using the np.angle ufunc, which returns the angle of a complex number in radians. For real numbers, it will return 0 for positive values and pi for negative values.
print(angles_arr_angle)

#Hypotenues
hyp_arr1 = np.array([3, 5, 7])
hyp_arr2 = np.array([4, 12, 24])
hypotenuse_arr = np.hypot(hyp_arr1, hyp_arr2) #This calculates the hypotenuse of a right triangle given the lengths of the two legs (hyp_arr1 and hyp_arr2) using the np.hypot ufunc, resulting in an array of hypotenuse lengths.
print(hypotenuse_arr)

#NumPy Hyperbolic Functions
#Hyperbolic Sine, Cosine, and Tangent functions
HSine_arr = np.array([0, 1, -1])
HSine_arr_sinh = np.sinh(HSine_arr) #This calculates the hyperbolic sine of each element in the array using the np.sinh ufunc, resulting in an array of hyperbolic sine values.
print(HSine_arr_sinh)

HCosine_arr = np.array([0, 1, -1])
HCosine_arr_cosh = np.cosh(HCosine_arr) #This calculates the hyperbolic cosine of each element in the array using the np.cosh ufunc, resulting in an array of hyperbolic cosine values.
print(HCosine_arr_cosh)

HTangent_arr = np.array([0, 1, -1])
HTangent_arr_tanh = np.tanh(HTangent_arr) #This calculates the hyperbolic tangent of each element in the array using the np.tanh ufunc, resulting in an array of hyperbolic tangent values.
print(HTangent_arr_tanh)

#Inverse Hyperbolic Sine, Cosine, and Tangent functions
AHSine_arr = np.array([0, 1, -1])
AHSine_arr_asinh = np.arcsinh(AHSine_arr) #This calculates the inverse hyperbolic sine of each element in the array using the np.arcsinh ufunc, resulting in an array of inverse hyperbolic sine values.
print(AHSine_arr_asinh)

AHCosine_arr = np.array([1, 0, -1])
AHCosine_arr_acosh = np.arccosh(AHCosine_arr) #This calculates the inverse hyperbolic cosine of each element in the array using the np.arccosh ufunc, resulting in an array of inverse hyperbolic cosine values. Note that the input values must be greater than or equal to 1 for real results.
print(AHCosine_arr_acosh)

AHTangent_arr = np.array([0, 1, -1])
AHTangent_arr_atanh = np.arctanh(AHTangent_arr) #This calculates  the inverse hyperbolic tangent of each element in the array using the np.arctanh ufunc, resulting in an array of inverse hyperbolic tangent values. Note that the input values must be between -1 and 1 for real results.
print(AHTangent_arr_atanh)  

#Finding Hyperbolic Angles
x_hyper_angle = np.arcsinh(1.0)
y_hyper_angle = np.arccosh(1.0)
z_hyper_angle = np.arctanh(0.5)
print(x_hyper_angle) #This calculates the hyperbolic angle whose hyperbolic sine is 1.0 using the np.arcsinh ufunc, resulting in a hyperbolic angle in radians.
print(y_hyper_angle) #This calculates the hyperbolic angle whose hyperbolic cosine is 1.0 using the np.arccosh ufunc, resulting in a hyperbolic angle in radians.
print(z_hyper_angle) #This calculates the hyperbolic angle whose hyperbolic tangent is 0.5 using the np.arctanh ufunc, resulting in a hyperbolic angle in radians.

#Hyperbolic Angles of Each Value in Arrays 
hyper_angles_arr = np.array([0, 1, -1])
hyper_angles_arr_angle = np.angle(hyper_angles_arr) #This calculates the angle of each element in the array using the np.angle ufunc, which returns the angle of a complex number in radians. For real numbers, it will return 0 for positive values and pi for negative values.
print(hyper_angles_arr_angle)

#Archsinh, Arccosh, and Arctanh functions
archsinh_arr = np.array([0, 1, -1])
archsinh_arr_asinh = np.arcsinh(archsinh_arr) #This calculates the inverse hyperbolic sine of each element in the array using the np.arcsinh ufunc, resulting in an array of inverse hyperbolic sine values.
print(archsinh_arr_asinh)

arccosh_arr = np.array([1, 2, 3])
arccosh_arr_acosh = np.arccosh(arccosh_arr) #This calculates the inverse hyperbolic cosine of each element in the array using the np.arccosh ufunc, resulting in an array of inverse hyperbolic cosine values. Note that the input values must be greater than or equal to 1 for real results.
print(arccosh_arr_acosh)

arctanh_arr = np.array([0, 0.5, -0.5])
arctanh_arr_atanh = np.arctanh(arctanh_arr) #This calculates the inverse hyperbolic tangent of each element in the array using the np.arctanh ufunc, resulting in an array of inverse hyperbolic tangent values. Note that the input values must be between -1 and 1 for real results.
print(arctanh_arr_atanh)

#Hyperbolic Hypotenuses
hyp_hyper_arr1 = np.array([3, 5, 7])
hyp_hyper_arr2 = np.array([4, 12, 24])
hypotenuse_hyper_arr = np.hypot(hyp_hyper_arr1, hyp_hyper_arr2) #This calculates the hypotenuse of a right triangle given the lengths of the two legs (hyp_hyper_arr1 and hyp_hyper_arr2) using the np.hypot ufunc, resulting in an array of hypotenuse lengths.
print(hypotenuse_hyper_arr)

#NumPy Set Operations
#Unique function
set_arr = np.array([1, 2, 3, 4, 4, 5, 5, 5])
unique_arr = np.unique(set_arr) #This finds the unique elements in the array using the np.unique ufunc, resulting in an array of unique values.
print(unique_arr)

#Union of two arrays
#Union of 1d arrays
set_arr1 = np.array([1, 2, 3, 4])
set_arr2 = np.array([3, 4, 5, 6])
union_arr = np.union1d(set_arr1, set_arr2) #This computes the union of two 1D arrays using the np.union1d ufunc, resulting in an array of unique values that are present in either of the input arrays.
print(union_arr)

# Intersection



