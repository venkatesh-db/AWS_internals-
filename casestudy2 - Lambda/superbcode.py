
import time
import json
import threading

#global heron-python
class LambdaContext:
    def __init__(self, function_name="MyLambda", memory_limit=128, timeout=3):
        self.function_name = function_name
        self.memory_limit_in_mb = memory_limit
        self.timeout = timeout
        self.aws_request_id = str(int(time.time() * 1000))

# Simulate cold start using a global flag
cold_start_flag = True
warm_context = None

def lambda_handler(event, context):
    global cold_start_flag
    if cold_start_flag:
        print("⚡ [COLD START] Initializing Lambda function container...")
        time.sleep(1.5)  # simulate cold start latency
        cold_start_flag = False
    else:
        print("🔥 [WARM START] Using reused execution context...")

    print(f"🔧 Function: {context.function_name}, RequestID: {context.aws_request_id}")
    print(f"📥 Event Received: {json.dumps(event)}")

    # Sample business logic
    name = event.get("name", "Guest")
    message = f"Hello {name}, from Lambda!"
    return {
        "statusCode": 200,
        "body": json.dumps({"message": message})
    }

# Simulate an AWS Lambda runtime
def invoke_lambda(event):
    
    global warm_context
    if not warm_context:
        warm_context = LambdaContext()
        
    # event --> dict object  , class object     
    response = lambda_handler(event, warm_context)
    print("🧾 Response:", response)

# ----------------------
# 🔁 Simulate Invocations
# ----------------------
if __name__ == "__main__":
    print("🚀 Invoking Lambda First Time (Cold Start)")
    invoke_lambda({"name": "Venkatesh"})

    print("\n⏱️ Waiting 3s before next call to simulate reuse...")
    time.sleep(3)

    print("\n🚀 Invoking Lambda Second Time (Warm Start)")
    invoke_lambda({"name": "Coderrange"})
