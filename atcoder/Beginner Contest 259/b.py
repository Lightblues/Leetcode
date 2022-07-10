""" 
B - Counterclockwise Rotation
将 (a,b) 逆时针循转 d度数
"""
import math
a,b,d = map(int, input().split())
if a==b==0:
    print(0, 0); exit()
if b>=0:
    angle = math.acos(a / math.sqrt(a*a + b*b))
else:
    angle = 2*math.pi - math.acos(a / math.sqrt(a*a + b*b))
angle += d*math.pi/180
r = math.sqrt(a*a + b*b)
print(r*math.cos(angle), r*math.sin(angle))
