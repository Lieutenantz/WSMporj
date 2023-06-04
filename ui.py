import tkinter as tk
from tkinter import *
from tkinter import ttk, font
from PIL import Image, ImageTk
from utils import get_config
import search_engine as se

fig_size = 300
topn = 20 # 展示的结果图片数

class Framelist(tk.Tk):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("WSM图片搜索引擎")
        self.window.geometry("1000x800")  # 设置主窗口大小

        self.entry = tk.Entry(self.window, width=50)
        self.entry.pack()

        self.entry_frame = tk.Frame(self.window, height = 30)
        self.entry_frame.pack(fill=X)
        # self.entry_frame.pack_propagate(False)
        self.entry_frame1 = tk.Frame(self.entry_frame)
        self.entry_frame1.pack()

        self.fitlter_label1 = tk.Label(self.entry_frame1, text="宽度范围：")
        self.fitlter_label1.pack(side=LEFT)
        self.entry_minw = tk.Entry(self.entry_frame1, width=10)
        self.entry_minw.pack(side=tk.LEFT)
        self.fitlter_label2 = tk.Label(self.entry_frame1, text="to")
        self.fitlter_label2.pack(side=LEFT)
        self.entry_maxw = tk.Entry(self.entry_frame1, width=10)
        self.entry_maxw.pack(side=tk.LEFT)
        self.fitlter_label3 = tk.Label(self.entry_frame1, text="        ")
        self.fitlter_label3.pack(side=LEFT)

        self.fitlter_label4 = tk.Label(self.entry_frame1, text="高度范围：")
        self.fitlter_label4.pack(side=LEFT)
        self.entry_minh = tk.Entry(self.entry_frame1, width=10)
        self.entry_minh.pack(side=tk.LEFT)
        self.fitlter_label5 = tk.Label(self.entry_frame1, text="to")
        self.fitlter_label5.pack(side=LEFT)
        self.entry_maxh = tk.Entry(self.entry_frame1, width=10)
        self.entry_maxh.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.window, text='search', 
                                       command=self.search, bg='red', fg='white')
        self.search_button.pack()
        
        self.frames = []

        self.scrollable_frame = tk.Frame(self.window, bg="white")  # 设置背景色为白色
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
            str = ""
            str += "name:"
            # print(image)
            str += image
            str += '\n'

            str = ""
            str += "score:"
            str += f"{self.scores[idx]}"
            str += '\n'

            text.insert(tk.END, str)

            custom_font = font.Font(family="Arial", size=20, weight="bold")
            text.configure(font=custom_font)

            # 创建一个tag，设置对应的属性
            text.tag_configure("center", justify="center")

            # 应用tag到文本范围
            text.tag_add("center", "1.0", "end")

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
            w1 = None
        w2 = self.entry_maxw.get()
        if not w1:
            w2 = None
        h1 = self.entry_minh.get()
        if not w1:
            h1 = None
        h2 = self.entry_maxh.get()
        if not w1:
            h2 = None
        
        # 返回的是图片路径和数据
        self.images, self.scores = self.SE.serve(text, topn, w1, w2, h1, h2)

        # 获得了存放图片的数组，接下来依据该数据的长度，创建等量的标签
        self.create_frames()
        
    # 根据路径获取单张图片
    def load_image(self, path):
        print(path)
        image = Image.open(path)
        resized_image = image.resize((280, 280), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

if __name__=="__main__":
    a = Framelist()
    a.run()
        


        

            
