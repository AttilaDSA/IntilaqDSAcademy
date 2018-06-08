
# coding: utf-8

# ## Matrice Repr

# In[28]:


def MShow(A):
    for l in A:
        print(l)


# In[29]:


A = [[1,0,1],[2,3,1],[2,3,1]]


# In[30]:


MShow(A)


# ## Matrice Addition

# In[16]:


def Add(A,B):
    nlines = len(A[1])
    ncols = len(A)
    
    return [[A[i][j]+B[i][j] for j in range(ncols)] for i in range(nlines)]
    


# In[17]:


#################################


# In[32]:


A = [[1,0],[2,3]]
B = [[3,1],[1,1]]


# In[35]:


print('A')
MShow(A)
print('B')
MShow(B)
print('A+B')
MShow(Add(A,B))


# In[20]:


#################################


# ## Matrice Multiplication

# In[1]:


def Mul(A,B):
    
    C = [[0 for _ in range(a_ncols)] for __ in range(b_nlines)]
    
    for i in range(a_ncols):
        for j in range(b_nlines):
            C[i][j] = sum([a*b for a,b in zip(A[i],[k[j] for k in B])])
            
    return C


# In[ ]:


#################################


# In[2]:


A = [[1,0],[2,3]]
B = [[3,1],[1,1]]


# In[36]:


print('A')
MShow(A)
print('B')
MShow(B)
print('AB')
MShow(Mul(A,B))


# In[ ]:


#################################


# ## Transvection Matrice

# In[56]:


def Mat_Transvection(n,i,j,a):
    In = [[int(k==l) for k in range(n)] for l in range(n)]
    Eij = [[a*int(k==j-1 and l==i-1) for k in range(n)] for l in range(n)]
    return Add(In,Eij)


# In[57]:


#################################


# In[58]:


MShow(Mat_Transvection(3,3,1,3))


# In[24]:


#################################


# #### Testing Transvect

# In[54]:


A = [[4,5,14],[1,11,23],[0,2,-5]]
MShow(A)


# In[59]:


T = Mat_Transvection(3,1,3,1)
MShow(T)


# #### Multiplication à gauche

# In[61]:


MShow(Mul(T,A))
print('')
MShow(A)


# #### Multiplication à droite

# In[62]:


MShow(Mul(A,T))
print('')
MShow(A)


# #### Commentaires
Tij*A   <=>  Li <- Li + a*Lj

A*Tij   <=>  Cj <- Cj + a*Ci
# ## Permutation Matrice

# In[65]:


def Mat_Permutation(n,i,j):
    In = [[int(k==l) for k in range(n)] for l in range(n)]
    In[i-1],In[j-1] = In[j-1],In[i-1] 
    return In


# In[69]:


#################################


# In[67]:


MShow(Mat_Permutation(3,2,3))


# In[68]:


#################################


# #### Testing Permutation

# In[71]:


A = [[4,5,14],[1,11,23],[0,2,-5]]
MShow(A)


# In[73]:


P = Mat_Permutation(3,1,3)
MShow(P)


# #### Multiplication à gauche

# In[74]:


MShow(Mul(P,A))
print('')
MShow(A)


# #### Multiplication à droite

# In[76]:


MShow(Mul(A,P))
print('')
MShow(A)


# #### Commentaires
Pij*A   <=>  Li <-> Lj

A*Pij   <=>  Cj <- Ci
# ## Application

# In[124]:


A = [[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,-1]]
MShow(A)


# #### L1 < L1 + L4

# In[125]:


A = Mul(Mat_Transvection(4,1,4,1),A)
MShow(A)


# #### L2 < L2 - L4

# In[126]:


A = Mul(Mat_Transvection(4,2,4,-1),A)
MShow(A)


# #### L3 < L3 - L4

# In[127]:


A = Mul(Mat_Transvection(4,3,4,-1),A)
MShow(A)


# #### L4 < L4 - 1/2*L1
# #### L4 < L4 + 1/2*L2
# #### L4 < L4 + 1/2*L3

# In[128]:


A = Mul(Mat_Transvection(4,4,1,-0.5),A)
A = Mul(Mat_Transvection(4,4,2,0.5),A)
A = Mul(Mat_Transvection(4,4,3,0.5),A)
MShow(A)


# #### L4 < L4 - 2L4
# #### L3 < L3 - 0.5L3
# #### L2 < L2 - 0.5L2
# #### L1 < L1 - 0.5L1

# In[129]:


A = Mul(Mat_Transvection(4,4,4,-2),A)
A = Mul(Mat_Transvection(4,3,3,-0.5),A)
A = Mul(Mat_Transvection(4,2,2,-0.5),A)
A = Mul(Mat_Transvection(4,1,1,-0.5),A)
MShow(A)


# ### Retrouver L'inverse

# In[130]:


B = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
MShow(B)


# In[131]:


B = Mul(Mat_Transvection(4,1,4,1),B)
B = Mul(Mat_Transvection(4,2,4,-1),B)
B = Mul(Mat_Transvection(4,3,4,-1),B)
B = Mul(Mat_Transvection(4,4,1,-0.5),B)
B = Mul(Mat_Transvection(4,4,2,0.5),B)
B = Mul(Mat_Transvection(4,4,3,0.5),B)
B = Mul(Mat_Transvection(4,4,4,-2),B)
B = Mul(Mat_Transvection(4,3,3,-0.5),B)
B = Mul(Mat_Transvection(4,2,2,-0.5),B)
B = Mul(Mat_Transvection(4,1,1,-0.5),B)
MShow(B)


# In[136]:


A = [[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,-1]]
MShow(Mul(A,B))
print('')
MShow(Mul(B,A))

