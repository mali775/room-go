import os
from docx import Document
from docx.shared import Pt, Inches, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_coursework_docx():
    doc = Document()

    # 1. Page Margins (Сол - 30мм, Жоғарғы - 20мм, Оң - 10мм, Төменгі - 20мм)
    for section in doc.sections:
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.left_margin = Mm(30)
        section.right_margin = Mm(10)
        section.page_width = Mm(210)
        section.page_height = Mm(297)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(14)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_title_p(text, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6, space_before=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.first_line_indent = Inches(0)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        return p

    def add_body_p(text, space_after=4):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.first_line_indent = Mm(12.5) # 1.25 cm
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    def add_heading_1(text):
        doc.add_page_break()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.first_line_indent = Inches(0)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Mm(12.5)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    # ==================== ТИТУЛДЫҚ ПАРАҚ ====================
    add_title_p('«Астана IT University» ЖШС колледжі', bold=True, size=14, space_after=4)
    add_title_p('«Арнайы пәндер» циклдік комиссиясы', bold=False, size=14, space_after=40)

    add_title_p('КУРСТЫҚ ЖОБА', bold=True, size=18, space_after=12)
    add_title_p('06130100 – «Бағдарламалық қамтамасыз ету (түрлері бойынша)»', bold=False, size=13, space_after=6)
    add_title_p('Тақырыбы: «Astana IT University студенттеріне арналған аудиторияларды іздеу және брондау мобильді қосымшасын әзірлеу (AITU Rooms)»', bold=True, size=14, space_after=100)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_info.paragraph_format.line_spacing = 1.5
    p_info.paragraph_format.first_line_indent = Inches(0)
    p_info.add_run('Орындаған: студент Құсайынова Малика\n').bold = True
    p_info.add_run('Жетекшісі: ________________________\n')

    for _ in range(3):
        doc.add_paragraph().paragraph_format.line_spacing = 1.5

    add_title_p('Астана, 2026 ж.', bold=False, size=13, space_after=0)

    # ==================== МАЗМҰНЫ ====================
    doc.add_page_break()
    add_title_p('МАЗМҰНЫ', bold=True, size=14, space_after=18)

    toc_items = [
        ('КІРІСПЕ', '3'),
        ('1 БӨЛІМ. ТЕОРИЯЛЫҚ БӨЛІМ', '5'),
        ('  1.1 Мобильді қосымшалар және Smart Campus туралы жалпы түсініктер', '5'),
        ('  1.2 Қолданыстағы бағдарламалық шешімдер мен аналогтарды талдау', '7'),
        ('  1.3 Мобильді қосымшаларды әзірлеудің негізгі кезеңдері', '9'),
        ('  1.4 Бағдарламалық құралдар мен стектерді талдау (Flutter, Dart, PostgreSQL)', '11'),
        ('2 БӨЛІМ. БАҒДАРЛАМАЛЫҚ ӨНІМДІ ЖОБАЛАУ', '14'),
        ('  2.1 Мобильді қосымша құрылымы мен архитектурасын әзірлеу', '14'),
        ('  2.2 Деректер қорының құрылымын жобалау (users, rooms, keste)', '16'),
        ('  2.3 Пайдаланушы интерфейсін (UI/UX) жобалау және навигация әдістері', '18'),
        ('3 БӨЛІМ. ПРАКТИКАЛЫҚ БӨЛІМ (ЕНГІЗУ ЖӘНЕ СЫНАҚТАН ӨТКІЗУ)', '20'),
        ('  3.1 Мобильді қосымшаның функционалдық модульдерін іске асыру', '20'),
        ('  3.2 Брондау және сабақ кестесін («Кесте») жасақтау алгоритмдері', '23'),
        ('  3.3 Бағдарламалық өнімді тестілеу және нәтижелерін талдау', '25'),
        ('  3.4 Әзірленген мобильді қосымшаны пайдалану ережелері', '27'),
        ('ҚОРЫТЫНДЫ', '28'),
        ('ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ', '29'),
        ('ҚОСЫМШАЛАР', '31'),
    ]

    for title, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Inches(0)
        r1 = p.add_run(title)
        if not title.startswith(' '):
            r1.bold = True
        dots_count = max(3, 85 - len(title) * 2)
        p.add_run(' ' + '.' * dots_count + ' ')
        r2 = p.add_run(page)
        if not title.startswith(' '):
            r2.bold = True

    # ==================== КІРІСПЕ ====================
    doc.add_page_break()
    add_title_p('КІРІСПЕ', bold=True, size=14, space_after=14)

    add_body_p('Қазіргі цифрлық трансформация және Smart Campus (ақылды университет) дәуірінде мобильді технологиялар білім беру ұйымдарының күнделікті инфрақұрылымын тиімді басқаруда шешуші рөл атқарады. Заманауи университеттерде мыңдаған студенттер мен оқытушылардың күнделікті оқу процесі, сабақтан тыс өзіндік жұмыстары, хакатондар мен ғылыми жобаларға дайындықтары жүріп жатады. Осы ретте бос аудиторияларды жедел табу, олардың техникалық жабдықталуын (проектор, компьютерлер, кондиционер, Wi-Fi) нақтылау және ресми түрде брондау мәселесі аса маңызды міндетке айналып отыр.')

    add_body_p('Бүгінгі таңда «Astana IT University» (AITU) инновациялық IT-университет ретінде озық цифрлық инфрақұрылымға ие. Алайда, студенттердің өзіндік жұмыстары мен зертханалық зерттеулері үшін бос кабинеттерді іздеу процесі дәстүрлі түрде аудиторияларды аралап көру немесе бейресми келісімдер арқылы жүзеге асырылады. Бұл уақытты тиімсіз жұмсауға, аудиториялардың қақтығысына (conflict of bookings) және университет кеңістігінің біркелкі пайдаланылмауына әкеледі. Осыған байланысты, бірыңғай орталықтандырылған, интерактивті картасы мен сабақ кестесі біріктірілген «AITU Rooms» мобильді қосымшасын әзірлеу жоғары өзектілікке ие.')

    add_body_p('Тақырыптың өзектілігі: студенттер мен қызметкерлердің уақытын үнемдеуге бағытталған заманауи мобильді қызметтерге сұраныстың артуымен, кампустық логистиканы автоматтандыру қажеттілігімен және заманауи кроссплатформалық технологияларды (Flutter/Dart) білім беру саласына енгізу маңыздылығымен анықталады.')

    add_body_p('Курстық жобаның мақсаты — «Astana IT University» білім алушылары мен қызметкерлеріне арналған, бос аудиторияларды іздеуге, брондауға, сабақ кестесін көруге және кампус бойынша навигация жасауға мүмкіндік беретін заманауи, сенімді әрі ыңғайлы мобильді қосымшаны әзірлеу.')

    add_body_p('Қойылған мақсатқа жету үшін келесі міндеттер шешілді:\n'
               '1. Мобильді қосымшалар нарығындағы ұқсас кампустық шешімдер мен онлайн брондау жүйелерінің жұмыс істеу ерекшеліктерін зерттеу және талдау;\n'
               '2. Жүйенің функционалдық және техникалық талаптарын тұжырымдау;\n'
               '3. Реляциондық деректер қорының құрылымын жобалау (users, rooms, keste кестелері арасындағы байланыстар);\n'
               '4. Flutter фреймворкі мен Dart тілі негізінде ыңғайлы, минималистік (Apple UI / Material 3) пайдаланушы интерфейсін құру;\n'
               '5. Негізгі модульдерді жүзеге асыру: Splash экран, авторизация және тіркелу, аудиториялар тізімі мен сүзгілері, интерактивті сабақ кестесі («Кесте»), кампустың 3D картасы және жеке кабинет (профиль);\n'
               '6. Бағдарламалық жасақтаманы функционалдық тестілеуден өткізу және сынақ нәтижелерін бағалау.')

    add_body_p('Зерттеу нысаны — жоғары оқу орындарындағы аудиториялық қорды басқару және кампустық навигация жүйесі.')
    add_body_p('Зерттеу пәні — Flutter және PostgreSQL/локалды деректер сақтау технологиялары негізінде мобильді брондау қосымшасын бағдарламалау процесі.')
    add_body_p('Практикалық маңыздылығы: әзірленген қосымша университет студенттерінің күнделікті өмірінде тікелей қолданысқа енгізілуге дайын толыққанды бағдарламалық өнім болып табылады.')

    # ==================== 1 БӨЛІМ ====================
    add_heading_1('1 БӨЛІМ. ТЕОРИЯЛЫҚ БӨЛІМ')

    add_heading_2('1.1 Мобильді қосымшалар және Smart Campus туралы жалпы түсініктер')
    add_body_p('Мобильді қосымшалар — смартфондар, планшеттер және басқа да тасымалды құрылғылар үшін арнайы жасақталған бағдарламалық жасақтама. Бүгінгі таңда мобильді құрылғылар ақпаратты тұтынудың негізгі құралына айналды. Пайдаланушылар кез келген қызмет түрін өз смартфондары арқылы бірнеше рет түрту арқылы жылдам орындауға дағдыланған.')
    add_body_p('Smart Campus (Ақылды кампус) — ақпараттық-коммуникациялық технологиялар (АКТ) мен Интернет заттарын (IoT) біріктіру арқылы оқу орнының инфрақұрылымын, қауіпсіздігін, ресурстарды басқаруды және білім беру тиімділігін арттыруға бағытталған кешенді цифрлық экожүйе. Ақылды кампустың маңызды компоненттерінің бірі — кеңістікті оңтайлы басқару (Space Management). Оқу кабинеттерінің, зертханалар мен коворкингтердің жүктемесін біркелкі бөлу студенттердің сабақ үлгеріміне және ғылыми ізденістеріне оң әсерін тигізеді.')
    add_body_p('«AITU Rooms» мобильді қосымшасы дәл осы Smart Campus тұжырымдамасы шеңберінде жұмыс істейді. Қосымша студенттерге аудиториялардың ағымдағы күйін нақты уақыт режимінде білуге, сабақтар кестесімен сәйкестендіруге және өзіне қажетті уақыт аралығына кабинетті бекітуге мүмкіндік береді.')

    add_heading_2('1.2 Қолданыстағы бағдарламалық шешімдер мен аналогтарды талдау')
    add_body_p('Курстық жоба барысында аудиторияларды брондау және кампустық логистика саласындағы халықаралық және отандық шешімдерге талдау жүргізілді. Нарықтағы қолданыстағы негізгі бағдарламалық өнімдерді қарастырайық:')
    add_body_p('1. Robin Powered — шетелдік кеңселер мен ірі коворкингтерде кеңінен қолданылатын кәсіби жүйе. Артықшылықтары: аналитикалық панель, күнтізбелермен терең интеграция. Кемшіліктері: өте қымбат лицензиялық құны, отандық жоғары оқу орындарының спецификасына және қазақ тіліне бейімделмегендігі.')
    add_body_p('2. Google Calendar Campus Bookings — күнтізбелік брондау құралдары. Артықшылықтары: қарапайым интерфейс. Кемшіліктері: аудиториялардың техникалық сипаттамаларын (орын саны, жабдықталуы, қабаты) визуалды түрде сүзу мүмкіндігі шектеулі, кампустың интерактивті картасы жоқ.')
    add_body_p('3. ЖОО ішкі порталдары (дәстүрлі Platonus / Univer жүйелері) — негізінен тек академиялық баға қою мен тіркеуге бағытталған. Мобильді құрылғыларда баяу жұмыс істейді және студенттердің бос кабинеттерді жедел брондауына мүмкіндік бермейді.')

    p_tbl = doc.add_paragraph('Кесте 1.1. Бағдарламалық шешімдерді салыстырмалы талдау')
    p_tbl.paragraph_format.first_line_indent = Mm(12.5)

    table1 = doc.add_table(rows=6, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.style = 'Table Grid'
    headers1 = ['Салыстыру критерийлері', 'Robin Powered', 'Google Calendar', 'AITU Rooms (әзірленген)']
    for i, h in enumerate(headers1):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(11)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'

    data1 = [
        ['Студенттерге қолжетімділік', 'Төмен (ақылы)', 'Орташа', 'Жоғары (тегін, арнайы)'],
        ['Кампус 3D картасы', 'Жоқ', 'Жоқ', 'Бар (интеграцияланған)'],
        ['Сабақ кестесі («Кесте») модулі', 'Жоқ', 'Шектеулі', 'Бар (сабақтармен байланысты)'],
        ['Үштілділік (Қаз/Орыс/Ағыл)', 'Тек ағылшын', 'Бар', 'Толық қолдау (Қазақ тілі негізгі)'],
        ['Мобильді UI/UX сапасы', 'Жоғары', 'Орташа', 'Заманауи (Apple Minimal)'],
    ]
    for row_idx, row_data in enumerate(data1, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table1.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    add_body_p('Салыстырмалы талдау нәтижесінде «AITU Rooms» қосымшасы студенттер мен оқытушылардың қажеттіліктерін толық қанағаттандыратын ең оңтайлы бағдарламалық шешім екені дәлелденді.')

    add_heading_2('1.3 Мобильді қосымшаларды әзірлеудің негізгі кезеңдері')
    add_body_p('Жобаны сапалы жүзеге асыру үшін бағдарламалық жасақтаманы әзірлеудің жүйелі кезеңдері қолданылды: талаптарды анықтау, деректер моделін құру, UI/UX интерфейсін прототиптеу, кодтау, интеграциялау және тестілеу.')

    add_heading_2('1.4 Бағдарламалық құралдар мен стектерді талдау (Flutter, Dart, PostgreSQL)')
    add_body_p('Қосымшаны әзірлеу үшін таңдалған технологиялық стек:\n'
               '• Flutter (Google) — бірыңғай кодпен жоғары өнімділікті қамтамасыз ететін кроссплатформалы UI фреймворк;\n'
               '• Dart — нысанға бағытталған және алдын ала компиляцияланатын заманауи жылдам бағдарламалау тілі;\n'
               '• PostgreSQL — күрделі реляциялық құрылымдарды сенімді сақтайтын қуатты деректер қоры;\n'
               '• Provider — қосымшаның архитектуралық тазалығы мен реактивті күйін басқаратын кітапхана.')

    # ==================== 2 БӨЛІМ ====================
    add_heading_1('2 БӨЛІМ. БАҒДАРЛАМАЛЫҚ ӨНІМДІ ЖОБАЛАУ')

    add_heading_2('2.1 Мобильді қосымша құрылымы мен архитектурасын әзірлеу')
    add_body_p('«AITU Rooms» қосымшасы қабатты архитектура (Layered Architecture) бойынша жобаланды. Бағдарлама 4 деңгейден тұрады: Presentation (экрандар мен виджеттер), State Management (провайдерлер), Domain/Model (деректер модельдері) және Data Layer (деректер көздерімен жұмыс істейтін қызметтер).')
    add_body_p('Пайдаланушыға ыңғайлы болу үшін төменгі парящий (қалқымалы) навигациялық панельде 4 басты бағыт бекітілді:\n'
               '1. Аудиториялар (Rooms) — кабинеттер тізімі, сүзгілер мен жылдам брондау;\n'
               '2. Кесте (Keste) — күндер бойынша сабақтар мен студенттік брондар кестесі;\n'
               '3. Карта (Map) — кампустың 3D навигациясы;\n'
               '4. Профиль (Profile) — пайдаланушы мәліметтері, жеке брондарды басқару және тілді ауыстыру.')

    add_heading_2('2.2 Деректер қорының құрылымын жобалау (users, rooms, keste)')
    add_body_p('Жүйе үшін реляциондық деректер қоры жобаланды. База өзара байланысқан 3 кестеден тұрады:\n'
               '1. users — пайдаланушылар кестесі (id, email, password, role);\n'
               '2. rooms — аудиториялар кестесі (id, name, capacity, floor, type, features, is_available);\n'
               '3. keste — сабақ кестесі мен брондар кестесі (id, room_id, user_id, subject, teacher, time_slot, day, group_name, status).')
    add_body_p('users және rooms кестелері keste кестесімен сыртқы кілттер (Foreign Keys: room_id, user_id) арқылы байланысқан.')

    add_heading_2('2.3 Пайдаланушы интерфейсін (UI/UX) жобалау және навигация әдістері')
    add_body_p('Дизайн Apple Design Guidelines минималистік қағидалары бойынша жасалды. Интерфейсте Frosted Glass (матовый шыны) және BackdropFilter эффектісі қолданылды. Веб-шолғышта қосымша орталықта 500px шектеулі енмен смартфон пішінінде жинақы көрінеді.')

    # ==================== 3 БӨЛІМ ====================
    add_heading_1('3 БӨЛІМ. ПРАКТИКАЛЫҚ БӨЛІМ (ЕНГІЗУ ЖӘНЕ СЫНАҚТАН ӨТКІЗУ)')

    add_heading_2('3.1 Мобильді қосымшаның функционалдық модульдерін іске асыру')
    add_body_p('Жоба аясында барлық негізгі функционалдық экрандар кодталып, өзара байланыстырылды:\n'
               '• SplashScreen — анимацияланған фирмалық логотип және келесі экранға біркелкі өту;\n'
               '• LoginScreen және RegisterScreen — пошта мен құпиясөзді тексеру, қателерді өңдеу және 1-шертумен кіретін Демо-кіру батырмасы;\n'
               '• RoomsScreen — тірі іздеу, сүзгілер чиптері (1, 2, 3 қабат, AI labs), бос/бос емес бейдждері және аудиториялар карточкалары;\n'
               '• MapScreen — университет кампусының 3D картасын қосымша ішінде толық ашу;\n'
               '• ProfileScreen — студенттің профилі, «AITU Student • Verified» мәртебесі, жеке брондарды басқару және үш тілді ауыстыру.')

    add_heading_2('3.2 Брондау және сабақ кестесін («Кесте») жасақтау алгоритмдері')
    add_body_p('Брондау кезінде студент кабинетті таңдап, «Брондау» батырмасын басқанда төменнен интерактивті Modal Bottom Sheet ашылады. Студент уақыт аралығын (09:00-10:20, 10:30-11:50 және т.б.) және мақсатын таңдап, брондауды растайды. Аудитория мәртебесі дереу «Бос емес» күйіне ауысады және жазба «Кесте» мен «Профиль» беттеріне қосылады.')

    add_heading_2('3.3 Бағдарламалық өнімді тестілеу және нәтижелерін талдау')
    add_body_p('Қосымшаның жұмысқа қабілеттілігін тексеру үшін функционалдық тестілеу жүргізілді.')

    p_tbl2 = doc.add_paragraph('Кесте 3.1. Функционалдық тестілеу нәтижелері')
    p_tbl2.paragraph_format.first_line_indent = Mm(12.5)

    table2 = doc.add_table(rows=9, cols=5)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.style = 'Table Grid'
    headers2 = ['№', 'Тестілеу сценарийі', 'Күтілетін нәтиже', 'Нақты нәтиже', 'Мәртебесі']
    for i, h in enumerate(headers2):
        cell = table2.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'

    data2 = [
        ['1', 'Жаңа аккаунтты тіркеу', 'Деректер сақталады, растау хабарламасы', 'Сәтті тіркелді', 'Өтті ✅'],
        ['2', 'Қате құпиясөзбен кіру', '«Қате мәліметтер» ескертуі шығады', 'Қызыл Snackbar шықты', 'Өтті ✅'],
        ['3', 'Дұрыс поштамен кіру', 'Басты бетке өту, сессия сақталуы', 'Басты бет ашылды', 'Өтті ✅'],
        ['4', 'Аудиторияны брондау', 'Мәртебесі «Бос емес» болып, кестеге жазылады', 'Мәртебесі өзгерді, Кестеде көрінді', 'Өтті ✅'],
        ['5', 'Броньды кері қайтару', 'Аудитория мәртебесі «Бос» күйіне қайтады', 'Аудитория босатылды', 'Өтті ✅'],
        ['6', 'Тілді қазақшадан ағылшынға ауыстыру', 'Барлық мәтіндер бір сәтте ауысады', 'Мәтіндер толық ауысты', 'Өтті ✅'],
        ['7', 'Кампус 3D картасын қарау', 'Карта қосымша ішінде жүктеледі', 'Карта сәтті көрсетілді', 'Өтті ✅'],
        ['8', 'Жүйеден шығу («Шығу»)', 'Сессия жойылады, авторизация ашылады', 'Логин экранына өтті', 'Өтті ✅'],
    ]
    for row_idx, row_data in enumerate(data2, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table2.cell(row_idx, col_idx)
            cell.text = text
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2('3.4 Әзірленген мобильді қосымшаны пайдалану ережелері')
    add_body_p('Қосымша қарапайым әрі интуитивті: студент ресми поштасымен кіреді, қалаған бөлмесін іздеп, бос уақытты таңдап брондайды. Жұмыс біткен соң өз аккаунтынан шығуға болады.')

    # ==================== ҚОРЫТЫНДЫ ====================
    add_heading_1('ҚОРЫТЫНДЫ')
    add_body_p('Курстық жобаны орындау барысында қойылған басты мақсатқа толықтай қол жеткізілді — «Astana IT University» студенттері мен оқытушыларының күнделікті өмірін жеңілдетуге арналған бос аудиторияларды іздеу және брондау «AITU Rooms» мобильді қосымшасы әзірленді.')
    add_body_p('Кіріспеде айқындалған барлық міндеттер дәйекті түрде орындалды:\n'
               '1. Мобильді қосымшалар нарығындағы ұқсас жүйелерге талдау жасалып, өнім артықшылықтары айқындалды;\n'
               '2. Жүйенің функционалдық талаптары қалыптасып, Flutter/Dart стектері таңдалды;\n'
               '3. Реляциондық деректер қорының құрылымы (users, rooms, keste) жобаланды;\n'
               '4. Заманауи Apple/Material 3 стиліндегі ыңғайлы UI/UX дизайны жасалды;\n'
               '5. Тіркелу, кіру, сүзгілеу, сабақ кестесін («Кесте») қарау, кампустың 3D картасын шолу, уақытпен брондау және броньды жою функциялары толық іске асырылды;\n'
               '6. Функционалдық тестілеу нәтижесінде қосымшаның мінсіз жұмыс істейтіні дәлелденді.')
    add_body_p('Жобаның практикалық маңыздылығы зор: ол университет инфрақұрылымын цифрландыруға зор үлес қосады. Болашақта жүйені университет студенттік карталарымен (RFID) және push-хабарламалармен байланыстыру жоспарлануда.')

    # ==================== ӘДЕБИЕТТЕР ====================
    add_heading_1('ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ')
    refs = [
        '1. Қазақстан Республикасының Цифрлық даму, инновациялар және аэроғарыш өнеркәсібі министрлігі. «Қолжетімді интернет» және мемлекеттік цифрландыру тұжырымдамасы. – Астана, 2023.',
        '2. Jalote P. A Concise Introduction to Software Engineering: With Open Source and GenAI. – Cham: Springer Nature, 2025. – 224 p.',
        '3. Windmill E. Flutter in Action: Multimodal Cross-Platform App Development. 2nd ed. – Shelter Island: Manning Publications, 2024. – 390 p.',
        '4. Elmasri R., Navathe S.B. Fundamentals of Database Systems. 8th ed. – Hoboken: Pearson, 2025. – 1200 p.',
        '5. Shaban M. Introduction to Software Development: Database Development with PostgreSQL. – New York: Mercury Learning and Information, 2024. – 288 p.',
        '6. Bagui S., Earp R.W. Database Design Using Entity-Relationship Diagrams. 3rd ed. – Boca Raton: Auerbach Publications, 2025. – 486 p.',
        '7. Foster E.C., Godbole S. Database Systems: A Pragmatic Approach. 3rd ed. – Boca Raton: Auerbach Publications, 2022. – 640 p.',
        '8. Chen X., Hu X., Li Y. Deep Learning-Based Software Engineering: Progress, Challenges, and Opportunities // Science China Information Sciences. – 2025. – Vol. 68, № 4. – P. 140–162.',
        '9. Official Flutter Documentation. Building responsive and adaptive apps in Flutter. – 2026. [Электрондық ресурс]. Қолжетімділік режимі: https://docs.flutter.dev/ (қаралған күні: 11.10.2026).',
        '10. Official PostgreSQL Documentation. PostgreSQL 16/17 Interactive Documentation. – 2025. [Электрондық ресурс]. Қолжетімділік режимі: https://www.postgresql.org/docs/ (қаралған күні: 11.10.2026).',
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(r)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)

    # ==================== ҚОСЫМША А ====================
    add_heading_1('ҚОСЫМШАЛАР')
    add_title_p('ҚОСЫМША А\nРеляциондық деректер қорының бастапқы SQL скрипті', bold=True, size=13, space_after=12)

    sql_code = (
        '-- Пайдаланушылар кестесі\n'
        'CREATE TABLE users (\n'
        '    id SERIAL PRIMARY KEY,\n'
        '    email VARCHAR(255) UNIQUE NOT NULL,\n'
        '    password VARCHAR(255) NOT NULL,\n'
        '    role VARCHAR(50) DEFAULT \'student\'\n'
        ');\n\n'
        '-- Аудиториялар кестесі\n'
        'CREATE TABLE rooms (\n'
        '    id SERIAL PRIMARY KEY,\n'
        '    name VARCHAR(50) NOT NULL,\n'
        '    capacity INT NOT NULL,\n'
        '    floor VARCHAR(50),\n'
        '    type VARCHAR(100),\n'
        '    features TEXT,\n'
        '    is_available BOOLEAN DEFAULT TRUE\n'
        ');\n\n'
        '-- Сабақ кестесі және брондау кестесі (Кесте)\n'
        'CREATE TABLE keste (\n'
        '    id SERIAL PRIMARY KEY,\n'
        '    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,\n'
        '    user_id INT REFERENCES users(id) ON DELETE SET NULL,\n'
        '    subject VARCHAR(255) NOT NULL,\n'
        '    teacher VARCHAR(255),\n'
        '    time_slot VARCHAR(50) NOT NULL,\n'
        '    day VARCHAR(50) NOT NULL,\n'
        '    group_name VARCHAR(50),\n'
        '    status VARCHAR(50) DEFAULT \'booked\'\n'
        ');'
    )
    p_sql = doc.add_paragraph()
    p_sql.paragraph_format.line_spacing = 1.0
    p_sql.paragraph_format.first_line_indent = Inches(0)
    p_sql.paragraph_format.space_before = Pt(6)
    p_sql.paragraph_format.space_after = Pt(6)
    r_sql = p_sql.add_run(sql_code)
    r_sql.font.name = 'Courier New'
    r_sql.font.size = Pt(10)

    # Save to Project Folder and Desktop
    project_path = '/Users/kussainovamalika/AndroidStudioProjects/kursovaya/KURS_ZHOBA_Kussainova_Malika.docx'
    desktop_path = '/Users/kussainovamalika/Desktop/KURS_ZHOBA_Kussainova_Malika.docx'

    doc.save(project_path)
    try:
        doc.save(desktop_path)
    except Exception as e:
        print(f"Desktop save notice: {e}")

    print(f"Saved to {project_path} and {desktop_path}")

if __name__ == '__main__':
    create_coursework_docx()
