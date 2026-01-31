# from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
#
# # Render sidebar once
# sidebar_state = render_global_sidebar()
#
# # Extract environment safely
# env = sidebar_state["environment"]
#
# # Environment → backend mapping
# ENV_TO_BASE_URL = {
#     "Production": "https://api.quantplatform.com",
#     "Staging": "https://staging-api.quantplatform.com",
# }
#
# # Resolve base URL
# base_url = ENV_TO_BASE_URL[env]
#
# # Final API endpoint
# url = f"{base_url}/api/v1/portfolio/analysis"
