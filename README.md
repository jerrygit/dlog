<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# dlog, timeit, and ddeco Python Utilities Manual

This manual provides a comprehensive guide to the usage and functionality of the `dlog`, `timeit`, and `ddeco` utilities as implemented in the provided code. These utilities are designed to enhance debugging, profiling, and logging in Python development, especially for functions and methods, with special handling for complex data types such as pandas DataFrames and Series[^1_1].

---

## **Overview**

- **dlog**: Debug logging function with contextual information (file, module, function, line, class).
- **timeit**: Decorator for measuring and reporting function execution time.
- **ddeco**: Decorator for detailed logging of function calls, inputs, and outputs, with smart formatting for various data types.

---

## **1. dlog Function**

### **Purpose**

`dlog` is a debug-friendly logging function that prints an object along with contextual information such as file path, module, function name, line number, and class name (if available). It is only active when the environment variable `DLOG_DEBUG` is set to `'true'`.

### **Usage**

```python
dlog(obj, **kwargs)
```

- **obj**: Any Python object to be logged.
- **kwargs**: Additional keyword arguments for the built-in `print` function (e.g., `sep`, `end`).


### **Features**

- **Conditional Logging**: Only logs if `DLOG_DEBUG` environment variable is `'true'`.
- **Contextual Header**: Logs the source file, class, module, function, and line number.
- **Indentation**: Indents logs based on call stack depth for better readability of nested calls.
- **Class Detection**: Attempts to display the class name if called within a method.
- **Header Suppression**: Avoids redundant headers for consecutive calls at the same indentation level.


### **Example**

```python
os.environ['DLOG_DEBUG'] = 'true'
dlog("Debug message")
```


---

## **2. timeit Decorator**

### **Purpose**

`timeit` is a decorator that measures and prints the execution time of the decorated function.

### **Usage**

```python
@timeit
def my_function(...):
    ...
```

- **No arguments**: Used directly as a decorator.


### **Features**

- **Execution Time Reporting**: Prints the function name and elapsed time in seconds after each call.


### **Example**

```python
@timeit
def compute():
    time.sleep(1)

compute()
# Output: compute 실행 시간: 1.0000초
```


---

## **3. ddeco Decorator**

### **Purpose**

`ddeco` is a decorator for detailed logging of function calls. It logs input arguments and return values, with smart formatting for common data types, including pandas DataFrames and Series.

### **Usage**

```python
@ddeco
def my_function(a, b):
    return a + b
```


### **Features**

- **Input Logging**: Logs function name, arguments, and keyword arguments (with length limitation for very long logs).
- **Output Logging**: Logs return type and value, with special formatting for:
    - **dict**: Pretty-printed key-value pairs.
    - **list/tuple/set**: Each item on a new line.
    - **str**: Multi-line strings are clearly delimited.
    - **pandas.DataFrame/Series**: Uses `.to_string()` for readability, summarizes large objects.
- **Length Limitation**: Truncates very long logs for readability.
- **Error Handling**: Catches and logs exceptions during logging without interrupting function execution.


### **Example**

```python
@ddeco
def add(a, b):
    return {'sum': a + b, 'product': a * b}

result = add(3, 4)
# Logs input arguments and formatted output
```


---

## **Implementation Notes**

- **Environment Variable**: Set `os.environ['DLOG_DEBUG'] = 'true'` to enable debug logging.
- **pandas Support**: The code imports pandas (`import pandas as pd`) for DataFrame and Series formatting.
- **Decorator Metadata**: Uses `functools.wraps` to preserve original function metadata.

---

## **Summary Table**

| Utility | Type | Purpose | Key Features |
| :-- | :-- | :-- | :-- |
| dlog | Function | Debug logging with context | File/module/function/line/class, indentation |
| timeit | Decorator | Measure function execution time | Prints elapsed time |
| ddeco | Decorator | Detailed logging of function calls/results | Smart formatting, pandas support, truncation |


---

## **Best Practices**

- Use `dlog` for ad-hoc debugging with rich context.
- Use `timeit` to profile performance hotspots.
- Use `ddeco` for comprehensive logging during development or troubleshooting, especially with complex data structures.

---

## **References**

- The code and documentation are based on the provided Python source[^1_1].
- For detailed class and method documentation, focus on input/output types and logging behavior[^1_2].

---

[^1_1]
[^1_2]

<div style="text-align: center">⁂</div>

[^1_1]: paste.txt

[^1_2]: programming.documentation

