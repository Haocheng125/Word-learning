import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict, Optional
from database import DatabaseManager
from pdf_reader import PDFReader
import os

class WordCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("单词学习助手")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.db = DatabaseManager()
        self.pdf_reader = PDFReader()
        
        self.current_list_id = None
        self.current_words = []
        self.current_index = 0
        self.queue = []
        self.showing_chinese = False
        
        self.setup_main_ui()

    def setup_main_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame, 
            text="单词学习助手", 
            font=('Microsoft YaHei UI', 24, 'bold')
        )
        title_label.pack(pady=(0, 30))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        load_pdf_btn = ttk.Button(
            button_frame, 
            text="加载PDF文件", 
            command=self.load_pdf_files,
            width=20
        )
        load_pdf_btn.pack(pady=5)
        
        load_folder_btn = ttk.Button(
            button_frame, 
            text="加载PDF文件夹", 
            command=self.load_pdf_folder,
            width=20
        )
        load_folder_btn.pack(pady=5)
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        lists_label = ttk.Label(
            main_frame, 
            text="已加载的单词列表", 
            font=('Microsoft YaHei UI', 14)
        )
        lists_label.pack(pady=(0, 10))
        
        # 创建可滚动的框架
        scrollable_frame = ttk.Frame(main_frame)
        scrollable_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建画布
        canvas = tk.Canvas(scrollable_frame, yscrollcommand=scrollbar.set, bg='#f0f0f0')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        scrollbar.config(command=canvas.yview)
        
        # 创建内部框架
        self.lists_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.lists_frame, anchor=tk.NW)
        
        # 绑定鼠标滚轮事件
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        
        # 更新画布大小
        def update_scrollregion():
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        
        self.refresh_word_lists()
        self.root.after(100, update_scrollregion)

    def refresh_word_lists(self):
        for widget in self.lists_frame.winfo_children():
            widget.destroy()
        
        word_lists = self.db.get_all_word_lists()
        
        if not word_lists:
            no_data_label = ttk.Label(
                self.lists_frame, 
                text="暂无单词列表，请先加载PDF文件",
                font=('Microsoft YaHei UI', 10),
                foreground='gray'
            )
            no_data_label.pack(pady=20)
            return
        
        for word_list in word_lists:
            list_frame = ttk.Frame(self.lists_frame)
            list_frame.pack(fill='x', pady=5)
            
            total_words = self.db.get_total_words_count(word_list['id'])
            list_name = f"{word_list['list_name']} ({total_words} 个单词)"
            
            name_label = ttk.Label(
                list_frame, 
                text=list_name, 
                font=('Microsoft YaHei UI', 11)
            )
            name_label.pack(side='left', padx=10)
            
            start_btn = ttk.Button(
                list_frame, 
                text="开始学习", 
                command=lambda lid=word_list['id']: self.start_learning(lid),
                width=10
            )
            start_btn.pack(side='right', padx=5)
            
            delete_btn = ttk.Button(
                list_frame, 
                text="删除", 
                command=lambda lid=word_list['id'], lname=word_list['list_name']: self.delete_list(lid, lname),
                width=6
            )
            delete_btn.pack(side='right', padx=5)

    def load_pdf_files(self):
        file_paths = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not file_paths:
            return
        
        loaded_count = 0
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            words = self.pdf_reader.read_pdf_to_words(file_path)
            
            if words:
                list_name = os.path.splitext(file_name)[0]
                list_id = self.db.create_word_list(list_name, file_name)
                self.db.add_words(list_id, words)
                loaded_count += 1
                print(f"Loaded {len(words)} words to '{list_name}'")
        
        if loaded_count > 0:
            messagebox.showinfo("成功", f"已加载 {loaded_count} 个单词列表")
        else:
            messagebox.showwarning("警告", "未能从所选PDF文件中提取单词")
        
        self.refresh_word_lists()

    def load_pdf_folder(self):
        folder_path = filedialog.askdirectory(title="选择包含PDF文件的文件夹")
        
        if not folder_path:
            return
        
        pdf_data = self.pdf_reader.read_folder_pdfs(folder_path)
        
        if not pdf_data:
            messagebox.showwarning("警告", "未找到可用的PDF文件")
            return
        
        loaded_count = 0
        for list_name, words in pdf_data.items():
            if words:
                list_id = self.db.create_word_list(list_name)
                self.db.add_words(list_id, words)
                loaded_count += 1
        
        messagebox.showinfo("成功", f"已加载 {loaded_count} 个单词列表")
        self.refresh_word_lists()

    def delete_list(self, list_id: int, list_name: str):
        if messagebox.askyesno("确认", f"确定要删除 '{list_name}' 吗？"):
            self.db.delete_word_list(list_id)
            self.refresh_word_lists()

    def start_learning(self, list_id: int):
        self.current_list_id = list_id
        self.current_words = self.db.get_words_by_list(list_id)
        
        if not self.current_words:
            messagebox.showwarning("警告", "该列表中没有单词")
            return
        
        progress = self.db.get_progress(list_id)
        self.current_index = progress['current_position']
        self.queue = progress['queue']
        
        self.show_learning_ui()

    def show_learning_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill='x', pady=(0, 20))
        
        back_btn = ttk.Button(
            top_frame, 
            text="返回主页", 
            command=self.back_to_main,
            width=12
        )
        back_btn.pack(side='left')
        
        total_words = len(self.current_words)
        progress = self.db.get_progress(self.current_list_id)
        completed_words = progress['completed_words']
        
        progress_label = ttk.Label(
            top_frame, 
            text=f"进度: {completed_words}/{total_words}",
            font=('Microsoft YaHei UI', 12)
        )
        progress_label.pack(side='right')
        
        card_frame = ttk.Frame(main_frame)
        card_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.word_card = tk.Frame(
            card_frame, 
            bg='white', 
            relief='raised', 
            borderwidth=2
        )
        self.word_card.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        self.word_label = tk.Label(
            self.word_card,
            text="",
            font=('Arial', 36, 'bold'),
            bg='white',
            fg='#333333',
            cursor='hand2'
        )
        self.word_label.pack(expand=True)
        self.word_label.bind('<Button-1>', self.toggle_chinese)
        
        self.chinese_label = tk.Label(
            self.word_card,
            text="",
            font=('Microsoft YaHei UI', 24),
            bg='white',
            fg='#666666'
        )
        self.chinese_label.pack(expand=True)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        prev_btn = ttk.Button(
            button_frame, 
            text="上一个", 
            command=self.previous_word,
            width=15
        )
        prev_btn.pack(side='left', padx=10)
        
        queue_btn = ttk.Button(
            button_frame, 
            text="加入队列", 
            command=self.add_to_queue,
            width=15
        )
        queue_btn.pack(side='left', padx=10)
        
        next_btn = ttk.Button(
            button_frame, 
            text="下一个", 
            command=self.next_word,
            width=15
        )
        next_btn.pack(side='left', padx=10)
        
        self.showing_chinese = False
        self.update_card()

    def update_card(self):
        if self.current_index >= len(self.current_words):
            self.show_completion()
            return
        
        word = self.current_words[self.current_index]
        self.word_label.config(text=word['english'])
        self.chinese_label.config(text="")
        self.showing_chinese = False

    def toggle_chinese(self, event=None):
        if self.current_index >= len(self.current_words):
            return
        
        word = self.current_words[self.current_index]
        
        if self.showing_chinese:
            self.chinese_label.config(text="")
            self.showing_chinese = False
        else:
            self.chinese_label.config(text=word['chinese'])
            self.showing_chinese = True

    def add_to_queue(self):
        if self.current_index >= len(self.current_words):
            return
        
        # 获取当前单词
        current_word = self.current_words[self.current_index]
        
        # 检查单词是否已经在列表末尾
        if self.current_words[-1]['id'] != current_word['id']:
            # 将单词移动到列表末尾
            self.current_words.pop(self.current_index)
            self.current_words.append(current_word)
            
            # 更新卡片显示当前位置的新单词
            self.update_card()
        
        # 保存进度
        self.save_progress()

    def next_word(self):
        if self.current_index >= len(self.current_words):
            return
        
        # 记录当前单词的学习历史
        current_word_id = self.current_words[self.current_index]['id']
        self.db.add_study_history(self.current_list_id, current_word_id)
        
        self.current_index += 1
        
        self.save_progress()
        self.update_card()
        
        # 更新进度显示
        total_words = len(self.current_words)
        progress = self.db.get_progress(self.current_list_id)
        completed_words = progress['completed_words']
        
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and "进度:" in child.cget('text'):
                        child.config(text=f"进度: {completed_words}/{total_words}")

    def previous_word(self):
        if self.current_index <= 0:
            messagebox.showinfo("提示", "已经是第一个单词了")
            return
        
        self.current_index -= 1
        self.save_progress()
        self.update_card()
        
        # 更新进度显示
        total_words = len(self.current_words)
        progress = self.db.get_progress(self.current_list_id)
        completed_words = progress['completed_words']
        
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and "进度:" in child.cget('text'):
                        child.config(text=f"进度: {completed_words}/{total_words}")

    def save_progress(self):
        if self.current_list_id and self.current_words and self.current_index < len(self.current_words):
            current_word_id = self.current_words[self.current_index]['id']
            completed_words = self.current_index + 1
            self.db.save_progress(self.current_list_id, self.current_index, current_word_id, self.queue, completed_words)

    def show_completion(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        completion_label = ttk.Label(
            main_frame,
            text="恭喜！您已完成所有单词的学习！",
            font=('Microsoft YaHei UI', 20, 'bold')
        )
        completion_label.pack(expand=True)
        
        back_btn = ttk.Button(
            main_frame,
            text="返回主页",
            command=self.back_to_main,
            width=15
        )
        back_btn.pack(pady=20)

    def back_to_main(self):
        self.save_progress()
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_main_ui()

    def on_closing(self):
        self.save_progress()
        self.db.close()
        self.root.destroy()

def main():
    try:
        root = tk.Tk()
        app = WordCardApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"Error: {e}\n\n{traceback.format_exc()}"
        print(error_msg)
        try:
            with open("error_log.txt", "w", encoding="utf-8") as f:
                f.write(error_msg)
        except:
            pass
        try:
            import tkinter.messagebox as mb
            root = tk.Tk()
            root.withdraw()
            mb.showerror("错误", f"程序启动失败:\n{e}")
        except:
            pass

if __name__ == "__main__":
    main()