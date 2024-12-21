from tkinter import Tk, filedialog, Label, Button, Text, END
from collections import defaultdict

def read_fragments(file_path):
    with open(file_path, 'r') as file:
        fragments = file.read().splitlines()
    return fragments

def build_graph(fragments):
    graph = defaultdict(list)
    for frag in fragments:
        suffix = frag[-2:]  # останні 2 цифри
        for other in fragments:
            if frag != other and other.startswith(suffix):
                graph[frag].append(other)
    return graph

def find_longest_path(graph, fragments):
    longest_path = []

    for start in fragments:
        visited = set()
        queue = [(start, [start])]

        while queue:
            current, path = queue.pop(0)
            visited.add(current)

            # Перевіряємо, чи є можливість додати фрагмент до шляху
            for neighbor in graph[current]:
                if neighbor not in visited:  # Перевірка на те, чи не був фрагмент вже в списку
                    queue.append((neighbor, path + [neighbor]))

            # Оновлюємо найдовший шлях
            if len(path) > len(longest_path):
                longest_path = path

    return longest_path

def assemble_sequence(path):
    if not path:
        return "", ""

    sequence = path[0]
    fragment_sequence = [path[0]]
    for frag in path[1:]:
        fragment_sequence.append(frag)
        sequence += frag[2:]  # Додаємо до послідовності лише останні цифри кожного фрагмента

    return "".join(fragment_sequence), sequence  # Формуємо результат без "&"

def process_file(file_path):
    fragments = read_fragments(file_path)
    graph = build_graph(fragments)
    longest_path = find_longest_path(graph, fragments)
    fragment_sequence, result_sequence = assemble_sequence(longest_path)
    sequence_length = len(fragment_sequence)  # Довжина послідовності (загальна кількість символів)
    return fragment_sequence, result_sequence, sequence_length

def open_file():
    file_path = filedialog.askopenfilename(title="Select the source file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        fragment_sequence, result, sequence_length = process_file(file_path)
        result_text.delete(1.0, END)
        result_text.insert(END,
                           f"Відповідь: {fragment_sequence}\n\nДовжина послідовності: {sequence_length}")

# Create GUI
root = Tk()
root.title("Puzzle Solver")
root.geometry("600x400")

Label(root, text="Puzzle Solver", font=("Arial", 16)).pack(pady=10)
Button(root, text="Load File", command=open_file, font=("Arial", 12)).pack(pady=10)

result_text = Text(root, wrap="word", font=("Arial", 12), height=15)
result_text.pack(padx=10, pady=10, fill="both", expand=True)

# Make the Text widget editable and allow copy-paste
result_text.config(state="normal")  # Ensure the Text widget is in normal state (editable)

# Allow user to copy text from the Text widget
result_text.config(state="normal")  # Confirm that the Text widget is in normal state and can be copied

root.mainloop()






