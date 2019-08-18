#-*-coding:utf-8-*-
"""
参考
    http://b4rracud4.hatenadiary.jp/entry/20181207/1544129263
    https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
    https://pg-chain.com/python-tkinter-entry
"""
import numpy as np

import tkinter as tk
import tkinter.messagebox as tkmsg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg  import FigureCanvasTkAgg

from functools import partial

import function as fnc

def Quit():
       root.quit()
       root.destroy()

def DrawCanvas(canvas, ax, colors = "gray"):
    value = EditBox_1.get()

    if value != '':
        EditBox_1.delete(0, tk.END)
        ax.cla()#前の描画データの消去
        gridSize = int(value)
        gridSize = (gridSize * 2 + 1) #半区画の区切りを算出

        velo = float(EditBox_2.get())
        ang_in = float(EditBox_3.get())
        ang = -float(EditBox_4.get())
        velo_ang = -float(EditBox_5.get())
        accel_ang = -float(EditBox_6.get())
        K = float(EditBox_7.get())
        offset_in = float(EditBox_8.get())
        offset_out = float(EditBox_9.get())
        
        #区画の線を引く
        for i in np.array(range(gridSize)) * 90.0:
            ax.plot(np.array([i, i]), np.array([0.0, (gridSize - 1) * 90]), color=colors, linestyle="dashed")
            ax.plot(np.array([0.0, (gridSize - 1) * 90]), np.array([i, i]), color=colors, linestyle="dashed")

            #斜めの線を引く
            if (i / 90.0) % 2 == 1:
                ax.plot(np.array([0.0, i]), np.array([(gridSize - 1) * 90 - i, (gridSize - 1) * 90]), color=colors, linestyle="dashed")
                ax.plot(np.array([(gridSize - 1) * 90 - i, (gridSize - 1) * 90]), np.array([0.0, i]), color=colors, linestyle="dashed")

                ax.plot(np.array([(gridSize - 1) * 90, i]), np.array([i, (gridSize - 1) * 90]), color=colors, linestyle="dashed")
                ax.plot(np.array([i, 0.0]), np.array([0.0, i]), color=colors, linestyle="dashed")
        
        #calculate curve timing
        controler0 = fnc.Control()
        controler0.calc_angle(accel_ang,ang,0.0,velo_ang,0.0)

        #drowe offset
        line0 = fnc.Line(in_ang=ang_in,in_velo=velo,in_K=K)
        dist = 0.0
        while dist < offset_in:
            line0.update_point()
            dist += velo*0.001
        plt.plot(line0.x,line0.y)


        #drow cycroid 1
        slip1 = fnc.Line(line0.x[-1],line0.y[-1],in_ang=ang_in,in_velo=velo,in_K=K)
        while slip1.ang + slip1.slip > ang_in + controler0.ang_fst:
            slip1.update_point(accel_ang,True)
        plt.plot(slip1.x,slip1.y)

        #drow circle
        slip2 = fnc.Line(slip1.x[-1],slip1.y[-1],slip1.ang,slip1.velo_ang,slip1.slip,in_velo=velo,in_K=K)
        while slip2.ang + slip2.slip > ang_in + controler0.ang_mid:
            slip2.update_point(slip_flag=True)
        plt.plot(slip2.x,slip2.y)

        #drow cycroid 2
        slip3 = fnc.Line(slip2.x[-1],slip2.y[-1],slip2.ang,slip2.velo_ang,slip2.slip,in_velo=velo,in_K=K)
        while slip3.ang + slip3.slip> ang_in + controler0.ang_end:
            slip3.update_point(-accel_ang,True)
        plt.plot(slip3.x,slip3.y)


        #drow offset out
        slip4 = fnc.Line(slip3.x[-1],slip3.y[-1],slip3.ang,0.0,slip3.slip,in_velo=velo,in_K=K)
        dist = 0.0
        while dist < offset_out:
            slip4.update_point()
            dist += velo*0.001
        plt.plot(slip4.x,slip4.y)
           
        canvas.draw()  #キャンバスの描画

if __name__ == "__main__":
    try:
        #GUIの生成
        root = tk.Tk()
        root.title("あー、てすてす")

        # ここでウインドウサイズを定義する
        #root.geometry('1400x1000')

        #グラフの設定
        fig,ax1 = plt.subplots()
        fig.gca().set_aspect('equal', adjustable='box')#グラフ領域の調整
        #fig = plt.figure(figsize=(5,5),dpi=200)
        #ax1 = fig.add_subplot(1,1,1)

        #キャンバスの生成
        Canvas = FigureCanvasTkAgg(fig, master=root)
        Canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

        #テキストボックスに関する諸々の設定
        EditBox_1 = tk.Entry(width=5)#テキストボックスの生成
        EditBox_1.grid(row=1, column=2)

        EditBox_2 = tk.Entry(width=5)
        EditBox_2.grid(row=2,column=2)

        EditBox_3=tk.Entry(width=5)
        EditBox_3.grid(row=3,column=2)

        EditBox_4=tk.Entry(width=5)
        EditBox_4.grid(row=4,column=2)

        EditBox_5=tk.Entry(width=5)
        EditBox_5.grid(row=5,column=2)

        EditBox_6=tk.Entry(width=5)
        EditBox_6.grid(row=6,column=2)

        EditBox_7=tk.Entry(width=5)
        EditBox_7.grid(row=1,column=4)

        EditBox_8=tk.Entry(width=5)
        EditBox_8.grid(row=2,column=4)

        EditBox_9=tk.Entry(width=5)
        EditBox_9.grid(row=3,column=4)

        #ラベルに関する諸々の設定
        GridLabel_1 = tk.Label(text="ますめ")
        GridLabel_1.grid(row=1, column=1)

        GridLabel_2 = tk.Label(text=u"並進速度")
        GridLabel_2.grid(row=2,column=1)

        GridLabel_3 = tk.Label(text="進入角度")
        GridLabel_3.grid(row=3,column=1)

        GridLabel_4 = tk.Label(text="ターン角度")
        GridLabel_4.grid(row=4,column=1)

        GridLabel_5 = tk.Label(text="角速度")
        GridLabel_5.grid(row=5,column=1)

        GridLabel_6 = tk.Label(text="角加速度")
        GridLabel_6.grid(row=6,column=1)

        GridLabel_7 = tk.Label(text="定数K")
        GridLabel_7.grid(row=1,column=3)

        GridLabel_8 = tk.Label(text="オフセットイン")
        GridLabel_8.grid(row=2,column=3)

        GridLabel_9 = tk.Label(text="オフセットアウト")
        GridLabel_9.grid(row=3,column=3)


        #ボタンに関する諸々の設定
        ReDrawButton = tk.Button(text="こうしん", width=15, command=partial(DrawCanvas, Canvas, ax1))#ボタンの生成
        ReDrawButton.grid(row=8, column=1, columnspan=2)#描画位置(テキトー)

        QuitButton = tk.Button(text="やめる", width=15, command=Quit)#ボタンの生成
        QuitButton.grid(row=9, column=1, columnspan=2)#描画位置(テキトー)
        
        DrawCanvas(Canvas,ax1)
        root.mainloop()#描画し続ける
    except:
        import traceback
        traceback.print_exc()
    finally:
        input(">>")#エラー吐き出したときの表示待ち
