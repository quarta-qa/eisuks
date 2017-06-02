from pages import *
import pytest


class TestSuite:
    """
    Данный test-suite включает в себя следующие positive tests закрытого контура:
    1. Авторизация;
    2. Создание нового личного дела;
    3. Заполнение необходимых полей в созданном личном деле;
    4. Создание новой ОШС, добавление подразделения и штатных единиц, введение их в действие;
    5. Назначение ранее созданного личного дела на должность в созданной ОШС;
    6. Добавление денежного содержания сотруднику;
    7. Увольнение сотрудника;
    8. Деавторизация.
    """

    @classmethod
    def setup_class(cls):
        """What happens BEFORE tests"""
        cls.driver = webdriver.Chrome("C:\Python34\Scripts\chromedriver.exe")
        # pages
        cls.main_page = MainPage(cls.driver)
        cls.driver.maximize_window()
        # cls.driver.implicitly_wait(.5)
        cls.driver.get(Links.main_page)
        cls.account = get_data_by_number(load_data("testData"), "accounts")

    @classmethod
    def teardown_class(cls):
        """What happens AFTER tests"""
        cls.driver.quit()

    def go_to(self, url):
        while self.driver.current_url != url:
            self.driver.get(url)
            sleep(.1)
        print("Переход по ссылке: %s" % url)

    @pytest.mark.parametrize("last_name", ["Автоматизация"])
    def te1st_new_personal_file(self, last_name):

        page = PersonalPage(self.driver)
        employee = get_data_by_value(load_data("testData"), "employees", "lastName", last_name)

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.personal_files)
        page.click_by_text("Добавить")
        page.last_name(employee["lastName"])
        page.first_name(employee["firstName"])
        page.middle_name(employee["middleName"])
        page.birthday(employee["birthday"])
        page.insurance_certificate_number(employee["insuranceCertificateNumber"])
        page.username(employee["username"])
        page.click_by_text("Сохранить")
        assert page.wait_for_text_appear("ФИО в падежах")

    @pytest.mark.parametrize("last_name", ["Автоматизация"])
    def te1st_personal_file_filling(self, last_name):

        page = PersonalFilePage(self.driver)
        employee = get_data_by_value(load_data("testData"), "employees", "lastName", last_name)

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.personal_files)
        page.click_by_text("Кандидаты")
        page.click_by_text(last_name)
        page.general_edit()
        page.last_name(employee["lastName"])
        page.first_name(employee["firstName"])
        page.middle_name(employee["middleName"])
        page.personal_file_number(employee["personalFileNumber"])
        page.birthday(employee["birthday"])
        page.okato(employee["okato"])
        page.criminal_record(employee["criminalRecord"])
        page.last_name_changing(employee["lastNameChanging"])
        page.gender(employee["gender"])
        page.click_by_text("Сохранить")
        assert page.wait_for_text_disappear("Сохранить")

    @pytest.mark.parametrize('amount', range(1))
    def te1st_new_department(self, amount):

        data = get_data_by_number(load_data("testData"), "departments")

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.staff_structure)
        page = StructureInfoPage(self.driver)
        page.wait_for_text_appear("Структура")
        page.click_by_text("Добавить")
        # p.organization(data["organization"])
        page.name(data["name"])
        page.fot(data["fot"])
        page.limit(data["limit"])
        page.click_by_text("Сохранить")
        page.click_by_text(data["name"])
        for i in data["divisions"]:
            StructureDetailsPage(self.driver).forming()
            if i["parent"]:
                element = page.wait_for_element_appear((By.XPATH, "//tr[contains(., '%s')]" % i["parent"]))
                element.find_element(By.XPATH, ".//input[@type='checkbox']").click()
            page.click_by_text("Добавить")
            page = DepartmentPage(self.driver)
            page.name(i["name"])
            page.name_genitive(i["nameGenitive"])
            page.name_dative(i["nameDative"])
            page.name_accusative(i["nameAccusative"])
            page.limit(i["limit"])
            page.code(i["code"])
            page.launch_date(i["launchDate"])
            page.order_number(i["orderNumber"])
            page.order_date(i["orderDate"])
            page.click_by_text("Штатная численность")
            for j in i["staffAmount"]:
                page.position(j["position"])
                page.amount(j["amount"])
                page.click_by_text("Добавить", 2)
            page.click_by_text("Сохранить")
        page = StructureDetailsPage(self.driver)
        page.launch()
        page.order_number(data["orderNumber"])
        page.order_date(data["orderDate"])
        page.launch_date(data["date"])
        page.click_by_text("Ввести в действие")
        self.go_to(Links.staff_structure)
        sleep(10)
        page = StructureDetailsPage(self.driver)
        page.click_by_text(data["name"])
        sleep(2)
        page.arrangement()
        page.click_by_text("Показать все")
        page.wait_for_text_appear("Назначить")
        flag = True
        for i in self.driver.find_elements(By.XPATH, "//small[.='Проект']"):
            if i.is_displayed():
                webdriver.ActionChains(self.driver).move_to_element(i).perform()
                flag = False
                break
        assert flag, "Ошибка: На странице присутствует ярлык \"Проект\""

    def tes1t_contest_replacement(self):
        structure_details_page = StructureDetailsPage(self.driver)
        advertisement_page = AdvertisementPage(self.driver)
        vacancy_list_page = VacancyListPage(self.driver)

        department = get_data_by_number(load_data("testData"), "departments")
        advertisement = get_data_by_number(load_data("testData"), "advertisements")

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.staff_structure)
        structure_details_page.click_by_text(department["name"])
        structure_details_page.arrangement()
        structure_details_page.click_by_text("Показать все")
        structure_details_page.click_by_text("Создать", 2)
        # Основная информация
        advertisement_page.type(advertisement["type"])
        advertisement_page.organization(advertisement["organization"])
        advertisement_page.is_competition(advertisement["isCompetition"])
        advertisement_page.reason(advertisement["reason"])
        advertisement_page.division(advertisement["division"])
        advertisement_page.subdivision(advertisement["subdivision"])
        advertisement_page.position(advertisement["position"])
        # Общие сведения
        advertisement_page.profile(advertisement["profile"])
        advertisement_page.okato_region(advertisement["okatoRegion"])
        advertisement_page.okato_area(advertisement["okatoArea"])
        advertisement_page.salary_from(advertisement["salaryFrom"])
        advertisement_page.salary_to(advertisement["salaryTo"])
        advertisement_page.buiseness_trip(advertisement["buisnessTrip"])
        advertisement_page.work_schedule(advertisement["workSchedule"])
        advertisement_page.is_fixed_schedule(advertisement["isFixedSchedule"])
        advertisement_page.work_contract(advertisement["workContract"])
        advertisement_page.guarantee(advertisement["guarantee"])
        advertisement_page.additional_info(advertisement["additionalInfo"])
        # Должностные обязанности
        advertisement_page.click_by_text("Должностные обязанности")
        advertisement_page.job_responsibility(advertisement["jobResponsibility"])
        # Квалификационные требования
        advertisement_page.click_by_text("Квалификационные требования")
        advertisement_page.requirements(advertisement["requirements"])
        advertisement_page.experience(advertisement["experience"])
        advertisement_page.work_experience(advertisement["workExperience"])
        advertisement_page.knowledge_description(advertisement["knowledgeDescription"])
        advertisement_page.additional_requirements(advertisement["additionalRequirements"])
        # Документы
        advertisement_page.click_by_text("Документы", 2)
        advertisement_page.registration_address(advertisement["registrationAddress"])
        advertisement_page.registration_time(advertisement["registrationTime"])
        advertisement_page.expiry_date(change_date(21))
        advertisement_page.announcement_date(today())
        # Контакты
        advertisement_page.click_by_text("Контакты")
        advertisement_page.post_index(advertisement["postIndex"])
        advertisement_page.address_mail(advertisement["addressMail"])
        advertisement_page.phone_1(advertisement["phone1"])
        advertisement_page.phone_2(advertisement["phone2"])
        advertisement_page.phone_3(advertisement["phone3"])
        advertisement_page.email(advertisement["email"])
        advertisement_page.person(advertisement["person"])
        advertisement_page.site(advertisement["site"])
        advertisement_page.additional(advertisement["additional"])
        advertisement_page.click_by_text("Сохранить")
        #
        self.go_to(Links.vacancy_list)
        vacancy_list_page.check()
        vacancy_list_page.click_by_text("На рассмотрение")
        vacancy_list_page.check(2)
        vacancy_list_page.click_by_text("На публикацию")

        LoginPage(self.driver).login("1", "123123/")
        self.main_page.click_by_text("Управление объявлениями")
        vacancy_list_page.check(2)
        self.main_page.click_by_text("Опубликовать")
        LoginPage(self.driver).login("l&m", "123123/")
        self.go_to(Links.main_page)
        sleep(300)
        self.main_page.click_by_text("Вакансии")
        self.main_page.set_text((By.XPATH, "(//input[@type='text'])[2]"), "Automation")
        self.main_page.click((By.XPATH, "//li[.='Automation']"))
        self.main_page.click_by_text("Поиск")
        self.main_page.click((By.XPATH, "//div[@class='vacancy-block vacancy-hovered' and contains(., 'Automation')]"))
        self.main_page.click_by_text("Откликнуться")
        self.main_page.click_by_text("Продолжить")
        self.main_page.set_select("Анкета 667-р 20.07.2015")
        self.main_page.click_by_text("Откликнуться")

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.vacancy_selection)
        self.main_page.click((By.XPATH, "//a[@data-ng-bind='item.responsesCount']"))
        self.main_page.click_by_text("Лобода Максим Юрьевич")
        self.driver.back()
        vacancy_list_page.check()
        self.main_page.click_by_text("Пригласить")
        self.main_page.click_by_text("Направить приглашение")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_appointment(self, user):
        """
        Проверяется возможность назначения сотрудника.
        """
        department = get_data_by_number(load_data("testData"), "departments")
        employee = get_data_by_value(load_data("testData"), "employees", "lastName", user)
        appointment = employee["appointment"]

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = StructureDetailsPage(self.driver)
        self.go_to(Links.staff_structure)
        page.click_by_text(department["name"])
        page.arrangement()
        page.department_select(department["divisions"][0]["name"])
        page.click_by_text("Назначить")

        page = AppointmentPage(self.driver)
        page.full_name(user)
        page.reason(appointment["reason"])
        page.duration(appointment["duration"])
        page.date_from(appointment["dateFrom"])
        page.trial(appointment["trial"])
        page.contract_date(appointment["contractDate"])
        page.contract_number(appointment["contractNumber"])
        page.click_by_text("Сохранить")
        self.go_to(Links.appointment)
        OrdersPage(self.driver).submit(user,
                                       appointment["order"],
                                       appointment["date"],
                                       appointment["fullName"],
                                       appointment["position"])
        self.go_to(Links.staff_structure)
        page = StructureDetailsPage(self.driver)
        page.click_by_text(department["name"])
        page.arrangement()
        page.department_select(department["divisions"][0]["name"])
        page.wait_for_text_appear("Создать")

    # тесты Головинского

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_rewards(self, user):
        """
        Прохождение государственной гражданской службы - Поощрения
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = AwardsPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Все")
        page.click_by_text(user)
        page.click_by_text("Награды и поощрения")

        page.scroll_to_top()
        page.click_by_text("Добавить")
        page.awards.type("Объявление благодарности с выплатой единовременного поощрения")
        page.awards.name("Благодарность Руководителя")
        page.awards.date(today())
        page.awards.amount("10000")
        page.awards.unit("руб.")
        page.awards.note("За эффективную работу")
        page.awards.should_be(True)
        page.awards.submit()

        page.click_by_text("Добавить", 2)
        page.state_awards.type("Присвоение почетных званий Российской Федерации")
        page.state_awards.name("Почетный юрист Российской Федерации")
        page.state_awards.list_date(today())
        page.state_awards.date(today())
        page.state_awards.order_number("159")
        page.state_awards.order_date(today())
        page.state_awards.award_number("")
        page.state_awards.certificate_number("159/951")
        page.state_awards.awarding_date(today())
        page.state_awards.note("")
        page.state_awards.submit()

        page.click_by_text("Добавить", 3)
        page.department_awards.type("Иные виды поощрений")
        page.department_awards.name("Медаль «За отличие в службе» Федеральной службы железнодорожных войск")
        page.department_awards.order_number("523")
        page.department_awards.order_date(today())
        page.department_awards.award_number("12")
        page.department_awards.certificate_number("523/325")
        page.department_awards.awarding_date(today())
        page.department_awards.note("")
        page.department_awards.submit()

        self.go_to(Links.awards)
        OrdersPage(self.driver).submit(user,
                                       "123",
                                       today(),
                                       "Иванов Иван",
                                       "Cпециалист")
        self.go_to(Links.personal_files)
        page.click_by_text("Все")
        page.click_by_text(user)
        page.click_by_text("Награды и поощрения")
        sleep(10)

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_enforcement(self, user):
        """
        Прохождение государственной гражданской службы - Дисциплинарные взыскания
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = EnforcementPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Все")
        page.click_by_text(user)
        page.click_by_text("Взыскания")
        page.scroll_to_top()
        page.click_by_text("Добавить")

        page.reason("Дисциплинарный проступок")
        page.order_number("32")
        page.order_date(today())
        page.period_from(today())
        page.period_to(today())
        page.action_date(today())
        page.action("Опоздание")
        page.explanatory_date(today())
        page.enforcement_reason("За совершение дисциплинарного проступка")
        page.type("Замечание")
        page.copy_date(today())
        page.enforcement_date(today())
        page.click_by_text("Сохранить")

        self.go_to(Links.enforcement)
        OrdersPage(self.driver).submit(user,
                                       "123",
                                       today(),
                                       "Иванов Иван",
                                       "Cпециалист")

        self.go_to(Links.personal_files)
        page.click_by_text("Все")
        page.click_by_text(user)
        page.click_by_text("Взыскания")
        page.scroll_to_top()
        page.table_row_radio()
        page.click_by_text("Редактировать")

        page.enforcement_expire_auto("")
        page.enforcement_expire_date(today())
        page.enforcement_expire_reason("Объявление благодарности")
        page.enforcement_expire_order_date(today())
        page.enforcement_expire_order_number("465")
        page.click_by_text("Сохранить")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_dispensary_planning(self, user):
        """
        Прохождение государственной гражданской службы - Планирование диспансеризации
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = DispensaryPlanningPage(self.driver)
        self.go_to(Links.dispensary_planning)
        page.table_select_user(user)
        page.click_by_text("Включить в диспансеризацию")
        page.date_from(today())
        page.date_to(today())
        page.submit()

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_dispensary(self, user):
        """
        Прохождение государственной гражданской службы - Диспансеризация
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = DispensaryPage(self.driver)
        self.go_to(Links.dispensary_list)
        page.click_by_text("Проект")

        page.click_by_text("Печать приказа о диспансеризации")

        page.table_row_checkbox()
        page.click_by_text("Редактировать")
        page.dispensary_date(today())
        page.reference_date(today())
        page.reference_number("123")
        page.is_healthy(True)
        page.click_by_text("Сохранить")
        page.click_by_text("Назад")

        page.table_row_checkbox()
        page.click_by_text("Редактировать")
        page.dispensary_date(today())
        page.reference_date(today())
        page.reference_number("321")
        page.is_healthy(False)
        page.click_by_text("Сохранить")
        page.click_by_text("Назад")

        page.table_row_checkbox()
        page.click_by_text("Формирование приказа об увольнении")
        self.driver.back()
        page.click_by_text("Назад")

        page.table_row_radio()
        page.click_by_text("Редактировать")
        page.date_from(today())
        page.date_to(today())
        page.order_date(today())
        page.order_number("123")
        page.institution("Лечебное учреждение 1")
        page.by(user)
        page.click_by_text("Сохранить")
        sleep(1)

        page.table_row_radio()
        page.click_by_text("Редактировать")
        page.click_by_text("Утвердить")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_disability_periods(self, user):
        """
        Прохождение государственной гражданской службы - Учет периодов нетрудоспособности
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = DisabilityPeriodsPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Назначенные")
        page.click_by_text(user)
        page.click_by_text("Листки нетрудоспособности")
        page.scroll_to_top()

        page.click_by_text("Добавить")
        page.list_number("232898")
        page.by("Государственное бюджетное учреждение здравоохранения \"Городская поликлиника № 12\"")
        page.period_from("16.03.2016")
        page.period_to("22.03.2016")
        page.reason("Травма")
        page.submit()

        self.go_to(Links.dashboard)
        page.click_by_text("Прохождение государственной гражданской службы")
        page.click_by_text("Учет периодов нетрудоспособности")
        page.click_by_text("Фильтр")
        page.set_text((By.XPATH, "(//input[@type='text'])[8]"), "232898", "Номер листа")
        page.click_by_text("Применить")
        page.table_row_radio()
        page.click_by_text("Редактировать")
        page.editing.reason("Заболевание")
        page.editing.submit()
        page.wait_for_text_appear("Фильтр")
        assert "Заболевание" in self.driver.page_source

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def tes1t_business_trip(self, user):
        """
        Прохождение государственной гражданской службы - Командировки
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = BusinessTripPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Назначенные")
        page.click_by_text(user)
        page.click_by_text("Командировки")
        page.scroll_to_top()

        page.click_by_text("Добавить")
        page.date_start("04.04.2016")
        page.date_end("15.04.2016")
        page.days_amount_without_road("10")
        page.source_financing("За счёт средств выделенных гос. органу")
        page.purpose("Обучение")
        page.reason("Заявление")
        page.route("Москва - Санкт-Петербург")
        page.task_number("137")
        page.task_date("30.03.2016")
        page.click_by_text("Добавить", 2)
        page.routes.country("Россия")
        page.routes.organization("Федеральная таможенная служба")
        page.routes.days_amount("12")
        page.routes.date_start("04.04.2016")
        page.routes.date_end("15.04.2016")
        page.routes.submit()
        page.scroll_to_top()
        page.submit()
        self.go_to(Links.business_trips)
        OrdersPage(self.driver).submit_business_trips(user,
                                                      "127",
                                                      "25.03.2016",
                                                      "Парамонов Лев Петрович",
                                                      "Начальник управления")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_business_trip_schedule(self, user):
        """
        Прохождение государственной гражданской службы - График служебных командировок
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = BusinessTripPage(self.driver)
        self.go_to(Links.business_trips_index)
        page.click_by_text("Фильтр")
        page.set_text((By.XPATH, "(//input[@type='text'])[3]"), user, "ФИО")
        page.click_by_text("Применить")
        assert user in self.driver.page_source

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_holidays(self, user):
        """
        Прохождение государственной гражданской службы - Отпуска на государственной гражданской службе
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = HolidaysPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Назначенные")
        page.click_by_text(user)
        page.click_by_text("Отпуска")
        page.scroll_to_top()
        page.click_by_text("Добавить")

        page.statement_date(today())
        page.base("Заявление")
        page.type("ежегодный отпуск")
        page.date_from(today())
        page.count_days("14")
        page.is_pay_once(True)
        page.is_material_aid(True)
        page.click_by_text("Расчет")
        page.click_by_text("Сохранить")
        page.accept_alert()

        self.go_to(Links.holidays)
        OrdersPage(self.driver).submit(user,
                                       "12",
                                       today(),
                                       "Парамонов Лев Петрович",
                                       "Начальник управления")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_holidays_schedule(self, user):
        """
        Прохождение государственной гражданской службы - График отпусков
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = HolidaysPage(self.driver)
        self.go_to(Links.holidays_schedule)
        page.click_by_text("Включить режим редактирования")
        page.set_select("2017")
        page.click((By.XPATH, "(//span[@class='custom-icon-close'])[1]"))
        page.click((By.XPATH, "(//span[@class='custom-icon-close'])[2]"))
        page.click_by_text("Добавить")
        page.set_date((By.XPATH, "(//input[@type='text'])[1]"), today(), "Дата с")
        page.set_text((By.XPATH, "(//input[@type='text'])[2]"), "14", "Количество дней")
        page.click_by_text("Сохранить")
        page.click_by_text(user)
        page.scroll_to_top()
        page.table_row_radio(2)
        page.click_by_text("Редактировать")
        page.statement_date(today())
        page.base("Заявление")
        page.type("ежегодный отпуск")
        page.date_from(today())
        page.count_days("14")
        page.is_pay_once(True)
        page.is_material_aid(True)
        page.click_by_text("Расчет")
        page.click_by_text("Сохранить")
        page.accept_alert()

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_ranks(self, user):
        """
        Прохождение государственной гражданской службы - Присвоение классных чинов
        """
        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = RanksPage(self.driver)
        self.go_to(Links.personal_files)
        page.click_by_text("Назначенные")
        page.click_by_text(user)
        page.click_by_text("Сведения о чинах и званиях")
        page.scroll_to_top()
        page.click_by_text("Добавить")
        page.set_select("Проект приказа на присвоение классного чина")
        page.condition("Очередной классный чин")
        page.type("Классные чины")
        page.organization("Automation")
        page.date(today())
        page.click_by_text("Сохранить")

        self.go_to(Links.ranks)
        OrdersPage(self.driver).submit(user,
                                       "123",
                                       today(),
                                       "Карякин Игорь Сергеевич",
                                       "Начальник")
        self.go_to(Links.personal_files)
        page.click_by_text("Назначенные")
        page.click_by_text(user)
        page.click_by_text("Сведения о чинах и званиях")
        page.scroll_to_top()

    # end

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def te1st_salary_payments(self, user):
        """
        Формирование кадрового состава - Денежное содержание
        """
        employee = get_data_by_value(load_data("testData"), "employees", "lastName", user)
        salary_payment = employee["salaryPayment"]

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = SalaryPaymentsPage(self.driver)
        self.go_to(Links.personal_files)
        page.search(employee["lastName"])
        page.click_by_text(user)
        page.click_by_text("Денежное содержание")
        page.click_by_text("Добавить")
        page.type(salary_payment["type"])
        page.amount(salary_payment["amount"])
        page.date_from(salary_payment["dateFrom"])
        page.click_by_text("Сохранить")
        page.wait_for_text_disappear("Сохранить")
        page.table_row_radio()
        page.click_by_text("Редактировать")
        page.amount("14")
        page.click_by_text("Сохранить")
        page.table_row_radio()
        page.click_by_text("Удалить")
        page.click_by_text("Да")
        page.click_by_text("Добавить")
        page.type(salary_payment["type"])
        page.amount(salary_payment["amount"])
        page.date_from(salary_payment["dateFrom"])
        page.click_by_text("Сохранить")
        self.go_to(Links.salary_payments)
        OrdersPage(self.driver).submit(user,
                                       salary_payment["order"],
                                       salary_payment["date"],
                                       salary_payment["fullName"],
                                       salary_payment["position"])
        self.go_to(Links.personal_files)
        page.search(user)
        page.click_by_text(user)
        page.click_by_text("Денежное содержание")
        assert "Проект" not in self.driver.page_source

    def te1st_commissions(self):
        """
        Формирование кадрового состава - Комиссии
        """
        page = CommissionsPage(self.driver)
        data = get_data_by_number(load_data("testData"), "commissions")

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        self.go_to(Links.commissions)
        page.click_by_text("Добавить")
        page.name(data["name"])
        page.organization(data["organization"])
        page.order_date(today())
        page.order_number(data["orderNumber"])
        page.full_name(data["fullName"])
        page.type(data["type"])
        page.start_date(today())
        page.end_date(change_date(3))
        page.click_by_text("Сохранить")
        page.table_row_checkbox()
        page.click_by_text("Редактировать")
        for i in data["members"]:
            page.members.click_by_text("Добавить")
            page.members.role(i["role"])
            page.members.full_name(i["fullName"])
            page.members.is_independent_expert(i["isIndependentExpert"])
            page.members.organization(i["organization"])
            page.members.position(i["position"])
            page.members.department(i["department"])
            page.members.phone(i["phone"])
            page.members.email(i["email"])
            page.members.personal_file_number(i["personalFileNumber"])
            page.members.click_by_text("Сохранить")
        for i in data["sessions"]:
            page.sessions.click_by_text("Добавить", 2)
            page.sessions.scroll_to_top()
            page.sessions.meeting_time(i["meeting_time"])
            page.sessions.place(i["place"])
            page.sessions.meeting_date(today())
            page.sessions.click_by_text("Сохранить")
            page.sessions.questions_amount()
            for j in i["questions"]:
                page.sessions.click_by_text("Добавить")
                page.sessions.content(j["content"])
                page.sessions.reporter(j["reporter"])
                page.sessions.click_by_text("Сохранить")
                page.sessions.table_row_checkbox()
                page.sessions.click_by_text("Вынести решение")
                page.sessions.decision(j["decision"])
                page.sessions.decision_reason(j["decisionReason"])
                page.sessions.click_by_text("Сохранить")
                page.sessions.click_by_text("Назад")
        page.click_by_text("Назад")
        page.wait_for_text_appear("Вид комиссии")
        page.table_row_checkbox()
        page.scroll_to_top()
        page.click_by_text("Экспорт")
        page.click_by_text("Удалить")
        page.click_by_text("Да")
        page.wait_for_text_appear("Операция успешно выполнена")
        self.go_to(Links.independent_experts)
        assert page.wait_for_text_appear("Карпов Сергей Иванович")

    @pytest.mark.parametrize("user", ['Автоматизация'])
    def t1est_dismissal(self, user):
        department = get_data_by_number(load_data("testData"), "departments")
        employee = get_data_by_value(load_data("testData"), "employees", "lastName", user)
        dismissal = employee["dismissal"]

        LoginPage(self.driver).login(self.account["username"], self.account["password"])
        page = PersonalFileDismissalPage(self.driver)
        self.go_to(Links.personal_files)
        page.search(user)
        page.click_by_text(user)
        page.click_by_text("Сведения о назначении и освобождении от должности")
        page.check()
        page.click_by_text("Освободить")
        page = DismissalPage(self.driver)
        page.date(dismissal["date"])
        page.reason(dismissal["reason"])
        page.click_by_text("Сохранить")
        self.go_to(Links.dismissal)
        OrdersPage(self.driver).submit(user,
                                       dismissal["order"],
                                       dismissal["date"],
                                       dismissal["fullName"],
                                       dismissal["position"])
        self.go_to(Links.staff_structure)
        page = StructureDetailsPage(self.driver)
        page.click_by_text(department["name"])
        page.arrangement()
        page.click_by_text("Показать все")

    def t1est_rules_list(self):

        LoginPage(self.driver).login("1", "123123/")
        p = MainPage(self.driver)
        p.click_by_text("Список прав")
        assert "Список прав системы безопасности" in self.driver.page_source

    def te1st_roles_management(self):

        LoginPage(self.driver).login("1", "123123/")
        p = MainPage(self.driver)
        p.click_by_text("Управление ролями")
        p.click_by_text("Добавить")
        p.set_text((By.XPATH, "//input[@name='caption']"), "Тестовая роль")
        p.set_select2((By.XPATH, "//div[contains(@id, 's2id')]"), "Высокий")
        p.click_by_text("Сохранить")
        p.set_date((By.XPATH, "//input[@type='search']"), "Тестовая роль")
        # assert "Список прав системы безопасности" in self.driver.page_source

    def te1st_users_management(self):

        LoginPage(self.driver).login("1", "123123/")
        p = MainPage(self.driver)
        p.click_by_text("Управление пользователями")

    def test_example(self):

        page = NewPersonnelFilePage(self.driver)
        LoginPage(self.driver).login("AndRyb", "123123/")
        page.click_by_text("Учет кадрового состава")
        page.click_by_text("Ведение электронных личных дел")
        page.click_by_text("Добавить")
        page.last_name("Иванов")
        page.first_name("Иван")
        page.middle_name("Иванович")
        page.birthday_date("12.04.1970")
        page.certificate_number("00193214196")
        page.account("")
        page.click_by_text("Сохранить")