"""
CLI Interactive DTMF Simulator for LocalJobs IVR
Allows command-line testing of the complete IVR state machine without browser or phone calls.
"""
import sys
from backend.app.services.ivr_service import ivr_service

def run_cli_simulator():
    print("=" * 60)
    print("      LOCALJOBS — INTERACTIVE IVR TELEPHONE SIMULATOR       ")
    print("=" * 60)
    caller_phone = input("Enter caller phone number [+919848012345]: ").strip()
    if not caller_phone:
        caller_phone = "+919848012345"

    call_id = "CLI-CALL-001"
    print(f"\n[DIALING 1800-LOCAL-JOB from {caller_phone} ...]")
    
    # 1. Incoming Call
    res = ivr_service.process_incoming_call(call_id, caller_phone)
    print(f"\n[SYSTEM VOICE] {res['prompt']}")

    while not res.get("terminate", False):
        print("\n" + "-" * 40)
        user_input = input("Enter DTMF key (0-9, *, #) or 'timeout' or 'q' to hang up: ").strip()
        
        if user_input.lower() in ["q", "quit", "exit"]:
            print("\n[CALL TERMINATED BY USER]")
            ivr_service.end_session(call_id)
            break

        if user_input.lower() == "timeout":
            res = ivr_service.process_dtmf_input(call_id, None, is_timeout=True)
        else:
            res = ivr_service.process_dtmf_input(call_id, user_input, is_timeout=False)

        print(f"\n[STATE: {res['state']}]")
        print(f"[SYSTEM VOICE] {res['prompt']}")

    print("\n" + "=" * 60)
    print("Call session completed.")
    print("=" * 60)

if __name__ == "__main__":
    run_cli_simulator()
