import os
from docx import Document
from docx.shared import Pt, Inches, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def build_docx():
    doc = Document()

    # Поля страницы: Сол - 30 мм, Жоғарғы - 20 мм, Оң - 10 мм, Төменгі - 20 мм
    for section in doc.sections:
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.left_margin = Mm(30)
        section.right_margin = Mm(10)
        section.page_width = Mm(210)
        section.page_height = Mm(297)

    # Базовые стили: Times New Roman, 14pt, 1.5 интервал
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(14)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_title_p(text, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
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
        p.paragraph_format.first_line_indent = Mm(12.5)  # 1.25 см абзац
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        return p

    def add_section_h1(text):
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

    def add_sub_h2(text):
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
    add_title_p('«Арнайы пәндер» циклдік комиссиясы', bold=False, size=14, space_after=60)

    add_title_p('КУРСТЫҚ ЖОБА', bold=True, size=18, space_after=12)
    add_title_p('06130100 – «Бағдарламалық қамтамасыз ету (түрлері бойынша)»', bold=False, size=13, space_after=6)
    add_title_p('Тақырыбы: «Astana IT University студенттеріне арналған аудиторияларды іздеу және брондау мобильді қосымшасын әзірлеу (AITU Rooms)»', bold=True, size=14, space_after=120)

    p_info = doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_info.paragraph_format.line_spacing = 1.5
    p_info.paragraph_format.first_line_indent = Inches(0)
    p_info.add_run('Орындаған: студент Құсайынова Малика\n').bold = True
    p_info.add_run('Жетекшісі: ________________________\n')

    for _ in range(4):
        doc.add_paragraph().paragraph_format.line_spacing = 1.5

    add_title_p('Астана, 2026 ж.', bold=False, size=13, space_after=0)

    # ==================== МАЗМҰНЫ (КЕСТЕДЕ) ====================
    doc.add_page_break()
    add_title_p('МАЗМҰНЫ', bold=True, size=14, space_after=18)

    toc_rows = [
        ('КІРІСПЕ', '3'),
        ('1 БӨЛІМ. ТЕОРИЯЛЫҚ БӨЛІМ', '5'),
        ('  1.1 Мобильді қосымшалар туралы жалпы түсініктер', '5'),
        ('  1.2 Қолданыстағы бағдарламалық шешімдерді шолу', '7'),
        ('  1.3 Мобильді қосымшаларды әзірлеудің негізгі кезеңдері', '9'),
        ('  1.4 Әзірлеуде қолданылатын бағдарламалық құралдарды талдау', '11'),
        ('ҚОРЫТЫНДЫ', '14'),
        ('ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ', '15'),
    ]

    toc_table = doc.add_table(rows=len(toc_rows), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False

    # Устанавливаем ширину колонок (140 мм и 30 мм)
    for row_idx, (sec_name, page_num) in enumerate(toc_rows):
        row = toc_table.rows[row_idx]
        
        # Левая колонка - название раздела
        cell_0 = row.cells[0]
        cell_0.width = Mm(140)
        p0 = cell_0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.line_spacing = 1.5
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(sec_name)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)
        if not sec_name.startswith('  '):
            r0.bold = True

        # Правая колонка - номер страницы
        cell_1 = row.cells[1]
        cell_1.width = Mm(30)
        p1 = cell_1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.5
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_num)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        if not sec_name.startswith('  '):
            r1.bold = True

    # ==================== КІРІСПЕ ====================
    add_section_h1('КІРІСПЕ')

    add_body_p('Қазіргі цифрлық трансформация және Smart Campus (ақылды университет) тұжырымдамасы аясында мобильді технологиялар білім беру ұйымдарының инфрақұрылымын тиімді басқаруда маңызды рөл атқарады. Университеттерде мыңдаған білім алушылар мен профессорлық-оқытушылар құрамы күнделікті оқу процесін, жобалық жұмыстарды, хакатондар мен ғылыми семинарларды жүзеге асырады. Осы ретте оқу кеңістігін, яғни бос аудиторияларды жедел табу және оларды ресми түрде брондау мәселесі аса өзекті міндеттердің біріне айналды.')

    add_body_p('«Astana IT University» озық технологиялық жоғары оқу орны ретінде заманауи цифрлық ортаны белсенді дамытуда. Дегенмен, студенттердің өзіндік дайындықтары үшін бос аудиторияларды іздеу процесі дәстүрлі түрде кабинеттерді аралап көру немесе бейресми түрде келісу арқылы өтеді. Бұл аудиториялық кеңістіктің біркелкі пайдаланылмауына, уақыттың босқа жұмсалуына және қақтығыстарға әкеледі. Осы мәселені жүйелі түрде шешу үшін интерактивті карта мен сабақ кестесі біріктірілген «AITU Rooms» мобильді қосымшасын әзірлеу жоғары практикалық мәнге ие.')

    add_body_p('Тақырыптың өзектілігі: студенттер мен оқытушылардың күнделікті уақытын үнемдеу қажеттілігімен, кампустық инфрақұрылымды цифрландырумен және мобильді құрылғылар арқылы аудиторияларды нақты уақыт режимінде басқаруға сұраныстың артуымен негізделеді.')

    add_body_p('Курстық жобаның мақсаты — «Astana IT University» студенттері мен қызметкерлеріне арналған, бос аудиторияларды нақты уақыт режимінде іздеуге, брондауға және сабақ кестесін қадағалауға мүмкіндік беретін кроссплатформалы мобильді қосымшаны әзірлеу.')

    add_body_p('Қойылған мақсатқа жету үшін келесі міндеттер айқындалды:\n'
               '1. Кампустық логистика және онлайн брондау саласындағы ұқсас бағдарламалық шешімдерге талдау жүргізу;\n'
               '2. Мобильді қосымшаның функционалдық және пайдаланушылық талаптарын қалыптастыру;\n'
               '3. Реляциондық деректер қорының құрылымын жобалау (users, rooms, keste кестелері);\n'
               '4. Flutter фреймворкі мен Dart бағдарламалау тілі негізінде ыңғайлы, минималистік интерфейс жасау;\n'
               '5. Басты функционалдық модульдерді (тіркелу, авторизация, іздеу, сүзгілер, 3D карта, брондау және сабақ кестесі) жүзеге асыру;\n'
               '6. Әзірленген бағдарламалық өнімді тестілеу және алынған нәтижелерді талдау.')

    add_body_p('Зерттеу нысаны — жоғары оқу орындарындағы аудиториялық қорды басқару процесі.')
    add_body_p('Зерттеу пәні — Flutter және PostgreSQL/локалды деректер сақтау технологиялары негізінде мобильді брондау жүйесін құру.')
    add_body_p('Практикалық маңыздылығы: әзірленген бағдарламалық өнім университет инфрақұрылымында тікелей қолданысқа енгізілуге дайын толыққанды қосымша болып табылады.')

    # ==================== 1 БӨЛІМ ====================
    add_section_h1('1 БӨЛІМ. ТЕОРИЯЛЫҚ БӨЛІМ')

    add_sub_h2('1.1 Мобильді қосымшалар туралы жалпы түсініктер')
    add_body_p('Мобильді қосымшалар — смартфондар, планшеттер және басқа да портативті құрылғыларда белгілі бір функцияларды орындау үшін арнайы әзірленген бағдарламалық жасақтама. Бүгінгі цифрлық қоғамда мобильді құрылғылар ақпарат алудың және күнделікті қызметтерді тұтынудың негізгі арнасына айналды.')
    add_body_p('Университеттік ортада мобильді қосымшалар «Smart Campus» (Ақылды кампус) концепциясының маңызды бөлігі болып табылады. Оқу орындарындағы кеңістікті оңтайлы басқару студенттерге ыңғайлы жағдай жасаумен қатар, аудиториялық қордың бос тұрып қалуын болдырмайды. «AITU Rooms» мобильді қосымшасы білім алушыларға кез келген уақытта университеттегі бос бөлмелердің күйін көруге және өзіндік зерттеулері үшін брондауға мүмкіндік береді.')

    add_sub_h2('1.2 Қолданыстағы бағдарламалық шешімдерді шолу')
    add_body_p('Курстық жобаны орындау барысында нарықтағы ұқсас халықаралық және отандық жүйелерге талдау жүргізілді. Негізгі бағдарламалық шешімдердің қатарына келесілер жатады:')
    add_body_p('1. Robin Powered — ірі халықаралық компаниялар мен коворкинг орталықтарында қолданылатын кәсіби брондау жүйесі. Артықшылықтары: аналитикалық есептер, күнтізбелермен байланыс. Кемшіліктері: лицензиясының жоғары бағасы және отандық білім беру стандарттары мен қазақ тіліне бейімделмеуі.')
    add_body_p('2. Google Calendar Campus Bookings — қарапайым күнтізбелік брондау құралы. Артықшылықтары: қолжетімділік. Кемшіліктері: аудиториялардың қабаты, техникалық жабдықталуы (iMac, 4K проектор, кондиционер) бойынша сүзу мүмкіндігі жоқ және кампустың 3D картасы қарастырылмаған.')
    add_body_p('3. ЖОО-ның ішкі дәстүрлі ақпараттық жүйелері (Platonus, Univer) — негізінен бағалау мен оқу журналдарын жүргізуге бағытталған. Мобильді құрылғыларда студенттерге нақты уақытта бос кабинетті жедел брондау функциясын ұсынбайды.')

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
    add_body_p('Салыстырмалы талдау нәтижесі көрсеткендей, әзірленген «AITU Rooms» мобильді қосымшасы білім алушылардың барлық талаптарына сай келетін ең оңтайлы шешім болып табылады.')

    add_sub_h2('1.3 Мобильді қосымшаларды әзірлеудің негізгі кезеңдері')
    add_body_p('Мобильді қосымшаны сапалы әзірлеу келесі жүйелі өмірлік цикл кезеңдерін қамтиды:\n'
               '1. Ақпарат жинау және техникалық тапсырманы қалыптастыру;\n'
               '2. Деректер базасының реляциондық архитектурасын жобалау;\n'
               '3. UI/UX интерфейсін прототиптеу (дизайн жүйесін құру);\n'
               '4. Бағдарламалық кодтау (фронтенд және логикалық қабаттар);\n'
               '5. Қосымшаны функционалдық сынақтан өткізу және тестілеу;\n'
               '6. Бағдарламалық өнімді құжаттау және енгізуге дайындау.')

    add_sub_h2('1.4 Әзірлеуде қолданылатын бағдарламалық құралдарды талдау')
    add_body_p('Курстық жобаны жүзеге асыру үшін таңдалған негізгі құралдар мен технологиялық стек:\n'
               '• Flutter (Google) — бірыңғай кодтық база (Single Codebase) арқылы Android, iOS және Web платформаларына бір уақытта жылдам компиляцияланатын заманауи фреймворк;\n'
               '• Dart бағдарламалау тілі — нысанға бағытталған (OOP), қатаң типтелген, алдын ала AOT және JIT компиляциясын қолдайтын тіл;\n'
               '• Provider — қосымшаның реактивті күйін (State Management) таза, үнемді және қауіпсіз басқаруға мүмкіндік беретін архитектуралық құрал;\n'
               '• PostgreSQL — деректер тұтастығы мен реляциялық байланыстарды қатаң қамтамасыз ететін ДҚБЖ;\n'
               '• SharedPreferences — пайдаланушы сессиясын және брондау күйін локальді түрде кэштеу кітапханасы.')

    # ==================== ҚОРЫТЫНДЫ ====================
    add_section_h1('ҚОРЫТЫНДЫ')

    add_body_p('Курстық жобаның бірінші кезеңі аясында алға қойылған барлық міндеттер толықтай орындалды. «Astana IT University» студенттері мен оқытушыларына арналған бос аудиторияларды табу және брондау жүйесінің теориялық және әдіснамалық негіздері кешенді түрде зерттелді.')

    add_body_p('Орындалған жұмыстардың негізгі қорытындылары:\n'
               '1. Smart Campus тұжырымдамасы аясында аудиториялық қорды цифрландырудың өзектілігі жан-жақты негізделді;\n'
               '2. Қолданыстағы отандық және халықаралық аналогтарға сыни талдау жасалып, әзірленетін жүйенің бәсекелестік артықшылықтары анықталды;\n'
               '3. Жүйе архитектурасы, қажетті функционалдық модульдер және пайдаланушы сценарийлері қалыптастырылды;\n'
               '4. Жоғары өнімділікті және кроссплатформалылықты қамтамасыз ететін технологиялық стек (Flutter, Dart, PostgreSQL, Provider) таңдалып, теориялық тұрғыдан дәйектелді.')

    add_body_p('Теориялық талдау нәтижесінде жинақталған ақпарат жобаның практикалық кезеңін сәтті іске асыруға толық негіз болды.')

    # ==================== ӘДЕБИЕТТЕР ====================
    add_section_h1('ПАЙДАЛАНЫЛҒАН ӘДЕБИЕТТЕР ТІЗІМІ')

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

    # Сохраняем в проект
    output_path = '/Users/kussainovamalika/AndroidStudioProjects/kursovaya/KURS_ESEP_1_BOLIM.docx'
    doc.save(output_path)
    print(f"Created: {output_path}")

if __name__ == '__main__':
    build_docx()
