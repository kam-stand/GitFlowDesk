# import tkinter as tk
# from tkinter import ttk, messagebox
# import requests

# class GitHubApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("GitFlowDesk")
#         self.geometry("800x600")

#         self.notebook = ttk.Notebook(self)
#         self.notebook.pack(fill='both', expand=True)

#         self.repo_tab = ttk.Frame(self.notebook)
#         self.issues_tab = ttk.Frame(self.notebook)
#         self.commits_tab = ttk.Frame(self.notebook)

#         self.notebook.add(self.repo_tab, text='Repositories')
#         self.notebook.add(self.issues_tab, text='Issues')
#         self.notebook.add(self.commits_tab, text='Commits')

#         # Repositories Tab with styled Listbox
#         self.repo_frame = tk.Frame(self.repo_tab, relief='ridge', borderwidth=2)
#         self.repo_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
#         self.repo_listbox = tk.Listbox(self.repo_frame)
#         self.repo_listbox.pack(side='left', fill='both', expand=True)
#         self.repo_listbox.bind('<<ListboxSelect>>', self.on_repo_select)
#         self.repo_scrollbar = tk.Scrollbar(self.repo_frame, command=self.repo_listbox.yview)
#         self.repo_listbox.config(yscrollcommand=self.repo_scrollbar.set)
#         self.repo_scrollbar.pack(side='right', fill='y')

#         # Issues Tab
#         self.issues_listbox = tk.Listbox(self.issues_tab)
#         self.issues_listbox.pack(side='left', fill='both', expand=True)
#         self.issues_listbox.bind('<<ListboxSelect>>', self.on_issue_select)
#         self.issues_scrollbar = tk.Scrollbar(self.issues_tab, command=self.issues_listbox.yview)
#         self.issues_listbox.config(yscrollcommand=self.issues_scrollbar.set)
#         self.issues_scrollbar.pack(side='right', fill='y')
#         self.issue_body_text = tk.Text(self.issues_tab, height=10)
#         self.issue_body_text.pack(side='bottom', fill='x')

#         # Commits Tab with Treeview for styling
#         self.commits_tree = ttk.Treeview(self.commits_tab, columns=('sha', 'message'), show='headings')
#         self.commits_tree.heading('sha', text='SHA')
#         self.commits_tree.heading('message', text='Commit Message')
#         self.commits_tree.column('sha', width=100, anchor='w')
#         self.commits_tree.column('message', width=600, anchor='w')
#         self.commits_tree.pack(side='left', fill='both', expand=True)
#         self.commits_scrollbar = tk.Scrollbar(self.commits_tab, command=self.commits_tree.yview)
#         self.commits_tree.config(yscrollcommand=self.commits_scrollbar.set)
#         self.commits_scrollbar.pack(side='right', fill='y')

#         # Username Entry
#         self.username_label = tk.Label(self.repo_tab, text="GitHub Username:")
#         self.username_label.pack(side='top', anchor='nw')
#         self.username_entry = tk.Entry(self.repo_tab)
#         self.username_entry.pack(side='top', anchor='nw')
#         self.load_button = tk.Button(self.repo_tab, text="Load Repositories", command=self.load_repositories)
#         self.load_button.pack(side='top', anchor='nw')

#         self.repos = []
#         self.selected_repo = None
#         self.issues = []

#     def load_repositories(self):
#         username = self.username_entry.get().strip()
#         if not username:
#             messagebox.showerror("Error", "Please enter a GitHub username.")
#             return
#         url = f"https://api.github.com/users/{username}/repos"
#         try:
#             resp = requests.get(url)
#             resp.raise_for_status()
#             self.repos = resp.json()
#             self.repo_listbox.delete(0, tk.END)
#             for repo in self.repos:
#                 self.repo_listbox.insert(tk.END, repo['name'])
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load repositories: {e}")

#     def on_repo_select(self, event):
#         selection = self.repo_listbox.curselection()
#         if not selection:
#             return
#         index = selection[0]
#         repo = self.repos[index]
#         self.selected_repo = repo
#         self.load_issues(repo)
#         self.load_commits(repo)

#     def load_issues(self, repo):
#         owner = repo['owner']['login']
#         repo_name = repo['name']
#         url = f"https://api.github.com/repos/{owner}/{repo_name}/issues"
#         try:
#             resp = requests.get(url)
#             resp.raise_for_status()
#             self.issues = resp.json()
#             self.issues_listbox.delete(0, tk.END)
#             for issue in self.issues:
#                 self.issues_listbox.insert(tk.END, issue['title'])
#             self.issue_body_text.delete('1.0', tk.END)
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load issues: {e}")

#     def on_issue_select(self, event):
#         selection = self.issues_listbox.curselection()
#         if not selection:
#             return
#         index = selection[0]
#         issue = self.issues[index]
#         body = issue.get('body', '')
#         self.issue_body_text.delete('1.0', tk.END)
#         self.issue_body_text.insert(tk.END, body)

#     def load_commits(self, repo):
#         owner = repo['owner']['login']
#         repo_name = repo['name']
#         url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
#         try:
#             resp = requests.get(url)
#             resp.raise_for_status()
#             commits = resp.json()
#             self.commits_tree.delete(*self.commits_tree.get_children())
#             for commit in commits:
#                 sha = commit['sha'][:7]
#                 message = commit['commit']['message']
#                 self.commits_tree.insert('', tk.END, values=(sha, message))
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load commits: {e}")

# if __name__ == "__main__":
#     app = GitHubApp()
#     app.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
import requests
import base64

class GitHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitFlowDesk")
        self.geometry("1000x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.repo_tab = ttk.Frame(self.notebook)
        self.issues_tab = ttk.Frame(self.notebook)
        self.commits_tab = ttk.Frame(self.notebook)
        self.content_tab = ttk.Frame(self.notebook)  # New Content tab

        self.notebook.add(self.repo_tab, text='Repositories')
        self.notebook.add(self.issues_tab, text='Issues')
        self.notebook.add(self.commits_tab, text='Commits')
        self.notebook.add(self.content_tab, text='Content')  # Add to notebook

        # Repositories Tab
        self.repo_frame = tk.Frame(self.repo_tab, relief='ridge', borderwidth=2)
        self.repo_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.repo_listbox = tk.Listbox(self.repo_frame)
        self.repo_listbox.pack(side='left', fill='both', expand=True)
        self.repo_listbox.bind('<<ListboxSelect>>', self.on_repo_select)
        self.repo_scrollbar = tk.Scrollbar(self.repo_frame, command=self.repo_listbox.yview)
        self.repo_listbox.config(yscrollcommand=self.repo_scrollbar.set)
        self.repo_scrollbar.pack(side='right', fill='y')


        # Issues Tab
        self.issues_listbox = tk.Listbox(self.issues_tab)
        self.issues_listbox.pack(side='left', fill='both', expand=True)
        self.issues_listbox.bind('<<ListboxSelect>>', self.on_issue_select)
        self.issues_scrollbar = tk.Scrollbar(self.issues_tab, command=self.issues_listbox.yview)
        self.issues_listbox.config(yscrollcommand=self.issues_scrollbar.set)
        self.issues_scrollbar.pack(side='right', fill='y')
        self.issue_body_text = tk.Text(self.issues_tab, height=10)
        self.issue_body_text.pack(side='bottom', fill='x')

        # Commits Tab
        self.commits_tree = ttk.Treeview(self.commits_tab, columns=('sha', 'message'), show='headings')
        self.commits_tree.heading('sha', text='SHA')
        self.commits_tree.heading('message', text='Commit Message')
        self.commits_tree.column('sha', width=100, anchor='w')
        self.commits_tree.column('message', width=600, anchor='w')
        self.commits_tree.pack(side='left', fill='both', expand=True)
        self.commits_scrollbar = tk.Scrollbar(self.commits_tab, command=self.commits_tree.yview)
        self.commits_tree.config(yscrollcommand=self.commits_scrollbar.set)
        self.commits_scrollbar.pack(side='right', fill='y')

        # Content Tab
        self.content_frame = tk.Frame(self.content_tab)
        self.content_frame.pack(fill='both', expand=True)

        # Treeview for repo content
        # Treeview for repo content
        self.content_tree = ttk.Treeview(self.content_frame)
        self.content_tree.pack(side='left', fill='both', expand=True)
        self.content_tree.bind("<<TreeviewSelect>>", self.on_content_select)
        self.content_tree.bind("<<TreeviewOpen>>", self.on_folder_open)
        # Scrollbar
        self.content_scrollbar = tk.Scrollbar(self.content_frame, command=self.content_tree.yview)
        self.content_tree.config(yscrollcommand=self.content_scrollbar.set)
        self.content_scrollbar.pack(side='left', fill='y')

        # File preview text box
        self.file_preview = tk.Text(self.content_frame, wrap='word')
        self.file_preview.pack(side='right', fill='both', expand=True)

        # Username Entry
        self.username_label = tk.Label(self.repo_tab, text="GitHub Username:")
        self.username_label.pack(side='top', anchor='nw')
        self.username_entry = tk.Entry(self.repo_tab)
        self.username_entry.pack(side='top', anchor='nw')
        self.load_button = tk.Button(self.repo_tab, text="Load Repositories", command=self.load_repositories)
        self.load_button.pack(side='top', anchor='nw')

        self.repos = []
        self.selected_repo = None
        self.issues = []

    def load_repositories(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a GitHub username.")
            return
        url = f"https://api.github.com/users/{username}/repos"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            self.repos = resp.json()
            self.repo_listbox.delete(0, tk.END)
            for repo in self.repos:
                self.repo_listbox.insert(tk.END, repo['name'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load repositories: {e}")

    def on_repo_select(self, event):
        selection = self.repo_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        repo = self.repos[index]
        self.selected_repo = repo
        self.load_issues(repo)
        self.load_commits(repo)
        self.load_repo_content(repo)

    def load_issues(self, repo):
        owner = repo['owner']['login']
        repo_name = repo['name']
        url = f"https://api.github.com/repos/{owner}/{repo_name}/issues"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            self.issues = resp.json()
            self.issues_listbox.delete(0, tk.END)
            for issue in self.issues:
                self.issues_listbox.insert(tk.END, issue['title'])
            self.issue_body_text.delete('1.0', tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load issues: {e}")

    def on_issue_select(self, event):
        selection = self.issues_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        issue = self.issues[index]
        body = issue.get('body', '')
        self.issue_body_text.delete('1.0', tk.END)
        self.issue_body_text.insert(tk.END, body)

    def load_commits(self, repo):
        owner = repo['owner']['login']
        repo_name = repo['name']
        url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            commits = resp.json()
            self.commits_tree.delete(*self.commits_tree.get_children())
            for commit in commits:
                sha = commit['sha'][:7]
                message = commit['commit']['message']
                self.commits_tree.insert('', tk.END, values=(sha, message))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load commits: {e}")

    def load_repo_content(self, repo):
        self.content_tree.delete(*self.content_tree.get_children())
        owner = repo['owner']['login']
        repo_name = repo['name']
        url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            contents = resp.json()
            for item in contents:
                node_id = self.content_tree.insert('', tk.END, text=item['name'], values=(item['type'], item['url']))
                if item['type'] == 'dir':
                    self.content_tree.insert(node_id, tk.END, text="Loading...")  # Placeholder for lazy loading
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load repository content: {e}")

    def on_content_select(self, event):
        selected = self.content_tree.selection()
        if not selected:
            return
        node = selected[0]
        item_values = self.content_tree.item(node, 'values')
        if len(item_values) < 2:
            return
        item_type, item_url = item_values
        if item_type == 'file':
            self.load_file_content(item_url)
    def load_directory_contents(self, parent_node, url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            contents = resp.json()
            for item in contents:
                node_id = self.content_tree.insert(parent_node, tk.END, text=item['name'], values=(item['type'], item['url']))
                if item['type'] == 'dir':
                    self.content_tree.insert(node_id, tk.END, text="Loading...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load directory contents: {e}")

    
    def on_folder_open(self, event):
        selected = self.content_tree.selection()
        if not selected:
            return
        node = selected[0]
        item_values = self.content_tree.item(node, 'values')
        if len(item_values) < 2:
            return

        item_type, item_url = item_values
        if item_type == 'dir':
            # Check if it's still the placeholder "Loading..."
            children = self.content_tree.get_children(node)
            if len(children) == 1 and self.content_tree.item(children[0], 'text') == "Loading...":
                self.content_tree.delete(children[0])  # Remove placeholder
                self.load_directory_contents(node, item_url)


    def load_file_content(self, url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            file_data = resp.json()
            content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
            self.file_preview.delete('1.0', tk.END)
            self.file_preview.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file content: {e}")

if __name__ == "__main__":
    app = GitHubApp()
    app.mainloop()
