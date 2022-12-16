
def format_value(index, value):
    """格式化数据"""
    if value is not None:
        if index["storage_type"] == "float":
            value = float(value)
        round_ = index['round']
        divisor = index['divisor']
        offset = index['offset']
        low_limit = index['low_limit']
        up_limit = index['up_limit']
        if divisor:
            value *= divisor
        if offset:
            value += offset
        # print(value)
        # 保留小数
        if round_:
            value = round(value, int(round_))
        # 规定范围
        if low_limit is not None and up_limit is not None:  # 上下限都存在
            if low_limit <= value <= up_limit:
                return value
        elif low_limit is not None and up_limit is None:    # 下限存在
            if low_limit <= value:
                return value
        elif up_limit is not None and low_limit is None:    # 上限存在
            if value <= up_limit:
                return value
        else:   # 都不存在
            return value
        # 不在范围舍弃数据
        return ''
    else:
        return ''
