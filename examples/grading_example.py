import asyncio
from src.services.openai_service import OpenAIService

async def test_grading():
    service = OpenAIService()
    
    # Test case
    problem = "Explain what a variable is in programming and provide an example."
    student_answer = """
    A variable is like a container that stores data in a program. 
    For example, you can create a variable called 'age' and store the number 25 in it:
    age = 25
    """
    expected_answer = """
    A variable is a named storage location in computer memory that can hold data.
    It allows programmers to store and manipulate values in their programs.
    Example:
    age = 25  # Creates a variable 'age' and assigns it the value 25
    """
    
    metadata = {
        "topic": "Programming Basics",
        "difficulty": "beginner",
        "student_level": "beginner",
        "previous_attempts": 0
    }
    
    print("Grading student's answer...")
    result = await service.grade_answer(
        problem=problem,
        student_answer=student_answer,
        expected_answer=expected_answer,
        metadata=metadata
    )
    
    print(f"\nScore: {result.score}/100")
    print(f"\nFeedback: {result.feedback}")
    print("\nMetadata:")
    for key, value in result.metadata.items():
        print(f"- {key}: {value}")
    print(f"\nGrading Confidence: {result.confidence}")

if __name__ == "__main__":
    asyncio.run(test_grading())
