from urllib.parse import urlparse

import urllib.request
import requests

import time

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import tkinter.messagebox as msgbox

# naver_openapi에 query 검색 결과 요청 함수
def request_naver(source, query, start, id, pw):
    client_id = id
    client_secret = pw

    client_id = '9XWXrMOThLlElbQtxhP2'
    client_secret = 'XsVFw5rRPO'


    header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
    encText = urllib.parse.quote(query)

    if source == 'blog':
        url = "https://openapi.naver.com/v1/search/blog.json?query=" + encText + "&display=100&start=" + str(start) # json 결과
    elif source == 'cafe':
        url = "https://openapi.naver.com/v1/search/cafearticle.json?query=" + encText + "&display=100&start=" + str(start) # json 결과

    r = requests.get(urlparse(url).geturl(), headers=header)
    if r.status_code == 200:
        return r.json()
    else:
        return r.status_code

# 결과 요청 및 json 응답 결과 중 원하는 결과 추출
def get_naver(source, query, id, pw):
    list = []
    page = 0
    if source == 'blog':
        while page < 10:  # 검색 시작 위치로 최대 1000까지 가능
            json_obj = (request_naver(source, query, (page * 100) + 1, id, pw))  # 한 페이지 당 최대 100개 가능
            for document in json_obj['items']:
                val = [document['title'].replace("<b>", "").replace("</b>", "").replace("amp;", ""),
                       document['description'].replace("<b>", "").replace("</b>", ""),
                       document['bloggername'], document['postdate'], document['link']]
                list.append(val)
            page += 1
            if json_obj['total'] < (page * 100): break
    elif source == 'cafe':
        while page < 10:  # 검색 시작 위치로 최대 1000까지 가능
            json_obj = (request_naver(source, query, (page * 100) + 1, id, pw))  # 한 페이지 당 최대 100개 가능
            for document in json_obj['items']:
                val = [document['title'].replace("<b>", "").replace("</b>", "").replace("amp;", ""),
                       document['description'].replace("<b>", "").replace("</b>", ""),
                       document['cafename'], document['link']]
                list.append(val)
            page += 1
            if json_obj['total'] < (page * 100): break
    return list


def btncmd():
    # query = '코로나'
    source = 'blog'
    txt.insert(END, "\n크롤링 진행중")

    query = entry.get()

    id = id_entry.get()
    pw = pw_entry.get()

    result = get_naver(source, query, id, pw)
    title = []
    content = []
    author = []
    postdate = []
    url = []

    for i, list in enumerate(result):
        title.append(list[0])
        content.append(list[1])
        author.append(list[2])
        postdate.append(list[3])
        url.append(list[4])

    for i in range(0, 100):
        label4.config(text=url[i])
        title_label.config(text=title[i])
        # content_label.config(text=content[i])
        scr.delete("1.0","end")
        scr.insert(END, content[i])
        author_label.config(text=author[i])
        ps = postdate[i]
        postdate_label.config(text=(ps[:4]+'년'+ps[4:6]+'월'+ps[6:]+'일'))

        p_var2.set(i)
        prog.update()
        time.sleep(0.1)

    txt.insert(END, "\n크롤링 완료")
    msgbox.showinfo("알림", "정상적으로 크롤링이 완료되었습니다")

def to_file():
    txt.insert(END, "\n파일 저장")
    msgbox.showinfo("알림", "파일이 저장되었습니다.")

if __name__ == "__main__":
    root = Tk()
    root.title("DrSong Crawling Tool")
    root.geometry("800x380")

    label1 = Label(root, text="닥터송 크롤링 툴")
    label1.pack(side="top", fill="both", expand=True)

    Crawling_frame = LabelFrame(root, text="크롤링")
    Crawling_frame.pack(side="top", fill="both", expand=True)

    option_frame=Frame(Crawling_frame)
    option_frame.pack(side="top")
    left_frame = Frame(Crawling_frame)
    left_frame.pack(side="left")
    right_frame = Frame(Crawling_frame)
    right_frame.pack(side="left")
    bottom_frame = Frame(Crawling_frame)
    bottom_frame.pack(side="bottom")
    console_frame = Frame(Crawling_frame)
    console_frame.pack(side="right")

    option = Label(option_frame, text="옵션 선택 ")
    option.pack(anchor=W)

    btn1 = Checkbutton(option_frame, text="네이버 블로그", variable=1)
    btn1.pack(side="left", anchor=W)
    btn2 = Checkbutton(option_frame, text="네이버 카페", variable=2)
    btn2.pack(side="left", anchor=W)
    btn3 = Checkbutton(option_frame, text="유튜브", variable=3)
    btn3.pack(side="left", anchor=W)
    btn4 = Checkbutton(option_frame, text="트위터", variable=4)
    btn4.pack(side="left", anchor=W)

    id = Label(left_frame, text="아이디 입력 : ")
    id.pack(anchor=W)

    id_entry = Entry(right_frame, width=32)
    id_entry.pack(anchor=W)

    pw = Label(left_frame, text="패스워드 입력 : ")
    pw.pack(anchor=W)

    pw_entry = Entry(right_frame, width=32, show='*')
    pw_entry.pack(anchor=W)

    p_var2 = DoubleVar()
    label1 = Label(left_frame, text="검색어 입력 : ")
    label1.pack(anchor=W)

    entry = Entry(right_frame, width=32)
    entry.pack(anchor=W)


    label5 = Label(console_frame, text="Crawling log")
    label5.pack(anchor=W)

    txt = Text(console_frame, width=32, height=5, border=0)
    txt.config(highlightbackground='black', highlightthickness=2)
    txt.insert(END, "로그 기록")
    txt.pack(anchor=W)

    # label = Label(left_frame)
    # label.pack(fill="x")

    label2 = Label(left_frame, text="크롤링 진행률 : ")
    label2.pack(anchor=W)

    prog = ttk.Progressbar(right_frame,  maximum=100, length=320, variable=p_var2)
    prog.pack(anchor=W)

    label3 = Label(left_frame, text="진행 url : ")
    label3.pack(anchor=W)

    # tmp = Label(right_frame)
    # tmp.pack()

    label4 = Label(right_frame, text="url")
    # label4 = Label(right_frame)
    label4.pack(anchor=W, fill=X)


    btn = Button(console_frame, width=5, text="검색",  command=btncmd)
    btn.pack()


#################################################################
    Data_frame = LabelFrame(root, text="데이터")
    Data_frame.pack(side="top", fill="both", expand=True)

    label_data = Frame(Data_frame, width=70)
    label_data.pack(side="left")

    left_data = Frame(Data_frame)
    left_data.pack(side="left")

    right_data = Frame(Data_frame)
    right_data.pack(side="left")

    title_label = Label(left_data)
    title_label.pack(anchor=W)

    scrol_w = 70
    scrol_h = 3
    scr = st.ScrolledText(left_data, width=scrol_w, height=scrol_h, wrap=tk.WORD)
    scr.config(highlightbackground='black', highlightthickness=1)
    scr.pack(anchor=W)

    t_label = Label(label_data, text="제목 : ")
    t_label.pack(anchor=W)

    c_label = Label(label_data, text="내용 : ", height=5)
    c_label.pack(anchor=W)

    a_label = Label(label_data, text="작성자 : ")
    a_label.pack(anchor=W)

    p_label = Label(label_data, text="작성 일시 : ")
    p_label.pack(anchor=W)

    author_label = Label(left_data)
    author_label.pack(anchor=W)

    postdate_label = Label(left_data)
    postdate_label.pack(anchor=W)

    btn3 = Button(right_data, text="Excel 파일로 저장", fg='black', command=to_file)
    btn3.pack()
    btn4 = Button(right_data, text="TXT 파일로 저장", command=to_file)
    btn4.pack()

    root.mainloop()
