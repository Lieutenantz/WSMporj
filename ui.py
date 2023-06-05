import tkinter as tk
from tkinter import *
from tkinter import ttk, font
from PIL import Image, ImageTk
from utils import get_config
import search_engine as se
import import_images as ii

color1 = "#66CCFF" # 蓝色，菜单底色
color2 = "#90EE90" # 浅绿，背景色
fig_size = 300
topn = 20 # 展示的结果图片数

class Framelist(tk.Tk):
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(bg="white")
        self.window.title("WSM IMAGE SEARCH ENGINE",)
        self.window.geometry("1000x800")  


        # 左侧展示图片的滚动栏
        self.scrollable_frame = tk.Frame(self.window, bg="white", width=1000)  # 设置背景色为白色
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollable_frame.pack_propagate(False)

        # 右侧的筛选搜索，添加图片菜单
        self.right_frame = tk.Frame(self.window, bg=color2, width=280,
                                    highlightthickness=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        # 右上方的搜索功能
        self.search_frame = tk.Frame(self.right_frame, bg=color1,height= 350, width=250,
                                     highlightthickness=2)
        self.search_frame.pack(side=tk.TOP,)
        self.search_frame.pack_propagate(False)
        
        self.search_frame_title_label = tk.Label(self.search_frame, 
                                                 text="image search",
                                                 bg=color1,
                                                 fg="red", 
                                                 font=("Microsoft YaHei", 14, "bold"))
        self.search_frame_title_label.pack(anchor="nw")

        self.entry_frame = tk.Frame(self.search_frame, bg=color1, width = 280, height= 50)
        self.entry_frame.pack(side=tk.TOP, fill=X)
        self.entry_frame.pack_propagate(False)
        self.entry_label = tk.Label(self.entry_frame, bg=color1,text="qeury:")
        self.entry_label.pack(side=tk.LEFT)
        self.entry = tk.Entry(self.entry_frame)
        self.entry.pack(side=tk.LEFT)

        self.entry_frame1 = tk.Frame(self.search_frame, bg=color1,width = 280, height= 50)
        self.entry_frame1.pack(side=tk.TOP, fill=X)
        self.entry_frame1.pack_propagate(False)
        self.fitlter_label1 = tk.Label(self.entry_frame1, bg=color1,text="minimum width")
        self.fitlter_label1.pack(side=LEFT)
        self.entry_minw = tk.Entry(self.entry_frame1)
        self.entry_minw.pack(side=tk.LEFT)

        self.entry_frame2 = tk.Frame(self.search_frame, bg=color1,width = 280, height= 50)
        self.entry_frame2.pack(side=tk.TOP, fill=X)
        self.entry_frame2.pack_propagate(False)
        self.fitlter_label2 = tk.Label(self.entry_frame2,bg=color1, text="maximum width")
        self.fitlter_label2.pack(side=LEFT)
        self.entry_maxw = tk.Entry(self.entry_frame2)
        self.entry_maxw.pack(side=tk.LEFT)


        self.entry_frame3 = tk.Frame(self.search_frame,bg=color1, width = 280, height= 50)
        self.entry_frame3.pack(side=tk.TOP, fill=X)
        self.entry_frame3.pack_propagate(False)
        self.fitlter_label3 = tk.Label(self.entry_frame3, bg=color1,text="minimum height")
        self.fitlter_label3.pack(side=LEFT)
        self.entry_minh = tk.Entry(self.entry_frame3)
        self.entry_minh.pack(side=tk.LEFT)

        self.entry_frame4 = tk.Frame(self.search_frame, bg=color1,width = 280, height= 50)
        self.entry_frame4.pack(side=tk.TOP, fill=X)
        self.entry_frame4.pack_propagate(False)
        self.fitlter_label4 = tk.Label(self.entry_frame4, bg=color1,text="maximum height")
        self.fitlter_label4.pack(side=LEFT)
        self.entry_maxh = tk.Entry(self.entry_frame4)
        self.entry_maxh.pack(side=tk.LEFT)

        self.search_button = ttk.Button(self.search_frame, text='search', 
                                       command=self.search)
        self.search_button.pack(side=tk.TOP)


        #上传图片功能
        self.upload_frame = tk.Frame(self.right_frame, bg=color1, height= 350, width=250,
                                     highlightthickness=2)
        self.upload_frame.pack(side=tk.BOTTOM)
        self.upload_frame.pack_propagate(False)

        self.search_frame_title_label = tk.Label(self.upload_frame, 
                                                 text="add new image",
                                                 bg=color1,
                                                 fg="red", 
                                                 font=("Microsoft YaHei", 14, "bold"))
        self.search_frame_title_label.pack(anchor="nw")

        self.upload_frame1 = tk.Frame(self.upload_frame, bg=color1, width = 280, height= 50)
        self.upload_frame1.pack(side=tk.TOP, fill=X)
        self.upload_label1 = tk.Label(self.upload_frame1, bg=color1, text="image/directory path ")
        self.upload_label1.pack(side=tk.LEFT)
        

        self.upload_frame2 = tk.Frame(self.upload_frame, bg=color1, width = 280, height= 50)
        self.upload_frame2.pack(side=tk.TOP, fill=X)
        self.upload_entry = tk.Entry(self.upload_frame2,width=200)
        self.upload_entry.pack(side=tk.LEFT,fill=X)

        self.upload_frame3 = tk.Frame(self.upload_frame, bg=color1, width = 280, height= 50)
        self.upload_frame3.pack(side=tk.TOP, fill=X)
        self.upload_button = ttk.Button(self.upload_frame3, text='添加图片', 
                                       command=self.add_image)
        self.upload_button.pack(side=tk.TOP)

        self.upload_demo = tk.Label(self.upload_frame, bg=color1, fg="#EE0000", text="",width=40)
        self.upload_demo.pack(side=tk.TOP)
        
        self.frames = []

        self.canvas = tk.Canvas(self.scrollable_frame, bg="white", highlightthickness=0)  # 设置Canvas背景色为白色，并去掉边框
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.scrollable_frame, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # 绑定鼠标滚轮事件

        self.frame_list = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_list, anchor=tk.NW)

        self.frame_list.bind("<Configure>", self._on_frame_configure)  # 监听frame大小变化事件

    def create_frames(self):
        print(f"images list len: {len(self.images)}")
        for idx, image in enumerate(self.images):
            # 创建该图片对应的frame, label和canvas
            style = ttk.Style()
            style.configure("Custom.TFrame", borderwidth=1, relief="raised", background="white")  # 设置圆角矩形样式

            frame = ttk.Frame(self.frame_list, style="Custom.TFrame",  
                             width=1000, height=300, padding=(30, 20))  # 添加边框
            frame.pack(side=tk.TOP, fill=tk.X, expand=True)
            frame.pack_propagate(False)

            canvas = tk.Canvas(frame, width=300, height=300, highlightthickness=0)
            canvas.pack(side=tk.LEFT)
            canvas.pack_propagate(False)

            # 获取图片
            picture = self.load_image(image)
            canvas.create_image(110, 100, image=picture)  # 在Canvas上显示图片
            canvas.image = picture  # 保存对PhotoImage的引用，防止被垃圾回收

            text = tk.Text(frame, width=600, height=260)
            text.pack(side=tk.RIGHT)
            text.pack_propagate(False)
            
            # 需要显示的属性
            information = ""
            information += "name:"
            information += image
            information += '\n'

            information += "score:"
            information += f"{self.scores[idx]*100:5.3f}%"
            information += '\n'
            
            information += "File size:"
            information +=f"{self.size_list[idx]//1024}KB"
            information += '\n'
            
            information += "Dimensions:"
            information += "{0}".format(self.widths[idx])
            information += "x"
            information += "{0}".format(self.heights[idx])
            information += '\n'

            text.insert(tk.END, information)

            custom_font = font.Font(family="Arial", size=20, weight="bold")
            text.configure(font=custom_font)

            # 创建一个tag，设置对应的属性
            text.tag_configure("center", justify="center")

            # 应用tag到文本范围
            text.tag_add("center", "1.0", "end")
            text.configure(state="disabled")

            self.frames.append(frame)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def run(self):
        config = get_config()
        self.SE = se.SearchEngine(config)

        self.window.mainloop()

    def search(self):
        text = self.entry.get()

        # 获取尺寸限制
        w1 = self.entry_minw.get()
        if not w1:
            w1 = 0
        w2 = self.entry_maxw.get()
        if not w1:
            w2 = None
        h1 = self.entry_minh.get()
        if not w1:
            h1 = 0
        h2 = self.entry_maxh.get()
        if not w1:
            h2 = None
        
        # 返回的是图片路径和数据
        self.images, self.scores, self.widths, self.heights, self.size_list = self.SE.serve(text, topn, w1, w2, h1, h2)

        for widget in self.frame_list.winfo_children():
            widget.destroy()
        # 获得了存放图片的数组，接下来依据该数据的长度，创建等量的标签
        self.create_frames()
        
    # 根据路径获取单张图片
    def load_image(self, path):
        print(path)
        image = Image.open(path)
        resized_image = image.resize((280, 280), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)
    
    def add_image(self):
        path = self.upload_entry.get()
        if ii.tools(path):
            self.upload_demo.config(text="新增图片成功")  # 插入新的文本
        else:
            self.upload_demo.config(text="新增图片失败")  # 插入新的文本


if __name__=="__main__":
    a = Framelist()
    a.run()
        


        

            
