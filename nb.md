# Percentile


## Concept

$R = \text{Ceiling}\left(\frac{k}{100} \cdot N\right)$

- $R$: Rank
- $k$: Desired percentile
- $N$: Total number of points
- $Ceiling(x)$: The smallest integer greater or equal to $x$



```python
import math

from IPython.display import Markdown, display
```

The sample data



```python
data = [40, 5, 5, 20, 25, 25, 30, 45, 45, 50, 55]
data
```
<div class="result" markdown>
```linenums='0'
    [40, 5, 5, 20, 25, 25, 30, 45, 45, 50, 55]
```
</div>
Sort the data



```python
sorted_data = sorted(data)
sorted_data
```
<div class="result" markdown>
```linenums='0'
    [5, 5, 20, 25, 25, 30, 40, 45, 45, 50, 55]
```
</div>
Define the desired percentile



```python
N = len(sorted_data)
k = 75
```

Calculate the rank R



```python
rank_float = (k / 100) * N
R = math.ceil(rank_float)
R
```
<div class="result" markdown>
```linenums='0'
    9
```
</div>
Get the value at rank R (0-based index is R-1)



```python
for index, number in enumerate(sorted_data):
    print(f"{index:5d} | {index + 1:4d}th | {number:5d}")

percentile_value = sorted_data[int(R) - 1]

print("\nResult:")
print(f"{k}th Percentile (Value at Rank {R}): {percentile_value}")
```
<div class="result" markdown>
```linenums='0'
        0 |    1th |     5
    1 |    2th |     5
    2 |    3th |    20
    3 |    4th |    25
    4 |    5th |    25
    5 |    6th |    30
    6 |    7th |    40
    7 |    8th |    45
    8 |    9th |    45
    9 |   10th |    50
   10 |   11th |    55

Result:
75th Percentile (Value at Rank 9): 45
```
</div>
The result means that 75% of the entire distribution is _less_ than 45


## Quartile

Quartile means a quarter

- $1^{st}$: 25%
- $2^{nd}$: 50%
- $3^{rd}$: 75%

