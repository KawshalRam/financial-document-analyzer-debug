## Importing libraries and files
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import FileReadTool
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
import pdfplumber

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and processes financial document PDFs, cleaning extra newlines."

    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str): Path of the pdf file.

        Returns:
            str: Full Financial Document file content
        """
        try:
            with pdfplumber.open(path) as pdf:
                content = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        content += page_text + "\n"
            
            # Clean and format the content
            while "\n\n\n" in content:
                content = content.replace("\n\n\n", "\n\n")
                
            return content
            
        except Exception as e:
            return f"Error reading financial document: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Analyzes financial document data for investment insights."

    def _run(self, financial_document_data: str) -> str:
        """Analyze financial document data for investment insights
        
        Args:
            financial_document_data: Processed financial document content
            
        Returns:
            str: Investment analysis results
        """
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        processed_data = processed_data.replace("  ", " ")
                
        # TODO: Implement advanced investment analysis logic here
        return f"Investment analysis completed for {len(processed_data)} characters of data"

## Creating Risk Assessment Tool
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Creates risk assessment from financial document data."

    def _run(self, financial_document_data: str) -> str:
        """Create risk assessment from financial document data
        
        Args:
            financial_document_data: Processed financial document content
            
        Returns:
            str: Risk assessment results
        """        
        # TODO: Implement risk assessment logic here
        return f"Risk assessment completed for financial data"