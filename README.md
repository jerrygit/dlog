<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# dlog, timeit, ddeco Python Utilities Manual

This manual explains installation, configuration, and usage of the `dlog`, `timeit`, and `ddeco` utilities for Python, with a focus on their unique debugging and logging features. It also provides sample outputs and highlights the key advantages of each utility.

---

## **Installation**

These utilities are implemented as regular Python functions and decorators. Only the `pandas` package is required for DataFrame/Series support.

```bash
pip install pandas
```

Copy the provided code into a Python module (e.g., `dlog_utils.py`) and import as needed.

---

## **Configuration**

Enable debug logging by setting the environment variable before running your script:

```python
import os
os.environ['DLOG_DEBUG'] = 'true'
```


---

## **Key Features**

### **dlog: Indentation Reflects Call Depth**

- **Automatic Indentation:**
The `dlog` function adjusts log message indentation based on the call stack depth. This means that as your code enters deeper function calls, the logs are indented further, visually representing the execution hierarchy[^1][^2].
- **Enhanced Traceability:**
This indentation makes it significantly easier to trace the flow of execution, especially in complex or nested code, as the structure of your logs mirrors the structure of your code[^1][^3][^2].


### **ddeco: Input and Output Logging**

- **Function Call Transparency:**
The `ddeco` decorator logs both the input arguments and the output value of any decorated function. This provides clear visibility into what data is entering and leaving your functions, making it a powerful tool for debugging and verifying logic[^1][^4].
- **Smart Formatting:**
Results are formatted according to their type (e.g., dicts, lists, pandas DataFrames), ensuring logs remain readable even for complex data structures[^1].

---

## **Usage Examples and Expected Output**

### **1. dlog Command Example**

**Code Example:**

```python
from dlog_utils import dlog

def bar(y):
    dlog(f"Inside bar: {y}")
    return y + 1

def foo(x):
    dlog(f"Start foo: {x}")
    result = bar(x * 2)
    dlog(f"End foo: {result}")
    return result

foo(10)
```

**Expected Output:**

```
....../your_script.py [None.__main__.foo:6]
....[^6]Start foo: 10
........../your_script.py [None.__main__.bar:3]
........[^3]Inside bar: 20
....[^8]End foo: 21
```

- Indentation increases as the call stack deepens, providing clear visual cues about the flow and nesting of function calls[^1][^2].

---

### **2. ddeco Decorator Example**

**Code Example:**

```python
from dlog_utils import ddeco

@ddeco
def add_and_multiply(a, b):
    return {'sum': a + b, 'product': a * b}

result = add_and_multiply(3, 4)
```

**Expected Output:**

```
..../your_script.py [None.__main__.add_and_multiply:4]
..[^4]함수 add_and_multiply 호출 - 입력 args: [3, 4], kwargs: {}
..[^6]함수 add_and_multiply 반환 - type: <class 'dict'>, 내용:
{
  sum: 7
  product: 12
}
```

- Both the input arguments and the formatted output are logged, making it easy to verify function behavior and debug issues[^1][^4].

---

### **3. ddeco with pandas DataFrame Example**

**Code Example:**

```python
import pandas as pd
from dlog_utils import ddeco

@ddeco
def process_df(df):
    return df.describe()

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
process_df(df)
```

**Expected Output:**

```
..../your_script.py [None.__main__.process_df:4]
..[^4]함수 process_df 호출 - 입력 args: [   A  B
0  1  4
1  2  5
2  3  6], kwargs: {}
..[^6]함수 process_df 반환 - type: <class 'pandas.core.frame.DataFrame'>, 내용:
DataFrame (shape: (2, 2)):
       A    B
count  3.0  3.0
mean   2.0  5.0
std    1.0  1.0
min    1.0  4.0
25%    1.5  4.5
50%    2.0  5.0
75%    2.5  5.5
max    3.0  6.0
```


---

### **4. timeit Decorator Example**

**Code Example:**

```python
from dlog_utils import timeit
import time

@timeit
def wait_and_return(x):
    time.sleep(1)
    return x

wait_and_return(42)
```

**Expected Output:**

```
wait_and_return 실행 시간: 1.0000초
```


---

## **Summary Table**

| Utility | Type | Purpose | Key Features |
| :-- | :-- | :-- | :-- |
| dlog | Function | Debug logging with context | Indentation by call depth, traceability |
| timeit | Decorator | Measure function execution time | Prints elapsed time |
| ddeco | Decorator | Log function calls and results | Logs inputs/outputs, smart formatting |


---

## **Best Practices**

- Use **dlog** to gain clear, hierarchical visibility of your code's execution flow—especially useful for debugging complex or deeply nested code[^1][^2].
- Use **ddeco** to automatically log and inspect function inputs and outputs, greatly simplifying debugging and validation of logic[^1][^4].
- Use **timeit** to profile performance-critical functions.

---

## **References**

- This manual is based on the provided Python source and best practices for debugging and logging in Python[^1][^4][^2].

---

<div style="text-align: center">⁂</div>

[^1]: paste.txt

[^2]: https://code.activestate.com/recipes/412603-stack-based-indentation-of-formatted-logging/

[^3]: https://github.com/karaposu/indented-logger

[^4]: https://topdlearning.com/5-key-benefits-of-using-python-decorators-for-optimized-coding-practices/

[^5]: https://stackoverflow.com/questions/5498907/show-log-context-level-by-indentation-or-prefix-length

[^6]: https://pypi.org/project/indented-logger/0.1.6/

[^7]: https://blog.codinghorror.com/the-problem-with-logging/

[^8]: https://www.datadoghq.com/blog/multiline-logging-guide/

[^9]: https://github.com/Delgan/loguru/issues/424

[^10]: https://www.xano.com/learn/Debugging-Function-Stacks-Debug-Log/

[^11]: https://www.sitepoint.com/javascript-decorators-what-they-are/

