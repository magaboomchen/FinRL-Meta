import importlib
import datetime
from datetime import timedelta
from typing import Union

import pandas as pd
from matplotlib import pyplot as plt
import tushare as ts

import meta
from meta.data_processors.tushare import ReturnPlotter
from meta.local.base.setting_loader import SettingLoader
tushare_setting = SettingLoader.load_tushare_setting()
tushare_token = tushare_setting['tushare_token']
from meta.local.base.list_lib import get_common_length_list
importlib.reload(meta.local.base.list_lib)

TICKET_TYPE_INDEX = "TICKET_TYPE_INDEX"
TICKET_TYPE_TICKET = "TICKET_TYPE_TICKET"


class ReturnPlotterPrivate(ReturnPlotter):
    '''
    Pro api: https://tushare.pro/document/1?doc_id=131
    pro.trade_cal: https://tushare.pro/document/2?doc_id=26
    pro.daily: https://tushare.pro/document/2?doc_id=27
    '''
    def get_baseline(self, ticket,
                    ticket_type: Union[TICKET_TYPE_INDEX, TICKET_TYPE_TICKET]=TICKET_TYPE_TICKET):
        ts.set_token(tushare_token)
        pro = ts.pro_api()
        pro = ts.pro_api(tushare_token)
        # print("ticket is {0}".format(ticket))
        self.start_datetime = datetime.datetime.strptime(self.start, "%Y-%m-%d")
        start_date = self.start_datetime.strftime("%Y%m%d")
        self.end_datetime = datetime.datetime.strptime(self.end, "%Y-%m-%d")
        # self.end_datetime = self.end_datetime - timedelta(days=1)
        end_date = self.end_datetime.strftime("%Y%m%d")
        if ticket_type == TICKET_TYPE_TICKET:
            df = pro.daily(ts_code=ticket, start_date=start_date, end_date=end_date)
        elif ticket_type == TICKET_TYPE_INDEX:
            print(TICKET_TYPE_INDEX)
            df = pro.index_daily(ts_code=ticket, start_date=start_date, end_date=end_date)
            # df = ts.get_hist_data(ticket, start=self.start, end=self.end)
        # print(df)
        # print("start date is {0}, end date is {1}".format(self.start, self.end))
        df.loc[:, "dt"] = df.index
        df.index = range(len(df))
        df.sort_values(axis=0, by="dt", ascending=True, inplace=True)
        df["date"] = pd.to_datetime(df["dt"], format="%Y-%m-%d")
        return df

    def plot(self, baseline_ticket:str=None, figure_filepath:str=None,
                ticket_type: Union[TICKET_TYPE_INDEX, TICKET_TYPE_TICKET]=TICKET_TYPE_TICKET):
        """
        Plot cumulative returns over time.
        use baseline_ticket to specify stock you want to use for comparison
        (default: equal weighted returns)
        """
        baseline_label = "Equal-weight portfolio"
        tic2label = {"399300.SZ": "CSI 300 Index", "000016.SH": "SSE 50 Index"}
        if baseline_ticket:
            # 使用指定ticket作为baseline
            baseline_df = self.get_baseline(baseline_ticket, ticket_type)
            baseline_df = baseline_df[
                baseline_df.dt != "2020-06-26"
            ]  # ours don't have date=="2020-06-26"
            # print(baseline_df)
            baseline = baseline_df.close.tolist()
            baseline_label = tic2label.get(baseline_ticket, baseline_ticket)
        else:
            # 均等权重
            all_date = self.trade.date.unique().tolist()
            baseline = []
            for day in all_date:
                day_close = self.trade[self.trade["date"] == day].close.tolist()
                avg_close = sum(day_close) / len(day_close)
                baseline.append(avg_close)

        ours = self.df_account_value.account_value.tolist()
        ours = self.pct(ours)
        # print(len(baseline))
        baseline = self.pct(baseline)

        days_per_tick = (
            60  # you should scale this variable accroding to the total trading days
        )
        time = list(range(len(ours)))
        datetimes = self.df_account_value.date.tolist()
        ticks = [tick for t, tick in zip(time, datetimes) if t % days_per_tick == 0]
        plt.title("Cumulative Returns")
        (ours, baseline) = get_common_length_list(ours, baseline)
        plt.plot(time, ours, label="DDPG Agent", color="green")
        plt.plot(time, baseline, label=baseline_label, color="grey")
        plt.xticks([i * days_per_tick for i in range(len(ticks))], ticks, fontsize=7)

        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")

        plt.legend()
        if figure_filepath:
            plt.savefig(figure_filepath)
        else:
            plt.show()