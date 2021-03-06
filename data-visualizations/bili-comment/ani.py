import colorsys
from colorthief import ColorThief
import json
import os
from p5 import setup, draw, run
import p5 as pf
from PIL import Image
import time
from reply_processer import *

t0 = time.time()

""" Global Variables """
mid = 546195 # 老番茄

root = "./ups/mid-{}/".format(mid)
frame_path = root+"frames/"
if not os.path.exists(frame_path):
    os.mkdir(frame_path)
cover_path = root+"covers/"
info_path = root+"infos/"

font = pf.create_font("C:/windows/fonts/arialuni.ttf",16)

# with open(info_path+"{}-vlist.json".format(mid), "r") as rf:
#     jsn = json.load(rf)

# vinfo_L: list
# each row: {aid: *, created: *, title: *, pic_url: *, length: *}, sorted by aid
with open(info_path +"vinfo.pkl", "rb") as rf:
    vinfo_L = pickle.load(rf)
# ninfo_L: 2d list (video_num x ct_group_cnt)
# each row: list of accumulate floor count of all ctime groups
with open(info_path +"ninfo.pkl", "rb") as rf:
    ninfo_L = pickle.load(rf)
# ct_L: list (1 x ct_group_cnt)
# ctime group point
with open(info_path +"tinfo.pkl", "rb") as rf:
    ct_L = pickle.load(rf)
# s_idx_L: 2d list (ct_group_cnt x k)
# each row: list (1 x k), top k aids ranked by accumulated floor nums at each ctime group
with open(info_path +"sinfo.pkl", "rb") as rf:
    s_idx_L = pickle.load(rf)

# print(len(s_idx_L), len(ct_L))
print(s_idx_L[-30])

rx,ry = 200,200
rw,rh = 50,50

""" Assitant functions """

cover_r_path = root+"covers-r/"
resize_cmd = "magick convert \"{}\" -resize {}x{} \"{}\""
def resize_covers():
    if not os.path.exists(cover_r_path):
        os.makedirs(cover_r_path)
    for i,fname in enumerate(os.listdir(cover_path)[:]):
        name,ext = os.path.splitext(fname)
        if ext != ".jpg":
            continue
        print("{:>3} Resizing {}".format(i+1, fname))
        img_name = cover_path + fname
        resize_img_name = cover_r_path + fname
        os.system(resize_cmd.format(img_name, 120, 90, resize_img_name))

# resize_covers()

palette_path = root+"covers-p/"
def get_palette():
    if not os.path.exists(palette_path):
        os.makedirs(palette_path)
    for i,fname in enumerate(os.listdir(cover_path)[:]):
        name,ext = os.path.splitext(fname)
        if ext != ".jpg":
            continue
        print("{:>3} Get palette of {}".format(i+1, fname))
        img_name = cover_path + fname
        # img.size = (w,h)
        img = Image.open(img_name)
        img = img.resize((120,90))
        # img = pf.load_image(img)
        clr_thf = ColorThief(img)
        palette_L = []
        palette_L = clr_thf.get_palette(color_count=4,quality=10)
        d_color = clr_thf.get_color(quality=10)
        palette_L.insert(0,d_color)
        for i,palette in enumerate(palette_L):
            clr_img = Image.new("RGBA",(50,50),palette)
            clr_img_name = "{}{}-{}{}".format(palette_path, name, i, ".png")
            clr_img.save(clr_img_name)
        img.save(palette_path+fname)
        # shutil.copy(img_name, "{}{}".format(palette_path,fname))

# get_palette()

"""  """

class Bar:
    def __init__(self,x=rx,y=ry,w=rw,h=rh):
        self.x, self.y, self.w, self.h = x, y, w, h

        self.x_align = "l"
        self.y_align = "c"

        self.is_fill = True
        self.fill_rgb = [255,255,255]

        self.is_stroke = False
        self.stroke_rgb = [255,0,255]
        self.stroke_weight = 1

        self.is_rect = True

        self.str = "hello"
        self.is_text = True

        self.is_disp = True

    @property
    def xy(self):
        return [self.x, self.y]

    def get_rect_x(self):
        rect_x_D = {
            "l": self.x,
            "c": self.x-self.w/2,
            "r": self.x-self.w
        }
        return rect_x_D[self.x_align]

    def get_rect_y(self):
        rect_y_D = {
            "t": self.y,
            "c": self.y-self.h/2,
            "b": self.y-self.h
        }
        return rect_y_D[self.y_align]

    def rect(self):
        if self.is_rect:
            with pf.push_style():
                if not self.is_stroke and not self.is_fill:
                    return
                pf.color_mode("RGB")
                if self.is_fill:
                    pf.fill(*self.fill_rgb)
                else:
                    pf.no_fill()
                if self.is_stroke:
                    pf.stroke_weight(self.stroke_weight)
                    pf.stroke(*self.stroke_rgb)
                else:
                    pf.no_stroke()
                pf.rect([self.get_rect_x(),self.get_rect_y()], self.w, self.h)

    def text(self):
        if self.is_text:
            with pf.push_style():
                pf.text(self.str, (self.x, self.y+30))
                print(pf.text_ascent(), pf.text_descent(), pf.text_width(self.str))
                pf.no_fill()
                pf.stroke(*self.stroke_rgb)
                pf.rect((self.x,self.y+30), pf.text_width(self.str), pf.text_ascent()+pf.text_descent(), mode="CORNER")
    def disp(self):
        self.rect()
        self.text()

def setup():
    ratio = 1.8
    pf.size(1280/ratio,720/ratio)
    pf.text_font(font)
    pf.text_size(50)
    pf.no_stroke()
    pf.no_loop()

def draw():
    pf.background(0)
    pf.rect_mode("CORNER")
    b = Bar(100,50)
    # b.is_fill = False
    b.str = "Hello，老番茄"
    b.disp()
    # c = Bar(100,50+b.h+1)
    # c.disp()
    # pf.save_frame(img_path + "screen_.png")

if __name__ == '__main__':
    # run(frame_rate = 30)
    print("Total elapsed time: {}s".format(round(time.time()-t0,1)))
