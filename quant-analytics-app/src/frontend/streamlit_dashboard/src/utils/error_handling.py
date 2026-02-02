import logging
import streamlit as st

logger = logging.getLogger(__name__)


def safe_render(fn, user_msg="Something went wrong"):
    try:
        fn()
    except Exception:
        logger.exception("UI render failed")
        st.error(user_msg)
