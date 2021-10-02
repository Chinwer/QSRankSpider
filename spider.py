import time
import traceback

from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from util import save_to_excel
from uni import AURank, Rank, GERank, QSRank, QSSubjectRank, USUniRank, University, WURank


WAIT_TIME = 1
WAIT_CLICK_EVENT_REGISTER_TIME = 2
LOG_FILENAME = 'log.txt'
START_URL = 'https://www.topuniversities.com/university-rankings/world-university-rankings/2022'


def get_all_detail_urls(driver: WebDriver) -> list[str]:
    res: list[str] = []
    driver.get(START_URL)

    university_href_xpath = '//div[contains(@class, "university-rank-row")]/div/a'
    next_page_xpath = '//li/a[@class="page-link next"]'

    # 130 pages in total
    scroll_js = 'var q = document.documentElement.scrollTop=300'
    driver.execute_script(scroll_js)
    for i in range(130):

        _ = WebDriverWait(driver, 30, 5).until(
            EC.presence_of_element_located((By.XPATH, university_href_xpath))
        )

        hrefs: list[WebElement] = driver.find_elements_by_xpath(university_href_xpath)
        hrefs: list[str] = [href.get_property('href') for href in hrefs]

        if len(hrefs):
            res.extend(hrefs)

        try:
            next_page: WebElement = driver.find_element_by_xpath(next_page_xpath)
            driver.execute_script('arguments[0].click()', next_page)
        except NoSuchElementException: 
            print("Reach the final page.")
            break
            
        time.sleep(1)

    with open("urls.txt", "w") as f:
        for url in res:
            f.write('{}\n'.format(url))

    return res


def get_all_urls_from_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        return f.readlines()


def parse_qs_rank(browser: WebDriver):
    tree = etree.HTML(browser.page_source)
    indicators = [''] * len(QSRank.INDICATORS)
    num = len(tree.xpath(Rank.NUM))
    rank = tree.xpath(QSRank.RANK)[0].strip()

    for i in range(num):
        indicators[i] = tree.xpath(QSRank.INDICATORS[i])[0].strip()

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    years = tree.xpath(Rank.YEARS)
    ranks = tree.xpath(Rank.RANKS)

    return QSRank(
        rank=rank,
        overall=indicators[0],
        academic_reputation=indicators[1],
        citations_per_faculty=indicators[2],
        employer_reputation=indicators[3],
        fs_ratio=indicators[4],
        inter_faculty_ratio=indicators[5],
        inter_students_ratio=indicators[6],
        years=years,
        ranks=ranks
    )


def parse_qs_subject_rank(idx: int, browser: WebDriver):
    # tree = etree.HTML(browser.page_source)

    indicators = [''] * len(QSSubjectRank.ITEM_LITERALS)
    # num = len(tree.xpath(Rank.NUM))
    num = len(browser.find_elements_by_xpath(Rank.NUM))
    name = browser.find_element_by_xpath(QSSubjectRank.get_nth_subject_name_xpath(idx)).get_attribute('text')
    # name = tree.xpath(QSSubjectRank.get_nth_subject_name_xpath(idx))[0].strip()
    rank = browser.find_element_by_xpath(QSSubjectRank.RANK).text
    # rank = tree.xpath(QSSubjectRank.RANK)[0].strip()

    for i in range(num):
        # item_name = tree.xpath(QSSubjectRank.ITEM_NAMES[i])[0].strip()
        # item_score = tree.xpath(QSSubjectRank.ITEM_SCORES[i])[0].strip()
        item_name = browser.find_element_by_xpath(QSSubjectRank.ITEM_NAMES[i]).text
        item_score = browser.find_element_by_xpath(QSSubjectRank.ITEM_SCORES[i]).text
        idx = QSSubjectRank.map_item_name_to_idx(item_name)
        indicators[idx] = item_score

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    # years = tree.xpath(Rank.YEARS)
    # ranks = tree.xpath(Rank.RANKS)
    years = browser.find_elements_by_xpath(Rank.YEARS)
    years = [str.split(x.text, '\n')[0] for x in years]
    ranks = browser.find_elements_by_xpath(Rank.RANKS)
    ranks = [x.text for x in ranks]

    return QSSubjectRank(
        name=name,
        rank=rank,
        overall=indicators[0],
        academic_reputation=indicators[1],
        employer_reputation=indicators[2],
        h_index_citations=indicators[3],
        citations_per_paper=indicators[4],
        years=years,
        ranks=ranks
    )


def parse_qs_subject_ranks(browser: WebDriver):
    try:
        _ = browser.find_element_by_id(QSSubjectRank.ELEM)
    except NoSuchElementException:
        return None

    browser.execute_script('document.querySelector("#{}").click()'.format(QSSubjectRank.ELEM))
    time.sleep(3)

    tree = etree.HTML(browser.page_source)
    subject_nums = len(tree.xpath(QSSubjectRank.SUBJECT_NUM))
    ranks = []
    for i in range(subject_nums):
        browser.execute_script(
            'document.querySelector("{}").click()'
            .format(QSSubjectRank.get_nth_subject_item_js_path(i + 1))
        )
        time.sleep(WAIT_TIME)
        ranks.append(parse_qs_subject_rank(i + 1, browser))

    return ranks


def parse_wu_rank(browser: WebDriver):
    try:
        _ = browser.find_element_by_id(WURank.ELEM)
    except NoSuchElementException:
        return None

    browser.execute_script('document.querySelector("#{}").click()'.format(WURank.ELEM))
    time.sleep(WAIT_TIME)

    tree = etree.HTML(browser.page_source)
    rank = tree.xpath(WURank.RANK)[0].strip()
    overall = tree.xpath(WURank.OVERALL)[0].strip()
    alumni_outcomes = tree.xpath(WURank.ALUMNI_OUTCOMES)[0].strip()
    diversity = tree.xpath(WURank.DIVERSITY)[0].strip()
    employability = tree.xpath(WURank.EMPLOYABILITY)[0].strip()
    thought_leadership = tree.xpath(WURank.THOUGHT_LEADERSHIP)[0].strip()
    value_for_money = tree.xpath(WURank.VALUE_FOR_MONEY)[0].strip()

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    years = tree.xpath(Rank.YEARS)
    ranks = tree.xpath(Rank.RANKS)

    return WURank(
        rank=rank,
        overall=overall,
        alumni_outcomes=alumni_outcomes,
        diversity=diversity,
        employability=employability,
        thought_leadership=thought_leadership,
        value_for_money=value_for_money,
        years=years,
        ranks=ranks
    )


def parse_us_uni_rank(browser: WebDriver):
    try:
        _ = browser.find_element_by_id(USUniRank.ELEM)
    except NoSuchElementException:
        return None

    browser.execute_script('document.querySelector("#{}").click()'.format(USUniRank.ELEM))
    time.sleep(WAIT_TIME)
    tree = etree.HTML(browser.page_source)
    rank = tree.xpath(USUniRank.RANK)[0].strip()
    num = len(tree.xpath(USUniRank.NUM))
    indicators = [''] * 5

    for i in range(num):
        indicators[i] = tree.xpath(USUniRank.INDICATORS[i])[0].strip()

    if num == 5:
        overall = indicators[0]
        research = indicators[1]
        learning_experience = indicators[2]
        diversity = indicators[3]
        employability = indicators[4]
    else:
        overall = ''
        research = indicators[0]
        learning_experience = indicators[1]
        diversity = indicators[2]
        employability = indicators[3]

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    years = tree.xpath(Rank.YEARS)
    ranks = tree.xpath(Rank.RANKS)

    return USUniRank(
        rank=rank,
        overall=overall,
        research=research,
        learning_experience=learning_experience,
        diversity=diversity,
        employability=employability,
        years=years,
        ranks=ranks
    )


def parse_ge_rank(browser: WebDriver):
    try:
        _ = browser.find_element_by_id(GERank.ELEM)
    except NoSuchElementException:
        return None

    browser.execute_script('document.querySelector("#{}").click()'.format(GERank.ELEM))
    time.sleep(WAIT_TIME)

    indicators = [''] * 6
    tree = etree.HTML(browser.page_source)
    num = len(tree.xpath(Rank.NUM))
    rank = tree.xpath(GERank.RANK)[0].strip()

    for i in range(num):
        indicators[i] = tree.xpath(GERank.INDICATORS[i])[0].strip()

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    years = tree.xpath(Rank.YEARS)
    ranks = tree.xpath(Rank.RANKS)

    return GERank(
        rank=rank,
        overall=indicators[0],
        employer_reputation=indicators[1],
        alumni_outcomes=indicators[2],
        partnerships=indicators[3],
        es_connections=indicators[4],
        ge_rate=indicators[5],
        years=years,
        ranks=ranks
    )


def parse_asian_rank(browser: WebDriver):
    try:
        _ = browser.find_element_by_id(AURank.ELEM)
    except NoSuchElementException:
        return None

    browser.execute_script('document.querySelector("#{}").click()'.format(AURank.ELEM))
    time.sleep(WAIT_TIME)

    indicators = [''] * len(AURank.INDICATORS)
    tree = etree.HTML(browser.page_source)
    num = len(tree.xpath(Rank.NUM))
    rank = tree.xpath(AURank.RANK)[0].strip()

    for i in range(num):
        indicators[i] = tree.xpath(AURank.INDICATORS[i])[0].strip()

    browser.execute_script('document.querySelector("{}").click()'.format(Rank.DATA_BTN))
    years = tree.xpath(Rank.YEARS)
    ranks = tree.xpath(Rank.RANKS)

    return AURank(
        rank=rank,
        overall=indicators[0],
        academic_reputation=indicators[1],
        employer_reputation=indicators[2],
        fs_ratio=indicators[3],
        inter_faculty=indicators[4],
        inter_students=indicators[5],
        fs_with_phd=indicators[6],
        papers_per_faculty=indicators[7],
        citations_per_paper=indicators[8],
        outbound_exchange=indicators[9],
        inbound_exchange=indicators[10],
        inter_rn=indicators[11],
        years=years,
        ranks=ranks
    )


def get_one_university(browser: WebDriver, url: str) -> University:
    tree = etree.HTML(browser.page_source)

    title = tree.xpath(University.TITLE)[0].strip()
    status = tree.xpath(University.STATUS)[0].strip()
    research_output = tree.xpath(University.RESEARCH_OUTPUT)[0].strip()
    sf_ratio = tree.xpath(University.SF_RATIO)[0].strip()
    try:
        inter_students = tree.xpath(University.INTER_STUDENTS)[0].strip()
    except IndexError:
        inter_students = ''
    size = tree.xpath(University.SIZE)[0].strip()

    total_students = tree.xpath(University.TOTAL_STUDENTS)[0].strip()
    total_pg_students = tree.xpath(University.TOTAL_PG_STUDENTS)[0].strip()
    total_ug_students = tree.xpath(University.TOTAL_UG_STUDENTS)[0].strip()
    try:
        inter_pg_students = tree.xpath(University.INTER_PG_STUDENTS)[0].strip()
        inter_ug_students = tree.xpath(University.INTER_UG_STUDENTS)[0].strip()
    except IndexError:
        inter_pg_students = ''
        inter_ug_students = ''
    total_faculty_staff = tree.xpath(University.TOTAL_FACULTY_STAFF)[0].strip()
    inter_faculty_staff = tree.xpath(University.INTER_FACULTY_STAFF)[0].strip()
    domes_faculty_staff = tree.xpath(University.DOMES_FACULTY_STAFF)[0].strip()

    scholarships = tree.xpath(University.SCHOLARSHIPS)
    if len(scholarships):
        scholarships = scholarships[0].strip()
    else:
        scholarships = ''

    time.sleep(WAIT_CLICK_EVENT_REGISTER_TIME)  # wait for ajax click event bound to element
    # try:
    #     qs_rank = parse_qs_rank(browser)
    # except Exception:
    #     qs_rank = handle_exception('{}, QS Rank Error!\n'.format(url))

    try:
        qs_subject_ranks = parse_qs_subject_ranks(browser)
    except Exception:
        traceback.format_exc()
        qs_subject_ranks = handle_exception('{}, QS Subject Rank Error!\n'.format(url))

    # try:
    #     wu_rank = parse_wu_rank(browser)
    # except Exception:
    #     wu_rank = handle_exception('{}, WU Rank Error!\n'.format(url))

    # try:
    #     us_uni_rank = parse_us_uni_rank(browser)
    # except Exception:
    #     us_uni_rank = handle_exception('{}, US Uni Error!\n'.format(url))

    # try:
    #     ge_rank = parse_ge_rank(browser)
    # except Exception:
    #     ge_rank = handle_exception('{}, GE Rank Error!\n'.format(url))

    # try:
    #     au_rank = parse_asian_rank(browser)
    # except Exception:
    #     au_rank = handle_exception('{}, Asian University Rank Error!\n'.format(url))

    return University(
        title=title,
        status=status,
        research_output=research_output,
        sf_ratio=sf_ratio,
        scholarships=scholarships,
        inter_students=inter_students,
        size=size,
        total_students=total_students,
        total_pg_students=total_pg_students,
        total_ug_students=total_ug_students,
        inter_pg_students=inter_pg_students,
        inter_ug_students=inter_ug_students,
        total_faculty_staff=total_faculty_staff,
        inter_faculty_staff=inter_faculty_staff,
        domes_faculty_staff=domes_faculty_staff,
        # qs_rank=qs_rank,
        # wu_rank=wu_rank,
        # us_uni_rank=us_uni_rank,
        # ge_rank=ge_rank,
        # au_rank=au_rank,
        qs_subject_ranks=qs_subject_ranks,
    )


def handle_exception(msg: str):
    with open(LOG_FILENAME, 'a') as f:
        f.write(msg)
    # print(msg)
 

def get_all_universities(urls: list[str], browser: WebDriver) -> list[University]:
    res: list[University] = []

    for i, url in enumerate(urls):
        url = url.strip()
        browser.get(url)

        try:
            uni = get_one_university(browser, url)
            # print(uni)
        except Exception:
            traceback.format_exc()
            handle_exception('{} Error!\n'.format(url))
            continue
        res.append(uni)

    return res


# Get all subjects of a single university
def get_one_uni_subjects(browser: WebDriver) -> list[str]:
    time.sleep(WAIT_CLICK_EVENT_REGISTER_TIME)  # wait for ajax click event bound to element
    try:
        _ = browser.find_element_by_id(QSSubjectRank.ELEM)
    except NoSuchElementException:
        return []

    browser.execute_script('document.querySelector("#{}").click()'.format(QSSubjectRank.ELEM))
    time.sleep(0.5)

    tree = etree.HTML(browser.page_source)
    subjects = tree.xpath(QSSubjectRank.SUBJECT_NAMES)

    return subjects


# Get all subjects of all universities
def get_all_subjects(urls: list[str], browser: WebDriver):
    res: list[str] = []

    for i, url in enumerate(urls):
        url = url.strip()
        browser.get(url)
        res += get_one_uni_subjects(browser)
        print('{}/1300'.format(i + 1))
    
    print('Total subjects types: {}'.format(len(res)))
    res: set = set(res)
    print('Total subjects types: (without repetition) {}'.format(len(res)))
    with open('subjects.txt', 'w') as f:
        for i in res:
            f.write('{}\n'.format(i))


def init_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.managed_default_content_settings.images': 2
    }
    options.add_experimental_option('prefs', prefs)
    return webdriver.Chrome(options=options)


def main():
    browser = init_driver()
    urls = get_all_urls_from_file('1.txt')[:1]
    unis = get_all_universities(urls, browser)
    save_to_excel(unis, 'res_1.xlsx')


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print('{} minutes.'.format((end_time - start_time) / 60))
