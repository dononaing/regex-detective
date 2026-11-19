import html
import re
import streamlit as st
from chapters.passes import get_passes_rounds
from chapters.archive import get_archive_rounds


st.set_page_config(page_title="Regex-детектив", page_icon="🕵️", layout="centered")

# Лёгкие стили для карточек в светлой теме
st.markdown(
    """
    <style>
    .start-box {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        border-top: 5px solid #b58900;
        border-radius: 10px;
        padding: 32px 24px;
        text-align: center;
        margin: 24px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    .start-title {
        color: #1f2328;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .start-sub {
        color: #424a53;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .case-card {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        border-left: 5px solid #b58900;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }
    .case-header {
        color: #9a6700;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .case-title {
        color: #1f2328;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .case-desc {
        color: #24292f;
        font-size: 15px;
        line-height: 1.5;
        white-space: pre-line;
    }
    .highlight-box {
        background-color: #f6f8fa;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        padding: 14px;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
        color: #1f2328;
    }
    .regex-match {
        background-color: #1a7f37;
        color: #ffffff;
        padding: 2px 5px;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Инициализация состояния
if "rounds" not in st.session_state:
    st.session_state.rounds = get_passes_rounds() + get_archive_rounds()
    st.session_state.screen = "start"  # "start" | "game" | "solutions"
    st.session_state.confirm_solutions = False
    st.session_state.current_idx = 0
    st.session_state.clues = []
    st.session_state.round_solved = False
    st.session_state.last_feedback = None

SOLUTIONS_BY_TITLE = {
    "Дело № 1. Поддельный пропуск": r"[A-Z]{2}-\d{3}",
    "Архив Скотланд-Ярда: Шифры Лестрейда": r"\bCASE-\d{4}\b",
    "Архив переписки: Тайные досье Майкрофта": r"\b[A-Z]{2}-\d{3}-[A-Z]\b",
}
FALLBACK_SOLUTIONS = [
    r"[A-Z]{2}-\d{3}",
    r"SEC-(2024|2025)[ABC]",
    r"\bCASE-\d{4}\b",
    r"\b[A-Z]{2}-\d{3}-[A-Z]\b",
]


def get_solution_for_round(index: int, title: str) -> str:
    if title in SOLUTIONS_BY_TITLE:
        return SOLUTIONS_BY_TITLE[title]
    if index < len(FALLBACK_SOLUTIONS):
        return FALLBACK_SOLUTIONS[index]
    return "Решение не указано"


def highlight_matches(text: str, pattern: str) -> str:
    if not pattern:
        return html.escape(text)
    try:
        compiled = re.compile(pattern)
    except re.error:
        return html.escape(text)

    result = []
    last_idx = 0
    for match in compiled.finditer(text):
        start, end = match.span()
        if start == end:
            continue
        result.append(html.escape(text[last_idx:start]))
        result.append(f'<span class="regex-match">{html.escape(match.group(0))}</span>')
        last_idx = end
    result.append(html.escape(text[last_idx:]))
    return "".join(result)


def reset_game_state():
    st.session_state.current_idx = 0
    st.session_state.clues = []
    st.session_state.round_solved = False
    st.session_state.last_feedback = None


rounds = st.session_state.rounds
total_rounds = len(rounds)
idx = st.session_state.current_idx

# Боковая панель
with st.sidebar:
    st.header("🗂 Материалы дела")
    st.progress(idx / total_rounds if total_rounds else 1.0)
    st.caption(f"Раскрыто эпизодов: {len(st.session_state.clues)} из {total_rounds}")

    if st.session_state.clues:
        for i, clue in enumerate(st.session_state.clues, start=1):
            st.info(f"**Улика #{i}:** {clue}")
    else:
        st.caption("Улик пока нет.")

    st.divider()
    if st.button("🏠 На стартовый экран", use_container_width=True):
        st.session_state.screen = "start"
        st.session_state.confirm_solutions = False
        st.rerun()

    if st.session_state.screen == "game":
        if st.button("🔄 Начать расследование заново", use_container_width=True):
            reset_game_state()
            st.rerun()

# --- ЭКРАН 1: СТАРТОВЫЙ ЭКРАН ---
if st.session_state.screen == "start":
    st.markdown(
        f"""
        <div class="start-box">
            <div class="start-title">🕵️ «Regex-детектив»</div>
            <div class="start-sub">Архив криминальных дел готов к проверке. Всего эпизодов: {total_rounds}.</div>
            <div class="start-sub"><strong>Начать расследование?</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 Начать расследование", type="primary", use_container_width=True):
        reset_game_state()
        st.session_state.confirm_solutions = False
        st.session_state.screen = "game"
        st.rerun()

    if st.button("📖 Условия и решения заданий", use_container_width=True):
        st.session_state.confirm_solutions = True

    if st.session_state.confirm_solutions:
        st.warning("⚠️ Вы точно хотите сюда? Вы увидите ответы на вопросы заданий!")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Да, открыть решения", type="primary", use_container_width=True):
                st.session_state.confirm_solutions = False
                st.session_state.screen = "solutions"
                st.rerun()
        with c2:
            if st.button("Отмена", use_container_width=True):
                st.session_state.confirm_solutions = False
                st.rerun()

    st.stop()

# --- ЭКРАН 2: УСЛОВИЯ И РЕШЕНИЯ ЗАДАНИЙ ---
if st.session_state.screen == "solutions":
    st.title("📖 Условия и решения заданий")
    if st.button("⬅️ Вернуться на стартовый экран"):
        st.session_state.screen = "start"
        st.rerun()

    st.divider()
    for i, rnd in enumerate(rounds):
        sol = get_solution_for_round(i, rnd.title)
        st.markdown(
            f"""
            <div class="case-card">
                <div class="case-header">Эпизод {i + 1}</div>
                <div class="case-title">{html.escape(rnd.title)}</div>
                <div class="case-desc">{html.escape(rnd.description)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("**Примеры из условия:**")
        st.code(rnd.examples, language="text")
        st.markdown("**Подсказка:** " + rnd.hint)
        st.markdown("**Эталонное регулярное выражение (ответ):**")
        st.code(sol, language="regex")
        st.divider()

    st.stop()

# --- ЭКРАН 3: ИГРОВОЙ ПРОЦЕСС ---
st.title("🕵️ «Regex-детектив»")

if idx >= total_rounds:
    st.success("🎉 Расследование завершено! Все эпизоды раскрыты.")
    st.subheader("Собранные улики:")
    for i, clue in enumerate(st.session_state.clues, start=1):
        st.markdown(f"**{i}.** {clue}")
    if st.button("🔄 Пройти ещё раз", type="primary"):
        reset_game_state()
        st.rerun()
    st.stop()

current_round = rounds[idx]

st.markdown(
    f"""
    <div class="case-card">
        <div class="case-header">Дело № {idx + 1} из {total_rounds}</div>
        <div class="case-title">{html.escape(current_round.title)}</div>
        <div class="case-desc">{html.escape(current_round.description)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("💡 Запросить подсказку информатора"):
    st.write(current_round.hint)

pattern = st.text_input(
    "Введите регулярное выражение:",
    key=f"pattern_input_{idx}",
    placeholder=r"Например: \bCASE-\d{4}\b",
)

st.caption("Предпросмотр совпадений на материалах дела (подсвечивается в реальном времени):")
highlighted_html = highlight_matches(current_round.examples, pattern)
st.markdown(f'<div class="highlight-box">{highlighted_html}</div>', unsafe_allow_html=True)

st.write("")
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔍 Проверить шаблон", type="primary", use_container_width=True):
        if not pattern.strip():
            st.session_state.last_feedback = (False, "Введите регулярное выражение перед проверкой.")
        else:
            ok, msg = current_round.check(pattern.strip())
            st.session_state.last_feedback = (ok, msg)
            if ok and not st.session_state.round_solved:
                st.session_state.round_solved = True
                st.session_state.clues.append(current_round.clue)

if st.session_state.last_feedback is not None:
    ok, msg = st.session_state.last_feedback
    if ok:
        st.success(msg)
        st.warning(f"🔑 **Улика получена:** {current_round.clue}")
    else:
        st.error(msg)

with col2:
    if st.session_state.round_solved:
        if st.button("➡️ Следующее дело", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.round_solved = False
            st.session_state.last_feedback = None
            st.rerun()