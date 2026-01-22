from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

app = FastAPI(
    title="Financial Document Analyzer",
    description="AI-powered financial document analysis system using CrewAI",
    version="1.0.0"
)

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the complete financial analysis crew with all agents and tasks
    
    Args:
        query: User's analysis question or request
        file_path: Path to the financial document PDF
        
    Returns:
        CrewOutput: Complete analysis results from all tasks
    """
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )
    
    result = financial_crew.kickoff({'query': query})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze - POST - Upload and analyze financial documents",
            "docs": "/docs - Interactive API documentation"
        }
    }

@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(..., description="Financial document PDF file"),
    query: str = Form(
        default="Provide a comprehensive financial analysis and investment recommendation",
        description="Your analysis question or request"
    )
):
    """Analyze financial document and provide comprehensive investment recommendations
    
    This endpoint:
    1. Verifies the document is a valid financial report
    2. Performs detailed financial analysis
    3. Provides investment recommendations
    4. Conducts risk assessment
    
    Args:
        file: PDF file containing financial document (10-K, 10-Q, earnings report, etc.)
        query: Your specific analysis question or investment objective
        
    Returns:
        Complete analysis including verification, financial metrics, investment advice, and risk assessment
    """
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported. Please upload a financial document in PDF format."
        )
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Provide a comprehensive financial analysis and investment recommendation"
        
        query = query.strip()
        
        # Process the financial document with all analysts
        print(f"Processing query: {query}")
        print(f"Document: {file.filename} ({len(content)} bytes)")
        
        response = run_crew(query=query, file_path=file_path)
        
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"financial_analysis_{timestamp}_{file_id}.txt"
        output_path = os.path.join("outputs", output_filename)
        
        # Save analysis to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Query: {query}\n")
            f.write(f"Document: {file.filename}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write(str(response))
        
        return {
            "status": "success",
            "query": query,
            "file_processed": file.filename,
            "file_size_bytes": len(content),
            "analysis": str(response),
            "output_file": output_path,
            "message": "Financial analysis completed successfully and saved to outputs directory"
        }
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing financial document: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temporary file: {cleanup_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)