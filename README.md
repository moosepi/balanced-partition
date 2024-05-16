# balanced-partition

Function to generate balanced partition(s) of a list of numbers (optionally associated with strings). Currently implemented algorithm is designed as a generalised version of [Merten's](https://arxiv.org/pdf/cs/9903011) complete anytime extension of the BLDM algorithm, with reference to the original [CKK](https://www.sciencedirect.com/science/article/pii/S0004370298000861) algorithm.

`NGMbalance.py` is a sample demonstrating how the algo may be used to e.g. balance teams for a game (using `ranks.txt` and `players.txt` as input).