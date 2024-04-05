from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator

app = FastAPI()

class ArithmeticOperation(BaseModel):
    operation: str
    operand1: float
    operand2: float

    @validator('operation')
    def validate_operation(cls, operation):
        valid_operations = ['add', 'subtract', 'multiply', 'divide']
        if operation not in valid_operations:
            raise ValueError(f'Invalid operation. Must be one of {valid_operations}')
        return operation

    @validator('operation', 'operand2')
    def validate_divide_by_zero(cls, v, values):
        operation = values.get('operation')
        operand2 = values.get('operand2')
        if operation == 'divide' and operand2 == 0:
            raise ValueError('Division by zero is not allowed')
        return v

class CalculationResult(BaseModel):
    result: float

@app.post("/calculate", response_model=CalculationResult)
async def calculate(operation: ArithmeticOperation, request: Request):
    try:
        op = operation.operation
        a = operation.operand1
        b = operation.operand2

        if op == 'add':
            result = a + b
        elif op == 'subtract':
            result = a - b
        elif op == 'multiply':
            result = a * b
        else:
            result = a / b

        return CalculationResult(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# ////////////// Question 2 Convert Temperature (/convert/temperature)

