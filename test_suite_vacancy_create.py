from pages import *
from setup import *
import pytest


class TestSuite:
    """
    Тест на создание вакансий.
    Создаёт вакансии любых типов, в зависмости от выбранного набора входных данных (параметр для json)
    """
    driver = webdriver.Chrome(Settings.path_to_driver)

    @classmethod
    def setup_class(cls):
        cls.driver.maximize_window()
        cls.driver.get(Links.main_page)
        cls.account = get_data_by_number(load_data("gossluzhba1.qtestweb.office.quarta-vk.ru"), "accounts", 3)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def go_to(self, url):
        while self.driver.current_url != url:
            self.driver.get(url)
            sleep(.1)
        print("Переход по ссылке: %s" % url)

    @pytest.mark.parametrize("order", [1, 2, 3, 4, 5, 6])
    def test_vacancy_create(self, order):
        data = load_data("gossluzhba1.qtestweb.office.quarta-vk.ru")["advertisements"][order]

        LoginPage(self.driver).login(self.account["username"], self.account["password"], self.account["fullName"])
        self.go_to(Links.vacancy_list)
        page = VacancyCreatePage(self.driver)
        page.click_by_text("Создать")
        sleep(1)
        page.type_vacancy(data["type_vacancy"])
        page.organization(data["organization"])
        page.wait_for_text_appear("Структурное подразделение")
        if order == 1:
            page.is_competition(data["is_competition"])
            sleep(1)
            page.post_is_competition.structural_unit(data["structural_unit"])
            page.post_is_competition.sub_structural(data["sub_structural"])
            page.post_is_competition.staff_unit(data["staff_unit"])
            page.post_is_competition.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.post_is_competition.position_category(data["position_category"])
            page.post_is_competition.position_group(data["position_group"])
            page.post_is_competition.okato_region(data["okato_region"])
            page.post_is_competition.okato_area(data["okato_area"])
            page.salary_from(data["salary_from"])
            page.salary_to(data["salary_to"])
            sleep(1)
            page.post_is_competition.business_trip(data["business_trip"])
            sleep(1)
            page.post_is_competition.work_day(data["work_day"])
            page.post_is_competition.work_schedule(data["work_schedule"])
            page.post_is_competition.work_contract(data["work_contract"])
            page.social_package_text(data["social_package_text"])
            page.post_is_competition.social_package_files(data["social_package_files"])
            sleep(1)
            page.additional_position_info_text(data["additional_position_info_text"])
            page.post_is_competition.additional_position_info_file(data["additional_position_info_file"])
            page.scroll_to_top()
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.post_is_competition.job_responsibility_files(data["job_responsibility_files"])
            page.post_is_competition.position_rules_files(data["position_rules_files"])
            page.click_by_text("Квалификационные требования")
            page.post_is_competition.education_level(data["education_level"])
            page.post_is_competition.government_experience(data["government_experience"])
            page.post_is_competition.professional_experience(data["professional_experience"])
            page.knowledge_description_text(data["knowledge_description_text"])
            page.post_is_competition.knowledge_description_files(data["knowledge_description_files"])
            page.additional_requirements(data["additional_requirements"])
            page.post_is_competition.test(data["test"])
            page.click_by_text("Документы", 2)
            page.announcement_date()
            page.expiry_date(data["expiry_date"])
            page.registration_address(data["registration_address"])
            page.registration_time(data["registration_time"])
            page.click_by_text("Добавить")
            page.post_is_competition.document_type(data["document_type"])
            page.description(data["description"])
            page.post_is_competition.template_file(data["template_file"])
            sleep(1)
            page.click_by_text("Добавить", 2)
            sleep(1)
            page.set_checkbox_by_order(4, False)
            page.sel()
            page.delete()
            sleep(1)
            page.click_by_text("Контакты")
            page.wait_for_text_appear("Почтовый адрес")
            page.post_is_competition.organization_address(data["organization_address"])
            page.address_mail(data["address_mail"])
            page.phone(data["phone"])
            page.phone2(data["phone2"])
            page.phone3(data["phone3"])
            page.email(data["email"])
            page.contact_person_other(data["contact_person_other"])
            page.web(data["web"])
            page.additional_info_text(data["additional_info_text"])
            sleep(0.5)
            page.post_is_competition.additional_info_files(data["additional_info_files"])
        if order == 2:
            page.reason(data["reason"])
            page.post_is_competition.structural_unit(data["structural_unit"])
            page.post_is_competition.sub_structural(data["sub_structural"])
            page.post_is_competition.staff_unit(data["staff_unit"])
            page.post_is_competition.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.post_is_competition.position_category(data["position_category"])
            page.post_is_competition.position_group(data["position_group"])
            page.post_is_competition.okato_region(data["okato_region"])
            page.post_is_competition.okato_area(data["okato_area"])
            page.salary_from(data["salary_from"])
            page.salary_to(data["salary_to"])
            sleep(1)
            page.post_is_competition.business_trip(data["business_trip"])
            sleep(1)
            page.post_is_competition.work_day(data["work_day"])
            page.post_is_competition.work_schedule(data["work_schedule"])
            page.post_is_competition.work_contract(data["work_contract"])
            page.social_package_text(data["social_package_text"])
            page.post_is_competition.social_package_files(data["social_package_files"])
            sleep(1)
            page.additional_position_info_text(data["additional_position_info_text"])
            page.post_is_competition.additional_position_info_file(data["additional_position_info_file"])
            page.scroll_to_top()
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.post_is_competition.job_responsibility_files(data["job_responsibility_files"])
            page.post_is_competition.position_rules_files(data["position_rules_files"])
            page.click_by_text("Квалификационные требования")
            page.post_is_competition.education_level(data["education_level"])
            page.post_is_competition.government_experience(data["government_experience"])
            page.post_is_competition.professional_experience(data["professional_experience"])
            page.knowledge_description_text(data["knowledge_description_text"])
            page.post_is_competition.knowledge_description_files(data["knowledge_description_files"])
            page.additional_requirements(data["additional_requirements"])
            page.post_is_competition.test(data["test"])
            page.click_by_text("Документы", 2)
            page.announcement_date()
            page.expiry_date(data["expiry_date"])
            page.registration_address(data["registration_address"])
            page.registration_time(data["registration_time"])
            page.click_by_text("Добавить")
            page.post_is_competition.document_type(data["document_type"])
            page.description(data["description"])
            page.post_is_competition.template_file(data["template_file"])
            sleep(1)
            page.click_by_text("Добавить", 2)
            sleep(1)
            page.set_checkbox_by_order(4, False)
            page.sel()
            page.delete()
            sleep(1)
            page.click_by_text("Контакты")
            page.wait_for_text_appear("Почтовый адрес")
            page.post_is_competition.organization_address(data["organization_address"])
            page.address_mail(data["address_mail"])
            page.phone(data["phone"])
            page.phone2(data["phone2"])
            page.phone3(data["phone3"])
            page.email(data["email"])
            page.contact_person_other(data["contact_person_other"])
            page.web(data["web"])
            page.additional_info_text(data["additional_info_text"])
            sleep(0.5)
            page.post_is_competition.additional_info_files(data["additional_info_files"])
        if order == 3:
            page.reserve_post.reserve(data["reserve"])
            page.reserve_post.structural_unit(data["structural_unit"])
            page.reserve_post.sub_structural(data["sub_structural"])
            page.reserve_post.post(data["post"])
            page.reserve_post.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.reserve_post.reserve_group(data["reserve_group"])
            page.reserve_post.okato_region(data["okato_region"])
            page.reserve_post.okato_area(data["okato_area"])
            page.salary_from(data["salary_from"])
            page.salary_to(data["salary_to"])
            sleep(1)
            page.reserve_post.business_trip(data["business_trip"])
            sleep(1)
            page.reserve_post.work_day(data["work_day"])
            page.reserve_post.work_schedule(data["work_schedule"])
            page.reserve_post.work_contract(data["work_contract"])
            page.social_package_text(data["social_package_text"])
            page.reserve_post.social_package_files(data["social_package_files"])
            page.additional_position_info_text(data["additional_position_info_text"])
            page.reserve_post.additional_position_info_file(data["additional_position_info_file"])
            page.scroll_to_top()
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.reserve_post.job_responsibility_files(data["job_responsibility_files"])
            page.reserve_post.position_rules_files(data["position_rules_files"])
            page.click_by_text("Квалификационные требования")
            page.reserve_post.education_level(data["education_level"])
            page.reserve_post.government_experience(data["government_experience"])
            page.reserve_post.professional_experience(data["professional_experience"])
            page.knowledge_description_text(data["knowledge_description_text"])
            page.reserve_post.knowledge_description_files(data["knowledge_description_files"])
            page.additional_requirements(data["additional_requirements"])
            page.reserve_post.test(data["test"])
            page.click_by_text("Документы", 2)
            page.announcement_date()
            page.expiry_date(data["expiry_date"])
            page.registration_address(data["registration_address"])
            page.registration_time(data["registration_time"])
            page.click_by_text("Добавить")
            page.reserve_post.document_type(data["document_type"])
            page.description(data["description"])
            page.reserve_post.template_file(data["template_file"])
            sleep(1)
            page.click_by_text("Добавить", 2)
            sleep(1)
            page.set_checkbox_by_order(3, False)
            page.sel()
            page.delete()
            sleep(1)
            page.click_by_text("Контакты")
            page.wait_for_text_appear("Почтовый адрес")
            page.reserve_post.organization_address(data["organization_address"])
            page.address_mail(data["address_mail"])
            page.phone(data["phone"])
            page.phone2(data["phone2"])
            page.phone3(data["phone3"])
            page.email(data["email"])
            page.contact_person_other(data["contact_person_other"])
            page.web(data["web"])
            page.additional_info_text(data["additional_info_text"])
            sleep(0.5)
            page.reserve_post.additional_info_files(data["additional_info_files"])
        if order == 4:
            page.reserve_group_posts.reserve(data["reserve"])
            page.reserve_group_posts.structural_unit(data["structural_unit"])
            page.reserve_group_posts.sub_structural(data["sub_structural"])
            page.reserve_group_posts.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.reserve_group_posts.reserve_group(data["reserve_group"])
            page.reserve_group_posts.okato_region(data["okato_region"])
            page.reserve_group_posts.okato_area(data["okato_area"])
            page.salary_from(data["salary_from"])
            page.salary_to(data["salary_to"])
            sleep(1)
            page.reserve_group_posts.business_trip(data["business_trip"])
            sleep(1)
            page.reserve_group_posts.work_day(data["work_day"])
            page.reserve_group_posts.work_schedule(data["work_schedule"])
            page.reserve_group_posts.work_contract(data["work_contract"])
            page.social_package_text(data["social_package_text"])
            page.reserve_group_posts.social_package_files(data["social_package_files"])
            page.additional_position_info_text(data["additional_position_info_text"])
            page.reserve_group_posts.additional_position_info_file(data["additional_position_info_file"])
            page.scroll_to_top()
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.reserve_group_posts.job_responsibility_files(data["job_responsibility_files"])
            page.reserve_group_posts.position_rules_files(data["position_rules_files"])
            page.click_by_text("Квалификационные требования")
            page.reserve_group_posts.education_level(data["education_level"])
            page.reserve_group_posts.government_experience(data["government_experience"])
            page.reserve_group_posts.professional_experience(data["professional_experience"])
            page.knowledge_description_text(data["knowledge_description_text"])
            page.reserve_group_posts.knowledge_description_files(data["knowledge_description_files"])
            page.additional_requirements(data["additional_requirements"])
            page.reserve_group_posts.test(data["test"])
            page.click_by_text("Документы", 2)
            page.announcement_date()
            page.expiry_date(data["expiry_date"])
            page.registration_address(data["registration_address"])
            page.registration_time(data["registration_time"])
            page.click_by_text("Добавить")
            page.reserve_group_posts.document_type(data["document_type"])
            page.description(data["description"])
            page.reserve_group_posts.template_file(data["template_file"])
            sleep(1)
            page.click_by_text("Добавить", 2)
            sleep(1)
            page.set_checkbox_by_order(3, False)
            page.sel()
            page.delete()
            sleep(1)
            page.click_by_text("Контакты")
            page.wait_for_text_appear("Почтовый адрес")
            page.reserve_group_posts.organization_address(data["organization_address"])
            page.address_mail(data["address_mail"])
            page.phone(data["phone"])
            page.phone2(data["phone2"])
            page.phone3(data["phone3"])
            page.email(data["email"])
            page.contact_person_other(data["contact_person_other"])
            page.web(data["web"])
            page.additional_info_text(data["additional_info_text"])
            sleep(0.5)
            page.reserve_group_posts.additional_info_files(data["additional_info_files"])
        if order == 5:
            page.vacant_study.structural_unit(data["structural_unit"])
            page.vacant_study.sub_structural(data["sub_structural"])
            page.vacant_study.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.vacant_study.position_category(data["position_category"])
            page.vacant_study.position_group(data["position_group"])
            page.vacant_study.okato_region(data["okato_region"])
            page.vacant_study.okato_area(data["okato_area"])
            page.salary_from(data["salary_from"])
            page.salary_to(data["salary_to"])
            sleep(1)
            page.vacant_study.business_trip(data["business_trip"])
            sleep(1)
            page.vacant_study.work_schedule(data["work_schedule"])
            page.vacant_study.work_day(data["work_day"])
            page.vacant_study.work_contract(data["work_contract"])
            page.social_package_text(data["social_package_text"])
            page.vacant_study.social_package_files(data["social_package_files"])
            page.additional_position_info_text(data["additional_position_info_text"])
            page.vacant_study.additional_position_info_file(data["additional_position_info_file"])
            page.scroll_to_top()
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.vacant_study.job_responsibility_files(data["job_responsibility_files"])
            page.vacant_study.position_rules_files(data["position_rules_files"])
            page.click_by_text("Квалификационные требования")
            page.vacant_study.education_level(data["education_level"])
            page.vacant_study.government_experience(data["government_experience"])
            page.vacant_study.professional_experience(data["professional_experience"])
            page.knowledge_description_text(data["knowledge_description_text"])
            page.vacant_study.knowledge_description_files(data["knowledge_description_files"])
            page.additional_requirements(data["additional_requirements"])
            page.vacant_study.test(data["test"])
            page.click_by_text("Документы", 2)
            page.announcement_date()
            page.expiry_date(data["expiry_date"])
            page.registration_address(data["registration_address"])
            page.registration_time(data["registration_time"])
            page.click_by_text("Добавить")
            page.vacant_study.document_type(data["document_type"])
            page.description(data["description"])
            page.vacant_study.template_file(data["template_file"])
            sleep(1)
            page.click_by_text("Добавить", 2)
            sleep(1)
            page.set_checkbox_by_order(3, False)
            page.sel()
            page.delete()
            sleep(1)
            page.click_by_text("Контакты")
            page.wait_for_text_appear("Почтовый адрес")
            page.vacant_study.organization_address(data["organization_address"])
            page.address_mail(data["address_mail"])
            page.phone(data["phone"])
            page.phone2(data["phone2"])
            page.phone3(data["phone3"])
            page.email(data["email"])
            page.contact_person_other(data["contact_person_other"])
            page.web(data["web"])
            page.additional_info_text(data["additional_info_text"])
            sleep(0.5)
            page.vacant_study.additional_info_files(data["additional_info_files"])
        if order == 6:
            page.vacant_state.structural_unit(data["structural_unit"])
            page.vacant_state.sub_structural(data["sub_structural"])
            page.vacant_state.staff_unit(data["staff_unit"])
            page.vacant_state.work_type(data["work_type"])
            page.work_type_other_text(data["work_type_other_text"])
            page.vacant_state.position_category(data["position_category"])
            page.vacant_state.position_group(data["position_group"])
            page.click_by_text("Должностные обязанности")
            page.job_responsibility_text(data["job_responsibility_text"])
            page.vacant_state.job_responsibility_files(data["job_responsibility_files"])
            page.vacant_state.position_rules_files(data["position_rules_files"])
        page.scroll_to_bottom()
        page.click_by_text("Сохранить")
        page.wait_for_text_appear("Создать")
        assert "Создать" in self.driver.page_source
