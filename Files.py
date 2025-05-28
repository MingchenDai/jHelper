import configparser
import pandas
import inspect


def exception_throw_out(depth:'int'=1) -> str:
    frame_info = inspect.stack()[depth]
    function_name = frame_info.function
    file_name = frame_info.filename
    exception_string = "jHelper failed at function " + function_name + " of file " + file_name
    return exception_string


def read_config(section, item):
    configParser = configparser.ConfigParser()
    configParser.read('config.ini')

    target = configParser[section][item]
    return target


def transfer_to_csv(raw_list: list, filename: 'str' = 'target.csv', location: 'str' = '.',
                    encoding: 'str' = 'utf-8') -> None:
    try:
        df = pandas.DataFrame(raw_list)
        df.to_csv(location + '/' + filename, index=False, header=True, encoding=encoding)
    except Exception as e:
        raise RuntimeError(exception_throw_out()) from e
