# s31139
#DNA sequence generator with FASTA output.


import random
import csv


def generate_sequence(length: int) -> str:
    return "".join(random.choices("ACGT", k=length))


def calculate_stats(sequence: str) -> dict:
    total = len(sequence)
    stats = {}
    for base in "ACGT":
        count = sequence.count(base)
        stats[base] = (count / total) * 100 if total > 0 else 0.0

    stats["GC"] = stats["G"] + stats["C"]
    return stats


def insert_name(sequence: str, name: str) -> str:
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name.lower() + sequence[pos:]

def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    header = f">{seq_id} {description}".strip()
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    return header + "\n" + "\n".join(lines)


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
