import os
import numpy as np
import pandas as pd

from uni import University
from pandas import DataFrame


def init_res_excel(filename: str) -> DataFrame:
    if os.path.exists(filename):
        return pd.read_excel(filename)

    return pd.DataFrame(columns=(
        'Title',
        'Status',
        'Research Output',
        'Student/Faculty Ratio',
        'Scholarships',
        'Size',
        'Total Students',
        'Total PG Students',
        'Total UG Students',
        'Int\'l Students',
        'Int\'l PG Students',
        'Int\'l UG Students',
        'Total faculty staff',
        'Int\'l staff',
        'Domestic staff',

        'QS World University Rankings',
        'Overall (QS)',
        'Academic Reputation (QS)',
        'Citations per Faculty (QS)',
        'Employer Reputation (QS)',
        'Faculty Student Ratio (QS)',
        'International Faculty Ratio (QS)',
        'International Students Ratio (QS)',
        'QS World University Rankings Over The Years',

        'QS WUR Ranking By Subject',
        'Overall (QS Subject)',
        'Academic Reputation (QS Subject)',
        'Employer Reputation (QS Subject)',
        'H-index Citations (QS Subejct)',
        'Citations per Paper (QS Subject)',
        'QS Subject Rankings Over The Years',

        'Graduate Employability Ranking',
        'Overall (GE)',
        'Employers Reputation (GE)',
        'Alumni Outcomes (GE)',
        'Partnerships with Employers (GE)',
        'Employer-Student Connections (GE)',
        'Graduate Employment Rate (GE)',
        'GE Rankings Over The Years',

        'World University Rankings - Masters in Supply Chain Management',
        'Overall (WUR)',
        'Alumni Outcomes (WUR)',
        'Diversity (WUR)',
        'Employability (WUR)',
        'Thought Leadership (WUR)',
        'Value for Money (WUR)',
        'WUR Over The Years',

        'US UNI (universities)',
        'Overall (US UNI)',
        'Research (US UNI)',
        'Learning Experience (US UNI)',
        'Diversity & Internationalisation (US UNI)',
        'Employability (US UNI)',
        'US UNI Rankings Over The Years',

        'Asian University Rankings',
        'Overall (AURank)',
        'Academic Reputation (AURank)',
        'Employer Reputation (AURank)',
        'Faculty Student Ratio (AURank)',
        'International Faculty (AURank)',
        'International Students (AURank)',
        'Faculty Staff with PhD (AURank)',
        'Papers per Faculty (AURank)',
        'Citations per paper (AURank)',
        'Outbound Exchange (AURank)',
        'Inbound Exchange (AURank)',
        'International Research Network (AURank)',
        'Ranking Over Years (AURank)'
    ))


def save_to_excel(res: list[University], filename="res.xlsx"):
    df = init_res_excel(filename)

    for u in res:
        df.loc[df.index.size] = [
            u.title,
            u.status,
            u.research_output,
            u.sf_ratio,
            u.scholarships,
            u.size,
            u.total_students,
            u.total_pg_students,
            u.total_ug_students,
            u.inter_students,
            u.inter_pg_students,
            u.inter_ug_students,
            u.total_faculty_staff,
            u.inter_faculty_staff,
            u.domes_faculty_staff,

            u.qs_rank.rank if u.qs_rank else '',
            u.qs_rank.overall if u.qs_rank else '',
            u.qs_rank.academic_reputation if u.qs_rank else '',
            u.qs_rank.citations_per_faculty if u.qs_rank else '',
            u.qs_rank.employer_reputation if u.qs_rank else '',
            u.qs_rank.fs_ratio if u.qs_rank else '',
            u.qs_rank.inter_faculty_ratio if u.qs_rank else '',
            u.qs_rank.inter_students_ratio if u.qs_rank else '',
            u.qs_rank.rank_over_years if u.qs_rank else '',

            u.qs_subject_rank.rank if u.qs_subject_rank else '',
            u.qs_subject_rank.overall if u.qs_subject_rank else '',
            u.qs_subject_rank.academic_reputation if u.qs_subject_rank else '',
            u.qs_subject_rank.employer_reputation if u.qs_subject_rank else '',
            u.qs_subject_rank.h_index_citations if u.qs_subject_rank else '',
            u.qs_subject_rank.citations_per_paper if u.qs_subject_rank else '',
            u.qs_subject_rank.rank_over_years if u.qs_subject_rank else '',

            u.ge_rank.rank if u.ge_rank else '',
            u.ge_rank.overall if u.ge_rank else '',
            u.ge_rank.employer_reputation if u.ge_rank else '',
            u.ge_rank.alumni_outcomes if u.ge_rank else '',
            u.ge_rank.partnerships if u.ge_rank else '',
            u.ge_rank.es_connections if u.ge_rank else '',
            u.ge_rank.ge_rate if u.ge_rank else '',
            u.ge_rank.rank_over_years if u.ge_rank else '',

            u.wu_rank.rank if u.wu_rank else '',
            u.wu_rank.overall if u.wu_rank else '',
            u.wu_rank.alumni_outcomes if u.wu_rank else '',
            u.wu_rank.diversity if u.wu_rank else '',
            u.wu_rank.employability if u.wu_rank else '',
            u.wu_rank.thought_leadership if u.wu_rank else '',
            u.wu_rank.value_for_money if u.wu_rank else '',
            u.wu_rank.rank_over_years if u.wu_rank else '',

            u.us_uni_rank.rank if u.us_uni_rank else '',
            u.us_uni_rank.overall if u.us_uni_rank else '',
            u.us_uni_rank.research if u.us_uni_rank else '',
            u.us_uni_rank.learning_experience if u.us_uni_rank else '',
            u.us_uni_rank.diversity if u.us_uni_rank else '',
            u.us_uni_rank.employability if u.us_uni_rank else '',
            u.us_uni_rank.rank_over_years if u.us_uni_rank else '',

            u.au_rank.rank if u.au_rank else '',
            u.au_rank.overall if u.au_rank else '',
            u.au_rank.academic_reputation if u.au_rank else '',
            u.au_rank.employer_reputation if u.au_rank else '',
            u.au_rank.fs_ratio if u.au_rank else '',
            u.au_rank.inter_faculty if u.au_rank else '',
            u.au_rank.inter_students if u.au_rank else '',
            u.au_rank.fs_with_phd if u.au_rank else '',
            u.au_rank.papers_per_faculty if u.au_rank else '',
            u.au_rank.citations_per_paper if u.au_rank else '',
            u.au_rank.outbound_exchange if u.au_rank else '',
            u.au_rank.inbound_exchange if u.au_rank else '',
            u.au_rank.inter_rn if u.au_rank else '',
            u.au_rank.rank_over_years if u.au_rank else ''
        ]
    
    # start from index 1 instead of 0
    df.index = np.arange(1, len(df) + 1)
    df.to_excel(filename, index=False)
