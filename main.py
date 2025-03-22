import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD
import json
import os

class MainApplication(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("ClassIsland-CCST")
        self.geometry("750x500")
        
        # 声明标签
        self.declaration_label = ttk.Label(self, text="（声明内容留空待后续填写）", font=('微软雅黑', 10))
        self.declaration_label.grid(row=0, column=0, columnspan=4, pady=5, sticky='w')

        # GitHub仓库地址输入
        self.github_frame = ttk.Frame(self)
        self.base_url_label = ttk.Label(self.github_frame, text="https://github.com/")
        self.entry_A = ttk.Entry(self.github_frame, width=15)
        self.slash_label = ttk.Label(self.github_frame, text="/")
        self.entry_B = ttk.Entry(self.github_frame, width=15)
        
        self.base_url_label.pack(side='left')
        self.entry_A.pack(side='left')
        self.slash_label.pack(side='left')
        self.entry_B.pack(side='left')
        self.github_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky='w')

        # 新增组织名称输入
        self.org_frame = ttk.Frame(self)
        self.org_label = ttk.Label(self.org_frame, text="组织名称：")
        self.entry_F = ttk.Entry(self.org_frame, width=30)
        self.org_label.pack(side='left')
        self.entry_F.pack(side='left', padx=5)
        self.org_frame.grid(row=2, column=0, columnspan=4, pady=5, sticky='w')

        # 本地配置文件
        self.config_frame = ttk.Frame(self)
        self.config_label = ttk.Label(self.config_frame, text="配置文件路径：")
        self.config_entry = tk.Entry(self.config_frame, width=40)
        self.browse_config_btn = ttk.Button(self.config_frame, text="浏览", command=self.select_config_file)
        self.update_btn = ttk.Button(self.config_frame, text="更新", command=self.update_config)
        
        # 拖拽绑定
        self.config_entry.drop_target_register('DND_Files')
        self.config_entry.dnd_bind('<<Drop>>', self.handle_drop)
        
        self.config_label.pack(side='left')
        self.config_entry.pack(side='left', padx=5)
        self.browse_config_btn.pack(side='left', padx=5)
        self.update_btn.pack(side='left')
        self.config_frame.grid(row=3, column=0, columnspan=4, pady=5, sticky='w')

        # 导出路径
        self.export_frame = ttk.Frame(self)
        self.export_label = ttk.Label(self.export_frame, text="导出目录：")
        self.export_entry = ttk.Entry(self.export_frame, width=40)
        self.browse_export_btn = ttk.Button(self.export_frame, text="浏览", command=self.select_export_path)
        
        self.export_label.pack(side='left')
        self.export_entry.pack(side='left', padx=5)
        self.browse_export_btn.pack(side='left')
        self.export_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky='w')

        # 专业拆分按钮组
        self.split_frame = ttk.Frame(self)
        # ClassPlans拆分按钮
        self.classplans_btn = ttk.Button(
            self.split_frame, 
            text="拆分ClassPlans",
            command=lambda: self.split_config(
                "ClassPlans",
                "classplans.json",
                '''{
    "Name": "",
    "TimeLayouts": {},
    "ClassPlans": 
（C）
    ,
    "Subjects": {}
}'''
            ),
            style='Accent.TButton'
        )
        self.classplans_btn.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        
        # 双按钮容器
        self.sub_split_frame = ttk.Frame(self.split_frame)
        # Subjects拆分按钮
        self.subjects_btn = ttk.Button(
            self.sub_split_frame,
            text="拆分Subjects",
            command=lambda: self.split_config(
                "Subjects",
                "subjects.json",
                '''{
    "Name": "",
    "TimeLayouts": {},
    "ClassPlans": {},
    "Subjects": 
（D）
    
}'''
            )
        )
        self.subjects_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        # TimeLayouts拆分按钮
        self.timelayouts_btn = ttk.Button(
            self.sub_split_frame,
            text="拆分TimeLayouts",
            command=lambda: self.split_config(
                "TimeLayouts",
                "timelayouts.json",
                '''{
    "Name": "",
    "TimeLayouts": 
（E）
    ,
    "ClassPlans": {},
    "Subjects": {}
}'''
            )
        )
        self.timelayouts_btn.pack(side='right', expand=True, fill='x', padx=5)
        
        self.sub_split_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')
        self.split_frame.grid(row=5, column=0, columnspan=4, pady=15, sticky='nsew')

        # 底部双按钮
        self.btn_frame = ttk.Frame(self)
        self.repo_btn = ttk.Button(self.btn_frame, text="仓库配置导出", command=self.export_repo_config)
        self.local_btn = ttk.Button(self.btn_frame, text="本地配置导出", command=self.export_local_config)
        
        self.repo_btn.pack(side='left', padx=20, ipadx=10)
        self.local_btn.pack(side='right', padx=20, ipadx=10)
        self.btn_frame.grid(row=6, column=0, columnspan=4, pady=10)

        # 配置样式
        self.style = ttk.Style()
        self.style.configure('Accent.TButton', font=('微软雅黑', 10, 'bold'))

    def handle_drop(self, event):
        """处理文件拖拽事件"""
        path = event.data.strip('{}')
        if path.lower().endswith('.json'):
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, path)

    def select_config_file(self):
        """选择配置文件"""
        path = filedialog.askopenfilename(filetypes=[("JSON文件", "*.json")])
        if path:
            self.config_entry.delete(0, tk.END)
            self.config_entry.insert(0, path)

    def update_config(self):
        """更新配置文件"""
        path = self.config_entry.get()
        if not os.path.exists(path):
            messagebox.showerror("错误", "配置文件不存在！")
        else:
            messagebox.showinfo("提示", "配置文件已更新")

    def select_export_path(self):
        """选择导出目录"""
        path = filedialog.askdirectory()
        if path:
            self.export_entry.delete(0, tk.END)
            self.export_entry.insert(0, path)
            os.makedirs(path, exist_ok=True)

    def split_config(self, field_name, output_file, template):
        """精确模板替换方法"""
        try:
            config_path = self.config_entry.get()
            export_dir = self.export_entry.get()
            
            if not all([config_path, export_dir]):
                raise ValueError("请先选择配置文件和导出目录")
                
            if not os.path.exists(config_path):
                raise FileNotFoundError("配置文件不存在")
                
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            target_data = config_data.get(field_name)
            if not target_data:
                raise KeyError(f"配置文件中缺少 {field_name} 字段")

            # 精确替换占位符
            placeholder_map = {
                "ClassPlans": "（C）",
                "Subjects": "（D）",
                "TimeLayouts": "（E）"
            }
            output_content = template.replace(
                placeholder_map[field_name],
                json.dumps(target_data, indent=4, ensure_ascii=False)
            )
            
            output_path = os.path.join(export_dir, output_file.lower())
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            messagebox.showinfo("操作成功", 
                f"{field_name}配置已成功导出至：\n{output_path}")
                
        except Exception as e:
            messagebox.showerror("操作失败", 
                f"错误详情：\n{str(e)}")

    def export_repo_config(self):
        """仓库配置导出逻辑"""
        user = self.entry_A.get()
        repo = self.entry_B.get()
        if not user or not repo:
            messagebox.showerror("错误", "请先填写GitHub用户名和仓库名")
            return
        messagebox.showinfo("提示", f"正在导出仓库配置：{user}/{repo}")

    def export_local_config(self):
        """本地配置导出逻辑"""
        messagebox.showinfo("提示", "正在导出本地配置")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()