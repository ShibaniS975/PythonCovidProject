from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(executable_path="C:\\New Softwares\\NewBrowserEXE\\chromedriver.exe")
driver.maximize_window()

df_covid_data = pd.DataFrame(columns=['Resource', 'Location', 'Details', 'Phone Number', 'Notes'])


def check_element(element_class, element_name):
    try:
        ret_val = element_class.find_element_by_class_name(element_name).text
    except:
        ret_val = 'NA'
    if ret_val == "" or ret_val == " ":
        ret_val = 'NA'
    return ret_val


# defining function
def covid_data(city):
    driver.get("https://verifiedcovidleads.com/")
    sleep(2)
    tab_bar_buttons = driver.find_element_by_id('tabBar').find_elements_by_tag_name('button')
    for i in tab_bar_buttons:
        resource_val = i.text
        print(resource_val)
        i.click()
        driver.find_element_by_class_name("sc-kKXzAB").send_keys(city)

        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(Keys.TAB)
        actions.perform()

        # to avoid error when there is no data in the page
        try:
            category_counter = driver.find_elements_by_xpath("//div[@class ='bottom-area']")
            temp = driver.find_element_by_xpath("//div[@class ='bottom-area']").text
        except:
            category_counter = None

        category_tab_data = []
        category_header = []
        category_title = []
        category_subtitle = []
        category_footer = []
        category_tab_data_filter = []
        category_header_filter = []
        category_title_filter = []
        category_subtitle_filter = []
        category_footer_filter = []

        while category_counter is not None:
            # Loop to get the struct
            previous_element = check_element(category_counter[0], 'card-title')
            previous_category_counter = category_counter

            for catCount in category_counter:
                category_tab_data.append(resource_val)
                category_footer.append(check_element(catCount, 'bottom-right-overlay'))
                category_header.append(check_element(catCount, 'card-header'))
                category_title.append(check_element(catCount, 'card-title'))
                category_subtitle.append(check_element(catCount, 'card-subtitle'))

            driver.execute_script("arguments[0].scrollIntoView();", category_counter[len(category_counter) - 1])
            category_counter = driver.find_elements_by_xpath(".//div[@class ='bottom-area']")

            # Check if more div elements are present - to be scrolled through
            if previous_element == check_element(category_counter[0],
                                                 'card-title') and previous_category_counter == category_counter:
                category_counter = None
            else:
                category_counter = driver.find_elements_by_xpath(".//div[@class ='bottom-area']")

        print("len(category_header)")
        print(len(category_header))

        # Remove duplicate
        #seen = set()
        # Loop through the Title and filter based on the Title
        # (Considering Phone Number [Title] as key for the data)
        for catHeadRange in range(len(category_title)):
            matchfound = 0
            for catHeadFilterRange in range(len(category_title_filter)):
                if category_title_filter[catHeadFilterRange] == category_title[
                       catHeadRange] and category_footer_filter[catHeadFilterRange] == category_footer[
                       catHeadRange] and category_header_filter[catHeadFilterRange] == category_header[
                       catHeadRange] and category_subtitle_filter[catHeadFilterRange] == category_subtitle[
                       catHeadRange]:
                    matchfound = 1
                    break

            if matchfound == 0:
                category_tab_data_filter.append(category_tab_data[catHeadRange])
                category_footer_filter.append(category_footer[catHeadRange])
                category_header_filter.append(category_header[catHeadRange])
                category_title_filter.append(category_title[catHeadRange])
                category_subtitle_filter.append(category_subtitle[catHeadRange])
                # Keeping the Title instance to avoid duplicate
                #seen.add(category_title[catHeadRange])

        # Sort Data based on Location
        for cat_overlay_range in range(len(category_footer_filter)):
            for cat_overlay_range2 in range(len(category_footer_filter)):
                if cat_overlay_range2 > cat_overlay_range:
                    if category_footer_filter[cat_overlay_range2].upper() < category_footer_filter[
                        cat_overlay_range].upper():
                        temp = category_footer_filter[cat_overlay_range2]
                        category_footer_filter[cat_overlay_range2] = category_footer_filter[cat_overlay_range]
                        category_footer_filter[cat_overlay_range] = temp
                        temp = category_header_filter[cat_overlay_range2]
                        category_header_filter[cat_overlay_range2] = category_header_filter[cat_overlay_range]
                        category_header_filter[cat_overlay_range] = temp
                        temp = category_title_filter[cat_overlay_range2]
                        category_title_filter[cat_overlay_range2] = category_title_filter[cat_overlay_range]
                        category_title_filter[cat_overlay_range] = temp
                        temp = category_subtitle_filter[cat_overlay_range2]
                        category_subtitle_filter[cat_overlay_range2] = category_subtitle_filter[cat_overlay_range]
                        category_subtitle_filter[cat_overlay_range] = temp
                        temp = category_tab_data_filter[cat_overlay_range2]
                        category_tab_data_filter[cat_overlay_range2] = category_tab_data_filter[cat_overlay_range]
                        category_tab_data_filter[cat_overlay_range] = temp
                        category_tab_data_filter[cat_overlay_range] = temp

        # store to dataFrame
        for catHeadRange2 in range(len(category_header_filter)):
            df_covid_data.loc[len(df_covid_data)] = [category_tab_data_filter[catHeadRange2],
                                                     category_footer_filter[catHeadRange2],
                                                     category_header_filter[catHeadRange2],
                                                     category_title_filter[catHeadRange2],
                                                     category_subtitle_filter[catHeadRange2]]


covid_data("")
df_covid_data.to_csv('output.csv')
driver.quit()
