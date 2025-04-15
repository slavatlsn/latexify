import os

a = set(map(lambda x: x[:x.rfind('.')], os.listdir(r'/src/runs/dataset/val/images')))
b = set(map(lambda x: x[:x.rfind('.')], os.listdir(r'/src/runs/dataset/val/labels')))

c = a - b
print(c)
#for el in c:
#    os.remove(r'C:\Users/user/PycharmProjects/latexify/datasets/dataset/train/images/'+el+'.png')
