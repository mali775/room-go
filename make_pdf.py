import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

os.environ['MPLCONFIGDIR'] = '/tmp/mpl_pdf_config'
os.makedirs('/tmp/mpl_pdf_config', exist_ok=True)

def generate_pdf():
    project_pdf = '/Users/kussainovamalika/AndroidStudioProjects/kursovaya/PREZENTATSIYA_Kussainova_Malika.pdf'
    desktop_pdf = '/Users/kussainovamalika/Desktop/PREZENTATSIYA_Kussainova_Malika.pdf'

    with PdfPages(project_pdf) as pdf:
        C_DARK = '#0F172A'
        C_BLUE = '#2563EB'
        C_LIGHT_BG = '#F8FAFC'
        C_CARD_BG = '#FFFFFF'
        C_TEXT_DARK = '#0F172A'
        C_TEXT_MUTED = '#64748B'
        C_BORDER = '#E2E8F0'

        def setup_slide(is_dark=False):
            fig = plt.figure(figsize=(16, 9), dpi=120)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_xlim(0, 16)
            ax.set_ylim(0, 9)
            ax.axis('off')
            bg = C_DARK if is_dark else C_LIGHT_BG
            ax.add_patch(patches.Rectangle((0, 0), 16, 9, color=bg, zorder=0))
            return fig, ax

        def add_header(ax, tag, title, subtitle):
            ax.add_patch(patches.FancyBboxPatch((1.0, 7.8), 2.8, 0.45, boxstyle="round,pad=0.1", ec="#BFDBFE", fc="#EFF6FF", zorder=2))
            ax.text(2.4, 8.02, tag, color="#2563EB", fontsize=11, fontweight='bold', ha='center', va='center', zorder=3)
            ax.text(1.0, 7.25, title, color=C_TEXT_DARK, fontsize=24, fontweight='bold', va='center')
            ax.text(1.0, 6.75, subtitle, color=C_TEXT_MUTED, fontsize=13, fontweight='normal', va='center')

        def add_footer(ax, slide_num):
            ax.plot([1.0, 15.0], [0.8, 0.8], color="#CBD5E1", lw=1)
            ax.text(1.0, 0.45, "AITU Rooms • Курстық жоба қорғалымы", color="#94A3B8", fontsize=11, fontweight='bold', va='center')
            ax.text(15.0, 0.45, f"Слайд {slide_num} / 10", color="#94A3B8", fontsize=11, fontweight='bold', ha='right', va='center')

        def draw_card(ax, x, y, w, h, title, desc_lines, is_accent=False, icon=""):
            fc = C_DARK if is_accent else C_CARD_BG
            ec = "#1E293B" if is_accent else C_BORDER
            tc_title = "#FFFFFF" if is_accent else C_TEXT_DARK
            tc_desc = "#94A3B8" if is_accent else C_TEXT_MUTED

            ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", ec=ec, fc=fc, lw=1.5, zorder=2))
            curr_y = y + h - 0.5
            if icon:
                ax.text(x + 0.35, curr_y, icon, fontsize=20, va='center', zorder=3)
                curr_y -= 0.55
            ax.text(x + 0.35, curr_y, title, color=tc_title, fontsize=15, fontweight='bold', va='center', zorder=3)
            curr_y -= 0.45
            for line in desc_lines:
                ax.text(x + 0.35, curr_y, line, color=tc_desc, fontsize=11, va='center', zorder=3)
                curr_y -= 0.35

        # ----------------- СЛАЙД 1: ТИТУЛДЫҚ БЕТ -----------------
        fig, ax = setup_slide(is_dark=True)
        ax.add_patch(patches.Circle((14.5, 7.5), radius=3.0, color="#1E3A8A", alpha=0.3, zorder=1))
        ax.add_patch(patches.Circle((1.5, 1.5), radius=2.5, color="#0284C7", alpha=0.2, zorder=1))
        ax.add_patch(patches.FancyBboxPatch((1.2, 7.6), 5.5, 0.55, boxstyle="round,pad=0.1", ec="#38BDF8", fc="#1E293B", zorder=2))
        ax.text(3.95, 7.87, "🏛️ «ASTANA IT UNIVERSITY» ЖШС КОЛЛЕДЖІ", color="#38BDF8", fontsize=12, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(1.2, 6.0, "AITU ROOMS", color="#FFFFFF", fontsize=48, fontweight='heavy', va='center', zorder=2)
        ax.text(1.2, 5.0, "Astana IT University студенттері мен оқытушыларына арналған\nбос аудиторияларды іздеу және брондау мобильді қосымшасы", color="#94A3B8", fontsize=18, va='center', zorder=2)
        ax.plot([1.2, 14.8], [2.4, 2.4], color="#334155", lw=1)
        ax.text(1.2, 1.8, "КУРСТЫҚ ЖОБА", color="#38BDF8", fontsize=13, fontweight='bold', zorder=2)
        ax.text(1.2, 1.3, "Пән: «Мобильді қосымшаларды әзірлеу»", color="#E2E8F0", fontsize=15, zorder=2)
        ax.add_patch(patches.FancyBboxPatch((9.2, 0.9), 5.6, 1.2, boxstyle="round,pad=0.15", ec="#334155", fc="#1E293B", zorder=2))
        ax.text(9.5, 1.7, "Құсайынова Малика", color="#FFFFFF", fontsize=18, fontweight='bold', zorder=3)
        ax.text(9.5, 1.3, "06130100 – Бағдарламалық қамтамасыз ету", color="#94A3B8", fontsize=12, zorder=3)
        ax.text(9.5, 0.95, "Астана, 2026 ж.", color="#38BDF8", fontsize=11, zorder=3)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 2: ӨЗЕКТІЛІК ЖӘНЕ МАҚСАТ -----------------
        fig, ax = setup_slide()
        add_header(ax, "МАҢЫЗДЫЛЫҒЫ", "Тақырыптың өзектілігі мен жобаның мақсаты", "Неліктен университет үшін бұл қосымша қажет болды?")
        draw_card(ax, 1.0, 1.5, 6.5, 4.8, "Өзекті мәселелер", [
            "• Сабақтан тыс уақытта бос кабинеттерді іздеу",
            "  үшін барлық қабаттарды аралау қажеттілігі;",
            "",
            "• Аудиториялар арасындағы қақтығыстар",
            "  (бір уақытта бірнеше студенттік топтың келуі);",
            "",
            "• Кабинеттердің техникалық жабдықталуы",
            "  (iMac, 4K проектор, Wi-Fi 6) туралы ақпараттың жоқтығы;",
            "",
            "• Smart Campus тұжырымдамасына сай бірыңғай",
            "  цифрлық мобильді жүйенің болмауы."
        ], icon="⚡")
        draw_card(ax, 8.5, 1.5, 6.5, 4.8, "Жобаның басты мақсаты", [
            "«Astana IT University» студенттері мен оқытушыларына",
            "бос оқу кеңістіктерін нақты уақыт режимінде табуға,",
            "интерактивті уақыт аралығымен брондауға,",
            "сабақ кестесін («Кесте») көруге және 3D карта арқылы",
            "кампус бойынша навигация жасауға арналған",
            "заманауи, сенімді әрі үштілді мобильді қосымшаны әзірлеу.",
            "",
            "Басты мақсат — студенттің уақытын үнемдеу және",
            "университет кеңістігін тиімді цифрландыру."
        ], is_accent=True, icon="🎯")
        add_footer(ax, 2)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 3: ҚОЙЫЛҒАН МІНДЕТТЕР -----------------
        fig, ax = setup_slide()
        add_header(ax, "ЖОСПАР МЕН МІНДЕТТЕР", "Жоба аясында шешілген негізгі міндеттер", "Мақсатқа жету үшін жүзеге асырылған 6 жүйелі қадам")
        tasks = [
            ("1", "Қолданыстағы кампустық сервистерге (Robin, Google Calendar) талдау жүргізу"),
            ("2", "Жүйенің функционалдық және пайдаланушылық талаптарын нақты тұжырымдау"),
            ("3", "Реляциондық деректер қорының құрылымын жобалау (users, rooms, keste кестелері)"),
            ("4", "Flutter/Dart негізінде Apple Minimal стиліндегі ыңғайлы UI/UX интерфейсін жасақтау"),
            ("5", "Интерактивті брондау, сабақ кестесі («Кесте») және кампустың 3D картасын іске асыру"),
            ("6", "Бағдарламалық жасақтаманы функционалдық тестілеуден өткізу және өнімділікті тексеру")
        ]
        coords = [(1.0, 4.2), (8.2, 4.2), (1.0, 2.7), (8.2, 2.7), (1.0, 1.2), (8.2, 1.2)]
        for (num, text), (x, y) in zip(tasks, coords):
            ax.add_patch(patches.FancyBboxPatch((x, y), 6.8, 1.2, boxstyle="round,pad=0.15", ec=C_BORDER, fc=C_CARD_BG, lw=1.2, zorder=2))
            ax.add_patch(patches.FancyBboxPatch((x + 0.25, y + 0.25), 0.7, 0.7, boxstyle="round,pad=0.08", ec="#2563EB", fc="#2563EB", zorder=3))
            ax.text(x + 0.6, y + 0.6, num, color="#FFFFFF", fontsize=13, fontweight='bold', ha='center', va='center', zorder=4)
            ax.text(x + 1.2, y + 0.6, text, color=C_TEXT_DARK, fontsize=10.5, fontweight='bold', va='center', zorder=4)
        add_footer(ax, 3)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 4: ТЕХНОЛОГИЯЛЫҚ СТЕК -----------------
        fig, ax = setup_slide()
        add_header(ax, "ТЕХНОЛОГИЯЛАР", "Қолданылған заманауи технологиялық стек", "Өнімділік пен кроссплатформалылықты қамтамасыз ететін құралдар")
        draw_card(ax, 1.0, 1.5, 3.2, 4.8, "Flutter & Dart", [
            "Google ұсынған",
            "Single Codebase фреймворк.",
            "Android, iOS және Web",
            "платформаларында жоғары",
            "өнімділікпен жұмыс істейді."
        ], icon="📱")
        draw_card(ax, 4.6, 1.5, 3.2, 4.8, "Provider", [
            "Реактивті күйді",
            "(State Management)",
            "және бизнес-логиканы",
            "таза, жылдам басқаруға",
            "арналған архитектура."
        ], icon="⚡")
        draw_card(ax, 8.2, 1.5, 3.2, 4.8, "PostgreSQL", [
            "Сенімділігі жоғары,",
            "ACID стандартына сай",
            "кәсіби реляциондық",
            "деректер қоры (users,",
            "rooms, keste кестелері)."
        ], icon="🗄️")
        draw_card(ax, 11.8, 1.5, 3.2, 4.8, "AITU 3D Map", [
            "Университет кампусының",
            "ресми 3D интерактивті",
            "картасын HtmlElementView",
            "арқылы тікелей қосымша",
            "ішіне біріктіру."
        ], icon="🗺️")
        add_footer(ax, 4)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 5: АРХИТЕКТУРА ЖӘНЕ ДҚ -----------------
        fig, ax = setup_slide()
        add_header(ax, "АРХИТЕКТУРА", "Жүйе архитектурасы және Деректер қоры", "Реляциондық байланыстар мен қабатты құрылым")
        draw_card(ax, 1.0, 1.5, 4.3, 4.8, "1. users кестесі", [
            "• id (PK, SERIAL)",
            "• email (VARCHAR, UNIQUE)",
            "• password (VARCHAR)",
            "• role (VARCHAR, default 'student')",
            "",
            "Студенттер мен оқытушылардың",
            "аккаунттары мен сессиясын",
            "сақтайды."
        ])
        draw_card(ax, 5.85, 1.5, 4.3, 4.8, "2. rooms кестесі", [
            "• id (PK, SERIAL)",
            "• name (мыс. C1.1.201)",
            "• capacity (36, 120 орын)",
            "• floor, type, building",
            "• features (жабдықталуы)",
            "• is_available (бос/бос емес)",
            "",
            "Аудиториялар деректері."
        ])
        draw_card(ax, 10.7, 1.5, 4.3, 4.8, "3. keste кестесі", [
            "• id (PK, SERIAL)",
            "• room_id (FK → rooms.id)",
            "• user_id (FK → users.id)",
            "• subject (пән/мақсат)",
            "• time_slot ('10:30-11:50')",
            "• day, status ('lecture', 'booked')",
            "",
            "Сабақтар мен студенттік брондар."
        ])
        add_footer(ax, 5)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 6: НЕГІЗГІ ЭКРАНДАР -----------------
        fig, ax = setup_slide()
        add_header(ax, "ИНТЕРФЕЙС", "Қосымшаның негізгі функционалдық экрандары", "Басты каталог, сүзгілер, тірі іздеу және жабдықталу бейдждері")
        draw_card(ax, 1.0, 1.5, 4.3, 4.8, "Splash & Авторизация", [
            "• Қараңғы стильдегі фирмалық",
            "  анимациялық логотип;",
            "• Email және құпиясөзді тексеру;",
            "• Қате мәліметке қызыл ескерту;",
            "• Тез көрсетуге арналған",
            "  1-шертумен «Демо-кіру» тетігі."
        ], icon="🚀")
        draw_card(ax, 5.85, 1.5, 4.3, 4.8, "Rooms (Басты каталог)", [
            "• Жиынтық нақты статистика:",
            "  Барлығы, Бос, Брондалған;",
            "• Тірі іздеу (кабинет немесе пән);",
            "• Сүзгілер чиптері: Қазір бос,",
            "  1, 2, 3 қабат, IT/AI зертханалары."
        ], icon="🏢")
        draw_card(ax, 10.7, 1.5, 4.3, 4.8, "Аудитория карточкалары", [
            "• Күйі: Жасыл (Бос) / Қызыл (Бос емес);",
            "• Жабдықталуы: 4K Проектор, iMac M3,",
            "  Wi-Fi 6, Кондиционер бейдждері;",
            "• Интерактивті «Брондау» тетігі."
        ], icon="✨")
        add_footer(ax, 6)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 7: БРОНДАУ ЖӘНЕ КЕСТЕ -----------------
        fig, ax = setup_slide()
        add_header(ax, "НЕГІЗГІ МОДУЛЬ", "Интерактивті брондау және «Кесте» модулі", "Уақыт таңдау, сабақтар кестесі және деректерді сақтау")
        draw_card(ax, 1.0, 1.5, 6.5, 4.8, "Брондау тетігі (Modal Bottom Sheet)", [
            "1. Студент бос аудитория карточкасындағы",
            "   «Брондау» батырмасын басады;",
            "",
            "2. Төменнен арнайы терезе ашылып, нақты уақытты",
            "   таңдайды (09:00-10:20, 10:30-11:50, 14:00-15:20...);",
            "",
            "3. Брондау мақсатын енгізеді (өздік жұмыс, хакатон);",
            "",
            "4. «Растау» басылғанда бөлме «Бос емес» болып өзгереді,",
            "   ал жазба бір сәтте сабақ кестесіне («Кесте»)",
            "   және жеке «Профильге» түседі."
        ], icon="⏱️")
        draw_card(ax, 8.5, 1.5, 6.5, 4.8, "«Кесте» (Timetable) бөлімі", [
            "• Төменгі мәзірдегі бөлек 2-ші басты қойынды;",
            "",
            "• Апта күндері бойынша толық сабақ кестесі",
            "  (Дүйсенбі, Сейсенбі, Сәрсенбі...);",
            "",
            "• Түрлі-түсті визуалды бейдждер: Көк (Дәріс),",
            "  Күлгін (Зертхана), Сарғыш (Тәжірибе),",
            "  Жасыл (Студенттік бронь);",
            "",
            "• Студент өз бронын 1-шертумен қайтара алады."
        ], is_accent=True, icon="📅")
        add_footer(ax, 7)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 8: КАРТА ЖӘНЕ ДИЗАЙН -----------------
        fig, ax = setup_slide()
        add_header(ax, "НАВИГАЦИЯ & ДИЗАЙН", "Кампус 3D картасы және Apple UI/UX эстетикасы", "Заманауи пайдаланушы тәжірибесі және үштілділік")
        draw_card(ax, 1.0, 1.5, 4.3, 4.8, "AITU 3D картасы", [
            "• Қосымшаның ішіне тікелей",
            "  енгізілген интерактивті карта;",
            "• Браузерге шықпай-ақ аудиторияның",
            "  ғимараттағы нақты орнын көру;",
            "• Картаны жаңа терезеде ашу батырмасы."
        ], icon="🧭")
        draw_card(ax, 5.85, 1.5, 4.3, 4.8, "Матовый шыны (Frosted Glass)", [
            "• Apple стандарттарына сай қалқымалы",
            "  төменгі мәзір (BackdropFilter);",
            "• Контент сырғығанда асты әдемі",
            "  бұлдырайды;",
            "• 500px адаптивті мобильді контейнер."
        ], icon="💎")
        draw_card(ax, 10.7, 1.5, 4.3, 4.8, "Толық үштілділік", [
            "• Қазақ тілі (негізгі әдепкі тіл),",
            "  Орыс және Ағылшын тілдері;",
            "• Профильде 1-шертумен тіл ауысады;",
            "• Студенттің жеке кабинеті мен",
            "  сессияны тазартатын «Шығу» функциясы."
        ], icon="🌐")
        add_footer(ax, 8)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 9: ТЕСТІЛЕУ НӘТИЖЕЛЕРІ -----------------
        fig, ax = setup_slide()
        add_header(ax, "СЫНАҚ & САПА", "Функционалдық тестілеу нәтижелері", "Жүйенің тұрақтылығы мен қатесіз жұмысы (8/8 Тест сәтті)")
        headers = ["№", "Тексерілген сценарий", "Күтілген нәтиже", "Нақты нәтиже", "Мәртебесі"]
        rows = [
            ["1", "Жаңа аккаунтты тіркеу", "Деректер сақталады, растау хабарламасы", "Сәтті тіркелді", "Өтті ✅"],
            ["2", "Қате мәліметпен кіру", "Қате туралы қызыл ескерту", "Қызыл Snackbar шықты", "Өтті ✅"],
            ["3", "Дұрыс поштамен кіру", "Басты бет ашылады, сессия сақталуы", "Басты бет ашылды", "Өтті ✅"],
            ["4", "Аудиторияны брондау", "«Бос емес» болып, кестеге жазылады", "Дереу жазылды", "Өтті ✅"],
            ["5", "Броньды кері қайтару", "Аудитория босатылады", "Бөлме сәтті босатылды", "Өтті ✅"],
            ["6", "Тілді ауыстыру (Қаз/Орыс/Ағыл)", "Мәтіндер бір сәтте ауысады", "Мәтіндер толық ауысты", "Өтті ✅"],
            ["7", "Кампус 3D картасын қарау", "Карта қосымша ішінде жүктеледі", "Карта сәтті көрсетілді", "Өтті ✅"],
            ["8", "Жүйеден шығу («Шығу»)", "Сессия тазарады, логин ашылады", "Логин экранына өтті", "Өтті ✅"],
        ]
        ax.add_patch(patches.FancyBboxPatch((1.0, 1.2), 14.0, 5.2, boxstyle="round,pad=0.15", ec=C_BORDER, fc=C_CARD_BG, lw=1.5, zorder=2))
        ax.add_patch(patches.Rectangle((1.0, 5.8), 14.0, 0.6, color=C_DARK, zorder=3))
        col_x = [1.3, 2.0, 6.2, 10.8, 13.6]
        for x, h in zip(col_x, headers):
            ax.text(x, 6.1, h, color="#FFFFFF", fontsize=11, fontweight='bold', va='center', zorder=4)
        curr_y = 5.4
        for r in rows:
            for x, val in zip(col_x, r):
                color = "#059669" if "✅" in val else C_TEXT_DARK
                fw = 'bold' if "✅" in val or x == 1.3 else 'normal'
                ax.text(x, curr_y, val, color=color, fontsize=10, fontweight=fw, va='center', zorder=4)
            ax.plot([1.0, 15.0], [curr_y - 0.25, curr_y - 0.25], color="#F1F5F9", lw=1, zorder=3)
            curr_y -= 0.52
        add_footer(ax, 9)
        pdf.savefig(fig)
        plt.close(fig)

        # ----------------- СЛАЙД 10: ҚОРЫТЫНДЫ -----------------
        fig, ax = setup_slide(is_dark=True)
        ax.add_patch(patches.Circle((14.5, 7.5), radius=3.0, color="#1E3A8A", alpha=0.3, zorder=1))
        ax.add_patch(patches.Circle((1.5, 1.5), radius=2.5, color="#0284C7", alpha=0.2, zorder=1))
        ax.add_patch(patches.FancyBboxPatch((1.2, 7.8), 4.8, 0.5, boxstyle="round,pad=0.1", ec="#38BDF8", fc="#1E293B", zorder=2))
        ax.text(3.6, 8.05, "ҚОРЫТЫНДЫ ЖӘНЕ НӘТИЖЕЛЕР", color="#38BDF8", fontsize=11, fontweight='bold', ha='center', va='center', zorder=3)
        ax.text(1.2, 7.0, "Жобаның нәтижесі мен болашағы", color="#FFFFFF", fontsize=38, fontweight='heavy', va='center', zorder=2)
        ax.text(1.2, 6.2, "«AITU Rooms» мобильді қосымшасы барлық қойылған талаптарға сай толықтай әзірленді\nжәне оқу орнына енгізуге дайын толыққанды өнім болып табылады.", color="#94A3B8", fontsize=15, va='center', zorder=2)
        draw_card(ax, 1.2, 2.6, 4.2, 3.0, "Практикалық маңызы", [
            "Студенттер мен оқытушылардың",
            "уақытын үнемдейді, оқу",
            "кеңістігін тиімді басқарады."
        ], icon="🎯")
        draw_card(ax, 5.9, 2.6, 4.2, 3.0, "Критерийлерге сәйкестік", [
            "Методичкадағы барлық 14",
            "бағалау критерийі 100%",
            "толықтай орындалды."
        ], icon="✅")
        draw_card(ax, 10.6, 2.6, 4.2, 3.0, "Болашақ даму бағыты", [
            "Telegram-ботпен байланыстыру",
            "және студенттік RFID",
            "карталармен интеграциялау."
        ], icon="🚀")
        ax.plot([1.2, 14.8], [1.8, 1.8], color="#334155", lw=1)
        ax.text(1.2, 1.2, "Назарларыңызға рақмет! Сұрақтарыңыз болса, қуана жауап беремін.", color="#FFFFFF", fontsize=20, fontweight='bold', zorder=2)
        ax.text(14.8, 1.2, "AITU Rooms 2026", color="#38BDF8", fontsize=16, fontweight='bold', ha='right', zorder=2)
        pdf.savefig(fig)
        plt.close(fig)

    try:
        import shutil
        shutil.copy(project_pdf, desktop_pdf)
        print(f"PDF successfully created: {desktop_pdf}")
    except Exception as e:
        print(f"Desktop copy notice: {e}")

    print(f"PDF saved in project: {project_pdf}")

if __name__ == '__main__':
    generate_pdf()
