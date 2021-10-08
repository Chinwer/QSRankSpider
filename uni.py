from os import stat


class Rank:
    NUM = '//div[@class="right"]//div[@class="circle"]'
    DATA = '//*[@id="rankingsTab"]/div[1]/div[1]/ul/li[2]/a'
    # YEARS = '//*[@id="rank-data"]/ul/li/text()'
    # RANKS = '//*[@id="rank-data"]/ul/li/div/text()'
    YEARS = '//*[@id="rank-data"]/ul/li'
    RANKS = '//*[@id="rank-data"]/ul/li/div'
    DATA_BTN = '#rankingsTab > div.left > div.tit-list > ul > li.nav-item.last > a'

    def __init__(self, rank, overall, years=[], ranks=[]):
        self.rank = rank
        self.overall = overall
        self.years = years
        self.ranks = ranks

        arr = ["{}:{}".format(self.years[i], self.ranks[i]) for i in range(len(self.years))]
        self.rank_over_years = ', '.join(arr)


# QS World University Rankings
class QSRank(Rank):
    ELEM = '//*[@id="wur-tab"]'
    RANK = '//*[@id="wur-tab"]/div/text()'

    OVERALL_LITERAL = 'Overall'
    ACADEMIC_REPUTATION_LITERAL = 'Academic Reputation'
    EMPLOYER_REPUTATION_LITERAL = 'Employer Reputation'
    FS_RATIO_LITERAL = 'Faculty Student Ratio'
    CITATIONS_PER_FACULTY_LITERAL = 'Citations per Faculty'
    INTER_FACULTY_RATIO_LITERAL = 'International Faculty Ratio'
    INTER_STUDENTS_RATIO_LITERAL = 'International Students Ratio'

    ITEM_LITERALS = [
        OVERALL_LITERAL,
        ACADEMIC_REPUTATION_LITERAL,
        EMPLOYER_REPUTATION_LITERAL,
        FS_RATIO_LITERAL,
        CITATIONS_PER_FACULTY_LITERAL,
        INTER_FACULTY_RATIO_LITERAL,
        INTER_STUDENTS_RATIO_LITERAL
    ]

    ITEM_SCORES = [
        '//div[@class="circle"][1]/div[1]/text()',
        '//div[@class="circle"][2]/div[1]/text()',
        '//div[@class="circle"][3]/div[1]/text()',
        '//div[@class="circle"][4]/div[1]/text()',
        '//div[@class="circle"][5]/div[1]/text()',
        '//div[@class="circle"][6]/div[1]/text()',
        '//div[@class="circle"][7]/div[1]/text()',
    ]
    ITEM_NAMES = [
        '//div[@class="circle"][1]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][2]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][3]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][4]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][5]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][6]/div[@class="itm-name"]/text()',
        '//div[@class="circle"][7]/div[@class="itm-name"]/text()',
    ]

    @staticmethod
    def map_item_name_to_idx(name: str) -> int:
        for i, l in enumerate(QSRank.ITEM_LITERALS):
            if name in l:
                return i
        return 0

    def __init__(
        self, rank, overall, academic_reputation, 
        citations_per_faculty, employer_reputation, fs_ratio,
        inter_faculty_ratio, inter_students_ratio,
        years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)

        self.academic_reputation = academic_reputation
        self.citations_per_faculty = citations_per_faculty
        self.employer_reputation = employer_reputation
        self.fs_ratio = fs_ratio
        self.inter_faculty_ratio = inter_faculty_ratio
        self.inter_students_ratio = inter_students_ratio

    def __str__(self) -> str:
        res = '\n\t------ QS WORLD University Rankings ------\n'

        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tAcademic Reputation: {}\n'.format(self.academic_reputation)
        res += '\tEmployer Reputation: {}\n'.format(self.employer_reputation)
        res += '\tFaculty Student Ratio: {}\n'.format(self.fs_ratio)
        res += '\tCitations per Faculty: {}\n'.format(self.citations_per_faculty)
        res += '\tInternational Faculty Ratio: {}\n'.format(self.inter_faculty_ratio)
        res += '\tInternational Students Ratio: {}\n'.format(self.inter_students_ratio)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


# QS WUR Ranking By Subject
class QSSubjectRank(Rank):
    ELEM = 'subj-tab'
    # RANK = '//*[@id="subj-tab"]/div/text()'
    RANK = '//*[@id="subj-tab"]/div'

    ITEM_SCORES = [
        '//div[@class="circle"][1]/div',
        '//div[@class="circle"][2]/div',
        '//div[@class="circle"][3]/div',
        '//div[@class="circle"][4]/div',
        '//div[@class="circle"][5]/div',
    ]
    ITEM_NAMES = [
        '//div[@class="circle"][1]/div[@class="itm-name"]',
        '//div[@class="circle"][2]/div[@class="itm-name"]',
        '//div[@class="circle"][3]/div[@class="itm-name"]',
        '//div[@class="circle"][4]/div[@class="itm-name"]',
        '//div[@class="circle"][5]/div[@class="itm-name"]',
    ]

    SUBJECT_NUM = '//*[@id="subr-dd"]/li'
    SUBJECT_BTN = '#subr-dd > li:nth-child'
    SUBJECT_NAMES = '//*[@id="subr-dd"]/li/a/text()'

    OVERALL_LITERAL = 'Overall'
    H_INDEX_CITATIONS_LITERAL = 'H-index Citations'
    ACADEMIC_REPUTATION_LITERAL = 'Academic Reputation'
    EMPLOYER_REPUTATION_LITERAL = 'Employer Reputation'
    CITATIONS_PER_PAPER_LITERAL = 'Citations per Paper'
    ITEM_LITERALS = [
        OVERALL_LITERAL,
        ACADEMIC_REPUTATION_LITERAL,
        EMPLOYER_REPUTATION_LITERAL,
        H_INDEX_CITATIONS_LITERAL,
        CITATIONS_PER_PAPER_LITERAL
    ]

    @staticmethod
    def map_item_name_to_idx(name: str) -> int:
        for i, l in enumerate(QSSubjectRank.ITEM_LITERALS):
            if name in l:
                return i
        return 0

    @staticmethod
    def get_nth_subject_item_js_path(idx: int) -> str:
        return '{}({}) > a'.format(QSSubjectRank.SUBJECT_BTN, str(idx))

    @staticmethod
    def get_nth_subject_name_xpath(idx: int) -> str:
        # return '//*[@id="subr-dd"]/li[{}]/a/text()'.format(idx)
        return '//*[@id="subr-dd"]/li[{}]/a'.format(idx)

    def __init__(
        self, name, rank, overall, academic_reputation,
        employer_reputation, h_index_citations, 
        citations_per_paper, years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)

        self.name = name
        self.academic_reputation = academic_reputation
        self.employer_reputation = employer_reputation
        self.h_index_citations = h_index_citations
        self.citations_per_paper = citations_per_paper

    def __str__(self) -> str:
        res = '\n\t------ QS WUR Ranking By Subject ------\n'

        res += '\tSubject Name: {}\n'.format(self.name)
        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tAcademic Reputation: {}\n'.format(self.academic_reputation)
        res += '\tEmployer Reputation: {}\n'.format(self.employer_reputation)
        res += '\tH-index Citations: {}\n'.format(self.h_index_citations)
        res += '\tCitations per Paper: {}\n'.format(self.citations_per_paper)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


# World University Rankings - Masters in Supply Chain Management
class WURank(Rank):
    ELEM = 'item-3822'
    RANK = '//*[@id="item-3822"]/div/text()'
    OVERALL = '//div[@class="circle"][1]/div/text()'
    ALUMNI_OUTCOMES = '//div[@class="circle"][2]/div/text()'
    DIVERSITY = '//div[@class="circle"][3]/div/text()'
    EMPLOYABILITY = '//div[@class="circle"][4]/div/text()'
    THOUGHT_LEADERSHIP = '//div[@class="circle"][5]/div/text()'
    VALUE_FOR_MONEY = '//div[@class="circle"][6]/div/text()'
    INDICATORS = [
        OVERALL,
        ALUMNI_OUTCOMES,
        DIVERSITY,
        EMPLOYABILITY,
        THOUGHT_LEADERSHIP,
        VALUE_FOR_MONEY
    ]

    def __init__(
        self, rank, overall, alumni_outcomes,diversity,
        employability, thought_leadership, value_for_money,
        years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)

        self.alumni_outcomes = alumni_outcomes
        self.diversity = diversity
        self.employability = employability
        self.thought_leadership = thought_leadership
        self.value_for_money = value_for_money

    def __str__(self) -> str:
        res = '\n\t------ World University Rankings - Masters in Supply Chain Management ------\n'

        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tAlumni Outcomes: {}\n'.format(self.alumni_outcomes)
        res += '\tDiversity: {}\n'.format(self.diversity)
        res += '\tEmployability: {}\n'.format(self.employability)
        res += '\tThought Leadership: {}\n'.format(self.thought_leadership)
        res += '\tValue for Money: {}\n'.format(self.value_for_money)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


# US UNI (universities)
class USUniRank(Rank):
    ELEM = 'item-3786'
    RANK = '//*[@id="item-3786"]/div/text()'
    OVERALL = '//div[@class="circle"][1]/div/text()'
    RESEARCH = '//div[@class="circle"][2]/div/text()'
    LEARNING_EXPERIENCE = '//div[@class="circle"][3]/div/text()'
    DIVERSITY = '//div[@class="circle"][4]/div/text()'
    EMPLOYABILITY = '//div[@class="circle"][5]/div/text()'
    INDICATORS = [
        OVERALL,
        RESEARCH,
        LEARNING_EXPERIENCE,
        DIVERSITY,
        EMPLOYABILITY
    ]

    def __init__(
        self, rank, overall, research,
        learning_experience, diversity, employability,
        years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)
        
        self.research = research
        self.learning_experience = learning_experience
        self.diversity = diversity
        self.employability = employability

    def __str__(self) -> str:
        res = '\n\t------ US UNI (universities) ------\n'

        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tResearch: {}\n'.format(self.research)
        res += '\tLearning Experience: {}\n'.format(self.learning_experience)
        res += '\tDiversity & Internationalisation: {}\n'.format(self.diversity)
        res += '\tEmployability: {}\n'.format(self.employability)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


# Graduate Employability Ranking
class GERank(Rank):
    ELEM = 'item-3598'
    RANK = '//*[@id="item-3598"]/div/text()'
    OVERALL = '//div[@class="circle"][1]/div/text()'
    EMPLOYER_REPUTATION = '//div[@class="circle"][2]/div/text()'
    ALUMNI_OUTCOMES = '//div[@class="circle"][3]/div/text()'
    PARTNERSHIPS = '//div[@class="circle"][4]/div/text()'
    ES_CONNECTIONS = '//div[@class="circle"][5]/div/text()'
    GE_RATE = '//div[@class="circle"][6]/div/text()'
    INDICATORS = [
        OVERALL,
        EMPLOYER_REPUTATION,
        ALUMNI_OUTCOMES,
        PARTNERSHIPS,
        ES_CONNECTIONS,
        GE_RATE
    ]

    def __init__(
        self, rank, overall, employer_reputation,
        alumni_outcomes, partnerships, es_connections,
        ge_rate, years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)

        self.employer_reputation = employer_reputation
        self.alumni_outcomes = alumni_outcomes
        # Partnerships with Employers
        self.partnerships = partnerships
        # Employer-Student Connections
        self.es_connections = es_connections
        # Graduate Employment Rate
        self.ge_rate = ge_rate

    def __str__(self) -> str:
        res = '\n\t------ Graduate Employability Ranking ------\n'

        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tEmployers Reputation: {}\n'.format(self.employer_reputation)
        res += '\tAlumni Outcomes: {}\n'.format(self.alumni_outcomes)
        res += '\tPartnerships with Employers: {}\n'.format(self.partnerships)
        res += '\tEmployer-Student Connections: {}\n'.format(self.es_connections)
        res += '\tGraduate Employment Rate: {}\n'.format(self.ge_rate)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


class AURank(Rank):
    ELEM = 'item-514'
    RANK = '//*[@id="item-514"]/div/text()'

    OVERALL = '//div[@class="circle"][1]/div/text()'
    ACADEMIC_REPUTATION = '//div[@class="circle"][2]/div/text()'
    EMPLOYER_REPUTATION = '//div[@class="circle"][3]/div/text()'
    FS_RATIO = '//div[@class="circle"][4]/div/text()'
    INTER_FACULTY = '//div[@class="circle"][5]/div/text()'
    INTER_STUDENTS = '//div[@class="circle"][6]/div/text()'
    FS_WITH_PHD = '//div[@class="circle"][7]/div/text()'
    PAPERS_PER_FACULTY = '//div[@class="circle"][8]/div/text()'
    CITATIONS_PER_PAPER = '//div[@class="circle"][9]/div/text()'
    OUTBOUND_EXCHANGE = '//div[@class="circle"][10]/div/text()'
    INBOUND_EXCHANGE = '//div[@class="circle"][11]/div/text()'
    INTER_RN = '//div[@class="circle"][12]/div/text()'

    INDICATORS = [
        OVERALL,
        ACADEMIC_REPUTATION,
        EMPLOYER_REPUTATION,
        FS_RATIO,
        INTER_FACULTY,
        INTER_STUDENTS,
        FS_WITH_PHD,
        PAPERS_PER_FACULTY,
        CITATIONS_PER_PAPER,
        OUTBOUND_EXCHANGE,
        INBOUND_EXCHANGE,
        INTER_RN
    ]

    def __init__(
        self, rank, overall, academic_reputation, employer_reputation, fs_ratio,
        inter_faculty, inter_students, fs_with_phd, papers_per_faculty,
        citations_per_paper, outbound_exchange, inbound_exchange, inter_rn,
        years=[], ranks=[]
    ):
        super().__init__(rank, overall, years, ranks)
        self.academic_reputation = academic_reputation
        self.employer_reputation = employer_reputation
        self.fs_ratio = fs_ratio
        self.inter_faculty = inter_faculty
        self.inter_students = inter_students
        self.fs_with_phd = fs_with_phd
        self.papers_per_faculty = papers_per_faculty
        self.citations_per_paper = citations_per_paper
        self.outbound_exchange = outbound_exchange
        self.inbound_exchange = inbound_exchange
        self.inter_rn = inter_rn

    def __str__(self) -> str:
        res = '\n\t------ Asian University Rankings ------\n'

        res += '\tRank: {}\n'.format(self.rank)
        res += '\tOverall: {}\n'.format(self.overall)
        res += '\tAcademic Reputation: {}\n'.format(self.academic_reputation)
        res += '\tEmployer Reputation: {}\n'.format(self.employer_reputation)
        res += '\tFaculty Student Ratio: {}\n'.format(self.fs_ratio)
        res += '\tInternational Faculty: {}\n'.format(self.inter_faculty)
        res += '\tInternational Students: {}\n'.format(self.inter_students)
        res += '\tFaculty Staff with PhD: {}\n'.format(self.fs_with_phd)
        res += '\tPapers per Faculty: {}\n'.format(self.papers_per_faculty)
        res += '\tCitations per paper: {}\n'.format(self.citations_per_paper)
        res += '\tOutbound Exchange: {}\n'.format(self.outbound_exchange)
        res += '\tInbound Exchange: {}\n'.format(self.inbound_exchange)
        res += '\tInternational Research Network: {}\n'.format(self.inter_rn)

        res += '\tRanking Over Years: {}\n'.format(self.rank_over_years)

        return res


class University:
    # xpath of all fields
    TITLE = '//div[@class="programeTitle"]/h1/text()|//div[@class="programeTitle"]/h1/a/text()'
    STATUS = '//li[@title="Status"]/span[2]/text()'
    RESEARCH_OUTPUT = '//li[@title="Research Output"]/span[2]/text()'
    SF_RATIO = '//li[@title="Student/Faculty Ratio"]/span[2]/text()'
    SCHOLARSHIPS = '//div[@class="uni_info"]//li[@title="Scholarships"]/span[2]/text()'
    INTER_STUDENTS = '//li[@title="International Students"]/span[2]/text()'
    SIZE = '//li[@title="Size"]/span[2]/text()'

    STUDENTS_STAFF = '//*[@id="graph"]/div[1]/div[1]/div[1]/div[1]/div/text()'

    TOTAL_STUDENTS = '//*[@id="graph"]/div[1]/div[1]/h4/div[2]/text()'
    TOTAL_PG_STUDENTS = '//*[@id="graph"]/div[1]/div[1]/div[1]/div[1]/div/text()'
    TOTAL_UG_STUDENTS = '//*[@id="graph"]/div[1]/div[1]/div[1]/div[2]/div/text()'
    INTER_PG_STUDENTS = '//*[@id="graph"]/div[1]/div[2]/div[1]/div[1]/div/text()'
    INTER_UG_STUDENTS = '//*[@id="graph"]/div[1]/div[2]/div[1]/div[2]/div/text()'
    TOTAL_FACULTY_STAFF = '//*[@id="graph"]/div[2]/div/h4/div[2]/text()'
    INTER_FACULTY_STAFF = '//*[@id="graph"]/div[2]/div/div[1]/div[1]/div/text()'
    DOMES_FACULTY_STAFF = '//*[@id="graph"]/div[2]/div/div[1]/div[2]/div/text()'

    def __init__(
        self, title: str, status: str, research_output: str, sf_ratio: float, 
        scholarships: str, inter_students: str, size: str,
        total_students: str, total_pg_students: str, total_ug_students:str,
        inter_pg_students: str, inter_ug_students: str,
        total_faculty_staff: str, inter_faculty_staff: str, domes_faculty_staff: str,
        qs_rank: QSRank=None, wu_rank: WURank=None, us_uni_rank: USUniRank=None, 
        ge_rank: GERank=None, au_rank: AURank=None,
        qs_subject_ranks: list[QSSubjectRank]=None
    ):

        # base information
        self.title = title
        self.status = status
        self.research_output = research_output
        self.sf_ratio = sf_ratio
        self.scholarships = scholarships
        self.inter_students = inter_students
        self.size = size
        self.status = status

        # students & staff
        self.total_students = total_students
        self.total_pg_students = total_pg_students
        self.total_ug_students = total_ug_students
        self.inter_pg_students = inter_pg_students
        self.inter_ug_students = inter_ug_students
        self.total_faculty_staff = total_faculty_staff
        self.inter_faculty_staff = inter_faculty_staff
        self.domes_faculty_staff = domes_faculty_staff

        # detail ranking information
        self.qs_rank = qs_rank
        self.wu_rank = wu_rank
        self.us_uni_rank = us_uni_rank
        self.ge_rank = ge_rank
        self.au_rank = au_rank
        self.qs_subject_ranks = qs_subject_ranks

    def __str__(self) -> str:
        res = '{\n'
        res += '\tTitle: {}\n'.format(self.title)
        res += '\tStatus: {}\n'.format(self.status)
        res += '\tResearch Output: {}\n'.format(self.research_output)
        res += '\tStudent/Faculty Ratio: {}\n'.format(self.sf_ratio)
        res += '\tScholarships: {}\n'.format(self.scholarships)
        res += '\tInternational Students: {}\n'.format(self.inter_students)
        res += '\tSize: {}\n'.format(self.size)

        res += '\tTotal Students: {}\n'.format(self.total_students)
        res += '\tTotal PG Students: {}\n'.format(self.total_pg_students)
        res += '\tTotal UG Students: {}\n'.format(self.total_ug_students)
        res += '\tInt\'l PG Students: {}\n'.format(self.inter_pg_students)
        res += '\tInt\'l UG Students: {}\n'.format(self.inter_ug_students)
        res += '\tTotal faculty staff: {}\n'.format(self.total_faculty_staff)
        res += '\tInt\'l staff: {}\n'.format(self.inter_faculty_staff)
        res += '\tDomestic staff: {}\n'.format(self.domes_faculty_staff)

        res += str(self.qs_rank) if self.qs_rank else ''
        res += str(self.wu_rank) if self.wu_rank else ''
        res += str(self.us_uni_rank) if self.us_uni_rank else ''
        res += str(self.ge_rank) if self.ge_rank else ''
        res += str(self.au_rank) if self.au_rank else ''

        if self.qs_subject_ranks:
            for i in self.qs_subject_ranks:
                res += str(i) if i else ''

        res += '}\n'

        return res
