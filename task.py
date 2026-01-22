## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a verification task (RUNS FIRST)
verification = Task(
    description="""Verify the financial document meets quality standards for: {query}

Steps to verify:
1. Confirm document is a legitimate financial report (10-K, 10-Q, earnings report, annual report, etc.)
2. Validate data completeness - check all required sections are present
3. Verify data consistency across different sections
4. Identify any missing critical financial information
5. Flag any anomalies, inconsistencies, or red flags

Use the FinancialDocumentTool to access and examine the document.""",

    expected_output="""Document verification report with:

1. **Document Type**: Identified type (e.g., "10-Q Quarterly Report", "Annual Report", "Earnings Release")
2. **Completeness Check**: 
   - ✅ Income statement present
   - ✅ Balance sheet present  
   - ✅ Cash flow statement present
   - ✅ Key metrics and ratios included
3. **Data Quality Assessment**: Any inconsistencies, errors, or missing calculations
4. **Red Flags**: Unusual items requiring further investigation
5. **Verification Status**: APPROVED / NEEDS REVIEW / REJECTED with justification

Only approve documents that contain actual financial data and meet reporting standards.""",

    agent=verifier,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)

## Creating financial analysis task (RUNS SECOND)
analyze_financial_document = Task(
    description="""Thoroughly analyze the verified financial document to answer: {query}

Analysis steps:
1. Extract key financial data (revenue, profit, EBITDA, cash flow, assets, liabilities)
2. Calculate and interpret important ratios (P/E, ROE, ROA, debt-to-equity, current ratio, profit margins)
3. Identify trends - compare current period to previous periods (YoY or QoQ growth)
4. Assess financial health indicators (liquidity, profitability, leverage, efficiency)
5. Compare metrics to industry benchmarks where possible
6. Highlight key risks and opportunities identified in the data
7. Provide evidence-based insights directly relevant to the user's query

Use the FinancialDocumentTool to read actual document data. Base all analysis on factual data from the document.""",

    expected_output="""A comprehensive financial analysis report including:

1. **Executive Summary**: 3-4 sentence overview of company's financial health and key findings

2. **Key Financial Metrics**:
   - Revenue: [Amount] (Growth: [%])
   - Net Income: [Amount] (Margin: [%])
   - EBITDA: [Amount] (Margin: [%])
   - Cash Flow: [Operating/Free cash flow amounts]
   - Total Assets: [Amount]
   - Total Liabilities: [Amount]
   - Shareholders Equity: [Amount]

3. **Financial Ratios**:
   - Profitability: ROE, ROA, Profit Margins
   - Liquidity: Current Ratio, Quick Ratio
   - Leverage: Debt-to-Equity, Interest Coverage
   - Efficiency: Asset Turnover, Inventory Turnover

4. **Trend Analysis**: 
   - Year-over-year or quarter-over-quarter changes in key metrics
   - Revenue growth trajectory
   - Margin expansion or contraction
   - Cash flow trends

5. **Financial Health Assessment**:
   - Strengths: What the company is doing well financially
   - Concerns: Financial weaknesses or warning signs
   - Competitive Position: How metrics compare to industry

6. **Investment Implications**: Data-driven insights answering the user's specific query

**All analysis must cite specific data from the document. No speculation or assumptions.**""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool(), search_tool],
    async_execution=False,
    context=[verification]  # Depends on verification completing first
)

## Creating investment analysis task (RUNS THIRD)
investment_analysis = Task(
    description="""Based on the verified financial analysis, provide professional investment recommendations for: {query}

Requirements:
1. Base ALL recommendations on the analyzed financial data from previous tasks
2. Consider risk-adjusted return potential
3. Align recommendations with investment objectives mentioned in query
4. Consider appropriate risk tolerance levels
5. Recommend diversified approaches when applicable
6. Include proper regulatory disclaimers
7. Be specific about entry points, position sizing, and time horizons

Context: Use insights from the financial_analyst's completed analysis and verifier's assessment.""",

    expected_output="""Professional investment recommendation report including:

1. **Investment Thesis** (3-4 sentences):
   - Why this investment opportunity aligns with the stated goals
   - Key value drivers identified from financial analysis
   - Expected investment timeline

2. **Financial Justification**:
   - Specific metrics supporting the recommendation
   - Valuation assessment (undervalued/fairly valued/overvalued)
   - Growth catalysts or value drivers

3. **Recommended Action**:
   - Clear recommendation: BUY / HOLD / SELL
   - Detailed rationale based on financial analysis
   - Target price or valuation range (if applicable)

4. **Position Sizing & Strategy**:
   - Suggested allocation percentage (e.g., "5-10% of portfolio")
   - Entry strategy (dollar-cost averaging vs lump sum)
   - Exit criteria or profit-taking levels

5. **Risk Considerations**:
   - Specific risks identified from financial data
   - Risk mitigation strategies
   - Scenarios that would invalidate the thesis

6. **Disclaimers**:
   - "This is not personalized financial advice"
   - "Past performance does not guarantee future results"
   - "All investments carry risk of loss"
   - "Consult a licensed financial advisor"

**Base all recommendations on actual financial data. No speculation or unsubstantiated claims.**""",

    agent=investment_advisor,
    tools=[search_tool],
    async_execution=False,
    context=[verification, analyze_financial_document]  # Depends on previous tasks
)

## Creating risk assessment task (RUNS FOURTH)
risk_assessment = Task(
    description="""Conduct comprehensive risk assessment using the financial analysis for: {query}

Risk analysis framework:
1. **Financial Risks**: Analyze leverage, liquidity issues, profitability trends, cash burn rate
2. **Market Risks**: Sector exposure, market competition, economic sensitivity, cyclicality
3. **Operational Risks**: Business model sustainability, management quality indicators, operational efficiency
4. **Regulatory/Compliance Risks**: Industry-specific regulations, pending legal issues
5. **Quantification**: Assign risk levels (Low/Medium/High) with specific evidence from financials

Use data from the financial analyst's work and market research. Provide objective, evidence-based risk analysis.""",

    expected_output="""Comprehensive risk assessment report:

1. **Executive Risk Summary**:
   - Overall Risk Profile: LOW / MEDIUM / HIGH
   - 2-3 sentence summary of primary risk factors
   - Risk-adjusted investment suitability

2. **Detailed Risk Analysis**:

   **Financial Risks** [Low/Medium/High]:
   - Debt levels and leverage ratios with actual numbers
   - Liquidity position and working capital concerns
   - Profitability trends and margin pressure
   - Cash flow stability or volatility

   **Market Risks** [Low/Medium/High]:
   - Industry competition and market position
   - Economic sensitivity and cyclical exposure
   - Market share trends
   - Pricing power and competitive moats

   **Operational Risks** [Low/Medium/High]:
   - Business model strengths/weaknesses
   - Management quality indicators from financials
   - Operational efficiency metrics
   - Key dependencies or single points of failure

   **Regulatory Risks** [Low/Medium/High]:
   - Industry-specific regulatory environment
   - Compliance track record
   - Pending regulatory changes

3. **Key Risk Factors** (Top 5):
   - List specific risks with evidence from financial data
   - Rank by severity and probability

4. **Risk Metrics**:
   - Debt-to-Equity ratio: [X]
   - Interest Coverage ratio: [X]
   - Current Ratio: [X]
   - Beta or volatility indicators (if available)

5. **Risk Mitigation Strategies**:
   - How to reduce or hedge identified risks
   - Portfolio diversification recommendations
   - Stop-loss levels or risk management techniques

6. **Risk-Adjusted Outlook**:
   - Expected returns considering risk level
   - Best case, base case, worst case scenarios
   - Probability-weighted return expectations

**All risk assessments must cite specific data from the financial document and analysis.**""",

    agent=risk_assessor,
    tools=[search_tool],
    async_execution=False,
    context=[verification, analyze_financial_document, investment_analysis]  # Depends on all previous tasks
)