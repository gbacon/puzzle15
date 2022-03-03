from z3 import *

HOLES = 15

Hole  = [BitVecVal(1 << i,    HOLES) for i in range(HOLES)]
Board = [BitVec(f'board_{i}', HOLES) for i in range(HOLES - 1)]

def used(b, h): return Board[b] & Hole[h] == Hole[h]
def empty(b, h): return Not(used(b, h))

def unchanged(p, q, h): return used(p, h) == used(q, h)
def injump(i, j, k, h): return h in [i, j, k]

def valid(p, q, i, j, k):
  '''
  For a peg in hole i to jump j and land in k,
  p’s i and j must have been used but its k empty, whereas
  q’s i and j must be empty but its k used. The rest of the
  pegs can have no change from p to q.
  '''
  return And(
    used(p, i), empty(q, i),
    used(p, j), empty(q, j),
    empty(p, k), used(q, k),
    *[unchanged(p, q, h) for h in range(HOLES) if not injump(i, j, k, h)])

'''
    0
   1 2
  3 4 5
 6 7 8 9
A B C D E
'''
NEIGHBORS = [
  [ 0,  1,  3], [0, 2,  5],
  [ 1,  3,  6], [1, 4,  8],
  [ 2,  4,  7], [2, 5,  9],
  [ 3,  4,  5], [3, 6, 10], [3, 7, 12],
  [ 4,  7, 11], [4, 8, 13],
  [ 5,  8, 12], [5, 9, 14],
  [ 6,  7,  8],
  [ 7,  8,  9],
  [10, 11, 12],
  [11, 12, 13],
  [12, 13, 14],
]

def legal_transition(p, q):
  return Or(
    [valid(p, q, *l)
      for n in NEIGHBORS
      for l in [n, reversed(n)]])

def main():
  s = Solver()
  for i in range(HOLES - 2):
    s.add(legal_transition(i, i+1))

  final_board = HOLES - 2
  h = HOLES - 1
  s.add(empty(0, h))
  s.add(used(final_board, h))

  if s.check() == sat:
    m = s.model()
    for i in range(HOLES - 1):
      show_board(m[Board[i]])
      print()
  else:
    print('Failed to solve')

def show_board(b):
  def binary_lsb_first(b):
    return f'{{:0{HOLES}b}}'.format(b.as_long())[::-1]

  s = binary_lsb_first(b)

  j = 0
  for i in range(1, 6):
    leftpad = ' ' * (5 - i)
    print(leftpad, ' '.join(s[j:j + i]), sep='')
    j = j + i

if __name__ == '__main__':
  main()