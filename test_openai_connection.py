import asyncio
from src.services.openai_service import OpenAIService
from src.learning_point import LearningPoint

async def test_openai_connection():
    try:
        # Create a test learning point
        test_point = LearningPoint(
            name="variables",
            description="Understanding what variables are and how to use them in programming"
        )
        
        # Initialize the OpenAI service
        service = OpenAIService()
        print("OpenAI service initialized successfully.")
        
        print("\nGenerating a test exercise...")
        exercises = await service.generate_exercises(
            learning_points=[test_point],
            count=1,
            difficulty="beginner",
            exercise_type="multiple_choice"
        )
        
        if exercises:
            print("\nSuccessfully generated an exercise:")
            print(f"\nQuestion: {exercises[0].question}")
            print(f"\nExpected Answer: {exercises[0].expected_answer}")
            print(f"\nExplanation: {exercises[0].explanation}")
        else:
            print("\nNo exercises were generated. Please check the error messages above.")
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openai_connection())
