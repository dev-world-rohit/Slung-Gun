import json, pygame, math

def export_file(path, data):
    file =  open(path, 'w')
    file.write(str(data))
    file.close()

def import_file(path):
    file = open(path, 'r')
    data = file.read()
    file.close()
    return data

def get_angle(pos_1, pos_2, img):
        x, y = pos_2[0] - pos_1[0] - int(img.get_width() / 2), pos_2[1] - pos_1[1] - int(img.get_height() / 2)
        angle = math.degrees(math.atan2(x, y)) - 90

        return angle

def get_distance(pos_1, pos_2):
        dis_x  = int(pos_1[1] - pos_2[0])
        dis_y = int(pos_1[1] - pos_2[1])
        dis_temp = math.pow(dis_x, 2) + math.pow(dis_y, 2)
        dis_real = math.pow(dis_temp, 0.5)
        return dis_temp