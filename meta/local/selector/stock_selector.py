'''
Get all stock of a industry in China A share.
Select interest stocks in this industry.
'''


class StockSelector(object):
    def __init__(self):
        pass

    def select_stocks(self):
        ticker_list_comp = [
            '600000.SH',    # 浦发银行
            '600009.SH',    # 上海机场
            '600016.SH',    # 民生银行
            '600028.SH',    # 中国石化
            '600030.SH',    # 中信证券
            '600031.SH',    # 三一重工
            '600036.SH',    # 招商银行
            '600050.SH',    # 中国联通
            '600104.SH',    # 上汽集团
            '600196.SH',    # 复星医药
            '600276.SH',    # 恒瑞医药
            '600309.SH',    # 万华化学
            '600519.SH',    # 贵州茅台
            '600547.SH',    # 山东黄金
            '600570.SH',     # 恒生电子
            ]

        ticker_list = [
            '600276.SH',    # 恒瑞医药
            '300760.SZ',    # 迈瑞医疗
            '603259.SH',    # 药明康德
            '600519.SH',    # 贵州茅台
            '600438.SH',    # 通威股份
            '002241.SZ',    # 歌尔股份
            '300750.SZ',    # 宁德时代
            '002466.SZ',    # 天齐锂业
            '000651.SZ',    # 格力电器
            '603288.SH',    # 海天味业
            '002557.SH',    # 洽洽食品
            '600740.SH',    # 陕西焦化
            '601088.SH',    # 中国神华
            '002179.SH',    # 中航光电
            '000768.SH',    # 中航西飞
            '600009.SH',    # 上海机场
            '600036.SH',    # 招商银行
            ]

        return ticker_list