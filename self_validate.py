import time
import os

def main(input_dir: str, output_dir: str) -> None:
    for filename in os.listdir(input_dir):

        input_path = f"{input_dir}{os.sep}{filename}"
        dfs_output = f"{output_dir}{os.sep}{filename}_dfs.txt"
        astar_output = f"{output_dir}{os.sep}{filename}_astar.txt"

        print(f"Input file: {filename}")

        start_time = time.time()
        os.system(f"python hrd.py {input_path} {dfs_output} {astar_output}")
        duration = time.time() - start_time

        print(f"\tFinished in {duration} seconds\n")

if __name__ == '__main__':
    main("test_inputs", "test_outputs")
