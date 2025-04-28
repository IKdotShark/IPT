import tkinter as tk
from tkinter import ttk, messagebox


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0


class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.node_radius = 20
        self.horizontal_gap = 50
        self.vertical_gap = 80

        self.window = tk.Tk()
        self.window.title("Binary Search Tree Visualizer")

        self.canvas = tk.Canvas(self.window, width=800, height=600, bg='white')
        self.canvas.pack(expand=True, fill='both')

        control_frame = ttk.Frame(self.window)
        control_frame.pack(pady=10)

        self.entry = ttk.Entry(control_frame, width=10)
        self.entry.pack(side='left', padx=5)

        ttk.Button(control_frame, text="Add", command=self.add_node).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Delete", command=self.delete_node).pack(side='left', padx=5)

        self.tree_root = None
        self.update_tree()

    def calculate_positions(self, node, x_min, x_max, y):
        if node is None:
            return 0

        node.x = (x_min + x_max) // 2
        node.y = y

        self.calculate_positions(node.left, x_min, node.x, y + self.vertical_gap)
        self.calculate_positions(node.right, node.x, x_max, y + self.vertical_gap)

    def draw_node(self, node):
        if node:
            self.canvas.create_oval(
                node.x - self.node_radius,
                node.y - self.node_radius,
                node.x + self.node_radius,
                node.y + self.node_radius,
                fill='lightblue'
            )
            self.canvas.create_text(node.x, node.y, text=str(node.key))

            if node.left:
                self.canvas.create_line(
                    node.x, node.y + self.node_radius,
                    node.left.x, node.left.y - self.node_radius,
                    width=2
                )
                self.draw_node(node.left)

            if node.right:
                self.canvas.create_line(
                    node.x, node.y + self.node_radius,
                    node.right.x, node.right.y - self.node_radius,
                    width=2
                )
                self.draw_node(node.right)

    def update_tree(self):
        self.canvas.delete("all")
        if self.tree_root:
            self.calculate_positions(self.tree_root, 50, self.canvas.winfo_width() - 50, 50)
            self.draw_node(self.tree_root)

    def add_node(self):
        try:
            key = int(self.entry.get())
            self.tree_root = self.insert(self.tree_root, key)
            self.update_tree()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def delete_node(self):
        try:
            key = int(self.entry.get())
            self.tree_root = self.tree_delete(self.tree_root, key)
            self.update_tree()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    # Функции работы с деревом (аналогичные предыдущим реализациям)
    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def tree_delete(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self.tree_delete(root.left, key)
        elif key > root.key:
            root.right = self.tree_delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self.tree_delete(root.right, temp.key)

        return root

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    visualizer = TreeVisualizer(None)
    visualizer.run()