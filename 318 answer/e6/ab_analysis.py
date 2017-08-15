import sys
from scipy import stats
import pandas as pd


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    data = pd.read_json(searchdata_file, orient='records', lines=True)

    data_odd_new = data[data.uid % 2 != 0]  # 348
    data_even_old = data[data.uid % 2 == 0]  # 333

    odd_new_never_searched = data_odd_new[data_odd_new.search_count == 0]
    odd_new_at_least_once = data_odd_new[data_odd_new.search_count > 0]

    even_old_never_searched = data_even_old[data_even_old.search_count == 0]
    even_old_at_least_once = data_even_old[data_even_old.search_count > 0]

    contingency = [[odd_new_never_searched.shape[0], odd_new_at_least_once.shape[0]],
                   [even_old_never_searched.shape[0],
                    even_old_at_least_once.shape[0]]]
    chi2, p, dof, expected = stats.chi2_contingency(contingency)

    more_searches_p = stats.mannwhitneyu(data_odd_new["search_count"], data_even_old["search_count"])

    data_odd_new_instructor = data_odd_new[data_odd_new.is_instructor == True]
    data_even_old_instructor = data_even_old[data_even_old.is_instructor == True]

    odd_new_instructor_never_searched = data_odd_new_instructor[data_odd_new_instructor.search_count == 0]
    odd_new_instructor_least_once = data_odd_new_instructor[data_odd_new_instructor.search_count > 0]

    even_old_instructor_never_searched = data_even_old_instructor[data_even_old_instructor.search_count == 0]
    even_old_instructor_least_once = data_even_old_instructor[data_even_old_instructor.search_count > 0]

    contingency = [[odd_new_instructor_never_searched.shape[0],
                    odd_new_instructor_least_once.shape[0]],
                   [even_old_instructor_never_searched.shape[0],
                    even_old_instructor_least_once.shape[0]]]
    chi2, more_instr_p, dof, expected = stats.chi2_contingency(contingency)

    more_instr_searches_p = stats.mannwhitneyu(data_odd_new_instructor["search_count"],
                                               data_even_old_instructor["search_count"])

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p,
        more_searches_p=more_searches_p.pvalue,
        more_instr_p=more_instr_p,
        more_instr_searches_p=more_instr_searches_p.pvalue,
    ))


if __name__ == '__main__':
    main()