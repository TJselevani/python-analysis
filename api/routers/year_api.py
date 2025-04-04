
# """
# Year Analysis Endpoints
# """


# # Example of the yearly earnings endpoint
# @app.get("/api/v1/yearly/earnings/{year}")
# def get_yearly_earnings(year: str):
#     """
#     Serve the yearly earnings trend.
#     """
#     data_path = os.path.join(JSON_DIR, "yearly", f"yearly_earnings_{year}.json")

#     def generate_yearly_earnings_method():
#         # Call the method to generate the yearly earnings trend
#         yearly_total_earnings_bar()

#     return generate_plot_json(data_path, generate_yearly_earnings_method, year)
