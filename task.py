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

def search_motif(sequence: str, motif: str):
    positions = []
    idx = sequence.find(motif)
    while idx != -1:
        positions.append(idx + 1)
        idx = sequence.find(motif, idx + 1)
    print(f"Motif '{motif}' positions: {positions}")


def get_reverse_complement(sequence: str) -> str:
    mapping = str.maketrans("ACGT", "TGCA")
    return sequence.translate(mapping)[::-1]


def transcribe_to_rna(sequence: str) -> str:
    return sequence.replace("T", "U")


def sliding_window_gc(sequence: str, window_size: int, filename: str):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start_position", "gc_content"])
        for i in range(len(sequence) - window_size + 1):
            window = sequence[i:i + window_size]
            gc = (window.count("G") + window.count("C")) / window_size * 100
            writer.writerow([i + 1, round(gc, 2)])

def main():
    length = validate_positive_int("Enter sequence length: ")

    while True:
        seq_id = input("Enter sequence ID: ")
        if " " not in seq_id and seq_id:
            break
        print("Error: ID cannot contain whitespace.")

    description = input("Enter a description of the sequence: ")
    user_name = input("Enter your name: ")

    bio_seq = generate_sequence(length)

    stats = calculate_stats(bio_seq)

    display_seq = insert_name(bio_seq, user_name)

    fasta_content = format_fasta(seq_id, description, display_seq)
    with open(f"{seq_id}.fasta", "w") as f:
        f.write(fasta_content)
    print(f"Sequence saved to file: {seq_id}.fasta")

    motif = input("Enter DNA motif to search for: ")
    search_motif(bio_seq, motif)

    rev_comp = get_reverse_complement(bio_seq)
    rna_seq = transcribe_to_rna(bio_seq)

    with open(f"{seq_id}.fasta", "a") as f:
        f.write("\n" + format_fasta(f"{seq_id}_RevComp", "Reverse Complement", rev_comp))
        f.write("\n" + format_fasta(f"{seq_id}_mRNA", "mRNA Sequence", rna_seq))

    sliding_window_gc(bio_seq, 10, f"{seq_id}_gc_window.csv")  # Feature 7

    print(f"\nSequence statistics (n={length})")
    for base in "ACGT":
        print(f"{base}: {stats[base]:.2f}%")
    print(f"GC-content: {stats['GC']:.2f}%")


if __name__ == "__main__":
    main()

