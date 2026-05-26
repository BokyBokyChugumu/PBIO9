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
