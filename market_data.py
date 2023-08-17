import time
from base import (
    click_on_match_data,
    get_match_counter,
    match_selector,
    open_new_tab,
    remove_cookies,
    selector_finder,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

parent_list = []
FINAL_COUNT, TOTAL_COUNT = 0, 0


def get_key_data(key_data):
    return [key.text for key in key_data]


def get_sub_data(sub_data_part):
    return [
        sub_element.text
        for sub_element in sub_data_part.find_elements(
            # By.CLASS_NAME, "bbm-BetBuilderParticipant_Odds"
            By.CLASS_NAME, "bbl-BetBuilderParticipant_Odds"
        )
    ]


def multi_sub_menu_data(driver, idx, selector, sub_headling):
    heading = []
    sub_data = []
    key_data = []
    actions = ActionChains(driver)
    time.sleep(3)
    if (
            len(
                driver.find_elements(
                    # By.CSS_SELECTOR, ".bbw-FilteredMarketOddsHScroller_LeftButton"
                    By.CSS_SELECTOR, ".bbl-FilteredMarketOddsHScroller_LeftButton"
                )
            )
            > 0
    ):
        for _ in range(
                len(
                    driver.find_elements(
                        # By.CSS_SELECTOR, ".bbw-FilteredMarketOddsHScroller_LeftButton"
                        By.CSS_SELECTOR, ".bbl-FilteredMarketOddsHScroller_LeftButton"
                    )
                )
                + 1
        ):
            actions.click(
                driver.find_elements(
                    # By.CSS_SELECTOR, ".bbw-FilteredMarketOddsHScroller_LeftButton"
                    By.CSS_SELECTOR, ".bbl-FilteredMarketOddsHScroller_LeftButton"
                )[0]
            )
            actions.perform()

    for counter, i in enumerate(selector):
        if (
                # len(selector_finder(driver, By.CSS_SELECTOR, ".bbm-ShowMoreForHScroll"))
                len(selector_finder(driver, By.CSS_SELECTOR, ".bbl-ShowMoreForHScroll"))
                >= 0
                and counter < 1
        ):
            actions = ActionChains(driver)
            actions.move_to_element(
                # selector_finder(driver, By.CSS_SELECTOR, ".bbm-ShowMoreForHScroll")[0]
                selector_finder(driver, By.CSS_SELECTOR, ".bbl-ShowMoreForHScroll")[0]
            )
            actions.click(
                # selector_finder(driver, By.CSS_SELECTOR, ".bbm-ShowMoreForHScroll")[0]
                selector_finder(driver, By.CSS_SELECTOR, ".bbl-ShowMoreForHScroll")[0]
            )
            actions.perform()
            key_data = get_key_data(
                selector_finder(
                    # driver, By.CSS_SELECTOR, ".bbw-BetBuilderParticipantLabel"
                    driver, By.CSS_SELECTOR, ".bbl-BetBuilderParticipantLabel_Name"
                )
            )
        heading.append(i.text)
        sub_data.append(
            get_sub_data(
                selector_finder(
                    driver,
                    By.CSS_SELECTOR,
                    # ".bbw-FilteredMarketOddsHScroller_Contents>div",
                    ".bbl-FilteredMarketOddsHScroller_Contents>div",
                )[counter]
            )
        )
        if (
                len(
                    driver.find_elements(
                        # By.CSS_SELECTOR, ".bbw-FilteredMarketOddsHScroller_RightButton"
                        By.CSS_SELECTOR, ".bbl-FilteredMarketOddsHScroller_RightButton"
                    )
                )
                > 0
        ):
            actions.click(
                driver.find_elements(
                    # By.CSS_SELECTOR, ".bbw-FilteredMarketOddsHScroller_RightButton"
                    By.CSS_SELECTOR, ".bbl-FilteredMarketOddsHScroller_RightButton"
                )[0]
            )
            actions.perform()

    formatted_data = []

    for i in range(len(key_data)):
        player_data = {
            heading[j]: sub_data[j][i]
            if j < len(sub_data) and i < len(sub_data[j])
            else ""
            for j in range(len(heading))
        }
        formatted_data.append({key_data[i]: player_data})

    return {sub_headling.text: formatted_data}


def multi_data(driver):
    selector = selector_finder(driver, By.CLASS_NAME, "gl-MarketGroupButton_Text")
    multiple_data = []
    group_btn = [btn_txt.text for btn_txt in selector[:2]]
    if "Goalscorer" in group_btn or "Disposals" in group_btn:
        for i in range(2):
            parent_key = selector[i].text
            if i == 1:
                click_on_match_data(driver, selector)
                time.sleep(3)
            click_on_match_data(driver, selector, i)
            # headling_one = selector_finder(
            #     driver, By.CSS_SELECTOR, ".bbw-MarketColumnHeader40Scrolled_Label"
            # )
            #
            # sub_headling_lst = selector_finder(
            #     driver, By.CSS_SELECTOR, ".bbw-TabSwitcherItem"
            # )

            headling_one = selector_finder(
                driver, By.CSS_SELECTOR, ".bbl-MarketColumnHeader40Scrolled_Label "
            )

            sub_headling_lst = selector_finder(
                driver, By.CSS_SELECTOR, ".bbl-TabSwitcherItem_TabText "
            )
            merge_data = []
            for j, value in enumerate(sub_headling_lst):
                if j == 0:
                    merge_data.append(
                        multi_sub_menu_data(driver, j, headling_one, value)
                    )
                if j == 1:
                    time.sleep(3)
                    sub_headling_lst[j].click()
                    # headling_two = selector_finder(
                    #     driver,
                    #     By.CSS_SELECTOR,
                    #     ".bbw-MarketColumnHeader50Scrolled_Label,.bbw-MarketColumnHeader40Scrolled ",
                    # )
                    headling_two = selector_finder(
                        driver,
                        By.CSS_SELECTOR,
                        ".bbl-MarketColumnHeader50Scrolled_Label, .bbl-MarketColumnHeader40Scrolled_Label ",
                    )
                    merge_data.append(
                        multi_sub_menu_data(driver, j, headling_two, value)
                    )
            multiple_data.append({parent_key: merge_data})
            time.sleep(3)
    return multiple_data


def game_data(driver, match_name="", flag=False):
    data_dict = {}
    main_key, sub_key, data = [], [], []

    time.sleep(3)
    sub_key = (
        driver.find_element(By.CSS_SELECTOR, ".gl-MarketGroupContainer > .gl-Market_General-haslabels")
        .text.strip()
        .split("\n")
    )
    time.sleep(3)
    data_value_lst = selector_finder(
        driver,
        By.CSS_SELECTOR,
        ".cm-CouponMarketGrid>.gl-MarketGroup .gl-MarketGroup_Wrapper .gl-MarketGroupContainer>.gl-Market_General-pwidth33-333:not(.gl-Market_General-haslabels)>.srb-ParticipantCenteredStackedMarketRow",
    )
    data.extend(
        data_value.text.replace("\n", " ").strip() for data_value in data_value_lst[:6]
    )

    main_key_value = selector_finder(
        driver,
        By.CSS_SELECTOR,
        ".cm-CouponMarketGrid>.gl-MarketGroup .gl-MarketGroup_Wrapper .gl-MarketGroupContainer>.gl-Market_General-pwidth33-333:not(.gl-Market_General-haslabels)>.gl-MarketColumnHeader",
    )
    main_key.extend(
        main_key_value.text.strip() for main_key_value in main_key_value[:3]
    )
    for key in main_key:
        index = main_key.index(key)
        values = data[index * len(sub_key): (index + 1) * len(sub_key)]
        data_dict[key] = dict(zip(sub_key, values))
    market_data = {"main_market_data": data_dict}
    parent_key = driver.find_element(By.CSS_SELECTOR, ".sph-EventHeader_Label").text
    parent_list.append(parent_key)
    return {parent_key: market_data}, parent_key


def live_selector_check(driver, selector, i):
    try:
        time.sleep(5)
        if selector[i].find_element(By.CSS_SELECTOR, ".pi-ScoreVariantSingleParticipant5 ").text:
            return True
        return False
    except Exception as e:
        return False


def get_main_market_data(driver, user_range):
    global TOTAL_COUNT
    match_selector(driver)

    selector, TOTAL_COUNT = get_match_counter(driver)
    print(TOTAL_COUNT)
    # range_data = TOTAL_COUNT // 2

    match_name = driver.find_element(
        By.CSS_SELECTOR, ".sph-EventHeader_Label, .sph-EventHeader_HeaderText"
    ).text
    remove_cookies(driver)

    main_data = []
    multi_market_data = []
    # TOTAL_COUNT = 2
    for i in range(TOTAL_COUNT):
        print(i)
        if live_selector_check(driver,selector, i):
            # FINAL_COUNT -= 1
            selector[i] = "Live match"
            main_data.append({"Live match": "Live match"})
            multi_market_data.append({"Live match": "Live match"})
            continue
        if i >= 1:
            selector, TOTAL_COUNT = get_match_counter(driver)
            # selector = selector[i:]
            # selector = selector[:range_data] if user_range else selector[range_data:]

        click_on_match_data(driver, selector, i)
        open_new_tab(driver, driver.current_url)
        match_wise_data, match_key = game_data(driver)
        main_data.append(match_wise_data)

        selector = selector_finder(
            driver,
            By.CLASS_NAME,
            "sph-MarketGroupNavBarButtonNew",
        )
        click_on_match_data(driver, selector)
        open_new_tab(driver, driver.current_url)
        multi_market_data.append(multi_data(driver))
        driver.execute_script(
            "return arguments[0].scrollIntoView(true);",
            driver.find_element(By.TAG_NAME, "body"),
        )
        selector = driver.find_element(By.CLASS_NAME, "sph-Breadcrumb")
        action = ActionChains(driver)
        action.move_to_element(selector)
        action.click(selector)
        action.perform()

        open_new_tab(driver, driver.current_url)
        main_data[i].get(match_key)["multi_market_data"] = multi_market_data[i]

    return match_name, main_data
