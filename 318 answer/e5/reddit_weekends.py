import pandas as pd
import numpy as np
import gzip
from scipy import stats
from scipy.stats import mannwhitneyu, ttest_ind
import sys


OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mannâ€“Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]

    station_fh = gzip.open(reddit_counts, 'rt', encoding='utf-8')
    stations = pd.read_json(station_fh, lines=True)

    stations = stations[stations.subreddit == "canada"]
    stations = stations[(stations['date'].dt.year == 2012) | (stations['date'].dt.year == 2013)].reset_index()

    del stations["index"]
    stations['weekday'] = stations['date'].dt.dayofweek
    weekday = stations[(stations['weekday'] == 5) | (stations['weekday'] == 6)].reset_index()
    weekend = stations[(stations['weekday'] != 5) & (stations['weekday'] != 6)].reset_index()
    del weekday["index"]
    del weekend["index"]

    initial_ttest_p = ttest_ind(weekday['comment_count'], weekend['comment_count'])
    initial_weekday_normality_p = stats.normaltest(weekday['comment_count'])
    initial_weekend_normality_p = stats.normaltest(weekend['comment_count'])
    initial_levene_p = stats.levene(weekday['comment_count'], weekend['comment_count'])

    # Fix1
    # sqrt
    weekday_sqrt = np.sqrt(weekday["comment_count"])
    weekend_sqrt = np.sqrt(weekend["comment_count"])
    # print(weekday_sqrt)

    transformed_weekday_normality_p = stats.normaltest(weekday_sqrt)
    transformed_weekend_normality_p = stats.normaltest(weekend_sqrt)
    transformed_levene_p = stats.levene(weekday_sqrt, weekend_sqrt)

    # Fix2
    # Logic copy from Prof Greg Baker
    def week(dt):
        isocal = dt.isocalendar()
        return '%i-%i' % (isocal[0], isocal[1])

    weekday_number = weekday.date.apply(week)
    weekend_number = weekend.date.apply(week)

    weekday["number"] = weekday_number
    weekend["number"] = weekend_number

    grouped_weekday = weekday.groupby(['number'])
    weekly_weekday = grouped_weekday.aggregate('sum')
    grouped_weekend = weekend.groupby(['number'])
    weekly_weekend = grouped_weekend.aggregate('sum')

    weekly_weekday_normality_p = stats.normaltest(weekly_weekday['comment_count'])
    weekly_weekend_normality_p = stats.normaltest(weekly_weekend['comment_count'])
    weekly_levene_p = stats.levene(weekly_weekday['comment_count'], weekly_weekend['comment_count'])
    weekly_ttest_p = ttest_ind(weekly_weekday['comment_count'], weekly_weekend['comment_count'])

    # Fix3
    utest_p = mannwhitneyu(weekday['comment_count'], weekend['comment_count'])

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initial_ttest_p.pvalue,
        initial_weekday_normality_p=initial_weekday_normality_p.pvalue,
        initial_weekend_normality_p=initial_weekend_normality_p.pvalue,
        initial_levene_p=initial_levene_p.pvalue,
        transformed_weekday_normality_p=transformed_weekday_normality_p.pvalue,
        transformed_weekend_normality_p=transformed_weekend_normality_p.pvalue,
        transformed_levene_p=transformed_levene_p.pvalue,
        weekly_weekday_normality_p=weekly_weekday_normality_p.pvalue,
        weekly_weekend_normality_p=weekly_weekend_normality_p.pvalue,
        weekly_levene_p=weekly_levene_p.pvalue,
        weekly_ttest_p=weekly_ttest_p.pvalue,
        utest_p=utest_p.pvalue,
    ))


if __name__ == '__main__':
    main()