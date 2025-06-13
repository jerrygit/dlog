import os
import inspect
import time
from functools import wraps
import pandas as pd
# Set environment variable for debug mode (optional)
os.environ['DLOG_DEBUG'] = 'true'


def dlog(obj, **kwargs):
    """
    Debug-friendly dlog function.
    Prints the object with file name, module name, and line number if dlog_MODE is enabled.
    Avoids printing the header if the indentation level is the same as the previous call.

    Parameters:
        obj: The object to be pretty-printed.
        **kwargs: Additional keyword arguments for print (e.g., color).
    """
    # Check if dlog_MODE is enabled
    dlog_MODE = os.getenv('DLOG_DEBUG', 'false').lower() == 'true'
    if not dlog_MODE:
        return  # Exit early if not in debug mode

    # Get caller information
    frame = inspect.currentframe().f_back

    module_name = frame.f_globals["__name__"]
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    
    module_path = os.path.abspath(frame.f_code.co_filename)

    # Calculate the call depth and current indent
    current_call_depth = len(inspect.stack())
    last_call_depth = getattr(dlog, 'last_call_depth', 0)

    current_indent = ".." * (current_call_depth)
    # current_indent = ".." * (last_call_depth - current_call_depth)

    # Get class name directly from the object if available
    class_name = None
    if 'self' in frame.f_locals and hasattr(frame.f_locals['self'], '__class__'):
        try:
            class_name = frame.f_locals['self'].__class__.__name__
        except AttributeError as e:
            print(f"{current_indent}[dlogWarning] Could not get class name directly from object: {e}")

    # If direct method fails, try inspect.stack() as a fallback
    if not class_name:
        for stack_frame in inspect.stack():
            if stack_frame[0].f_locals:
                try:
                    class_name = stack_frame[0].f_locals['__class__'].__name__
                    break  # Stop after finding the first class name
                except (KeyError, AttributeError):
                    pass

    # if not class_name:
    #     print(f"{current_indent}[dlogWarning] Could not determine class name.")

    # Get the last indent level stored on the function object itself
    last_indent = getattr(dlog, 'last_indent', None)

    # Check if the indent level has changed since the last call
    print_header = (current_indent != last_indent)

    if print_header:
        # Print the header line
        print(f"{current_indent}{module_path} [{class_name}.{module_name}.{function_name}:{line_number}]")
        # Update the last known indent level on the function object
        dlog.last_indent = current_indent
        dlog.last_call_depth = current_call_depth

    # Always print the actual object/message, indented correctly
    print(f"{current_indent}{[line_number]}{obj}", **kwargs)

dlog.last_indent = None
dlog.last_call_depth = 0



def timeit(func):
    """함수 실행 시간을 측정하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"{func.__name__} 실행 시간: {elapsed:.4f}초")
        return result
    return wrapper

def ddeco(func):
    @wraps(func)  # Use wraps to preserve function metadata
    def wrapper(*args, **kwargs):
        # 함수 호출 정보 로깅
        # args와 kwargs도 내용이 길 수 있으므로, 필요하다면 유사한 방식으로 포맷팅할 수 있습니다.
        # 여기서는 간단하게 표현합니다.
        try:
            # 객체의 __str__ 또는 __repr__이 매우 길 수 있으므로,
            # 로깅 길이를 제한하거나 주요 정보만 추출하는 것이 좋을 수 있습니다.
            args_repr = ", ".join(repr(arg) for arg in args)
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            # 너무 긴 로그 방지를 위해 길이 제한 (예시)
            log_args = (args_repr[:200] + '...') if len(args_repr) > 200 else args_repr
            log_kwargs = (kwargs_repr[:200] + '...') if len(kwargs_repr) > 200 else kwargs_repr

            dlog(f"함수 {func.__name__} 호출 - 입력 args: [{log_args}], kwargs: {{{log_kwargs}}}")
        except Exception as e:
            dlog(f"함수 {func.__name__} 호출 로깅 중 에러 (입력): {e}")


        result = func(*args, **kwargs)

        # 함수 반환 값 로깅 (타입 및 내용)
        result_type_str = str(type(result)) # repr(type(result))도 가능

        try:
            # 기본적으로 result 자체를 문자열로 변환하여 로그
            result_log_str = str(result)

            # result의 타입에 따라 또는 길이에 따라 포맷팅 결정
            # 1. 길이 확인이 가능한 타입인지 먼저 체크 (AttributeError 방지)
            has_length = hasattr(result, '__len__')

            if has_length and len(result) > 1:
                if isinstance(result, dict):
                    # 딕셔너리: 각 키-값 쌍을 줄바꿈하여 표시
                    items_str = "\n".join([f"  {k}: {v}" for k, v in result.items()])
                    result_log_str = f"{{\n{items_str}\n}}"
                elif isinstance(result, (list, tuple, set)):
                    # 리스트, 튜플, 셋: 각 항목을 줄바꿈하여 표시
                    items_str = ",\n".join([f"  {repr(item)}" for item in result]) # repr로 각 항목 표현
                    if isinstance(result, list):
                        result_log_str = f"[\n{items_str}\n]"
                    elif isinstance(result, tuple):
                        result_log_str = f"(\n{items_str}\n)"
                    else: # set
                        result_log_str = f"{{\n{items_str}\n}}"
                elif isinstance(result, str) and '\n' in result:
                    # 여러 줄 문자열: 그대로 유지하되, 앞뒤로 구분 명확히
                    result_log_str = f"'''\n{result}\n'''"
                elif isinstance(result, pd.DataFrame):
                    # Pandas DataFrame: to_string() 사용하여 보기 좋게 변환
                    # 너무 큰 DataFrame은 일부만 표시하거나, shape 정보만 표시할 수도 있음
                    if result.empty:
                        result_log_str = "Empty DataFrame"
                    else:
                        try:
                            # DataFrame이 너무 크면 to_string()이 매우 길어질 수 있음
                            # 예: 처음 5줄, 마지막 5줄만 표시하거나, shape 정보와 함께 요약
                            if len(result) > 10: # 예시: 10줄 초과 시 요약
                                result_log_str = f"DataFrame (shape: {result.shape}):\n{result.head().to_string()}\n...\n{result.tail().to_string()}"
                            else:
                                result_log_str = f"DataFrame (shape: {result.shape}):\n{result.to_string()}"
                        except Exception as e_pd_df:
                            result_log_str = f"Pandas DataFrame (Error converting to string: {e_pd_df})"

                elif isinstance(result, pd.Series):
                    # Pandas Series: to_string() 사용
                    if result.empty:
                        result_log_str = "Empty Series"
                    else:
                        try:
                            if len(result) > 10: # 예시: 10개 초과 시 요약
                                result_log_str = f"Series (name: {result.name}, shape: {result.shape}):\n{result.head().to_string()}\n...\n{result.tail().to_string()}"
                            else:
                                result_log_str = f"Series (name: {result.name}, shape: {result.shape}):\n{result.to_string()}"
                        except Exception as e_pd_s:
                            result_log_str = f"Pandas Series (Error converting to string: {e_pd_s})"
                # else:
                #   길이가 1 초과인 다른 타입들은 기본 str(result) 사용
                #   필요에 따라 추가적인 타입 핸들링 가능

            elif not has_length:
                # 길이가 없는 객체 (예: int, float, bool, 사용자 정의 객체 등)
                # 또는 길이가 1이하인 경우
                result_log_str = repr(result) # repr()을 사용하여 타입 정보를 좀 더 명확히 하거나, str() 그대로 사용

            # 너무 긴 로그는 잘라서 표시 (최종 방어선)
            if len(result_log_str) > 1000: # 예시: 1000자 초과 시
                result_log_str = result_log_str[:1000] + "\n... (truncated)"


            dlog(f"함수 {func.__name__} 반환 - type: {result_type_str}, 내용:\n{result_log_str}")

        except Exception as e:
            dlog(f"함수 {func.__name__} 반환 로깅 중 에러 (결과): {e}\n원본 결과 (에러 시): {repr(result)}")


        return result
    return wrapper

# def ddeco_(func):
#     @wraps(func)  # Use wraps to preserve function metadata
#     def wrapper(*args, **kwargs):
#         # Use the modified dlog for logging inputs/outputs if needed
#         dlog(f"함수 {func.__name__} 호출 - 입력 args: \n{args}, kwargs: {kwargs}")

#         result = func(*args, **kwargs)

#         dlog(f"함수 {func.__name__} 반환: type :{type(result)} \n{result}")
#         return result
#     return wrapper
# Initialize the 'last_indent' attribute on the function object.
# This ensures the first call will always print the header.
# Set it to None or any value that a valid indent string won't be.
