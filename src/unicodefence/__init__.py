"""UnicodeFence: inspect text for invisible Unicode controls."""

from .scanner import Finding, ScanResult, scan_file, scan_text

__all__ = ["Finding", "ScanResult", "scan_file", "scan_text"]
__version__ = "0.1.0"
