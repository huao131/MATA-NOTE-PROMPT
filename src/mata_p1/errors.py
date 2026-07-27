"""P1 helpers preserving the P0 STOP_AND_REPORT model."""
from mata_p0.errors import ContractViolation, StopAndReport
def stop(code: str, path: str, message: str) -> None:
    raise StopAndReport(ContractViolation(code, path, message))
__all__ = ["ContractViolation", "StopAndReport", "stop"]
