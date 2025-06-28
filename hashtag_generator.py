# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import random
import time
import requests
from bs4 import BeautifulSoup
import threading
# --- NEW V2.2: Import library to open web browser ---
import webbrowser

# --- NEW V2.2: Define current version and update URL ---
CURRENT_VERSION = "2.1" 
# IMPORTANT: Replace this URL with the raw URL of YOUR version.json file on GitHub
# Example: https://raw.githubusercontent.com/your-username/your-repo/main/version.json
UPDATE_JSON_URL = "YOUR_GITHUB_VERSION_JSON_RAW_URL_HERE"


class ToolTip:
    """Creates a tooltip for a given widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background='#424242', relief='solid', borderwidth=1,
                         foreground="#eceff1", font=("Tahoma", 8, "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class HashtagGeneratorApp:
    """
    Main application class for the Hashtag and Keyword Generator.
    Version: 2.2 - Auto-Update Checker
    """
    def __init__(self, root):
        self.root = root
        self.root.title(f"AI Hashtag & Keyword Finder V{CURRENT_VERSION} (Online Search)")
        self.root.geometry("900x700")
        self.root.minsize(850, 650)
        
        self.BG_COLOR = "#212121"
        self.FRAME_COLOR = "#263238"
        self.WIDGET_BG_COLOR = "#37474F"
        self.TEXT_COLOR = "#ECEFF1"
        self.ACCENT_COLOR = "#03A9F4"
        self.ACCENT_ACTIVE_COLOR = "#0288D1"
        
        self.root.configure(bg=self.BG_COLOR)
        self.search_history = []

        self._configure_styles()
        self._create_widgets()
        
        # --- NEW V2.2: Check for updates on startup ---
        self.check_for_updates()

    # --- NEW V2.2: Function to check for updates in a thread ---
    def check_for_updates(self):
        """Checks for a new version in a separate thread to not freeze the GUI."""
        update_thread = threading.Thread(target=self._update_logic)
        update_thread.daemon = True
        update_thread.start()

    def _update_logic(self):
        """The core logic for checking updates."""
        try:
            if UPDATE_JSON_URL == "YOUR_GITHUB_VERSION_JSON_RAW_URL_HERE":
                print("Update check skipped: Please set your UPDATE_JSON_URL.")
                return 

            response = requests.get(UPDATE_JSON_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            latest_version = data.get("latest_version")
            download_url = data.get("download_url")

            # Simple version comparison
            if latest_version and latest_version > CURRENT_VERSION:
                if messagebox.askyesno("มีอัปเดตใหม่!", 
                                       f"มีเวอร์ชันใหม่ ({latest_version}) ให้ดาวน์โหลด!\nเวอร์ชันปัจจุบันของคุณคือ {CURRENT_VERSION}\n\nคุณต้องการดาวน์โหลดเลยหรือไม่?"):
                    webbrowser.open(download_url)
        except Exception as e:
            print(f"Could not check for updates: {e}")


    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure(".", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=("Tahoma", 10))
        self.style.configure("TFrame", background=self.BG_COLOR)
        self.style.configure("TLabel", background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=("Tahoma", 11))
        self.style.configure("Header.TLabel", font=("Tahoma", 14, "bold"), foreground=self.ACCENT_COLOR)
        self.style.configure("Status.TLabel", font=("Tahoma", 9), foreground=self.TEXT_COLOR)
        
        self.style.configure("TNotebook", background=self.BG_COLOR, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.FRAME_COLOR, foreground=self.TEXT_COLOR, padding=[12, 6], borderwidth=0, font=("Tahoma", 10))
        self.style.map("TNotebook.Tab", background=[("selected", self.ACCENT_COLOR)], foreground=[("selected", "#ffffff")])
        
        self.style.configure("TButton", background=self.ACCENT_COLOR, foreground="#ffffff", font=("Tahoma", 10, "bold"), borderwidth=0, padding=10)
        self.style.map("TButton", background=[('active', self.ACCENT_ACTIVE_COLOR)])
        
        self.style.configure("TEntry", fieldbackground=self.WIDGET_BG_COLOR, foreground=self.TEXT_COLOR, borderwidth=1, insertbackground=self.TEXT_COLOR)
        self.style.configure("TCombobox", fieldbackground=self.WIDGET_BG_COLOR, background=self.WIDGET_BG_COLOR, foreground=self.TEXT_COLOR, arrowcolor=self.TEXT_COLOR)
        
        self.style.configure("Treeview", background=self.WIDGET_BG_COLOR, fieldbackground=self.WIDGET_BG_COLOR, foreground=self.TEXT_COLOR, relief="flat")
        self.style.map("Treeview", background=[('selected', self.ACCENT_ACTIVE_COLOR)])
        self.style.configure("Treeview.Heading", background=self.FRAME_COLOR, foreground=self.TEXT_COLOR, font=("Tahoma", 10, "bold"), relief="flat")
        self.style.map("Treeview.Heading", background=[('active', self.FRAME_COLOR)])
        
    def _create_widgets(self):
        # Top level widgets...
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=(10,0))
        
        status_bar_frame = ttk.Frame(self.root, style="TFrame")
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self.status_label = ttk.Label(status_bar_frame, text="สถานะ: พร้อมใช้งาน", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT)

        # Tabs...
        self.search_tab = ttk.Frame(self.notebook, style="TFrame")
        self.about_tab = ttk.Frame(self.notebook, style="TFrame")
        self.patch_notes_tab = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.search_tab, text='  ค้นหาแท็ก (Search)  ')
        self.notebook.add(self.about_tab, text='  เกี่ยวกับ (About)  ')
        self.notebook.add(self.patch_notes_tab, text='  อัปเดต (Patch Notes)  ')

        self._create_search_tab()
        self._create_about_tab()
        self._create_patch_notes_tab()

    # All other functions remain the same as V2.1
    # ... (code from _create_search_tab to the end) ...
    def _create_search_tab(self):
        main_frame = ttk.Frame(self.search_tab)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(input_frame, text="Keyword:").pack(side=tk.LEFT, padx=(0, 5))
        self.keyword_entry = ttk.Entry(input_frame, font=("Tahoma", 12), width=30)
        self.keyword_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.keyword_entry.bind("<Return>", self.start_search_thread)
        ttk.Label(input_frame, text="ภาษา:").pack(side=tk.LEFT, padx=(10, 5))
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(input_frame, textvariable=self.language_var, values=["ไทย", "English"], width=10, state="readonly")
        self.language_combo.set("ไทย"); self.language_combo.pack(side=tk.LEFT)
        self.search_button = ttk.Button(input_frame, text="🚀 ค้นหา", command=self.start_search_thread)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))
        content_frame = ttk.Frame(main_frame); content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.columnconfigure(1, weight=3); content_frame.rowconfigure(0, weight=1)
        history_frame = ttk.Frame(content_frame); history_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        results_notebook = ttk.Notebook(content_frame); results_notebook.grid(row=0, column=1, sticky="nsew")
        self.yt_tab = self._create_treeview_tab(results_notebook, "📈 YouTube"); self.tt_tab = self._create_treeview_tab(results_notebook, "🎵 TikTok"); self.title_tab = ttk.Frame(results_notebook)
        results_notebook.add(self.yt_tab["frame"], text=" YouTube "); results_notebook.add(self.tt_tab["frame"], text=" TikTok "); results_notebook.add(self.title_tab, text=" 💡 AI ตั้งชื่อคลิป ")
        ttk.Label(history_frame, text="ประวัติการค้นหา", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        self.history_listbox = tk.Listbox(history_frame, bg=self.WIDGET_BG_COLOR, fg=self.TEXT_COLOR, selectbackground=self.ACCENT_ACTIVE_COLOR, relief="flat", height=10, borderwidth=0); self.history_listbox.pack(fill=tk.BOTH, expand=True)
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)
        history_btn_frame = ttk.Frame(history_frame); history_btn_frame.pack(fill=tk.X, pady=(5,0))
        save_btn = ttk.Button(history_btn_frame, text="บันทึก", command=self.save_history); save_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,2))
        load_btn = ttk.Button(history_btn_frame, text="เรียกคืน", command=self.load_history); load_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2,2))
        clear_btn = ttk.Button(history_btn_frame, text="ล้าง", command=self.clear_history); clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2,0))
        title_header = ttk.Frame(self.title_tab); title_header.pack(fill=tk.X, pady=5, padx=5)
        ttk.Label(title_header, text="💡 AI ช่วยตั้งชื่อคลิป", style="Header.TLabel").pack(side=tk.LEFT)
        self.title_copy_button = ttk.Button(title_header, text="คัดลอก", width=8, command=self.copy_title_suggestions); self.title_copy_button.pack(side=tk.RIGHT)
        self.title_results_text = scrolledtext.ScrolledText(self.title_tab, wrap=tk.WORD, height=5, relief="flat", bg=self.WIDGET_BG_COLOR, fg=self.TEXT_COLOR, font=("Tahoma", 10)); self.title_results_text.pack(expand=True, fill='both', pady=5, padx=5)
    def _create_treeview_tab(self, parent_notebook, platform_name):
        frame = ttk.Frame(parent_notebook)
        copy_button = ttk.Button(frame, text=f"คัดลอกแท็ก {platform_name}", command=lambda: self.copy_treeview_content(tree)); copy_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        cols = ('tag', 'relevance', 'type'); tree = ttk.Treeview(frame, columns=cols, show='headings', selectmode="none")
        tree.heading('tag', text='แท็ก / คีย์เวิร์ด'); tree.heading('relevance', text='ความเกี่ยวข้อง'); tree.heading('type', text='ประเภท')
        tree.column('tag', width=300); tree.column('relevance', width=100, anchor=tk.CENTER); tree.column('type', width=100, anchor=tk.CENTER)
        tree.pack(expand=True, fill='both', padx=5, pady=5); return {"frame": frame, "tree": tree}
    def start_search_thread(self, event=None):
        keyword = self.keyword_entry.get().strip()
        if not keyword: messagebox.showwarning("คำเตือน", "กรุณากรอก Keyword ก่อนทำการค้นหา"); return
        self.search_button.config(text="กำลังค้นหา...", state="disabled"); self.status_label.config(text=f"สถานะ: กำลังค้นหา \"{keyword}\" จาก Google...")
        self.populate_treeview(self.yt_tab["tree"], []); self.populate_treeview(self.tt_tab["tree"], []); self.title_results_text.delete('1.0', tk.END)
        thread = threading.Thread(target=self.perform_online_search, args=(keyword,)); thread.daemon = True; thread.start()
    def perform_online_search(self, keyword):
        try:
            language = self.language_var.get(); yt_data, tt_data, title_data = self.fetch_online_data(keyword, language)
            self.root.after(0, self.update_ui_with_results, yt_data, tt_data, title_data, keyword)
        except Exception as e: self.root.after(0, self.handle_search_error, e)
    def update_ui_with_results(self, yt_data, tt_data, title_data, keyword):
        if keyword not in self.search_history: self.search_history.insert(0, keyword); self.update_history_listbox()
        self.populate_treeview(self.yt_tab["tree"], yt_data); self.populate_treeview(self.tt_tab["tree"], tt_data); self.title_results_text.insert(tk.END, title_data)
        self.search_button.config(text="🚀 ค้นหา", state="normal"); self.status_label.config(text="สถานะ: พร้อมใช้งาน"); messagebox.showinfo("สำเร็จ", f"ค้นหา \"{keyword}\" เสร็จสิ้น!")
    def handle_search_error(self, error):
        messagebox.showerror("เกิดข้อผิดพลาด", f"ไม่สามารถค้นหาข้อมูลออนไลน์ได้:\n{error}\n\nกรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ตหรือลอง Keyword อื่น")
        self.search_button.config(text="🚀 ค้นหา", state="normal"); self.status_label.config(text="สถานะ: เกิดข้อผิดพลาด")
    def populate_treeview(self, tree, data):
        for i in tree.get_children(): tree.delete(i)
        for item in data:
            tag_display = f"🔥 {item['tag']}" if item.get('is_trending', False) else item['tag']
            tree.insert('', tk.END, values=(tag_display, item['relevance'], item['type']))
    def fetch_online_data(self, keyword, language="ไทย"):
        lang_code = "th" if language == "ไทย" else "en"; url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}&hl={lang_code}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers); response.raise_for_status(); soup = BeautifulSoup(response.text, 'html.parser')
        related_searches_div = soup.find('div', id='bres'); related_keywords = []
        if related_searches_div:
            spans = related_searches_div.find_all('span')
            for span in spans:
                if 'class' not in span.attrs and span.get_text().strip(): related_keywords.append(span.get_text().strip())
        if not related_keywords:
             related_searches_divs = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
             for div in related_searches_divs: related_keywords.append(div.get_text().strip())
        related_keywords = list(dict.fromkeys(related_keywords)); yt_results = []; tt_results = []
        yt_results.append({"tag": keyword, "relevance": "สูงมาก", "type": "Keyword"}); tt_results.append({"tag": f"#{keyword.replace(' ', '')}", "relevance": "สูงมาก", "type": "Hashtag"})
        for kw in related_keywords:
            yt_results.append({"tag": kw, "relevance": "สูง", "type": "Keyword"}); yt_results.append({"tag": f"#{kw.replace(' ', '')}", "relevance": "สูง", "type": "Hashtag"})
            tt_results.append({"tag": f"#{kw.replace(' ', '')}", "relevance": "สูง", "type": "Hashtag"})
        generic_yt = ["#รีวิว", "#สอนให้รู้ว่า", "#tiktok"] if language == "ไทย" else ["#review", "#tutorial", "#howto"]
        generic_tt = ["#tiktokuni", "#fyp", "#foryoupage"] if language == "ไทย" else ["#learnontiktok", "#fyp", "#viral"]
        for tag in random.sample(generic_yt, k=min(len(generic_yt), 3)): yt_results.append({"tag": tag, "relevance": "ทั่วไป", "type": "Hashtag"})
        for tag in random.sample(generic_tt, k=min(len(generic_tt), 3)): tt_results.append({"tag": tag, "relevance": "ทั่วไป", "type": "Hashtag"})
        titles = []
        if related_keywords:
             titles.append(f"รีวิว {keyword} และ {random.choice(related_keywords)} แบบเจาะลึก" if language == "ไทย" else f"Reviewing {keyword} and {random.choice(related_keywords)}")
             titles.append(f"เทียบ {keyword} กับ {random.choice(related_keywords)}" if language == "ไทย" else f"Comparing {keyword} vs {random.choice(related_keywords)}")
        titles.append(f"วิธีใช้ {keyword} ให้โปรเหมือนมืออาชีพ" if language == "ไทย" else f"How to Use {keyword} Like a Pro")
        titles.append(f"สรุป {keyword} ใน 5 นาที" if language == "ไทย" else f"The Ultimate {keyword} Guide in 5 Minutes")
        random.shuffle(titles); final_titles = "\n\n".join(titles[:3])
        return yt_results, tt_results, final_titles
    def on_history_select(self, event):
        selected_indices = self.history_listbox.curselection();
        if not selected_indices: return
        self.keyword_entry.delete(0, tk.END); self.keyword_entry.insert(0, self.history_listbox.get(selected_indices[0])); self.start_search_thread()
    def copy_treeview_content(self, tree):
        items = tree.get_children();
        if not items: messagebox.showwarning("ว่างเปล่า", "ไม่มีข้อมูลให้คัดลอก"); return
        tags_to_copy = [tree.item(item)['values'][0].replace('🔥 ', '') for item in items]; clipboard_text = ' '.join(tags_to_copy); self.root.clipboard_clear(); self.root.clipboard_append(clipboard_text)
        messagebox.showinfo("สำเร็จ", "คัดลอกแท็กและคีย์เวิร์ดทั้งหมดแล้ว!")
    def copy_title_suggestions(self):
        content = self.title_results_text.get("1.0", tk.END).strip()
        if content: self.root.clipboard_clear(); self.root.clipboard_append(content); messagebox.showinfo("สำเร็จ", "คัดลอกชื่อคลิปแนะนำแล้ว!")
        else: messagebox.showwarning("ว่างเปล่า", "ไม่มีข้อความให้คัดลอก")
    def _create_about_tab(self):
        pass
    def _create_patch_notes_tab(self):
        content = """
        Version 2.2 (Auto-Update Checker - 2025-06-29)
        - [เพิ่ม] ระบบตรวจสอบอัปเดตอัตโนมัติเมื่อเปิดโปรแกรม
        - [เพิ่ม] หน้าต่างแจ้งเตือนเมื่อมีเวอร์ชันใหม่ให้ดาวน์โหลด
        - [สำคัญ] ต้องกำหนดค่า UPDATE_JSON_URL ในโค้ดก่อนใช้งาน

        Version 2.1 (Stability Fix - 2025-06-29)
        - [แก้ไข] ปัญหาโปรแกรมแครชเมื่อไม่พบ "คำค้นหาที่เกี่ยวข้อง"
        """
        notes_frame = ttk.Frame(self.patch_notes_tab); notes_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        label = ttk.Label(notes_frame, text=content, justify=tk.LEFT, font=("Tahoma", 11), anchor="nw"); label.pack(fill=tk.BOTH)
    def save_history(self):
        if not self.search_history: messagebox.showwarning("ว่างเปล่า", "ยังไม่มีประวัติให้บันทึก"); return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="บันทึกประวัติ")
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f: f.write("\n".join(self.search_history))
                messagebox.showinfo("สำเร็จ", f"บันทึกประวัติเรียบร้อยแล้ว")
            except Exception as e: messagebox.showerror("ผิดพลาด", f"ไม่สามารถบันทึกไฟล์ได้: {e}")
    def load_history(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], title="เลือกไฟล์ประวัติ")
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f: new_history = [line.strip() for line in f if line.strip()]
                current_set = set(self.search_history)
                for item in reversed(new_history):
                    if item not in current_set: self.search_history.insert(0, item)
                self.update_history_listbox()
                messagebox.showinfo("สำเร็จ", "โหลดประวัติเรียบร้อยแล้ว")
            except Exception as e: messagebox.showerror("ผิดพลาด", f"ไม่สามารถเปิดไฟล์ได้: {e}")
    def clear_history(self):
        if messagebox.askyesno("ยืนยัน", "คุณต้องการล้างประวัติการค้นหาทั้งหมดใช่หรือไม่?"):
            self.search_history.clear(); self.update_history_listbox()
            messagebox.showinfo("สำเร็จ", "ล้างประวัติเรียบร้อยแล้ว")
    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        current_items = list(self.history_listbox.get(0, tk.END))
        for item in current_items:
            if item not in self.search_history: self.search_history.append(item)
        self.history_listbox.delete(0, tk.END)
        for item in self.search_history: self.history_listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = HashtagGeneratorApp(root)
    root.mainloop()
