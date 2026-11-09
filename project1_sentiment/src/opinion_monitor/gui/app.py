"""Tkinter GUI; network work runs off the UI thread. Calls only opinion_monitor.pipeline."""

import queue
import sys
import threading
import tkinter as tk
import traceback
from tkinter import ttk

from opinion_monitor import pipeline
from opinion_monitor.data_sources.base import SourceError
from opinion_monitor.model.sentiment_model import ModelNotFoundError

SNIPPET_LEN = 110
GREEN = "#1b7f2a"
RED = "#b3261e"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

COLUMNS = {
    "sentiment": ("Sentiment", 95, "center"),
    "confidence": ("Confidence", 90, "center"),
    "rating": ("Source rating", 100, "center"),
    "text": ("Review", 560, "w"),
}
SORT_KEYS = {
    "sentiment": lambda it: it.label,
    "confidence": lambda it: it.confidence,
    "rating": lambda it: -1 if it.review.rating is None else it.review.rating,
}


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Opinion Monitor - movie review sentiment")
        self.geometry("980x640")
        self.minsize(760, 480)
        self._queue: queue.Queue = queue.Queue()
        self._result: pipeline.AnalysisResult | None = None
        self._sort_column: str | None = None
        self._sort_reverse = False
        self._setup_style()
        self._build_widgets()

    # --- layout ---------------------------------------------------------
    def _setup_style(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        self.option_add("*Font", FONT)
        style.configure(".", font=FONT)
        style.configure("Treeview", rowheight=26, font=FONT)
        style.configure("Treeview.Heading", font=FONT_BOLD, padding=4)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Summary.TLabel", font=FONT_BOLD)
        style.configure("Status.TLabel", relief="sunken", padding=4)
        style.configure("Share.Horizontal.TProgressbar", troughcolor=RED, background=GREEN, thickness=14)

    def _build_widgets(self) -> None:
        # Status bar is packed first so it always keeps its space and errors stay visible.
        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self._status_var, style="Status.TLabel", anchor="w").pack(
            fill="x", side="bottom"
        )

        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Movie review sentiment", style="Title.TLabel").pack(anchor="w")

        search = ttk.Frame(root)
        search.pack(fill="x", pady=(8, 4))
        ttk.Label(search, text="Movie title:").pack(side="left")
        self._title_var = tk.StringVar()
        entry = ttk.Entry(search, textvariable=self._title_var, width=44)
        entry.pack(side="left", padx=8)
        entry.bind("<Return>", lambda _e: self._on_analyze())
        entry.focus()
        self._button = ttk.Button(search, text="Fetch and analyze", command=self._on_analyze)
        self._button.pack(side="left")
        self._busy = ttk.Progressbar(search, mode="indeterminate", length=120)

        summary = ttk.Frame(root)
        summary.pack(fill="x", pady=(8, 6))
        self._summary_var = tk.StringVar(value="No data yet. Enter a movie title and press Enter.")
        self._summary_label = ttk.Label(summary, textvariable=self._summary_var, style="Summary.TLabel")
        self._summary_label.pack(anchor="w")
        self._share_bar = ttk.Progressbar(
            summary, style="Share.Horizontal.TProgressbar", maximum=100, value=0
        )
        self._share_bar.pack(fill="x", pady=(4, 0))
        ttk.Label(summary, text="green = positive, red = negative", foreground="#666").pack(anchor="w")

        panes = ttk.PanedWindow(root, orient="vertical")
        panes.pack(fill="both", expand=True, pady=(6, 6))

        table_frame = ttk.Frame(panes)
        self._tree = ttk.Treeview(
            table_frame, columns=tuple(COLUMNS), show="headings", selectmode="browse"
        )
        for column, (heading, width, anchor) in COLUMNS.items():
            command = (lambda c=column: self._sort_by(c)) if column in SORT_KEYS else ""
            self._tree.heading(column, text=heading, command=command)
            self._tree.column(column, width=width, anchor=anchor, stretch=(column == "text"))
        self._tree.tag_configure("positive", foreground=GREEN)
        self._tree.tag_configure("negative", foreground=RED)
        self._tree.tag_configure("odd", background="#f4f6f8")
        self._tree.bind("<<TreeviewSelect>>", self._on_select)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._tree.pack(side="left", fill="both", expand=True)
        panes.add(table_frame, weight=3)

        detail_frame = ttk.Frame(panes)
        self._detail = tk.Text(
            detail_frame, height=8, wrap="word", state="disabled", font=FONT,
            padx=8, pady=6, relief="solid", borderwidth=1,
        )
        self._detail.tag_configure("meta", foreground="#555", font=("Segoe UI", 9, "italic"))
        detail_scroll = ttk.Scrollbar(detail_frame, orient="vertical", command=self._detail.yview)
        self._detail.configure(yscrollcommand=detail_scroll.set)
        detail_scroll.pack(side="right", fill="y")
        self._detail.pack(side="left", fill="both", expand=True)
        panes.add(detail_frame, weight=2)

    # --- actions --------------------------------------------------------
    def _on_analyze(self) -> None:
        query = self._title_var.get().strip()
        if not query:
            self._status_var.set("Enter a movie title.")
            return
        self._button.state(["disabled"])
        self._busy.pack(side="left", padx=10)
        self._busy.start(12)
        self._status_var.set(f"Fetching reviews for '{query}'...")
        threading.Thread(target=self._worker, args=(query,), daemon=True).start()
        self.after(100, self._poll_queue)

    def _worker(self, query: str) -> None:
        try:
            result = pipeline.analyze(query)
            for item in result.items:
                item.display_text  # warm the cache off the UI thread
            self._queue.put(("ok", result))
        except (SourceError, ModelNotFoundError) as exc:
            print(f"[opinion_monitor] {type(exc).__name__}: {exc}", file=sys.stderr)
            self._queue.put(("error", str(exc)))
        except Exception as exc:
            traceback.print_exc()
            self._queue.put(("error", f"Unexpected error ({type(exc).__name__}): {exc}"))

    def _poll_queue(self) -> None:
        try:
            kind, payload = self._queue.get_nowait()
        except queue.Empty:
            self.after(100, self._poll_queue)
            return
        self._busy.stop()
        self._busy.pack_forget()
        self._button.state(["!disabled"])
        try:
            if kind == "ok":
                self._show_result(payload)
            else:
                self._show_error(payload)
        except Exception as exc:
            traceback.print_exc()
            self._show_error(f"Could not display results ({type(exc).__name__}): {exc}")

    def _show_error(self, message: str) -> None:
        self._result = None
        self._tree.delete(*self._tree.get_children())
        self._share_bar["value"] = 0
        self._summary_label.configure(foreground=RED)
        self._summary_var.set(f"Could not analyze: {message}")
        self._set_detail("")
        self._status_var.set(f"Error: {message}")

    # --- rendering ------------------------------------------------------
    def _show_result(self, result: pipeline.AnalysisResult) -> None:
        self._result = result
        self._summary_label.configure(foreground="")
        self._sort_column, self._sort_reverse = None, False
        self._populate(range(len(result.items)))
        self._update_headings()

        total = len(result.items)
        self._summary_var.set(
            f"{result.subject}: {total} reviews  |  "
            f"positive {result.positive_count} ({result.positive_share:.0%})  |  "
            f"negative {result.negative_count} ({1 - result.positive_share:.0%})"
        )
        self._share_bar["value"] = result.positive_share * 100
        self._set_detail("Select a review above to read it in full.")
        self._status_var.set(f"Done. Analyzed {total} reviews from TMDB. Click a column heading to sort.")

    def _populate(self, order) -> None:
        assert self._result is not None
        self._tree.delete(*self._tree.get_children())
        for row, index in enumerate(order):
            item = self._result.items[index]
            snippet = " ".join(item.display_text.split())
            if len(snippet) > SNIPPET_LEN:
                snippet = snippet[:SNIPPET_LEN].rstrip() + "..."
            rating = "-" if item.review.rating is None else f"{item.review.rating:g}"
            self._tree.insert(
                "",
                "end",
                iid=str(index),
                values=(item.label.capitalize(), f"{item.confidence:.0%}", rating, snippet),
                tags=(item.label, "odd" if row % 2 else "even"),
            )

    def _sort_by(self, column: str) -> None:
        if self._result is None:
            return
        self._sort_reverse = (not self._sort_reverse) if column == self._sort_column else (column != "sentiment")
        self._sort_column = column
        items = self._result.items
        order = sorted(range(len(items)), key=lambda i: SORT_KEYS[column](items[i]), reverse=self._sort_reverse)
        self._populate(order)
        self._update_headings()

    def _update_headings(self) -> None:
        for column, (heading, _w, _a) in COLUMNS.items():
            arrow = ""
            if column == self._sort_column:
                arrow = "  ▼" if self._sort_reverse else "  ▲"
            self._tree.heading(column, text=heading + arrow)

    def _on_select(self, _event) -> None:
        selection = self._tree.selection()
        if not selection or self._result is None:
            return
        item = self._result.items[int(selection[0])]
        rating = f", source rating {item.review.rating:g}" if item.review.rating is not None else ""
        meta = (
            f"{item.review.author or 'anonymous'}{rating}  |  "
            f"model: {item.label} ({item.confidence:.0%})\n\n"
        )
        self._set_detail(item.display_text, meta=meta)

    def _set_detail(self, text: str, meta: str = "") -> None:
        self._detail.configure(state="normal")
        self._detail.delete("1.0", "end")
        if meta:
            self._detail.insert("end", meta, "meta")
        self._detail.insert("end", text)
        self._detail.configure(state="disabled")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
