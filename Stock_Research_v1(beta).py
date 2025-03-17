import yfinance as yf


def fetch_financial_data(ticker):
    """Fetches financial data for a given stock ticker using Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data = {}
    try:
        # Fetch key statistics
        data["company_name"] = stock.info.get("shortName", "N/A")
        data["pe_ratio_company"] = stock.info.get("trailingPE", 0)
        data["forward_pe"] = stock.info.get("forwardPE", 0)
        data["eps_growth"] = stock.info.get("earningsGrowth", None)  # Set to None if missing
        data["roe"] = stock.info.get("returnOnEquity", None)  # Set to None if missing
        data["roa"] = stock.info.get("returnOnAssets", None)
        data["revenue_growth"] = stock.info.get("revenueGrowth", None)
        data["de_ratio"] = stock.info.get("debtToEquity", None)
        data["current_ratio"] = stock.info.get("currentRatio", None)

        # Manually input missing data
        for key in ["eps_growth", "roe", "revenue_growth", "de_ratio", "current_ratio"]:
            if data[key] is None:
                data[key] = float(input(f"⚠️ Missing {key.replace('_', ' ').title()}. Please enter it manually: ") or 0)

        # Convert percentages
        data["eps_growth"] *= 100
        data["roe"] *= 100
        data["roa"] = data["roa"] * 100 if data["roa"] else 0
        data["revenue_growth"] *= 100
        data["de_ratio"] /= 100

        # PEG Ratio Calculation
        data["peg_ratio"] = (data["pe_ratio_company"] / data["eps_growth"]) if data["eps_growth"] > 0 else float('inf')

        print(f"\n✅ Data fetched for {data['company_name']}\n")
        print("📊 Fundamental Data:")
        for key, value in data.items():
            if key != "company_name":
                print(f"{key.replace('_', ' ').title()}: {value}")

        return data

    except Exception as e:
        print(f"⚠️ Error fetching data: {e}")
        return None


def collect_data():
    """Collects stock data automatically via Yahoo Finance"""
    ticker = input("\nEnter Stock Ticker (e.g., ZOMATO.NS for Zomato): ").upper()
    stock = yf.Ticker(ticker)  # Define stock here
    data = fetch_financial_data(ticker)

    if data:
        # Ask for industry-level data manually
        data['pe_ratio_industry'] = float(input("\nEnter P/E Ratio (Industry Avg.): ") or 0)
        data['industry_roe'] = float(input("Enter Industry Average ROE: ") or 0)

        return data
    else:
        print("❌ Failed to retrieve data.")
        return None


def valuation_analysis(data):
    if data['forward_pe'] < data['pe_ratio_company']:
        future_growth = "Analysts expect higher earnings (Bullish)"
    else:
        future_growth = "Future earnings growth is uncertain"

    if data['peg_ratio'] < 1:
        valuation = "Undervalued"
    elif data['peg_ratio'] > 1.5:
        valuation = "Overvalued"
    else:
        valuation = "Fairly Valued"

    if data["roe"] > data["industry_roe"]:
        company_quality = "Above Industry Average (Good ROE)"
    elif data["roe"] > 12:
        company_quality = "Decent ROE (Check other factors)"
    else:
        company_quality = "Below Average ROE (Risky)"

    return valuation, company_quality, future_growth


def growth_analysis(data, industry_eps_avg, industry_revenue_avg):
    if data['eps_growth'] > industry_eps_avg and data['revenue_growth'] > industry_revenue_avg:
        return "Expanding"
    else:
        return "Stagnant or Declining"


def risk_metrics(data):
    risk = {
        'debt_risk': "Low" if data['de_ratio'] < 1 else "High",
        'liquidity': "Stable" if data['current_ratio'] > 1.5 else "Unstable"
    }
    return risk


def determine_company_type(data):
    """ Classifies company as Growth, Stable, or Balanced based on financials """
    if data["revenue_growth"] > 15 and data["roe"] < 12:
        return "growth"
    elif data["roe"] > 15 and data["revenue_growth"] < 10:
        return "stable"
    else:
        return "balanced"


def get_dynamic_weights(company_type):
    
    if company_type == "growth":
        return {"w1": 0.35, "w2": 0.15, "w3": 0.4, "w4": 0.1}
    elif company_type == "stable":
        return {"w1": 0.3, "w2": 0.5, "w3": 0, "w4": 0.1}  # No penalty for negative revenue growth
    else:
        return {"w1": 0.35, "w2": 0.3, "w3": 0.25 if data['revenue_growth'] > 0 else 0.1, "w4": 0.1}


def intrinsic_score(data):
    """ Calculates intrinsic score based on dynamic weights """
    company_type = determine_company_type(data)
    weights = get_dynamic_weights(company_type)

    score = (weights["w1"] * (1 / data["peg_ratio"] if data["peg_ratio"] != float('inf') and data["peg_ratio"] != 0 else 0) +
             weights["w2"] * data["roe"] +
             weights["w3"] * max(data["revenue_growth"], 0) - 
             weights["w4"] * data["de_ratio"])

    return round(score, 2), company_type


if __name__ == "__main__":
    try:
        data = collect_data()
        if not data:
            exit()

        print("\n🔎 Proceeding with Valuation Analysis...")
        valuation, company_quality, future_growth = valuation_analysis(data)
        print(f"Valuation: {valuation}")
        print(f"Company Quality: {company_quality}")
        print(f"Future Growth Outlook: {future_growth}")

        industry_eps_avg = float(input("\nEnter Industry EPS Growth Rate (%): ") or 0)
        industry_revenue_avg = float(input("Enter Industry Revenue Growth Rate (%): ") or 0)
        growth_status = growth_analysis(data, industry_eps_avg, industry_revenue_avg)
        print(f"Growth Status: {growth_status}")

        risk = risk_metrics(data)
        print(f"Debt Risk: {risk['debt_risk']}")
        print(f"Liquidity: {risk['liquidity']}")

        score, company_type = intrinsic_score(data)
        print(f"\nIntrinsic Score: {score}")
        print(f"Company Type: {company_type}")

        threshold = 50
        if score > threshold + 10:
            print("📈 Strong Buy")
        elif score > threshold:
            print("✅ Buy")
        elif score == threshold:
            print("⚖️ Hold")
        elif score < threshold - 10:
            print("❌ Strong Sell")
        else:
            print("⚠️ Avoid/Sell")

    except Exception as e:
        print(f"An error occurred: {e}")
