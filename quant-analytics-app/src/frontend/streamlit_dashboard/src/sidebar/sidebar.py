import streamlit as st


def render_global_sidebar() -> dict:
    """
    Render the global sidebar UI shared across all pages.

    Returns:
        dict: global sidebar state (environment, future flags, etc.)
    """
    st.sidebar.title("Quant Analytics Platform")

    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown(
        """
        Use the page selector above ⬆️  
        to switch between projects.
        """,
    )

    st.sidebar.divider()

    st.sidebar.subheader("Global Settings")

    environment = st.sidebar.selectbox(
        "Environment",
        ["Production", "Staging"],
        index=0,
    )

    st.sidebar.divider()

    return {
        "environment": environment,
    }
