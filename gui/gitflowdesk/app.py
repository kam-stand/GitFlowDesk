import tkinter as tk
from tkinter import ttk
import requests

USER = "kam-stand"
REPOS_URL = f"https://api.github.com/users/{USER}/repos"
ISSUES_URL_TEMPLATE = f"https://api.github.com/repos/{USER}/{{repo_name}}/issues"
COMMITS_URL_TEMPLATE = f"https://api.github.com/repos/{USER}/{{repo_name}}/commits"


class GitHubViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitFlow 🌊 - GitHub Viewer")
        self.geometry("1000x600")
        self.configure(bg="#e9ecef")

        # --- LEFT PANEL: Repository Buttons ---
        tools_frame = tk.Frame(self, width=250, bg="#f8f9fa")
        tools_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(tools_frame, text="Repositories", bg="#f8f9fa", font=("Arial", 14, "bold")).pack(pady=(10, 15))

        # Scrollable area for repo buttons
        repo_canvas = tk.Canvas(tools_frame, bg="#f8f9fa", highlightthickness=0)
        repo_scrollbar = ttk.Scrollbar(tools_frame, orient="vertical", command=repo_canvas.yview)
        self.repo_frame = tk.Frame(repo_canvas, bg="#f8f9fa")

        self.repo_frame.bind(
            "<Configure>", lambda e: repo_canvas.configure(scrollregion=repo_canvas.bbox("all"))
        )
        repo_canvas.create_window((0, 0), window=self.repo_frame, anchor="nw")
        repo_canvas.configure(yscrollcommand=repo_scrollbar.set)

        repo_canvas.pack(side="left", fill="both", expand=True)
        repo_scrollbar.pack(side="right", fill="y")

        # --- RIGHT PANEL: Issues & Commits ---
        self.view_frame = tk.Frame(self, bg="#dee2e6")
        self.view_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(
            self.view_frame,
            text="Select a repository",
            bg="#adb5bd",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
        ).pack(fill=tk.X)

        # Container for two scrollable sections
        content_frame = tk.Frame(self.view_frame, bg="#dee2e6")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Issues Section
        issues_container = tk.Frame(content_frame, bg="#dee2e6")
        issues_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(issues_container, text="Issues", bg="#dee2e6", font=("Arial", 12, "bold")).pack()

        self.issues_canvas = tk.Canvas(issues_container, bg="#dee2e6", highlightthickness=0)
        issues_scrollbar = ttk.Scrollbar(issues_container, orient="vertical", command=self.issues_canvas.yview)
        self.issues_frame = tk.Frame(self.issues_canvas, bg="#dee2e6")

        self.issues_frame.bind(
            "<Configure>", lambda e: self.issues_canvas.configure(scrollregion=self.issues_canvas.bbox("all"))
        )
        self.issues_canvas.create_window((0, 0), window=self.issues_frame, anchor="nw")
        self.issues_canvas.configure(yscrollcommand=issues_scrollbar.set)

        self.issues_canvas.pack(side="left", fill="both", expand=True)
        issues_scrollbar.pack(side="right", fill="y")

        # Commits Section
        commits_container = tk.Frame(content_frame, bg="#dee2e6")
        commits_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(commits_container, text="Commits", bg="#dee2e6", font=("Arial", 12, "bold")).pack()

        self.commits_canvas = tk.Canvas(commits_container, bg="#dee2e6", highlightthickness=0)
        commits_scrollbar = ttk.Scrollbar(commits_container, orient="vertical", command=self.commits_canvas.yview)
        self.commits_frame = tk.Frame(self.commits_canvas, bg="#dee2e6")

        self.commits_frame.bind(
            "<Configure>", lambda e: self.commits_canvas.configure(scrollregion=self.commits_canvas.bbox("all"))
        )
        self.commits_canvas.create_window((0, 0), window=self.commits_frame, anchor="nw")
        self.commits_canvas.configure(yscrollcommand=commits_scrollbar.set)

        self.commits_canvas.pack(side="left", fill="both", expand=True)
        commits_scrollbar.pack(side="right", fill="y")

        # Load Repositories on start
        self.load_repositories()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def load_repositories(self):
        """Fetch GitHub repos and create buttons."""
        try:
            response = requests.get(REPOS_URL)
            if response.status_code == 200:
                repos = response.json()
                for repo in repos:
                    name = repo.get("name", "Unknown")
                    btn = tk.Button(
                        self.repo_frame,
                        text=name,
                        relief="ridge",
                        width=25,
                        command=lambda n=name: self.show_repo_details(n),
                        font=("Arial", 10),
                        bg="#ffffff",
                        activebackground="#dbe4ff"
                    )
                    btn.pack(padx=5, pady=3, fill="x")
            else:
                tk.Label(self.repo_frame, text=f"Error: {response.status_code}", bg="#f8f9fa").pack()
        except Exception as e:
            tk.Label(self.repo_frame, text=f"Exception: {e}", bg="#f8f9fa").pack()

    def show_repo_details(self, repo_name):
        """Fetch and display issues and commits with scrollable layout."""
        self.clear_frame(self.issues_frame)
        self.clear_frame(self.commits_frame)

        # Fetch Issues
        issues_url = ISSUES_URL_TEMPLATE.format(repo_name=repo_name)
        issues = self.fetch_data(issues_url)
        if issues:
            for issue in issues:
                title = issue.get("title", "No title")
                issue_box = tk.Frame(self.issues_frame, bg="white", relief="solid", borderwidth=1)
                tk.Label(issue_box, text=title, bg="white", wraplength=300, justify="left").pack(padx=5, pady=5)
                issue_box.pack(padx=5, pady=5, fill="x")
        else:
            tk.Label(self.issues_frame, text="No issues found", bg="#dee2e6").pack(pady=10)

        # Fetch Commits
        commits_url = COMMITS_URL_TEMPLATE.format(repo_name=repo_name)
        commits = self.fetch_data(commits_url)
        if commits:
            for commit in commits:
                sha = commit.get("sha", "")[:8]  # Short SHA
                commit_box = tk.Frame(self.commits_frame, bg="white", relief="solid", borderwidth=1)
                tk.Label(commit_box, text=sha, bg="white", font=("Courier", 10)).pack(padx=5, pady=5)
                commit_box.pack(padx=5, pady=5, fill="x")
        else:
            tk.Label(self.commits_frame, text="No commits found", bg="#dee2e6").pack(pady=10)

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return []


if __name__ == "__main__":
    app = GitHubViewer()
    app.mainloop()
