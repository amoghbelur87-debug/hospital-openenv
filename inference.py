import os

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

def predict(input_data):
    return {
        "prediction": "ok",
        "input": input_data
    }

# Remove the main block - OpenEnv handles the server
# if __name__ == "__main__":
#     # Test the inference function
#     print("Testing inference...")
#
#     if IMPORT_SUCCESS:
#         # Test reset
#         result = inference({"action": "reset"})
#         print(f"Reset result: {result['status']}")
#
#         # Test step
#         result = inference({"action": "step", "data": {"action": -1}})
#         print(f"Step result: {result['status']}")
#
#         # Test get state
#         result = inference({"action": "get_state"})
#         print(f"Get state result: {result['status']}")
#
#         print("Inference tests completed!")
#     else:
#         print("Cannot test inference - modules not imported")

def get_state() -> Dict[str, Any]:
    """Get current environment state"""
    global current_env

    if current_env is None:
        return {"status": "error", "message": "Environment not initialized"}

    try:
        state = current_env._get_state()
        return {"status": "success", "state": state}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def setup():
    """Initialize the environment on startup"""
    print("Setting up Hospital Guardian AI environment...")
    reset_environment()
    print("Environment initialized successfully!")

def inference(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main inference function for Hugging Face OpenEnv

    Expected request format:
    {
        "action": "reset|step|get_state",
        "data": {...}  # Additional data for the action
    }
    """
    try:
        action = request.get("action", "")
        data = request.get("data", {})

        if action == "reset":
            return reset_environment()

        elif action == "step":
            action_value = data.get("action", -1)
            if not isinstance(action_value, int):
                return {"status": "error", "message": "action must be an integer"}
            return step_environment(action_value)

        elif action == "get_state":
            return get_state()

        else:
            return {
                "status": "error",
                "message": "Invalid action. Use 'reset', 'step', or 'get_state'"
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Initialize on import
setup()

if __name__ == "__main__":
    # Test the inference function
    print("Testing inference...")

    # Test reset
    result = inference({"action": "reset"})
    print(f"Reset result: {result['status']}")

    # Test step
    result = inference({"action": "step", "data": {"action": -1}})
    print(f"Step result: {result['status']}")

    # Test get state
    result = inference({"action": "get_state"})
    print(f"Get state result: {result['status']}")

    print("Inference tests completed!")
