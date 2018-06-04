
# coding: utf-8

# In[38]:


from PIL import Image
import numpy as np
import os


# # Lecture de l'image 

# In[170]:


def ChargerImage(path):
    
    image_ = Image.open('images.jpg').convert('L')
    
    image_width = image_.width
    image_array = np.array(image_.getdata()).reshape(image_.size[0], image_.size[1], 1)
    
    return image_width,image_array


# # D’une image, un tableau

# In[171]:


def Transform_img_tab(image_array):
    
    array_pixels = []
    for image_line in image_array:
        [array_pixels.extend([pixel[0] for pixel in image_line])]
    
    return array_pixels
    


# # D’un tableau, une image

# In[172]:


def Transform_tab_img(Tab,image_width):
    return [Tab[x*image_width:(x+1)*image_width] for x in range(len(Tab)//image_width)]


# # Sauvegarde

# In[173]:


def save_img(path,image_array):
    np_image_array = np.array(image_array,dtype=np.uint8)
    Image.fromarray(np_image_array,"L").save(path)


# # Tri avec des screenshots (Tri à Bulles)

# In[195]:


def tri_bulle_image(TabImage,image_width,frame_rate=50000,base_filename='./IMG'):
    
    filename_index = 0
    frame_index = frame_rate
    
    for i in range(len(TabImage)):
        for j in range(i,len(TabImage)):
            
            if TabImage[i] < TabImage[j]:
                TabImage[i],TabImage[j] = TabImage[j],TabImage[i]
                
            frame_index -= 1
            if frame_index == 0:
                save_img(base_filename+str(filename_index)+'.png',Transform_tab_img(TabImage,image_width))
                filename_index += 1
                frame_index = frame_rate
    
    return TabImage


# # Tri avec des screenshots (Tri par séléction)

# In[190]:


def tri_select_image(TabImage,image_width,frame_rate=50000,base_filename='./IMG'):
    
    filename_index = 0
    frame_index = frame_rate
    
    for i in range(len(TabImage)-1):
        
        j = (TabImage[i:]).index(min(TabImage[i:]))
        j += i
        TabImage[i],TabImage[j] = TabImage[j],TabImage[i]

        frame_index -= 1
        if frame_index == 0:
            save_img(base_filename+str(filename_index)+'.png',Transform_tab_img(TabImage,image_width))
            filename_index += 1
            frame_index = frame_rate
    
    return TabImage


# # Lancement

# In[199]:


img = ChargerImage('image.jpg')
dim = img[0]
img = img[1]


#tabimg_ = tri_bulle_image(Transform_img_tab(img),dim,frame_rate=5000,base_filename='Images_Tri_Bulle/IMG')
#tabimg_ = tri_select_image(Transform_img_tab(img),dim,frame_rate=50,base_filename='Images_Tri_Select/IMG')

