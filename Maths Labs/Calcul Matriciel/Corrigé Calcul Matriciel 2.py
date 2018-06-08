
# coding: utf-8

# ## Matrice Repr

# In[12]:


def MShow(A):
    for l in A:
        print(l)


# ## Calcul Récursif du Déterminant

# In[66]:


def det(A,n):
    if n==1:
        return A[0][0]
    elif n==2:
        return A[0][0]*A[1][1]-A[0][1]*A[1][0]
    else:
        i=0
        Cij = [0 for _ in range(n)]
        for j in range(n):
            B = [
                [A[k][l] for l in range(n) if l != j]
                for k in range(n) if k != i
            ]
            Cij[j] = (-1)**(i+j)*det(B,n-1)
        
        return sum([A[0][j]*Cij[j] for j in range(n)])


# In[61]:


###########################


# In[67]:


A=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,-1]]
MShow(A)


# In[68]:


det(A,4)


# In[69]:


B=[[0.5, 0.0, 0.0, 0.5],[0.0, 0.5, 0.0, -0.5],[0.0, 0.0, 0.5, -0.5],[0.5, -0.5, -0.5, 0.5]]
MShow(B)


# In[70]:


det(B,4)


# In[284]:


# B étant l'inverse de A (Trouvé dans le Lab précédent),
# il vérifie la propriété:
# det(A) = 1/det(B)


# In[71]:


###########################


# ## Tests Temps d'exécution

# In[72]:


import random
def RandMat(d):
    return [[random.randint(0,100) for _ in range(d)] for __ in range(d)]


# In[287]:


MShow(RandMat(3))


# In[286]:


from time import time
for dim in range(2,13):
    A = RandMat(dim)
    t = time()
    det(A,dim)
    print("Temps exécution (s): "+str(int(time()-t))+". Dimension A: "+str(dim))


# ### Conclusion
Le temps d'exécution est trop élevé ! 
La fonction T qui donne le temps d'exécution en fonction de la dimension de la matrice est clairement en exponentielle.
# ## Optimisation 1
Au départ, l'algorithme fonctionnait en choisissant arbitrairement une ligne par rapport à laquelle développer. Suite à cette optimisation, nous allons choisir la ligne ou la colonne qui contient le plus de 0 pour éviter  du calcul inutile :

det(M) = sum(Mij*det(m(i,j))  =>  det(M) = sum(Mij*det(m(i,j)) / Mij != 0)    

m(i,j) étant la matrices obtenue en suprimant la ligne i et la colonne j.
# In[88]:


def det_opt_1(A,n):
    if n==1:
        return A[0][0]
    elif n==2:
        return A[0][0]*A[1][1]-A[0][1]*A[1][0]
    elif n <= 8:
        # On optimise seulement lorsque la taille de la matrice dépasse 9
        return det(A,n)
    else:
        # Number of Zeros per line of A
        lzeros = [l.count(0) for l in A]
        # Number of Zeros per column of A
        czeros = [[A[i][j] for i in range(n)].count(0) for j in range(n)]
        
        dev_line = None
        dev_col = None
        num_zeros = 0
        if max(czeros) > max(lzeros):
            dev_line = lzeros.index(max(lzeros))
            num_zeros = max(lzeros)
        else:
            dev_col = czeros.index(max(czeros))
            num_zeros = max(czeros)
        
        Cij = [0 for _ in range(n)]
        if(dev_line):
            # Developpement par rapport à la ligne qui à le plus de 0
            for j in range(n):
                B = [
                    [A[k][l] for l in range(n) if l != j]
                    for k in range(n) if k != dev_line
                ]
                if A[dev_line][j] != 0:
                    Cij[j] = (-1)**(i+j)*det_opt_1(B,n-1)
                else:
                    Cij[j] = 0
                
            return sum([A[dev_line][j]*Cij[j] for j in range(n)])
        else:
            # Developpement par rapport à la colonne qui à le plus de 0
            for i in range(n):
                B = [
                    [A[k][l] for l in range(n) if l != dev_col]
                    for k in range(n) if k != i
                ]
                if A[i][dev_col] != 0:
                    Cij[j] = (-1)**(i+j)*det_opt_1(B,n-1)
                else:
                    Cij[j] = 0
        
            return sum([A[i][dev_col]*Cij[i] for i in range(n)])


# ## Tests Temps d'exécution

# In[86]:


for dim in range(2,13):
    A = RandMat(dim)
    t = time()
    det_opt_1(A,dim)
    print("Temps exécution (s): "+str(int(time()-t))+". Dimension A: "+str(dim))


# ### Conclusion
Le temps d'exécution n'a pas changé !
Cette optimisation reste infructueuse car elle dépend du nombre de zeros que contient la matrice, et si elle n'en contient pas, alors on aura un temps d'exécution encore plus important que la fonction non optimisée.
# ## Optimisation 2
Dans cette partie nous allons créer les zeros, grace à la propriété du déterminant det(AB) = det(A)*det(B).

La transvection ne change pas le déterminant car det(Tij)=1:
    det(Tij*A)=det(A*Tij)=det(A)*det(Tij) = det(A) 
La permutation multiplie le determinant par -1 car det(Pij)=-1:
    det(Pij*A)=det(A*Pij)=det(A)*det(Pij) = -det(A)
    
Nous allons donc procédér à la permutation et à la transvection pour faire apparaitre le maximum de zéros dans la matrice.
Pour celà nous allons transformer notre matrice en matrice triangulaire inférieure.

           a  b  c  d                        q  0  0  0
           e  f  g  h             =>         r  s  0  0
           i  j  k  l                        t  u  v  0
           m  n  o  p                        w  x  y  z
# In[104]:


def Add(A,B):
    nlines = len(A)
    ncols = len(A[1])
    
    return [[A[i][j]+B[i][j] for j in range(ncols)] for i in range(nlines)]
    


# In[105]:


def Mul(A,B):
    b_nlines = len(B)
    a_ncols = len(A[1])
    
    C = [[0 for _ in range(a_ncols)] for __ in range(b_nlines)]
    
    for i in range(a_ncols):
        for j in range(b_nlines):
            C[i][j] = sum([a*b for a,b in zip(A[i],[k[j] for k in B])])
            
    return C


# In[183]:


# La fonction mat_round transform les coeffs de la matrice qui sont
# très proches de 0 (< 10**-12) en 0 
def Mat_Round(M,n):
    for i in range(n):
        for j in range(n):
            if M[i][j] < 10e-12:
                M[i][j] = 0
    return M


# In[89]:


def Mat_Transvection(n,i,j,a):
    In = [[int(k==l) for k in range(n)] for l in range(n)]
    Eij = [[a*int(k==j-1 and l==i-1) for k in range(n)] for l in range(n)]
    return Add(In,Eij)


# In[135]:


def Mat_Permutation(n,i,j):
    In = [[int(k==l) for k in range(n)] for l in range(n)]
    In[i-1],In[j-1] = In[j-1],In[i-1] 
    return In


# In[270]:


# Algorithme triangularisation:
"""
Methode du pivot de gauss
--------------------------------
nb_permutation = 0
Pour i de 1 à N-1
    Pivot = Choix_Pivot()
    Pour j de i+1 à N
        Cj <- Cj - (Aij/Pivot)*Ci 
--------------------------------       
Avec    Cj : la colonne j
        Aij : l'élément Aij de la matrice
--------------------------------  
"""

def triangulariser(A,n):
    nb_permutation = 0
    
    A = Mat_Round(A,n)
    
    for i in range(n-1):
        # Choix du pivot
        pivot = sorted([abs(A[i][j]) for j in range(i,n)],reverse=True)[0]
        if pivot == 0:
            continue
        index_pivot = [abs(A[i][j]) for j in range(i,n)].index(pivot)+i
        pivot = float(A[i][index_pivot])
        
        # Permutation (mettre le pivot sur la diagonale)
        if i+1 != index_pivot+1:
            A = Mul(A,Mat_Permutation(n,i+1,index_pivot+1))
            nb_permutation += 1
        
        # Transvection des colonnes
        for j in range(i+1,n):
            A = Mul(A,Mat_Transvection(n,i+1,j+1,-A[i][j]/pivot))
            #A = Mat_Round(A,n)
                    
    return nb_permutation,A


# In[271]:


###########################


# In[272]:


A=[[1,1,1,1,1],[1,1,-1,-1,1],[1,-1,1,-1,1],[1,-1,-1,-1,1],[1,-1,-1,-1,-1]]
MShow(A)


# In[273]:


det(A,5)


# In[274]:


n,C = triangulariser(A,len(A))


# In[275]:


MShow(C)


# In[276]:


det(C,5)


# In[ ]:


###########################


# In[277]:


def det_opt_2(A,n):
    np,C = triangulariser(A,n)
    # Une fois triangulaire, le determinant devient tous simplement
    # le produit de la diagonale
    dtr = 1
    for i in range(n):
        dtr = dtr*C[i][i]
    return dtr*((-1)**np)


# In[278]:


###########################


# In[279]:


A


# In[280]:


det_opt_2(A,len(A))


# In[ ]:


###########################


# ## Tests Temps d'exécution

# In[282]:


for dim in range(2,50):
    A = RandMat(dim)
    t = time()
    det_opt_2(A,dim)
    print("Temps exécution (s): "+str(int(time()-t))+". Dimension A: "+str(dim))


# ### Conclusion
La conclusion se fait toute seule en regardant le gain de temps qu'on vient d'achever.
Et on peut encore optimiser .... 
                                                                Bon Weekend