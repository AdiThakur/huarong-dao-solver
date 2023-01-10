## Huarong Dao Solver

This `python` script uses `DFS` and `A*` to solve the [Huarong Dao](https://en.wikipedia.org/wiki/Klotski) puzzle. It can be invoked by running the following command:

```
python3 hrd.py  <input file>  <DFS output file>  <A* output file>
```

---

#### Input Format

`<input file>` is a plain text file that stores the initial puzzle configuration that you wish to solve. It contains `20` digits arranged in `5` rows and `4` digits per row, representing the initial configuration of the puzzle. The empty squares are denoted by `0`. The single pieces are denoted by `7`. The `2x2` piece is denoted by `1`. The five `1x2` pieces are denoted by one of `{2, 3, 4, 5, 6}`.

The most classical configuration can be represented in this format as this:

```
2113
2113
4665
4775
7007
```

---

#### Output Format

The two output files store the solutions found by `DFS` and `A*` respectively.

The first line indicates the cost of the solution, which in this case represents the number of states that the corresponding algorithm had to search through. Next, the file contains the sequence of states from the initial configuration to a goal state; each such state is followed by a newline.

The empty squares are denoted by `0`. The single pieces are denoted by `4`, and the `2x2` piece is denoted by `1`. The horizontal `1x2` pieces are denoted by `2`, and the vertical `1x2` pieces are denoted by `3`.